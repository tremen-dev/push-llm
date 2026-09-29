"""SPEC-008: Clínica Ártica pilot batch (Viveiro and A Mariña, three levels AV/AR/AG).

CA-1 prompts equal to the SPEC-007 set, CA-2 pilot brands, CA-3 batch by configuration,
CA-4 the Vigo batch does not change. Offline: no keys, no network.
"""
import csv
import re

import pytest

import analysis
import matching
import providers
import run_probe
import settings
from conftest import PROBE_DIR, REPO_DIR
from fakes import (FakeClaudeClient, FakeGeminiClient, FakeOpenAIClient, claude_resp,
                   gemini_resp, openai_resp)

VIVEIRO = PROBE_DIR / "batches" / "viveiro.json"
BASELINE_MD = REPO_DIR / "docs" / "piloto-artica" / "prompts-baseline.md"
FIXTURES = PROBE_DIR / "tests" / "fixtures"
LEVELS = ("AV", "AR", "AG")
KEYS = {"ANTHROPIC_API_KEY": "k", "OPENAI_API_KEY": "k", "GEMINI_API_KEY": "k"}
CLIENT = "Clínica Ártica"


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def baseline_questions():
    """Every question row of the SPEC-007 set: id -> (text, intent). Own tiny parser."""
    out = {}
    for line in BASELINE_MD.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and re.fullmatch(r"A[VRGM]\d{2}", cells[0]):
            out[cells[0]] = (cells[1], cells[3] if len(cells) >= 6 else None)
    return out


@pytest.fixture(scope="module")
def vcfg():
    return settings.load_config(VIVEIRO)


@pytest.fixture(scope="module")
def default_cfg():
    return settings.load_config()


# ---------------------------------------------------------------- CA-1

def test_ca1_pilot_prompts_equal_to_frozen_set_id_and_literal_text():
    doc = {k: v for k, v in baseline_questions().items() if k[:2] in LEVELS}
    probe = {r["id"]: r for r in read_csv(PROBE_DIR / "prompts.csv") if r["id"][:2] in LEVELS}
    assert set(doc) == set(probe)
    assert {p[:2] for p in probe} == set(LEVELS)
    assert len(probe) == 24
    for pid, (text, intent) in doc.items():
        r = probe[pid]
        assert r["prompt"] == text, pid
        assert r["intent"] == intent, pid
        assert r["specialty"] == "aesthetic", pid
        assert r["city"] == "Viveiro", pid


def test_ca1_brand_questions_am_are_not_in_the_probe():
    assert "AM01" in baseline_questions()
    assert not [r for r in read_csv(PROBE_DIR / "prompts.csv") if r["id"].startswith("AM")]


def test_ca1_prompt_ids_unique():
    ids = [r["id"] for r in read_csv(PROBE_DIR / "prompts.csv")]
    assert len(ids) == len(set(ids))


# ---------------------------------------------------------------- CA-2

def test_ca2_brands_csv_loads_and_has_the_client(vcfg):
    brands = {b["brand"]: b for b in matching.load_brands()}
    c = brands[CLIENT]
    assert (c["specialty"], c["city"], c["type"]) == ("aesthetic", "Viveiro", "independent")
    aliases = {matching.norm(a) for a in c["aliases"].split(";")}
    # sdd-metricas dictamen, SPEC-007 ledger (a1): "Ártica" alone and the domain count
    assert {"artica", "artica medicina estetica", "clinicaartica"} <= aliases
    assert c["exact_aliases"] == []


def test_ca2_no_bare_common_word_alias_for_pilot_brands(vcfg):
    common = {"luxury", "ribera", "gaia", "avance", "capilar", "medical", "hair", "torres",
              "clinica", "hospital", "estetica", "doctor", "novoa", "vila", "mariña", "virxe"}
    for b in _pilot_only_rows(vcfg):
        for a in b["aliases"].split(";") + [b["brand"]]:
            assert matching.norm(a) not in {matching.norm(w) for w in common}, (b["brand"], a)


def _pilot_only_rows(vcfg):
    vigo = set(settings.batch(settings.load_config())["brands"])
    return [b for b in matching.load_brands() if b["brand"] not in vigo
            and b["brand"] in settings.batch(vcfg)["brands"]]


