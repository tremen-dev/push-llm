"""run_probe CLI: CA-2 (modelo desde config / env), CA-3 (columnas por fila),
CA-5 (modo análisis sin proveedores), CA-7 (reanudar), CA-8 (salida fuera del repo)."""
import csv
import json
import shutil
import subprocess

import pytest

import providers
import run_probe
from conftest import PROBE_DIR, REPO_DIR
from test_analysis import FIXTURE

KEYS = {"ANTHROPIC_API_KEY": "k", "OPENAI_API_KEY": "k", "GEMINI_API_KEY": "k"}


class FakeAsk:
    def __init__(self, status="ok", text="Te recomiendo Clínica Torres."):
        self.calls = []
        self.status, self.text = status, text

    def __call__(self, name, prompt, cfg, model, client=None):
        self.calls.append((name, prompt, model))
        return providers.ProviderResult(self.status, self.text, f"served-{model}", 1000, 100, 2,
                                        ["https://a.es", "https://b.es"])


def run(tmp_path, *args, env=None, ask=None):
    ask = ask or FakeAsk()
    argv = ["--out", str(tmp_path), "--sleep", "0", *args]
    run_probe.main(argv, env=KEYS if env is None else env, ask=ask)
    return ask


def read_rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ---------- CA-3 ----------

def test_ca3_row_has_all_metadata_columns(tmp_path):
    run(tmp_path, "--only", "D01", "--providers", "openai", "--runs", "1")
    rows = read_rows(tmp_path / "results.csv")
    assert len(rows) == 1
    r = rows[0]
    for col in ("prompt_id", "specialty", "city", "provider", "run", "brands_mentioned",
                "directories_mentioned", "answer", "timestamp_utc", "model", "input_tokens",
                "output_tokens", "web_searches", "cost_eur", "status", "cited_urls"):
        assert col in r, col
    assert r["timestamp_utc"].endswith("Z")
    assert r["model"].startswith("served-")
    assert (r["input_tokens"], r["output_tokens"], r["web_searches"]) == ("1000", "100", "2")
    assert float(r["cost_eur"]) > 0
    assert r["status"] == "ok" and r["cited_urls"] == "https://a.es;https://b.es"
    assert r["brands_mentioned"] == "Clínica Torres"


def test_ca3_error_row_keeps_status_and_blank_searches(tmp_path):
    class Err(FakeAsk):
        def __call__(self, name, prompt, cfg, model, client=None):
            self.calls.append(name)
            return providers.ProviderResult("error", "", model, error="Boom: x")
    run(tmp_path, "--only", "D01", "--providers", "claude", "--runs", "1", ask=Err())
    r = read_rows(tmp_path / "results.csv")[0]
    assert r["status"] == "error" and r["web_searches"] == "" and "Boom" in r["answer"]


def test_multiline_answer_is_stored_raw(tmp_path):
    run(tmp_path, "--only", "D01", "--providers", "openai", "--runs", "1",
        ask=FakeAsk(text="Línea 1\nLínea 2"))
    assert read_rows(tmp_path / "results.csv")[0]["answer"] == "Línea 1\nLínea 2"


# ---------- CA-2 ----------

def test_ca2_model_used_comes_from_config_file(tmp_path):
    data = json.loads((PROBE_DIR / "probe_config.json").read_text(encoding="utf-8"))
    data["providers"]["gemini"]["model"] = "model-from-config"
    cfgp = tmp_path / "cfg.json"
    cfgp.write_text(json.dumps(data), encoding="utf-8")
    ask = run(tmp_path / "o", "--config", str(cfgp), "--only", "D01", "--providers", "gemini",
              "--runs", "1")
    assert ask.calls[0][2] == "model-from-config"


def test_ca2_env_var_overrides_model_in_run(tmp_path):
    ask = run(tmp_path, "--only", "D01", "--providers", "claude", "--runs", "1",
              env={**KEYS, "CLAUDE_MODEL": "env-model"})
    assert ask.calls[0][2] == "env-model"


def test_runs_default_from_config_per_provider(tmp_path):
    ask = run(tmp_path, "--only", "D01", "--providers", "openai")
    assert len(ask.calls) == 3


