"""F-SPEC-002-1 (c): run_probe loads the repo-root .env by itself (ADR-006, ADR-007).

Offline: every .env here is a temporary fixture; the real one is never read.
"""
import csv
import os

import pytest

import providers
import run_probe

SECRET = {"ANTHROPIC_API_KEY": "FIXTURE-anthropic-aaa111", "OPENAI_API_KEY": "FIXTURE-openai-bbb222",
          "GEMINI_API_KEY": "FIXTURE-gemini-ccc333"}


class FakeAsk:
    def __init__(self):
        self.calls = []

    def __call__(self, name, prompt, cfg, model, client=None):
        self.calls.append(name)
        return providers.ProviderResult("ok", "Te recomiendo Clínica Torres.", model, 10, 5, 1, [])


def write_env(path, text):
    path.write_text(text, encoding="utf-8")
    return path


# ---------------------------------------------------------------- parser

def test_parse_skips_comments_blank_lines_and_empty_values():
    text = ("# comment\n\n   # indented comment\nOPENAI_API_KEY=abc\nANTHROPIC_API_KEY=\n"
            "GEMINI_API_KEY =   \n# CLAUDE_MODEL=x\nPUSHLLM_PRIVADO = D:\\priv ada \n")
    assert run_probe.parse_dotenv(text) == {"OPENAI_API_KEY": "abc",
                                            "PUSHLLM_PRIVADO": "D:\\priv ada"}


def test_parse_quotes_export_crlf_bom_and_first_equals():
    text = ('\ufeffA="quoted value"\r\nB=\'single\'\r\nexport C=c1\r\nD=x=y\r\nE=""\r\n'
            "not a line\r\n1BAD=v\r\n=v\r\n")
    assert run_probe.parse_dotenv(text) == {"A": "quoted value", "B": "single", "C": "c1",
                                            "D": "x=y"}


def test_parse_the_versioned_template_loads_nothing():
    template = (run_probe.HERE.parent / ".env.example").read_text(encoding="utf-8")
    assert run_probe.parse_dotenv(template) == {}


# ---------------------------------------------------------------- loader

def test_load_sets_missing_vars_and_never_overwrites_existing(tmp_path):
    path = write_env(tmp_path / ".env", "OPENAI_API_KEY=from-file\nGEMINI_API_KEY=from-file\n"
                                        "ANTHROPIC_API_KEY=from-file\nEMPTY=\n")
    env = {"OPENAI_API_KEY": "from-session", "ANTHROPIC_API_KEY": ""}
    loaded = run_probe.load_dotenv(path, env)
    assert env == {"OPENAI_API_KEY": "from-session", "ANTHROPIC_API_KEY": "",
                   "GEMINI_API_KEY": "from-file"}
    assert loaded == ["GEMINI_API_KEY"]


def test_load_without_file_changes_nothing(tmp_path):
    env = {"X": "1"}
    assert run_probe.load_dotenv(tmp_path / "missing" / ".env", env) == []
    assert env == {"X": "1"}


def test_default_dotenv_is_the_repo_root_one():
    assert run_probe.REPO_ROOT == run_probe.HERE.parent and run_probe.DOTENV_NAME == ".env"


def test_tests_never_point_at_the_real_dotenv():
    # conftest redirects DOTENV_PATH for every test: the real .env is never read.
    assert run_probe.DOTENV_PATH != run_probe.REPO_ROOT / run_probe.DOTENV_NAME
    assert not run_probe.DOTENV_PATH.exists()


# ---------------------------------------------------------------- main

def _all_output(tmp_path, capsys):
    cap = capsys.readouterr()
    files = "".join(p.read_text(encoding="utf-8") for p in tmp_path.rglob("*") if p.is_file()
                    and p.name != ".env")
    return cap.out + cap.err + files


def test_main_enables_providers_from_dotenv_without_writing_values(tmp_path, capsys):
    dotenv = write_env(tmp_path / ".env", "".join(f"{k}={v}\n" for k, v in SECRET.items()))
    out = tmp_path / "out"
    ask = FakeAsk()
    env = {}
    run_probe.main(["--only", "D01", "--runs", "1", "--sleep", "0", "--out", str(out)],
                   env=env, ask=ask, dotenv=dotenv)
    assert sorted(set(ask.calls)) == ["claude", "gemini", "openai"]
    with open(out / "results.csv", newline="", encoding="utf-8") as f:
        assert len(list(csv.DictReader(f))) == 3
    text = _all_output(tmp_path, capsys)
    assert "ANTHROPIC_API_KEY" in text  # names may be reported ...
    for value in SECRET.values():  # ... values never: stdout, stderr, results.csv, summary.md
        assert value not in text


def test_main_session_value_wins_over_dotenv(tmp_path):
    dotenv = write_env(tmp_path / ".env", "OPENAI_API_KEY=file-key\nOPENAI_MODEL=file-model\n")
    env = {"OPENAI_API_KEY": "session-key", "OPENAI_MODEL": "session-model"}
    ask = FakeAsk()
    seen = []
    ask_model = lambda name, prompt, cfg, model, client=None: (seen.append(model), ask(  # noqa: E731
        name, prompt, cfg, model))[1]
    run_probe.main(["--only", "D01", "--runs", "1", "--sleep", "0", "--out", str(tmp_path / "o"),
                    "--providers", "openai"], env=env, ask=ask_model, dotenv=dotenv)
    assert env["OPENAI_API_KEY"] == "session-key" and seen == ["session-model"]


def test_main_dotenv_can_provide_pushllm_privado_for_analyze(tmp_path, capsys):
    priv = tmp_path / "priv"
    (priv / "probe").mkdir(parents=True)
    src = run_probe.HERE / "tests" / "fixtures" / "vigo_results.csv"
    (priv / "probe" / "results.csv").write_bytes(src.read_bytes())
    dotenv = write_env(tmp_path / ".env", f"PUSHLLM_PRIVADO={priv}\n")
    run_probe.main(["--analyze"], env={}, dotenv=dotenv)
    assert (priv / "probe" / "summary.md").exists()


def test_main_without_dotenv_behaves_as_before(tmp_path):
    with pytest.raises(SystemExit, match="no provider configured"):
        run_probe.main(["--only", "D01", "--out", str(tmp_path)], env={}, ask=FakeAsk(),
                       dotenv=tmp_path / "absent.env")


def test_main_with_real_environ_loads_default_dotenv(tmp_path, monkeypatch):
    dotenv = write_env(tmp_path / ".env", "OPENAI_API_KEY=FIXTURE-openai-environ\n")
    monkeypatch.setattr(run_probe, "DOTENV_PATH", dotenv)
    fake_environ = {}
    monkeypatch.setattr(os, "environ", fake_environ)
    ask = FakeAsk()
    run_probe.main(["--only", "D01", "--runs", "1", "--sleep", "0", "--out", str(tmp_path / "o"),
                    "--providers", "openai"], ask=ask)
    assert ask.calls == ["openai"]
    assert fake_environ["OPENAI_API_KEY"] == "FIXTURE-openai-environ"  # SDK clients read os.environ
