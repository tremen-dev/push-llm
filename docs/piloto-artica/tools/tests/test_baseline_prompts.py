"""SPEC-007 CA-1: the patient question set in docs/piloto-artica/prompts-baseline.md."""
import re

import pytest

import baseline_docs as bd
from baseline_docs import PILOT_DIR

PROMPTS_MD = PILOT_DIR / "prompts-baseline.md"
# Candidate competitors of SPEC-008 (gate notes) + the clinic itself: none may appear in AV.
FORBIDDEN_IN_AV = ["Ártica", "Artica", "Luxury", "Ribera", "Polusa", "Virxe da Mariña",
                   "Gaia", "Dorsia", "Pío Vila", "Pio Vila", "CapMédica", "Capmedica",
                   "Avance Capilar"]


@pytest.fixture(scope="module")
def doc():
    return bd.parse_prompts_doc(PROMPTS_MD.read_text(encoding="utf-8"))


def test_measurement_questions_count_and_ids(doc):
    av = doc["measurement"]
    assert 12 <= len(av) <= 16
    assert [q["id"] for q in av] == [f"AV{i:02d}" for i in range(1, len(av) + 1)]


def test_every_question_has_line_intent_scope_language(doc):
    for q in doc["measurement"]:
        assert q["line"] in bd.LINES, q
        assert q["intent"] in bd.INTENTS, q
        assert q["scope"].strip(), q
        assert q["language"] in {"es", "gl"}, q


def test_coverage_conditions(doc):
    cov = bd.coverage(doc["measurement"])
    assert all(cov["lines"][line] >= 1 for line in ("facial", "corporal", "capilar", "cirugia_facial"))
    assert all(cov["intents"][i] >= 1 for i in ("discovery", "price", "comparison", "trust", "specific"))
    assert cov["viveiro"] >= 4
    assert cov["mariña"] >= 2
    assert cov["lugo"] >= 2
    assert cov["gl"] >= 2


def test_coverage_summary_in_doc_matches_table(doc):
    """The human-readable coverage line must not drift from the table."""
    cov = bd.coverage(doc["measurement"])
    assert bd.render_coverage(cov) in PROMPTS_MD.read_text(encoding="utf-8").replace("\n", " ")


@pytest.mark.parametrize("name", FORBIDDEN_IN_AV)
def test_no_clinic_or_competitor_in_measurement_questions(doc, name):
    for q in doc["measurement"]:
        assert not re.search(rf"\b{re.escape(bd.norm(name))}\b", bd.norm(q["text"])), q


def test_no_location_dependent_question_without_place(doc):
    for q in doc["measurement"]:
        t = bd.norm(q["text"])
        assert not re.search(r"\b(cerca de mi|preto de min|mi zona|aqui cerca)\b", t), q
        assert bd.names_a_place(q["text"]), q


def test_brand_questions_apart(doc):
    am = doc["brand"]
    assert 1 <= len(am) <= 2
    assert [q["id"] for q in am] == [f"AM{i:02d}" for i in range(1, len(am) + 1)]
    assert all("artica" in bd.norm(q["text"]) for q in am)
    assert doc["brand_heading"] == "Preguntas de marca (no cuentan para el SoV)"


def test_parser_rejects_bad_rows():
    bad = ("## Preguntas de medición (cuentan para el SoV)\n\n"
           "| id | pregunta | línea | intent | ámbito | idioma |\n|---|---|---|---|---|---|\n"
           "| AV01 | ¿Hola en Viveiro? | facial | bogus | Viveiro | es |\n")
    doc = bd.parse_prompts_doc(bad)
    assert doc["measurement"][0]["intent"] not in bd.INTENTS


def test_coverage_counts_places_on_text_not_scope():
    qs = [{"id": "AV01", "text": "Clínicas en Foz y en Lugo", "line": "facial", "intent": "price",
           "scope": "x", "language": "es"}]
    cov = bd.coverage(qs)
    assert cov["mariña"] == 1 and cov["lugo"] == 1 and cov["viveiro"] == 0


# ------------------------------------------------ amendment 2026-09-29: three levels (ADR-005)
FROZEN_AV = PILOT_DIR / "tools" / "tests" / "av-2026-09-29.tsv"
OPENNESS_RE = r"\b(vivo en|vivo entre|cerca de|por la zona|pola zona|preto de|aunque tenga que desplazarme|ainda que tena que desprazarme)\b"


def test_core_av_identical_to_published_version(doc):
    frozen = [tuple(line.rstrip("\n").split("\t", 1))
              for line in FROZEN_AV.read_text(encoding="utf-8").splitlines()
              if line and not line.startswith("#")]
    assert [(q["id"], q["text"]) for q in doc["measurement"]] == frozen


