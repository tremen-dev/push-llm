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
            if p in JUSTIFIED_SHARED_IN_PILOT:
                continue
            assert p not in seen, (p, seen.get(p), b["brand"])
            seen[p] = b["brand"]


# "villoria": both existing Villoria rows are pilot members (finding 2 of the interim
# verification); resolved by specialty, see SPEC-008 ledger "Colisiones de alias".
JUSTIFIED_SHARED_IN_PILOT = {"villoria"}


@pytest.mark.parametrize("text,expected", [
    ("Para los párpados, Clínica Villoria en Vigo.", ["Clínica Villoria"]),
    ("Clínica Villoria L'Essence hace blefaroplastia.", ["Clínica Villoria L'Essence"]),
    ("Villoria, en Vigo.", ["Clínica Villoria L'Essence"]),
])
def test_ca2_villoria_mentions_go_to_the_right_row_in_pilot_batch(vcfg, text, expected):
    got = [b["brand"] for b in matching.find_mentions(text, _members(vcfg), "aesthetic",
                                                      "Viveiro")]
    assert got == expected


@pytest.mark.parametrize("text", ["Mira xn--clinicavirxedamaria-d4b.com",
                                  "Web: clinicavirxedamariña.com", "Clínica Virxe da Mariña"])
def test_ca2_virxe_da_marina_domain_forms(vcfg, text):
    got = [b["brand"] for b in matching.find_mentions(text, _members(vcfg), "aesthetic",
                                                      "Viveiro")]
    assert got == ["Clínica Virxe da Mariña"]


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

PY_CMD = re.compile(r"^(?:\.\\\.venv\\Scripts\\)?python(?:\.exe)? run_probe\.py (.*)$")
MAX_CALLS_PER_PROVIDER = 54  # CA-5 baseline: AV 15 x 3 runs + AR/AG 9 x 1 run
LEDGER = (REPO_DIR / "docs" / "epicas" / "EPIC-002-piloto-concierge-con-clinica-artica"
          / "SPEC-008-catalogo-de-viveiro-y-a-marina-en-el-probe.ledger.md")


def _commands(text):
    out = []
    for ln in text.splitlines():
        m = PY_CMD.match(ln.strip())
        if m:
            out.append([a.strip('"') for a in m.group(1).split()])
    return out


def _assert_commands_within_budget(cmds, tmp_path):
    """Run each command offline (fake provider, --out redirected): none exceeds the budget."""
    out = tmp_path / "run"
    for argv in cmds:
        if "--analyze" in argv:
            continue
        argv = list(argv)
        if "--out" in argv:
            i = argv.index("--out")
            del argv[i:i + 2]
        if "--config" in argv:  # the commands are run from probe/
            i = argv.index("--config") + 1
            argv[i] = str(PROBE_DIR / argv[i])
        extra = [] if "--resume" in argv else ["--resume"]
        ask = FakeAsk()
        run_probe.main([*argv, *extra, "--out", str(out), "--sleep", "0",
                        "--providers", "openai"], env=KEYS, ask=ask)
        assert len(ask.calls) <= MAX_CALLS_PER_PROVIDER, (argv, len(ask.calls))


def test_ca6_readme_documents_pilot_batch_with_working_commands(tmp_path):
    readme = (PROBE_DIR / "README.md").read_text(encoding="utf-8")
    section = readme.split("## Batches", 1)[1].split("\n## ", 1)[0]
    assert "is the Vigo/Pontevedra batch" in section
    assert "piloto-artica/probe" in section
    cmds = _commands(section)
    assert len(cmds) >= 3
    for argv in cmds:
        args = run_probe.parse_args(argv)
        assert (PROBE_DIR / args.config).resolve() == VIVEIRO.resolve()
    _assert_commands_within_budget(cmds, tmp_path)


