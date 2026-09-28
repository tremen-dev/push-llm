"""SPEC-007 CA-3 (capture protocol) and CA-4 (empty capture template)."""
import re

import pytest

import baseline_docs as bd
from conftest import PILOT_DIR

PROTOCOL = PILOT_DIR / "protocolo-captura.md"
TEMPLATE = PILOT_DIR / "plantilla-captura.csv"
MAX_WORDS_TWO_PAGES = 1100  # printable in <= 2 A4 pages at a readable size


def _flat(md: str) -> str:
    """Lower-case text without markdown emphasis and with line breaks folded."""
    return re.sub(r"\s+", " ", md.replace("*", "")).lower()


@pytest.fixture(scope="module")
def protocol():
    return PROTOCOL.read_text(encoding="utf-8")


def test_protocol_fits_two_pages(protocol):
    assert len(protocol.split()) <= MAX_WORDS_TWO_PAGES


@pytest.mark.parametrize("field", bd.PROTOCOL_FIELDS)
def test_protocol_lists_every_mandatory_field(protocol, field):
    assert f"`{field}`" in protocol


@pytest.mark.parametrize("snippet", [
    # per app: clean session, account/plan, how to note the model
    "ChatGPT", "Gemini", "Google", "chat temporal", "incógnito", "memoria",
    "actividad", "cuenta gratuita", "modelo",
    # how to ask
    "texto literal", "una pregunta por conversación nueva", "orden del set",
    # what to capture
    "captura", "desplaza", "enlace compartido",
    # same conditions in every pass, incl. SPEC-012
    "mismas en todas las pasadas", "SPEC-012",
    # location
    "municipio", "Viveiro",
])
def test_protocol_covers(protocol, snippet):
    assert snippet.lower() in _flat(protocol)


@pytest.mark.parametrize("rule", [
    "no pulses ningún enlace a la web de la clínica",
    "no busques el nombre de la clínica en google",
    "las preguntas am solo en chatgpt y gemini",
    "registro de desviaciones",
])
def test_protocol_anti_contamination_rules(protocol, rule):
    assert rule in _flat(protocol)


def test_template_is_header_only():
    header, n_lines = bd.template_header(TEMPLATE.read_text(encoding="utf-8"))
    assert n_lines == 1
    assert header == bd.TEMPLATE_COLUMNS


def test_template_crosses_protocol_fields_and_ca4_extras():
    header, _ = bd.template_header(TEMPLATE.read_text(encoding="utf-8"))
    assert set(bd.PROTOCOL_FIELDS) <= set(header)
    for extra in ("clinicas_nombradas", "artica_nombrada", "posicion_artica",
                  "dominios_citados", "enlace_compartido", "fichero_captura", "observaciones"):
        assert extra in header


def test_protocol_documents_every_template_column(protocol):
    for col in bd.TEMPLATE_COLUMNS:
        assert f"`{col}`" in protocol, col
