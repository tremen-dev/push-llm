"""SPEC-009: meeting kit and proposal for Clínica Ártica (templates in docs/piloto-artica/reunion).

One test (or group) per agent CA: CA-1 guion, CA-2 questions, CA-3 proposal, CA-4 agreements,
CA-5 support sheet, CA-6 (the dictamen conditions reach the texts) and CA-10 (no jargon, no
personal data, no figures). The builder of the filled proposal is tested with synthetic
values: nothing of the client goes into these tests (ADR-004)."""
import json
import os
import re
from pathlib import Path

import pytest

import meeting_docs as md
from meeting_docs import REUNION_DIR

GUION = REUNION_DIR / "guion.md"
APOYO = REUNION_DIR / "apoyo.md"
PROPUESTA = REUNION_DIR / "propuesta.md"
ACUERDOS = REUNION_DIR / "acuerdos.md"
ENCARGO = REUNION_DIR / "encargo-tratamiento.md"
KIT = [GUION, APOYO, PROPUESTA, ACUERDOS, ENCARGO]


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def test_kit_files_exist():
    for p in KIT:
        assert p.is_file(), p


# ------------------------------------------------------------------ CA-1 guion

def test_ca1_minutes_add_up_to_at_most_45():
    blocks = md.guion_blocks(read(GUION))
    assert blocks, "sin bloques con minutaje"
    assert sum(b.minutes for b in blocks) <= 45


def test_ca1_required_blocks_in_order():
    titles = [md.norm_text(b.title) for b in md.guion_blocks(read(GUION))]
    positions = []
    for key in md.GUION_REQUIRED_BLOCKS:
        idx = next((i for i, t in enumerate(titles) if key in t), None)
        assert idx is not None, f"falta el bloque {key!r}"
        positions.append(idx)
    assert positions == sorted(positions)


def test_ca1_every_block_has_literal_text():
    for b in md.guion_blocks(read(GUION)):
        assert b.literal_lines, f"bloque sin texto literal: {b.title}"


def test_ca1_block_contents():
    text = md.norm_text(read(GUION))
    blocks = {md.norm_text(b.title): md.norm_text(b.body) for b in md.guion_blocks(read(GUION))}

    def body(key):
        return next(v for k, v in blocks.items() if key in k)

    assert "no vamos a decidir nada" in body("apertura")
    assert "por escrito" in body("apertura")
    assert "hoja" in body("dato primero") and "callar" in body("dato primero")
    how = body("como funciona")
    for lever in md.LEVER_MARKERS:
        assert re.search(lever, how), lever
    assert "4 y 12 semanas" in how and "no se garantiza" in how
    assert "sin perder la comarca" in how and "ferrolterra" in how
    assert "{fecha_envio}" in body("cierre") and "{destinatarios}" in body("cierre")
    assert "hoy no hace falta decidir nada" in text


def test_ca1_block_parser_on_synthetic_text():
    t = "## 1. Apertura — 3 min\n> Hola.\n\n## 2. Cierre — 2 min\n*solo nota*\n"
    blocks = md.guion_blocks(t)
    assert [b.minutes for b in blocks] == [3, 2]
    assert blocks[0].literal_lines == ["Hola."]
    assert blocks[1].literal_lines == []


# ------------------------------------------------------------------ CA-2 questions

def test_ca2_at_least_12_questions():
    assert len(md.questions(read(GUION))) >= 12


def test_ca2_coverage_checklist():
    cov = md.question_coverage(md.questions(read(GUION)))
    missing = [topic for topic, ids in cov.items() if not ids]
    assert missing == []


def test_ca2_no_hypothetical_questions():
    assert md.hypothetical_hits(read(GUION)) == []


@pytest.mark.parametrize("text,hit", [
    ("¿Pagaríais 200 € por esto?", True),
    ("¿Os interesaría aparecer?", True),
    ("¿Te interesaría?", True),
    ("¿Usaríais un panel?", True),
    ("¿Estaríais dispuestos a pagar?", True),
    ("¿Cómo llegó el último paciente?", False),
    ("¿Qué tratamientos queréis llenar?", False),
])
def test_ca2_hypothetical_detector(text, hit):
    assert bool(md.hypothetical_hits(text)) is hit


# ------------------------------------------------------------------ CA-3 proposal

def test_ca3_proposal_passes_its_checklist():
    assert md.proposal_issues(read(PROPUESTA)) == []


def test_ca3_proposal_fits_in_one_page():
    assert md.word_count(read(PROPUESTA)) <= md.PROPOSAL_MAX_WORDS


def test_ca3_prices_equal_d7():
    text = read(PROPUESTA)
    assert "450 € + IVA" in text and "199 €/mes + IVA" in text
    amounts = set(re.findall(r"(\d[\d.]*)\s*€", text))
    assert amounts == {"450", "199"}


def test_ca3_no_galicia_no_percent_no_points():
    text = read(PROPUESTA)
    assert "galicia" not in md.norm_text(text)
    for line in text.splitlines():
        if "%" in line or re.search(r"\bpuntos\b", line, re.I):
            assert "IVA" in line and "€" in line, line


