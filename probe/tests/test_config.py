"""CA-1 (dictamen de modelos) y CA-2 (configuración, no código)."""
import json
import re

import pytest

from conftest import PROBE_DIR, REPO_DIR
import settings

LEDGER = (REPO_DIR / "docs/epicas/EPIC-001-ciclo-0-baseline-y-validacion-del-problema"
          / "SPEC-001-ajustes-del-probe-para-el-baseline.ledger.md")


def dictamen_rows():
    text = LEDGER.read_text(encoding="utf-8")
    section = text.split("### Dictamen sdd-probe", 1)[1].split("###", 1)[0]
    rows = {}
    for line in section.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 4 and cells[0] in ("claude", "openai", "gemini"):
            rows[cells[0]] = {"model": cells[1].strip("`"), "tool": cells[2].strip("`"),
                              "effort": cells[3].strip("`")}
    return rows


def test_ca1_ledger_has_dated_probe_dictamen_for_three_providers():
    text = LEDGER.read_text(encoding="utf-8")
    assert re.search(r"### Dictamen sdd-probe \(\d{4}-\d{2}-\d{2}\)", text)
    assert set(dictamen_rows()) == {"claude", "openai", "gemini"}


def test_ca1_config_matches_dictamen_literally():
    cfg = settings.load_config()
    for name, row in dictamen_rows().items():
        p = cfg["providers"][name]
        assert p["model"] == row["model"], name
        assert p["web_search_tool"] == row["tool"], name
        assert (p["effort"] or "—") == row["effort"], name


def test_ca1_claude_default_is_not_premium():
    cfg = settings.load_config()
    assert "opus" not in cfg["providers"]["claude"]["model"]


def test_ca2_every_provider_has_ids_runs_prices_date_and_source():
    cfg = settings.load_config()
    for name, p in cfg["providers"].items():
        assert p["model"] and p["runs"] >= 1, name
        price = p["price"]
        for k in ("input_usd_per_mtok", "output_usd_per_mtok", "search_usd", "date", "source"):
            assert price[k] not in (None, ""), (name, k)
    assert cfg["currency"]["usd_per_eur"] > 0 and cfg["currency"]["source"]


def test_ca2_model_comes_from_config_file(tmp_path):
    data = json.loads((PROBE_DIR / "probe_config.json").read_text(encoding="utf-8"))
    data["providers"]["claude"]["model"] = "model-from-test-config"
    path = tmp_path / "cfg.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    cfg = settings.load_config(path)
    assert settings.resolve_model("claude", cfg, env={}) == "model-from-test-config"


@pytest.mark.parametrize("name,var", [("claude", "CLAUDE_MODEL"), ("openai", "OPENAI_MODEL"),
                                      ("gemini", "GEMINI_MODEL")])
def test_ca2_env_var_overrides_config(name, var):
    cfg = settings.load_config()
    assert settings.resolve_model(name, cfg, env={var: "override-x"}) == "override-x"
    assert settings.resolve_model(name, cfg, env={var: ""}) == cfg["providers"][name]["model"]


def _price_literals():
    cfg = settings.load_config()
    vals = {cfg["currency"]["usd_per_eur"]}
    for p in cfg["providers"].values():
        vals |= {p["price"][k] for k in ("input_usd_per_mtok", "output_usd_per_mtok", "search_usd")}
    return sorted({repr(float(v)) for v in vals})


PRICE_LITERALS = _price_literals() if (PROBE_DIR / "settings.py").exists() else []


def test_ca2_no_model_ids_or_prices_literal_in_python_code():
    pattern = re.compile(r"(claude|gpt|gemini)-[0-9a-z][\w.\-]*", re.I)
    for py in PROBE_DIR.glob("*.py"):
        src = py.read_text(encoding="utf-8")
        assert not pattern.search(src), f"model id literal in {py.name}: {pattern.search(src).group(0)}"
        for price in PRICE_LITERALS:
            assert not re.search(rf"(?<![\w.]){re.escape(price)}(?![\w.])", src), (py.name, price)
