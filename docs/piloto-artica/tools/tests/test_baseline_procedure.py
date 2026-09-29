"""SPEC-007 CA-7 (amendment 2026-09-29 (c)): the written recount procedure matches the
dictamen (k)-(s) and the thresholds of count_baseline.py, one comparison per level (6-AV
and 6-AR), so that it can be reproduced by hand or with a spreadsheet."""
import re

import pytest

import count_baseline as cb
from baseline_docs import PILOT_DIR

PROCEDURE = PILOT_DIR / "procedimiento-recuento.md"


def _flat(md: str) -> str:
    return re.sub(r"\s+", " ", md.replace("*", "").replace("`", "")).lower()


@pytest.fixture(scope="module")
def md():
    return PROCEDURE.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def flat(md):
    return _flat(md)


def _part(md: str, heading: str) -> str:
    m = re.search(rf"^###? {re.escape(heading)}.*?$(.*?)(?=^#{{2,3}} |\Z)", md, re.M | re.S)
    assert m, heading
    return _flat(m.group(1))


@pytest.mark.parametrize("snippet", [
    "una sola pasada", "49 filas",
    "comparación app frente a probe",
    "brands_mentioned", "searched_urls", "status = ok",
    "ninguna cifra ni veredicto junta los niveles",
    "no entra en el criterio go",
    "calibracion-antes.md", "--probe-av", "--probe-ar",
])
def test_procedure_covers(flat, snippet):
    assert snippet in flat


@pytest.mark.parametrize("snippet", [
    "baseline oficial", "spec-008 ca-7",
    "más de la mitad", "empate", "mediana",
    f"{cb.MAX_WINDOW_DAYS} días",
    f"{cb.MIN_COMPARABLE} casillas comparables",
    f"{round(cb.MIN_AGREEMENT * 100)} %",
    f"{round(cb.MAX_SOV_GAP * 100)} pts",
    f"± {cb.POSITION_TOLERANCE} puestos",
    "coinciden de forma razonable en av: sí",
    "ya sois la clínica que la ia recomienda en a mariña",
    "ninguna cifra av del probe",
])
def test_procedure_section_6_av(md, snippet):
    assert snippet in _part(md, "6-AV")


@pytest.mark.parametrize("snippet", [
    "spec-008 ca-12", "3 runs", "no las filas ar del baseline oficial",
    f"{cb.AR_MAX_WINDOW_DAYS} días",
    f"{cb.AR_MIN_VALID_RUNS} runs válidos",
    "unánime", "repartida", "compatible", "discrepancia gruesa",
    f"{cb.AR_MIN_COMPARABLE} casillas comparables",
    f"{cb.AR_MIN_DECISIVE} casillas decisivas",
    f"como mucho {cb.AR_MAX_GROSS} discrepancia gruesa",
    "sin discrepancia gruesa en ar: sí", "veredicto débil",
    "sin porcentajes", "no se usa el sov",
    "vilaboa", "viveiro",
    "ninguna cifra ar del probe", "frase del objetivo", "(c)",
])
def test_procedure_section_6_ar(md, snippet):
    assert snippet in _part(md, "6-AR")


def test_ar_section_never_names_av_thresholds(md):
    ar = _part(md, "6-AR")
    assert f"{round(cb.MIN_AGREEMENT * 100)} %" not in ar and "coinciden de forma razonable en ar" not in ar


@pytest.mark.parametrize("snippet", [
    "solo búsquedas ar", "x de 5", "sin porcentajes", "solo se describe",
])
def test_procedure_google_only_ar(md, snippet):
    assert snippet in _part(md, "3.")


def test_procedure_patient_view_per_level(md):
    two = _part(md, "2.")
    assert "núcleo av" in two and "área de influencia ar" in two
    assert "lista de puestos" in two and "una marca" in two


@pytest.mark.parametrize("gone", [
    "pasada 2", "p1", "estabilidad por pregunta", "sov ponderado (rn-03",
    "recuento-antes.md", "cambio claro", "google solo el bloque av", "--probe results.csv",
])
def test_procedure_drops_the_old_rules(flat, gone):
    assert gone not in flat