def test_ca6_ledger_human_commands_within_budget_and_use_venv_python(tmp_path):
    steps = LEDGER.read_text(encoding="utf-8").split("## Instrucciones para el humano", 1)[1]
    steps = steps.split("\n## ", 1)[0]
    assert "Activate.ps1" not in steps
    # order of the enmienda (b): smoke -> SPEC-013 hecho -> CA-9 -> freeze -> baseline -> CA-10
    for step in ("F-SPEC-013-5", "SPEC-013", "CA-9", "congelación", "Aviso de techo",
                 "primera acción", "probe-smoke-spec013"):
        assert step in steps, step
    assert "después de la pasada 1" not in steps
    run_lines = [ln for ln in steps.splitlines()
                 if "run_probe.py" in ln and not ln.lstrip().startswith("#")
                 and not ln.lstrip().startswith("-")]
    assert run_lines and all(ln.strip().startswith(".\\.venv\\Scripts\\python") for ln in run_lines)
    cmds = _commands(steps)
    assert len(cmds) == len(run_lines)
    _assert_commands_within_budget(cmds, tmp_path)


# ---------------------------------------------------------------- CA-5 (runs per level)

def test_ca5_simple_pilot_command_uses_runs_per_level(tmp_path):
    ask = FakeAsk()
    run_probe.main(["--config", str(VIVEIRO), "--out", str(tmp_path), "--sleep", "0",
                    "--providers", "openai"], env=KEYS, ask=ask)
    runs = {}
    for r in read_csv(tmp_path / "results.csv"):
        runs.setdefault(r["prompt_id"][:2], set()).add(r["run"])
    assert runs == {"AV": {"1", "2", "3"}, "AR": {"1"}, "AG": {"1"}}  # official baseline
    assert len(ask.calls) == 15 * 3 + 9 == MAX_CALLS_PER_PROVIDER


def test_ca5_levels_option_selects_levels_and_runs_override(tmp_path):
    ask = FakeAsk()
    run_probe.main(["--config", str(VIVEIRO), "--out", str(tmp_path), "--sleep", "0",
                    "--providers", "openai", "--levels", "AV", "--runs", "3"], env=KEYS, ask=ask)
    ids = {r["prompt_id"] for r in read_csv(tmp_path / "results.csv")}
    assert {i[:2] for i in ids} == {"AV"} and len(ask.calls) == 45


@pytest.mark.parametrize("argv", [["--config", str(VIVEIRO), "--levels", "AX"],
                                  ["--levels", "AV"]])
def test_ca5_unknown_level_or_batch_without_levels_is_refused(tmp_path, argv):
    with pytest.raises(SystemExit):
        run_probe.main([*argv, "--out", str(tmp_path), "--sleep", "0"], env=KEYS,
                       ask=FakeAsk())


# ---------------------------------------------------------------- CA-8 (--out guard)

@pytest.mark.parametrize("out", ["", "  ", "C:\\", "/"])
def test_ca8_out_empty_or_root_is_refused(out):
    ask = FakeAsk()
    with pytest.raises(SystemExit):
        run_probe.main(["--config", str(VIVEIRO), "--out", out, "--only", "AV01",
                        "--runs", "1", "--sleep", "0"], env=KEYS, ask=ask)
    assert ask.calls == []


@pytest.mark.parametrize("out,windows,bad", [
    ("\\piloto-artica\\probe-smoke", True, True),  # "$env:PUSHLLM_PRIVADO\..." with empty var
    ("D:\\privado\\piloto-artica\\probe-smoke", True, False),
    ("C:\\", True, True),
    ("C:", True, True),
    ("/home/u/privado/probe-smoke", False, False),
    ("/", False, True),
    ("", False, True),
])
def test_ca8_unsafe_out_rules(out, windows, bad):
    assert run_probe.unsafe_out(out, windows=windows) is bad


# ---------------------------------------------------------------- review observations