def test_ca3_no_free_option_or_discount():
    t = md.norm_text(read(PROPUESTA))
    for word in ("gratis", "gratuit", "descuento", "rebaja", "oferta"):
        assert word not in t


def test_ca3_checklist_detects_a_bad_proposal():
    bad = "## Objetivo\nOs garantizamos salir en Galicia, +20 puntos.\n450 €\n"
    issues = md.proposal_issues(bad)
    assert any("Galicia" in i for i in issues)
    assert any("garantiza" in i for i in issues)
    assert any("199" in i for i in issues)
    assert any("Ferrolterra" in i for i in issues)


def test_ca3_word_count_ignores_markup_and_comments():
    assert md.word_count("<!-- cols -->\n## Qué incluye\n- **Una** cosa | otra\n") == 5


# ------------------------------------------------------------------ CA-4 agreements

def test_ca4_agreements_cover_a_to_e_and_dictamen():
    t = md.norm_text(read(ACUERDOS))
    for key, patterns in md.AGREEMENT_CHECKS.items():
        for p in patterns:
            assert re.search(p, t), f"{key}: falta {p!r}"


def test_ca4_traceability_to_adr004_and_dictamen():
    t = read(ACUERDOS)
    for ref in ("ADR-004 §1", "ADR-004 §5", "ADR-004 §6", "RN-09", "SPEC-011 CA-7",
                "SPEC-009 CA-6"):
        assert ref in t, ref


# ------------------------------------------------------------------ CA-5 support sheet

def test_ca5_at_least_8_objections_including_the_required_ones():
    objections = md.objections(read(APOYO))
    assert len(objections) >= 8
    joined = md.norm_text(" | ".join(objections))
    for required in md.REQUIRED_OBJECTIONS:
        assert md.norm_text(required) in joined, required


def test_ca5_every_objection_has_a_literal_answer():
    for q, answer in md.objection_answers(read(APOYO)).items():
        assert answer.strip(), q


def test_ca5_required_answers_say_what_the_spec_asks():
    answers = {md.norm_text(k): md.norm_text(v) for k, v in md.objection_answers(read(APOYO)).items()}

    def ans(fragment):
        return next(v for k, v in answers.items() if md.norm_text(fragment) in k)

    assert "revision" in ans("antes y después")
    injerto = ans("injerto capilar")
    assert "medimos" in injerto or "se mide" in injerto
    assert "cadenas" in injerto and "no te lo prometo" in injerto
    marina = ans("perdemos lo que ya tenemos")
    assert "cada semana" in marina and "no se garantiza" in marina
    assert "450" in ans("cuánto cuesta") and "por escrito" in ans("cuánto cuesta")


def test_ca5_at_least_4_back_to_facts_phrases():
    assert len(md.back_to_facts(read(APOYO))) >= 4


# ------------------------------------------------------------------ CA-6 conditions reach the texts

def test_ca6_processor_contract_has_article_28_content():
    t = md.norm_text(read(ENCARGO))
    for p in md.PROCESSOR_CONTRACT_CHECKS:
        assert re.search(p, t), p


def test_ca6_proposal_and_agreements_reference_the_processor_contract():
    assert "encargo" in md.norm_text(read(ACUERDOS))
    assert "anexo" in md.norm_text(read(PROPUESTA))


# ------------------------------------------------------------------ CA-10 no jargon, no personal data

def reunion_texts():
    return sorted(p for p in REUNION_DIR.glob("*.md"))


@pytest.mark.parametrize("path", reunion_texts(), ids=lambda p: p.name)
def test_ca10_no_jargon_or_personal_data(path):
    assert md.ca10_issues(read(path)) == []


@pytest.mark.parametrize("text,kind", [
    ("Mejora tu visibilidad en IA", "término"),
    ("Os garantizamos salir los primeros", "garantía"),
    ("Aseguramos más pacientes", "garantía"),
    ("Escribe a nadie@example.com", "email"),
    ("Llama al 600 123 456", "teléfono"),
    ("Salís en el 80 % de las respuestas", "cifra"),
    ("Os nombró en 7 de 10 preguntas", "cifra"),
    ("Habla con la Dra. Pérez", "persona"),
    ("Saldréis en toda Galicia", "Galicia"),
])
def test_ca10_detector(text, kind):
    assert any(kind in i for i in md.ca10_issues(text)), md.ca10_issues(text)


@pytest.mark.parametrize("text", [
    "No se garantiza aparecer.",
    "Nadie puede garantizar un puesto, y no te lo aseguramos.",
    "Escribe a {email_contacto}",
    "12 semanas desde la primera acción; informe cada 15 días.",
    "450 € + IVA",
])
def test_ca10_allows_negative_guarantees_markers_and_plan_numbers(text):
    assert md.ca10_issues(text) == []


