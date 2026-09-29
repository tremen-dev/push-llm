"""CA-1 (dictamen de modelos) y CA-2 (configuración, no código) de SPEC-001; CA-2 de SPEC-002
(la config se compara con el dictamen sdd-probe **vigente**: el más reciente fechado)."""
import json
import re

import pytest

from conftest import PROBE_DIR, REPO_DIR
import settings

EPIC_001 = REPO_DIR / "docs/epicas/EPIC-001-ciclo-0-baseline-y-validacion-del-problema"
LEDGER = EPIC_001 / "SPEC-001-ajustes-del-probe-para-el-baseline.ledger.md"
LEDGER_SPEC_002 = EPIC_001 / "SPEC-002-ejecucion-del-probe-baseline-y-veredicto-de-la-hipotesis.ledger.md"
# Most specific first: on a date tie the SPEC-002 dictamen wins (SPEC-002 CA-2).
DICTAMEN_LEDGERS = (LEDGER_SPEC_002, LEDGER)
PROVIDERS = ("claude", "openai", "gemini")
HEADING = re.compile(r"^### Dictamen sdd-probe \((\d{4}-\d{2}-\d{2})\)", re.M)


def _table_rows(section: str) -> dict:
    rows = {}
    for line in section.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 4 and cells[0] in PROVIDERS:
            rows[cells[0]] = {"model": cells[1].strip("`"), "tool": cells[2].strip("`"),
                              "effort": cells[3].strip("`")}
    return rows


def dictamenes(text: str) -> list[tuple[str, dict]]:
    """(date, rows) for every dated sdd-probe dictamen with a full three-provider table."""
    out = []
    for m in HEADING.finditer(text):
        section = text[m.end():].split("\n#", 1)[0]
        rows = _table_rows(section)
        if set(rows) == set(PROVIDERS):
            out.append((m.group(1), rows))
    return out


def vigente(ledgers=DICTAMEN_LEDGERS) -> tuple[str, object, dict]:
    """The most recent dated dictamen across the ledgers (ties: the first ledger wins)."""
    best = None
    for path in ledgers:
        if not path.exists():
            continue
        for date, rows in dictamenes(path.read_text(encoding="utf-8")):
            if best is None or date > best[0]:
                best = (date, path, rows)
    assert best, "no dated sdd-probe dictamen with a three-provider table"
    return best


def dictamen_rows():
    return vigente()[2]


TABLE = ("| Proveedor | Modelo | Búsqueda web | Effort | Fuente |\n|---|---|---|---|---|\n"
         "| claude | `c-{0}` | `t` | `low` | s |\n| openai | `o-{0}` | `t` | `low` | s |\n"
         "| gemini | `g-{0}` | `t` | — | s |\n")


def test_vigente_picks_most_recent_date_and_spec_002_on_tie(tmp_path):
    old, new = tmp_path / "spec001.md", tmp_path / "spec002.md"
    old.write_text("### Dictamen sdd-probe (2026-09-23) — x\n" + TABLE.format("old"),
                   encoding="utf-8")
    new.write_text("## Notas\n### Dictamen sdd-probe (2026-09-29) — y\n" + TABLE.format("new")
                   + "\n### Otra cosa\n| claude | `nope` | `t` | `low` | s |\n", encoding="utf-8")
    date, path, rows = vigente((new, old))
    assert (date, path, rows["claude"]["model"]) == ("2026-09-29", new, "c-new")
    assert vigente((tmp_path / "missing.md", old))[2]["openai"]["model"] == "o-old"
    same = tmp_path / "same.md"
    same.write_text("### Dictamen sdd-probe (2026-09-23)\n" + TABLE.format("tie"), encoding="utf-8")
    assert vigente((same, old))[2]["gemini"]["model"] == "g-tie"



def test_spec002_ca2_vigente_dictamen_is_the_spec_002_one():
    date, path, _ = vigente()
    assert path == LEDGER_SPEC_002
    assert date >= "2026-09-29"


def test_spec002_ca2_config_dictamen_date_is_the_vigente_one():
    assert settings.load_config()["dictamen_date"] == vigente()[0]


def test_spec002_ca2_effort_low_in_claude_and_openai_api_default_in_gemini():
    rows = dictamen_rows()
    assert rows["claude"]["effort"] == rows["openai"]["effort"] == "low"
    assert settings.load_config()["providers"]["gemini"]["effort"] is None


def test_spec002_ca2_viveiro_batch_inherits_vigente_models_and_prices():
    vcfg = settings.load_config(PROBE_DIR / "batches" / "viveiro.json")
    base = settings.load_config()
    assert vcfg["providers"] == base["providers"] and vcfg["currency"] == base["currency"]
    for name, row in dictamen_rows().items():
        assert vcfg["providers"][name]["model"] == row["model"], name
        assert settings.resolve_model(name, vcfg, env={}) == row["model"], name


def test_ca1_ledger_has_dated_probe_dictamen_for_three_providers():
    text = LEDGER.read_text(encoding="utf-8")
    assert re.search(r"### Dictamen sdd-probe \(\d{4}-\d{2}-\d{2}\)", text)
    assert set(dictamen_rows()) == set(PROVIDERS)


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