def test_review_observations_list_brand_with_no_doctor_terms(vcfg):
    rows = [analysis_row("AV01", "openai", 1, "ok",
                         "Luxury Clínica es un centro de estética sin médico. Clínica Ártica sí."),
            analysis_row("AV02", "openai", 1, "ok", "Clínica Ártica tiene médica titulada."),
            analysis_row("AR01", "gemini", 1, "ok", "Gaia Pro Aging: personal no sanitario.")]
    res = analysis.analyze(rows, _members(vcfg), vcfg)
    assert [(o["prompt_id"], o["brands"]) for o in res["review"]] == [
        ("AV01", ["Luxury Clínica Médico Estética"]), ("AR01", ["Gaia Pro Aging"])]
    md = analysis.render_summary(res, vcfg)
    obs = md.split("## Observaciones para revisar a mano", 1)[1]
    assert "no es una métrica" in obs and "AV01" in obs and "AV02" not in obs


# ---------------------------------------------------------------- CA-9 / CA-10 (Go with the probe)

def core_rows(with_client):
    """AV rows: {(pid, provider, run): True/False}; every provider answers every cell."""
    return [analysis_row(pid, prov, run, "ok",
                         "Te recomiendo Clínica Ártica." if hit else "No conozco ninguna.")
            for (pid, prov, run), hit in with_client.items()]


def _all_cells(runs=3, n=4, hit=lambda pid, prov, run: False):
    return {(f"AV{i:02d}", prov, run): hit(f"AV{i:02d}", prov, run)
            for i in range(1, n + 1) for prov in ("openai", "gemini", "claude")
            for run in range(1, runs + 1)}


def test_ca9_config_fixes_the_go_instrument(vcfg):
    b = settings.batch(vcfg)
    runs = {lv["prefix"]: lv["runs"] for lv in b["levels"]}
    assert runs == {"AV": 3, "AR": 1, "AG": 1}  # dictamen CA-9 (a)/(c): baseline = "after"
    assert b["go"]["ceiling"] == 0.85           # CA-10
    assert b["go"]["min_valid_share"] == 0.9    # dictamen CA-9 (f)
    assert b["client_review_aliases"] == ["Ártica"]  # dictamen CA-9 (h)


@pytest.mark.parametrize("hits,warned", [(20, True), (17, True), (16, False), (0, False)])
def test_ca10_ceiling_warning_only_from_core_weighted(vcfg, hits, warned):
    # 20 AV prompts x 1 run x 3 providers; the client in the first `hits` of each provider
    cells = {(f"AV{i:02d}", prov, 1): i <= hits
             for i in range(1, 21) for prov in ("openai", "gemini", "claude")}
    res = analysis.analyze(core_rows(cells), _members(vcfg), vcfg)
    assert res["core_weighted"] == pytest.approx(hits / 20)
    md = analysis.render_summary(res, vcfg)
    assert ("Aviso de techo" in md) is warned
    if warned:
        core = md.split("## Nivel AV", 1)[1].split("\n## Nivel AR", 1)[0]
        assert "Aviso de techo" in core and "85 %" in core


def test_ca10_ceiling_ignores_other_levels(vcfg):
    rows = core_rows(_all_cells(runs=1))  # core at 0 %
    rows += [analysis_row(f"AR0{i}", p, 1, "ok", "Clínica Ártica.")
             for i in range(1, 6) for p in ("openai", "gemini", "claude")]
    md = analysis.render_summary(analysis.analyze(rows, _members(vcfg), vcfg), vcfg)
    assert "Aviso de techo" not in md


def test_ca9_weighted_sov_per_run_and_pooled(vcfg):
    # openai: client in run 1 only; gemini/claude never -> run1 = 0.55/0.90, others 0
    cells = _all_cells(runs=3, hit=lambda pid, prov, run: prov == "openai" and run == 1)
    res = analysis.analyze(core_rows(cells), _members(vcfg), vcfg)
    assert res["core_weighted_by_run"] == pytest.approx(
        {"1": 0.55 / 0.90, "2": 0.0, "3": 0.0})
    assert res["core_weighted"] == pytest.approx((1 / 3) * 0.55 / 0.90)  # pooled, (b)
    md = analysis.render_summary(res, vcfg)
    core = md.split("## Nivel AV", 1)[1].split("\n## Nivel AR", 1)[0]
    assert "SoV ponderado del núcleo por run" in core
    assert "| 1 | 61.1 % |" in core and "| 3 | 0.0 % |" in core


