"""SPEC-007 CA-3 (capture protocol) and CA-4 (empty capture template)."""
import re

import pytest

import baseline_docs as bd
from baseline_docs import PILOT_DIR

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


@pytest.mark.parametrize("snippet", [
    "#artica-adjetivo", "#medica-sin-clinica",               # P-1, P-2
])
def test_protocol_reflects_human_answers(protocol, snippet):
    assert snippet in _flat(protocol)


@pytest.mark.parametrize("snippet", [
    # P-4 revised by the human on 2026-09-29: fixed municipality Vilaboa for every pass
    "municipio fijo: vilaboa", "todas las pasadas (antes y después)",
    "idéntico en todas las pasadas",                       # device location setting
    "resúmenes de ia", "maps", "afecta poco",              # written limitation
    "nada de vpn", "simular el gps",
    "observación de sensibilidad a la ubicación", "fuera del cómputo",
])
def test_protocol_fixed_municipality_vilaboa(protocol, snippet):
    assert snippet in _flat(protocol)


def test_protocol_no_longer_asks_for_viveiro_as_measurement_place(protocol):
    assert "mide desde viveiro o a mariña" not in _flat(protocol)


@pytest.mark.parametrize("snippet", [
    # amendment 2026-09-29 (b): the manual pass is a calibration of the probe
    "49 consultas", "60–90 min", "20–25 min",
    "`antes`", "`despues`",
    "primero el bloque av y después las am",        # chatgpt and gemini
    "google solo el bloque av",
    "baseline oficial del probe", "7 días",          # CA-2 (k5): pairing and window
    "el corte cae entre apps",                       # 2-day split rule (CA-5)
    "mismas en las dos pasadas",
])
def test_protocol_calibration_covers(protocol, snippet):
    assert snippet in _flat(protocol)


def test_protocol_calibration_asks_no_ar_or_ag(protocol):
    """CA-3 evidence: AR/AG do not appear in the question order of the protocol."""
    order = protocol.split("## Cómo preguntar", 1)[1].split("\n## ", 1)[0]
    assert not re.search(r"\bA[RG]\b|\bA[RG]\d\d\b", order)


def test_protocol_calibration_has_no_second_before_pass(protocol):
    flat = _flat(protocol)
    assert "pasada 2" not in flat and "`p1`" not in flat and "76 consultas" not in flat


# ------------------------------------------------------------ calibration order and prefill
@pytest.fixture(scope="module")
def order():
    doc = bd.parse_prompts_doc((PILOT_DIR / "prompts-baseline.md").read_text(encoding="utf-8"))
    return bd.calibration_order(doc)


def test_calibration_order_has_49_queries(order):
    assert len(order) == bd.CALIBRATION_QUERIES == 49


AR = [f"AR{i:02d}" for i in range(1, 6)]
AV = [f"AV{i:02d}" for i in range(1, 16)]


def test_calibration_order_blocks(order):
    """CA-3 (amendment (c)): ChatGPT AR -> AV -> AM (22), Gemini the same (22), Google AR
    only (5); AR first in every app (human decision at the gate)."""
    ids = lambda app: [q["id"] for q in order if q["app"] == app]  # noqa: E731
    assert ids("chatgpt") == AR + AV + ["AM01", "AM02"]
    assert ids("gemini") == AR + AV + ["AM01", "AM02"]
    assert ids("google") == AR
    assert [q["app"] for q in order] == ["chatgpt"] * 22 + ["gemini"] * 22 + ["google"] * 5


def test_calibration_order_has_no_ag_and_no_google_av_or_am(order):
    assert not [q for q in order if q["id"].startswith("AG")]
    assert not [q for q in order if q["app"] == "google" and q["id"][:2] in {"AV", "AM"}]


def test_calibration_order_uses_the_frozen_texts(order):
    doc = bd.parse_prompts_doc((PILOT_DIR / "prompts-baseline.md").read_text(encoding="utf-8"))
    texts = {q["id"]: q["text"] for q in doc["measurement"] + doc["regional"] + doc["brand"]}
    assert all(q["text"] == texts[q["id"]] for q in order)


def test_expected_layout_matches_the_order(order):
    layout = {}
    for q in order:
        layout.setdefault((q["app"], q["id"][:2]), []).append(q["id"])
    assert layout == {k: list(v) for k, v in bd.EXPECTED_LAYOUT.items()}
    assert sum(len(v) for v in bd.EXPECTED_LAYOUT.values()) == 49


def test_prefill_rows_follow_the_template(order):
    rows = bd.prefill_rows(order, "antes")
    assert len(rows) == 49 and list(rows[0]) == bd.TEMPLATE_COLUMNS
    assert {r["pasada"] for r in rows} == {"antes"}
    assert {r["municipio"] for r in rows} == {"Vilaboa"}
    assert {r["resumen_ia"] for r in rows if r["app"] != "google"} == {"n-a"}
    assert {r["resumen_ia"] for r in rows if r["app"] == "google"} == {""}
    assert next(r for r in rows if r["id_pregunta"] == "AV14")["idioma"] == "gl"
    assert next(r for r in rows if r["id_pregunta"] == "AR01")["idioma"] == "gl"
    assert [r["id_pregunta"] for r in rows][:6] == AR + ["AV01"]


def test_prefill_rejects_unknown_pass(order):
    with pytest.raises(ValueError):
        bd.prefill_rows(order, "p1")


def test_questions_in_order_text(order):
    text = bd.questions_in_order(order)
    assert text.count("\nAR01  ") == 3 and text.count("\nAV01  ") == 2
    assert text.count("\nAM01  ") == 2 and "AG01" not in text
    assert "49 consultas" in text
    google = text.split("==== Google", 1)[1]
    assert "AR05  " in google and "AV01" not in google and "AM01" not in google
    chatgpt = text.split("==== ChatGPT", 1)[1].split("==== Gemini", 1)[0]
    assert chatgpt.index("AR01") < chatgpt.index("AV01") < chatgpt.index("AM01")
    assert "22 preguntas" in chatgpt


def test_prefill_cli_writes_the_three_private_files(tmp_path):
    assert bd.main(["--prefill", str(tmp_path)]) == 0
    for name in ("captura-antes-prerrellenada.csv", "captura-despues-prerrellenada.csv",
                 "preguntas-en-orden.txt"):
        assert (tmp_path / name).exists(), name
    lines = (tmp_path / "captura-despues-prerrellenada.csv").read_text(
        encoding="utf-8-sig").splitlines()
    assert len(lines) == 50 and ",despues,AR01,chatgpt," in lines[1]
    assert lines[-1].split(",")[2:4] == ["AR05", "google"]