# Collisions of a new pilot alias with an existing one, justified in the SPEC-008 ledger
# ("Colisiones de alias justificadas"). Empty means: no collision at all.
JUSTIFIED_COLLISIONS: set[str] = set()


def test_ca2_new_aliases_do_not_collide_with_existing_ones(vcfg):
    vigo_names = set(settings.batch(settings.load_config())["brands"])
    existing = {p for b in matching.load_brands() if b["brand"] in vigo_names
                for p in b["patterns"] + b["short_patterns"]}
    new = [b for b in matching.load_brands() if b["brand"] not in vigo_names]
    clashes = {p for b in new for p in b["patterns"] + b["short_patterns"] if p in existing}
    assert clashes == JUSTIFIED_COLLISIONS


def test_ca2_no_alias_shared_between_two_brands_of_the_pilot_batch(vcfg):
    members = matching.batch_brands(matching.load_brands(), settings.batch(vcfg)["brands"])
    seen = {}
    for b in members:
        for p in b["patterns"]:
            assert p not in seen, (p, seen.get(p), b["brand"])
            seen[p] = b["brand"]


def test_ca2_no_new_exact_aliases():
    assert {b["brand"] for b in matching.load_brands() if b["exact_aliases"]} == {"IVI Vigo"}


def test_ca2_every_pilot_competitor_is_verified_in_the_ledger(vcfg):
    ledger = (REPO_DIR / "docs" / "epicas" / "EPIC-002-piloto-concierge-con-clinica-artica"
              / "SPEC-008-catalogo-de-viveiro-y-a-marina-en-el-probe.ledger.md")
    text = ledger.read_text(encoding="utf-8")
    table = text.split("### Competidores verificados", 1)[1].split("###", 1)[0]
    verified = {}
    for line in table.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 4 and cells[2].startswith("http"):
            verified[cells[0]] = cells
    for b in matching.batch_brands(matching.load_brands(), settings.batch(vcfg)["brands"]):
        if b["type"] == "directory" or b["brand"] == CLIENT:
            continue
        assert b["brand"] in verified, f"{b['brand']} has no source in the ledger"
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", verified[b["brand"]][3]), b["brand"]


# ---------------------------------------------------------------- CA-3

def test_ca3_batch_config_extends_default_and_overrides_location(vcfg, default_cfg):
    assert vcfg["user_location"]["city"] == "Viveiro"
    assert vcfg["user_location"]["region"] == "Galicia"
    assert vcfg["user_location"]["country"] == "ES"
    assert vcfg["providers"] == default_cfg["providers"]  # prices: single source of truth
    assert vcfg["currency"] == default_cfg["currency"]
    b = settings.batch(vcfg)
    assert b["output_subdir"] == "piloto-artica/probe"
    assert "Viveiro" in b["local_cities"] and "Vigo" not in b["local_cities"]


@pytest.mark.parametrize("name,client,resp,get_loc", [
    ("claude", FakeClaudeClient, lambda: [claude_resp("x")],
     lambda kw: kw["tools"][0]["user_location"]),
    ("openai", FakeOpenAIClient, lambda: openai_resp("x"),
     lambda kw: kw["tools"][0]["user_location"]),
])
def test_ca3_requests_carry_viveiro_location(vcfg, name, client, resp, get_loc):
    c = client(resp())
    providers.ask(name, "¿?", vcfg, vcfg["providers"][name]["model"], client=c)
    loc = get_loc(c.calls[0])
    assert (loc["city"], loc["region"], loc["country"]) == ("Viveiro", "Galicia", "ES")


def test_ca3_gemini_location_only_in_prompt_text(vcfg):
    c = FakeGeminiClient(gemini_resp("x"))
    providers.ask("gemini", "¿Dónde en Viveiro?", vcfg, "m", client=c)
    kw = c.calls[0]
    assert "Viveiro" in kw["contents"] and "user_location" not in str(kw["config"])


class FakeAsk:
    def __init__(self, text="Te recomiendo Clínica Ártica."):
        self.calls, self.text = [], text

    def __call__(self, name, prompt, cfg, model, client=None):
        self.calls.append((name, prompt, cfg["user_location"]["city"]))
        return providers.ProviderResult("ok", self.text, model, 100, 10, 1, [])