def test_ca10_private_person_names_absent_from_repo():
    """Names come from the private values file (never from the repo); skipped without it."""
    root = os.environ.get("PUSHLLM_PRIVADO")
    valores = Path(root or "-") / "piloto-artica" / "reunion" / "valores.json"
    if not valores.is_file():
        pytest.skip("sin espacio privado")
    names = json.loads(valores.read_text(encoding="utf-8")).get("_personas", [])
    assert names
    for p in reunion_texts():
        t = md.norm_text(read(p))
        for n in names:
            assert not re.search(rf"\b{re.escape(md.norm_text(n))}\b", t), (p.name, "persona")


# ------------------------------------------------------------------ builder (synthetic values)

VALUES = {
    "clinica": "Clínica Ejemplo",
    "matiz_punto_de_partida": ", aunque no en todas las respuestas",
    "tratamientos": "tratamientos faciales",
    "sinergia": "",
    "destinatarios": "la dirección",
    "autor": "el fundador",
    "email_contacto": "equipo@ejemplo.test",
    "fecha": "octubre de 2026",
    "fecha_envio": "el lunes",
    "responsable_nombre": "Clínica Ejemplo, S. L.", "responsable_nif": "B00000000",
    "encargado_nombre": "tremen.dev", "encargado_nif": "00000000T",
    "_pendiente": [],
}


def test_fill_replaces_markers_and_reports_unfilled():
    assert md.fill("Hola {clinica}, {x}", {"clinica": "A"}) == "Hola A, {x}"
    assert md.unfilled("Hola {clinica}, {x}") == ["clinica", "x"]


def test_filled_templates_have_no_markers_left():
    for p in (PROPUESTA, ACUERDOS, ENCARGO):
        assert md.unfilled(md.fill(read(p), VALUES)) == [], p.name


def test_render_markdown_subset():
    html = md.md_to_html("## Título\nTexto **fuerte** y *suave*.\n\n- uno\n- dos\n\n"
                         "1. a\n2. b\n\n| A | B |\n|---|---|\n| 1 | 2 |\n\n> cita\n")
    assert "<h3>Título</h3>" in html
    assert "<strong>fuerte</strong>" in html and "<em>suave</em>" in html
    assert html.count("<li>") == 4 and "<ol>" in html
    assert '<table class="tbl tight">' in html and "<td>2</td>" in html
    assert "<blockquote>" in html


def test_render_layout_markers():
    html = md.md_to_html("<!-- cols -->\n## A\ntexto\n<!-- col -->\n## B\notro\n<!-- /cols -->\n"
                         "<!-- callout -->\n**No se garantiza.** Nada.\n")
    assert '<div class="cols-2"><div>' in html and "</div><div>" in html
    assert '<div class="callout accent">' in html


def test_render_escapes_html():
    assert "&lt;script&gt;" in md.md_to_html("<script>x</script> texto")


def test_build_document_is_self_contained_and_filled():
    html = md.build_document(VALUES, draft=False)
    assert "Clínica Ejemplo" in html
    assert md.unfilled(html) == []
    assert '<link rel="stylesheet"' not in html      # CSS inlined: works from any folder
    assert "--ember" in html                          # tokens of tremen-ds
    assert 'class="cover v-tremendo"' in html and 'class="v-papel doc"' in html
    assert "pagedjs" in html and "data-doc-ready" in html
    body = html.split("</head>", 1)[1]
    assert body.count('<section class="page') == 3   # proposal + two annexes


def test_build_refuses_pending_values_unless_draft():
    values = dict(VALUES, _pendiente=["tratamientos"])
    with pytest.raises(ValueError):
        md.build_document(values, draft=False)
    assert "BORRADOR" in md.build_document(values, draft=True)


def test_build_refuses_unfilled_markers():
    values = {k: v for k, v in VALUES.items() if k != "tratamientos"}
    with pytest.raises(ValueError):
        md.build_document(values, draft=True)


def test_write_outputs_refuses_the_repo(tmp_path):
    with pytest.raises(ValueError):
        md.write_outputs(VALUES, md.REPO_DIR / "tmp-salida", draft=True)
    written = md.write_outputs(VALUES, tmp_path, draft=True)
    names = sorted(p.name for p in written)
    assert "propuesta.html" in names and "propuesta.md" in names and "acuerdos.md" in names


def test_filled_checks_apply_to_the_filled_proposal():
    filled = md.fill(read(PROPUESTA), VALUES)
    assert md.proposal_issues(filled) == []
    assert md.word_count(filled) <= md.PROPOSAL_MAX_WORDS


def test_check_private_copies_allow_names_and_contact(tmp_path):
    f = tmp_path / "hoja-privada.md"
    f.write_text("Habla con la Dra. Ejemplo en equipo@ejemplo.test\n", encoding="utf-8")
    assert any("persona" in p for p in md.check_files([f]))
    assert md.check_files([f], private=True) == []
    f.write_text("Sale en el 80 % de las respuestas\n", encoding="utf-8")
    assert md.check_files([f], private=True)          # figures are never allowed