def test_provider_without_key_is_skipped(tmp_path):
    ask = run(tmp_path, "--only", "D01", "--runs", "1", env={"OPENAI_API_KEY": "k"})
    assert [c[0] for c in ask.calls] == ["openai"]


def test_smoke_selection_is_twelve_calls(tmp_path):
    ask = run(tmp_path, "--only", "D01,E01,F01,O01", "--runs", "1")
    assert len(ask.calls) == 12


# ---------- CA-5 ----------

def test_ca5_analyze_mode_never_calls_providers(tmp_path, monkeypatch):
    with open(tmp_path / "results.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(FIXTURE[0]))
        w.writeheader()
        w.writerows(FIXTURE)

    def boom(*a, **k):
        raise AssertionError("provider called in analysis mode")
    monkeypatch.setattr(providers, "ADAPTERS", {n: boom for n in ("claude", "openai", "gemini")})
    run_probe.main(["--analyze", "--out", str(tmp_path)], env={}, ask=boom)
    md = (tmp_path / "summary.md").read_text(encoding="utf-8")
    assert "| dental | openai | 2 | 1 | 50.0 % | error: 1 |" in md


def test_probe_run_writes_summary(tmp_path):
    run(tmp_path, "--only", "D01", "--providers", "openai", "--runs", "1")
    assert "| dental | openai | 1 | 1 | 100.0 %" in (tmp_path / "summary.md").read_text(encoding="utf-8")


# ---------- CA-7 ----------

def test_ca7_resume_only_calls_missing_or_failed_combinations(tmp_path):
    run(tmp_path, "--only", "D01", "--providers", "openai", "--runs", "1")
    first = (tmp_path / "results.csv").read_bytes()
    failing = FakeAsk(status="error", text="")
    run(tmp_path, "--resume", "--only", "D01", "--providers", "openai", "--runs", "2", ask=failing)
    assert len(failing.calls) == 1  # run 1 ok -> skipped; run 2 -> called (fails)
    again = FakeAsk()
    run(tmp_path, "--resume", "--only", "D01", "--providers", "openai", "--runs", "2", ask=again)
    assert len(again.calls) == 1  # run 2 had only an error row
    data = (tmp_path / "results.csv").read_bytes()
    assert data.startswith(first)  # previous rows intact
    rows = read_rows(tmp_path / "results.csv")
    assert [(r["run"], r["status"]) for r in rows] == [("1", "ok"), ("2", "error"), ("2", "ok")]
    final = FakeAsk()
    run(tmp_path, "--resume", "--only", "D01", "--providers", "openai", "--runs", "2", ask=final)
    assert final.calls == []


def test_without_resume_refuses_to_overwrite_existing_results(tmp_path):
    run(tmp_path, "--only", "D01", "--providers", "openai", "--runs", "1")
    with pytest.raises(SystemExit):
        run(tmp_path, "--only", "D01", "--providers", "openai", "--runs", "1")


# ---------- CA-8 ----------

def test_ca8_out_dir_option_wins(tmp_path):
    assert run_probe.output_dir(str(tmp_path / "x"), {"PUSHLLM_PRIVADO": str(tmp_path)}) == tmp_path / "x"


def test_ca8_pushllm_privado_used_when_no_option(tmp_path):
    assert run_probe.output_dir(None, {"PUSHLLM_PRIVADO": str(tmp_path)}) == tmp_path / "probe"


def test_ca8_default_inside_repo_is_gitignored():
    default = run_probe.output_dir(None, {})
    assert default == PROBE_DIR / "out"
    if shutil.which("git") is None:
        pytest.skip("git not available")
    for name in ("results.csv", "summary.md", "smoke/results.csv"):
        rel = (default / name).relative_to(REPO_DIR).as_posix()
        res = subprocess.run(["git", "check-ignore", "-q", rel], cwd=REPO_DIR)
        assert res.returncode == 0, f"{rel} not ignored"


# ---------- SPEC-006 CA-6 ----------

def test_spec006_ca6_ivi_alone_goes_to_brands_mentioned(tmp_path):
    run(tmp_path, "--only", "F01", "--providers", "openai", "--runs", "1",
        ask=FakeAsk(text="IVI es la referencia"))
    rows = read_rows(tmp_path / "results.csv")
    assert rows[0]["specialty"] == "fertility"
    assert "IVI Vigo" in rows[0]["brands_mentioned"].split(";")