def test_ca3_viveiro_batch_runs_only_its_prompts_with_viveiro_location(tmp_path):
    ask = FakeAsk()
    run_probe.main(["--config", str(VIVEIRO), "--out", str(tmp_path), "--sleep", "0",
                    "--runs", "1", "--providers", "openai"], env=KEYS, ask=ask)
    rows = read_csv(tmp_path / "results.csv")
    assert {r["prompt_id"][:2] for r in rows} == set(LEVELS)
    assert len(rows) == 24
    assert {c[2] for c in ask.calls} == {"Viveiro"}
    assert {r["brands_mentioned"] for r in rows} == {CLIENT}


def test_ca3_only_outside_the_batch_is_refused(tmp_path):
    with pytest.raises(SystemExit):
        run_probe.main(["--config", str(VIVEIRO), "--out", str(tmp_path), "--sleep", "0",
                        "--only", "AV01,D01"], env=KEYS, ask=FakeAsk())


def test_ca3_default_output_is_private_pilot_dir(tmp_path, vcfg):
    out = run_probe.output_dir(None, {"PUSHLLM_PRIVADO": str(tmp_path)}, settings.batch(vcfg))
    assert out == tmp_path / "piloto-artica" / "probe"


def test_ca3_pilot_brand_with_city_vigo_takes_part_in_viveiro_batch(vcfg):
    members = matching.batch_brands(matching.load_brands(), settings.batch(vcfg)["brands"])
    vigo_members = [b for b in members if b["city"] == "Vigo"]
    assert vigo_members, "the pilot batch should include at least one brand based in Vigo"
    b = vigo_members[0]
    hits = matching.find_mentions(f"Te recomiendo {b['brand']}.", members, "aesthetic", "Viveiro")
    assert [h["brand"] for h in hits] == [b["brand"]]


def test_ca3_batch_brands_rejects_unknown_names():
    with pytest.raises(ValueError, match="No Existe"):
        matching.batch_brands(matching.load_brands(), ["No Existe"])


def level_rows():
    r = analysis_row
    return [
        r("AV01", "openai", 1, "ok", "Clínica Ártica, en Viveiro."),
        r("AV01", "openai", 2, "ok", "No sé."),
        r("AV02", "gemini", 1, "ok", "Ártica Medicina Estética."),
        r("AV02", "claude", 1, "error", "[error] x"),
        r("AR01", "openai", 1, "ok", "Clínica Ártica."),
        r("AR01", "openai", 2, "ok", "Clínica Ártica."),
        r("AR02", "gemini", 1, "ok", "Clínica Ártica o Doctoralia."),
        r("AG01", "openai", 1, "ok", "Clínica Ártica."),
    ]


def analysis_row(pid, provider, run, status, answer):
    return {"prompt_id": pid, "specialty": "aesthetic", "city": "Viveiro", "provider": provider,
            "run": str(run), "status": status, "answer": answer, "cost_eur": "0.01"}


def _members(cfg):
    return matching.batch_brands(matching.load_brands(), settings.batch(cfg)["brands"])


def test_ca3_core_weighted_sov_uses_only_av(vcfg):
    rows = level_rows()
    full = analysis.analyze(rows, _members(vcfg), vcfg)
    core_only = analysis.analyze([r for r in rows if r["prompt_id"].startswith("AV")],
                                 _members(vcfg), vcfg)
    assert full["core_weighted"] == pytest.approx(core_only["core_weighted"])
    # openai 1/2, gemini 1/1: (0.5*0.55 + 1.0*0.25) / 0.80
    assert full["core_weighted"] == pytest.approx(0.525 / 0.80)
    assert full["levels"]["AR"]["openai"]["with_client"] == 2


def test_ca3_summary_reports_each_level_apart_and_counts_only_outside_core(vcfg):
    md = analysis.render_summary(analysis.analyze(level_rows(), _members(vcfg), vcfg), vcfg)
    lines = md.splitlines()
    heads = [ln for ln in lines if ln.startswith("## ")]
    assert any("AV" in h for h in heads) and any("AR" in h for h in heads)
    assert any("AG" in h for h in heads)
    ar = md.split("## Nivel AR", 1)[1].split("\n## Nivel AG", 1)[0]
    ag = md.split("## Nivel AG", 1)[1].split("\n## Coste", 1)[0]
    for section in (ar, ag):  # sdd-metricas (j): counts "x de n", never percentages
        assert "%" not in section
    assert "2 de 2" in ar
    assert "65.6 %" in md.split("## Nivel AR", 1)[0]  # core weighted SoV


