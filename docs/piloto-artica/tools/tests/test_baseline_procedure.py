"""SPEC-007 CA-7 (amendment 2026-09-29 (b)): the written recount procedure matches the
dictamen (k)-(n) and the thresholds of count_baseline.py, so that it can be reproduced by
hand or with a spreadsheet."""
import re

import pytest

import count_baseline as cb
from baseline_docs import PILOT_DIR

PROCEDURE = PILOT_DIR / "procedimiento-recuento.md"


@pytest.fixture(scope="module")
def flat():
    md = PROCEDURE.read_text(encoding="utf-8")
    return re.sub(r"\s+", " ", md.replace("*", "").replace("`", "")).lower()


@pytest.mark.parametrize("snippet", [
    "una sola pasada",
    "comparación app frente a probe",
    "brands_mentioned", "searched_urls", "status = ok",
    "más de la mitad", "empate", "mediana",
    f"{cb.MAX_WINDOW_DAYS} días",
    f"{cb.MIN_COMPARABLE} casillas comparables",
    f"{round(cb.MIN_AGREEMENT * 100)} %",
    f"{round(cb.MAX_SOV_GAP * 100)} pts",
    f"± {cb.POSITION_TOLERANCE} puestos",
    f"{cb.AIO_CLEAR_CHANGE} búsquedas",
    "coinciden de forma razonable: sí",
    "ninguna cifra del probe",
    "no entra en el criterio go",
    "calibracion-antes.md",
])
def test_procedure_covers(flat, snippet):
    assert snippet in flat


@pytest.mark.parametrize("gone", [
    "pasada 2", "p1", "estabilidad por pregunta", "sov ponderado (rn-03",
    "área de influencia) y ag", "recuento-antes.md",
])
def test_procedure_drops_the_old_manual_measurement(flat, gone):
    assert gone not in flat