def test_three_measurement_sections_with_total_limit(doc):
    assert doc["regional_heading"] == bd.REGIONAL_HEADING
    assert doc["galicia_heading"] == bd.GALICIA_HEADING
    total = len(doc["measurement"]) + len(doc["regional"]) + len(doc["galicia"])
    assert total <= 24


def test_ids_unique_and_prefixed_by_level(doc):
    ids = [q["id"] for sec in ("measurement", "regional", "galicia", "brand") for q in doc[sec]]
    assert len(ids) == len(set(ids))
    assert [q["id"] for q in doc["regional"]] == [f"AR{i:02d}" for i in range(1, len(doc["regional"]) + 1)]
    assert [q["id"] for q in doc["galicia"]] == [f"AG{i:02d}" for i in range(1, len(doc["galicia"]) + 1)]


def test_no_repeated_question_text(doc):
    texts = [bd.norm(q["text"]) for sec in ("measurement", "regional", "galicia", "brand")
             for q in doc[sec]]
    assert len(texts) == len(set(texts))


def test_regional_level_conditions(doc):
    ar = doc["regional"]
    assert 4 <= len(ar) <= 5
    cov = bd.coverage_regional(ar)
    assert cov["ferrolterra"] >= 1
    assert cov["north_lugo"] >= 1
    assert cov["west_asturias"] >= 1
    assert cov["mariña_or_viveiro"] == 0
    assert cov["openness"] >= 3
    assert len({q["line"] for q in ar}) >= 2
    assert len({q["intent"] for q in ar}) >= 2
    assert cov["gl"] >= 1
    for q in ar:
        assert q["line"] in bd.LINES and q["intent"] in bd.INTENTS and q["language"] in {"es", "gl"}
        if bd.names_any(q["text"], bd.WEST_ASTURIAS):
            assert q["language"] == "es", q


def test_regional_openness_regex_matches_definition(doc):
    n = sum(bool(re.search(OPENNESS_RE, bd.norm(q["text"]))) for q in doc["regional"])
    assert n == bd.coverage_regional(doc["regional"])["openness"]


def test_galicia_level_conditions(doc):
    ag = doc["galicia"]
    assert 3 <= len(ag) <= 4
    assert {q["line"] for q in ag} == {"capilar", "cirugia_facial"}
    assert any(q["intent"] in {"price", "comparison"} for q in ag)
    assert any(q["language"] == "gl" for q in ag)
    for q in ag:
        assert q["scope"] == "Galicia", q
        assert bd.names_any(q["text"], ["galicia"]), q
        assert not bd.names_any(q["text"], bd.CITIES_AND_COMARCAS), q


def test_level_coverage_lines_match_tables(doc):
    flat = PROMPTS_MD.read_text(encoding="utf-8").replace("\n", " ")
    assert bd.render_coverage_regional(bd.coverage_regional(doc["regional"])) in flat
    assert bd.render_coverage_galicia(doc["galicia"]) in flat


@pytest.mark.parametrize("name", FORBIDDEN_IN_AV)
def test_no_clinic_or_competitor_in_regional_and_galicia(doc, name):
    for q in doc["regional"] + doc["galicia"]:
        assert not re.search(rf"\b{re.escape(bd.norm(name))}\b", bd.norm(q["text"])), q


def test_every_level_question_names_a_place(doc):
    for q in doc["regional"] + doc["galicia"]:
        t = bd.norm(q["text"])
        assert not re.search(r"\b(cerca de mi|preto de min|mi zona|aqui cerca)\b", t), q
        assert bd.names_a_place(q["text"]), q


def test_mondonedo_is_a_mariña_so_never_regional():
    assert bd.names_any("Vivo en Mondoñedo", bd.MARIÑA_MUNICIPALITIES)


# ------------------------------------------------ amendment 2026-09-29 (b): calibration
def _flat(md: str) -> str:
    return re.sub(r"\s+", " ", md.replace("*", "").replace("`", "")).lower()


@pytest.mark.parametrize("snippet", [
    "la medición a mano mide solo av y am",          # intro: manual = calibration
    "el probe mide av, ar y ag",
    "baseline oficial del probe",                    # CA-8: freeze at the latest there
    "fecha que fije el humano en el ledger",
])
def test_intro_and_state_reflect_the_calibration(snippet):
    assert snippet in _flat(PROMPTS_MD.read_text(encoding="utf-8"))


def test_freeze_no_longer_tied_to_pass_1():
    assert "fecha de inicio de la pasada 1" not in _flat(PROMPTS_MD.read_text(encoding="utf-8"))