def test_ca3_analyze_mode_writes_level_summary(tmp_path):
    rows = level_rows()
    with open(tmp_path / "results.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    run_probe.main(["--config", str(VIVEIRO), "--analyze", "--out", str(tmp_path)], env={})
    md = (tmp_path / "summary.md").read_text(encoding="utf-8")
    assert "## Nivel AV" in md and "Clínica Ártica" in md


# ---------------------------------------------------------------- CA-4

def test_ca4_default_batch_is_vigo(default_cfg):
    b = settings.batch(default_cfg)
    assert default_cfg["user_location"]["city"] == "Vigo"
    assert set(b["local_cities"]) == {"Vigo", "Pontevedra"} == matching.LOCAL_CITIES
    assert b["output_subdir"] == "probe"
    assert CLIENT not in b["brands"]


def test_ca4_default_run_never_executes_pilot_prompts(tmp_path):
    ask = FakeAsk(text="x")
    run_probe.main(["--out", str(tmp_path), "--sleep", "0", "--runs", "1",
                    "--providers", "openai"], env=KEYS, ask=ask)
    ids = {r["prompt_id"] for r in read_csv(tmp_path / "results.csv")}
    assert len(ids) == 44 and not {i for i in ids if i[:2] in LEVELS}
    assert {c[2] for c in ask.calls} == {"Vigo"}


def test_ca4_vigo_summary_identical_to_before_the_change(tmp_path):
    (tmp_path / "results.csv").write_bytes((FIXTURES / "vigo_results.csv").read_bytes())
    run_probe.main(["--analyze", "--out", str(tmp_path)], env={})
    after = (tmp_path / "summary.md").read_text(encoding="utf-8")
    before = (FIXTURES / "vigo_summary_before.md").read_text(encoding="utf-8")
    assert after == before


def test_ca4_pilot_brand_based_in_vigo_is_not_in_vigo_batch(default_cfg, vcfg):
    vigo = set(settings.batch(default_cfg)["brands"])
    pilot_in_vigo = [b for b in _pilot_only_rows(vcfg) if b["city"] in ("Vigo", "Pontevedra")]
    assert pilot_in_vigo, "fixture needs a pilot brand based in Vigo or Pontevedra"
    for b in pilot_in_vigo:
        assert b["brand"] not in vigo
    members = matching.batch_brands(matching.load_brands(), vigo)
    text = " ".join(b["brand"] for b in pilot_in_vigo)
    assert matching.find_mentions(text, members, "aesthetic", "Vigo") == []


def test_ca4_every_brand_belongs_to_some_batch(default_cfg, vcfg):
    names = {b["brand"] for b in matching.load_brands()}
    declared = set(settings.batch(default_cfg)["brands"]) | set(settings.batch(vcfg)["brands"])
    assert names == declared


# ---------------------------------------------------------------- CA-6

def test_ca6_readme_documents_pilot_batch_with_working_commands():
    readme = (PROBE_DIR / "README.md").read_text(encoding="utf-8")
    section = readme.split("## Batches", 1)[1].split("\n## ", 1)[0]
    assert "is the Vigo/Pontevedra batch" in section
    assert "piloto-artica/probe" in section
    cmds = [ln for ln in section.splitlines() if ln.startswith("python run_probe.py")]
    assert len(cmds) >= 3
    for cmd in cmds:
        argv = cmd.split()[2:]
        args = run_probe.parse_args([a.strip('"') for a in argv])
        assert (PROBE_DIR / args.config).resolve() == VIVEIRO.resolve()
        if args.only:
            ids = {p["id"] for p in run_probe.batch_prompts(
                read_csv(PROBE_DIR / "prompts.csv"), settings.batch(settings.load_config(VIVEIRO)))}
            assert set(args.only.split(",")) <= ids
