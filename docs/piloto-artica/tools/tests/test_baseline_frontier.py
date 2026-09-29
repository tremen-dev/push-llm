"""ADR-001/ADR-004 pass rule on docs/piloto-artica (support for CA-11) and the forbidden
terms of the meeting sheet (CA-10, same criterion as SPEC-004 CA-12)."""
import pytest

import baseline_docs as bd
from baseline_docs import PILOT_DIR

DOCS = sorted(p for p in PILOT_DIR.glob("*.*") if p.suffix in {".md", ".csv"})


@pytest.mark.parametrize("path", DOCS, ids=lambda p: p.name)
def test_repo_docs_pass_the_frontier(path):
    assert bd.frontier_issues(path.read_text(encoding="utf-8"), bd.brand_names()) == []


def test_frontier_detects_email_phone_and_figure_next_to_brand():
    names = bd.brand_names()
    text = ("Escribe a nadie@example.com\nLlama al 600 123 456\n"
            "Clínica Ártica sale en el 40 % de las respuestas\n")
    issues = bd.frontier_issues(text, names)
    assert any(i.startswith("email") for i in issues)
    assert any(i.startswith("teléfono") for i in issues)
    assert any(i.startswith("cifra junto a marca") for i in issues)


def test_ids_and_dates_next_to_brand_are_not_figures():
    assert bd.frontier_issues("| AM01 | ¿Qué sabes de Clínica Ártica? | 2026-09-29 |",
                              bd.brand_names()) == []


@pytest.mark.parametrize("text,found", [
    ("Esto es lo que dice ChatGPT de la clínica.", []),
    ("Tu SoV es bajo", ["SoV"]),
    ("Los LLM no te nombran", ["LLM"]),
    ("mejorar la visibilidad en IA", ["visibilidad en IA"]),
    ("sin posicionamiento garantizado", ["posicionamiento garantizado"]),
    ("geografía y geólogos", []),   # whole words only
])
def test_forbidden_meeting_terms(text, found):
    assert bd.forbidden_terms(text) == found