def test_ca9_stability_per_question_and_provider(vcfg):
    def hit(pid, prov, run):
        if prov != "openai":
            return False
        return {"AV01": True, "AV02": run == 2}.get(pid, False)
    res = analysis.analyze(core_rows(_all_cells(runs=3, hit=hit)), _members(vcfg), vcfg)
    assert res["core_stability"] == {"all": 1, "some": 1, "none": 10, "cells": 12}
    md = analysis.render_summary(res, vcfg)
    assert "en todos sus runs válidos: 1 de 12" in md
    assert "en alguno: 1 de 12" in md and "en ninguno: 10 de 12" in md


def test_ca9_go_measurement_complete_only_with_enough_valid_rows_per_provider(vcfg):
    cells = _all_cells(runs=3, n=4)
    rows = core_rows(cells)  # 12 rows per provider, all ok
    res = analysis.analyze(rows, _members(vcfg), vcfg)
    assert res["go_complete"] is True
    # two errors of 12 for gemini: 10/12 = 0.83 < 0.9 -> not complete
    bad = [dict(r, status="error") if r["provider"] == "gemini" and r["run"] == "1"
           and r["prompt_id"] in ("AV01", "AV02") else r for r in rows]
    res = analysis.analyze(bad, _members(vcfg), vcfg)
    assert res["go_complete"] is False
    assert "Medición completa para el criterio Go: **no**" in analysis.render_summary(res, vcfg)
    # a weighted provider missing altogether -> not complete
    res = analysis.analyze([r for r in rows if r["provider"] != "claude"], _members(vcfg), vcfg)
    assert res["go_complete"] is False


def test_ca9_bare_artica_answers_are_counted_and_flagged_for_review(vcfg):
    rows = [analysis_row("AV01", "openai", 1, "ok", "La zona ártica es fría."),
            analysis_row("AV02", "openai", 1, "ok", "Clínica Ártica en Viveiro."),
            analysis_row("AV03", "openai", 1, "ok", "Ártica, en clinicaartica.com."),
            analysis_row("AV04", "openai", 1, "ok", "Nada.")]
    res = analysis.analyze(rows, _members(vcfg), vcfg)
    assert res["levels"]["AV"]["openai"]["with_client"] == 3  # RN-01 literal: all count
    assert res["bare_client"]["AV"] == [("AV01", "openai", "1")]
    md = analysis.render_summary(res, vcfg)
    assert "solo por \"Ártica\" suelta" in md and "AV01 × openai (run 1)" in md


def test_ca9_levels_outside_core_list_cells_with_client_without_percentages(vcfg):
    rows = [analysis_row("AR01", "openai", 1, "ok", "Clínica Ártica."),
            analysis_row("AR02", "gemini", 1, "ok", "Nada."),
            analysis_row("AG01", "claude", 1, "ok", "Clínica Ártica.")]
    res = analysis.analyze(rows, _members(vcfg), vcfg)
    assert res["cells_with_client"]["AR"] == [("AR01", "openai", 1, 1)]
    md = analysis.render_summary(res, vcfg)
    ar = md.split("## Nivel AR", 1)[1].split("\n## Nivel AG", 1)[0]
    assert "AR01 × openai (1 de 1 runs)" in ar and "%" not in ar


def test_ca9_models_served_are_reported(vcfg):
    rows = [dict(analysis_row("AV01", "openai", 1, "ok", "x"), model="gpt-a"),
            dict(analysis_row("AV01", "openai", 2, "ok", "x"), model="gpt-b"),
            dict(analysis_row("AR01", "claude", 1, "ok", "x"), model="claude-a")]
    res = analysis.analyze(rows, _members(vcfg), vcfg)
    assert res["models"] == {"openai": ["gpt-a", "gpt-b"], "claude": ["claude-a"]}
    md = analysis.render_summary(res, vcfg)
    assert "## Modelos servidos" in md and "| openai | gpt-a; gpt-b |" in md
