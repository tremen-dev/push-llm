"""SPEC-007 CA-1: the patient question set in docs/piloto-artica/prompts-baseline.md."""
import re

import pytest

import baseline_docs as bd
from conftest import PILOT_DIR

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
