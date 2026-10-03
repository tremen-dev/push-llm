"""SPEC-009: checks and builder for the meeting kit and proposal of the Clínica Ártica pilot.

The templates live in ``docs/piloto-artica/reunion/`` (public repo, no client data: ADR-004).
The filled versions (names, dates, findings) and the PDF live only in
``$PUSHLLM_PRIVADO/piloto-artica/reunion/``. Usage::

    python docs/piloto-artica/tools/meeting_docs.py check [FILE.md ...]
        # CA-1..CA-5 and CA-10 checks on the repo templates, plus any extra (filled) file
    python docs/piloto-artica/tools/meeting_docs.py build \
        --valores "$PUSHLLM_PRIVADO/piloto-artica/reunion/valores.json" \
        --salida "$PUSHLLM_PRIVADO/piloto-artica/reunion/propuesta" [--borrador]
        # fills propuesta.md, acuerdos.md and encargo-tratamiento.md and writes a single,
        # self-contained propuesta.html (tremen-ds doc.css, Paged.js). Then:
    node docs/piloto-artica/tools/build_pdf.mjs <salida>/propuesta.html <salida>/propuesta.pdf

The PDF step is the approach of the "Recepción digital" proposal (Paged.js + Playwright or
Chrome headless), with the CSS inlined so the HTML works from the private folder.
"""
from __future__ import annotations

import argparse
import html as html_lib
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
PILOT_DIR = HERE.parent
REPO_DIR = PILOT_DIR.parent.parent
REUNION_DIR = PILOT_DIR / "reunion"
DS_DIR = REPO_DIR / "design" / "tremen-ds"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from baseline_docs import EMAIL_RE, PHONE_RE, forbidden_terms  # noqa: E402

PROPOSAL_MAX_WORDS = 450
PROPOSAL_DOCS = ("propuesta.md", "acuerdos.md", "encargo-tratamiento.md")
PAGED_JS = "https://cdn.jsdelivr.net/npm/pagedjs@0.4.3/dist/paged.polyfill.js"
DS_CSS = ("colors_and_type.css", "components/nav.css", "components/eyebrows.css",
          "components/stamp.css", "doc.css")


def norm_text(s: str) -> str:
    """Lower case without accents; punctuation kept, whitespace collapsed."""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s.lower()).strip()


# ---------------------------------------------------------------- CA-1 guion blocks

@dataclass
class Block:
    title: str
    minutes: int
    body: str
    literal_lines: list[str] = field(default_factory=list)


BLOCK_RE = re.compile(r"^##\s+(.+?)\s+[—–-]\s+(\d+)\s*min\s*$", re.M)
GUION_REQUIRED_BLOCKS = ("apertura", "dato primero", "preguntas", "como funciona",
                         "acuerdos", "cierre")
# The four levers of 04-mechanics-of-llm-visibility.md §2, in plain words.
LEVER_MARKERS = (r"directorios", r"paginas que respond", r"otros hablen de vosotros",
                 r"mismos datos")


def guion_blocks(text: str) -> list[Block]:
    matches = list(BLOCK_RE.finditer(text))
    blocks = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[m.end():end]
        literal = [ln.lstrip("> ").strip() for ln in body.splitlines()
                   if ln.startswith(">") and ln.lstrip("> ").strip()]
        blocks.append(Block(m.group(1).strip(), int(m.group(2)), body, literal))
    return blocks


# ---------------------------------------------------------------- CA-2 questions

QUESTION_RE = re.compile(r"\*\*(P\d+)\*\*\s*[—–-]?\s*(.+)")
QUESTION_TOPICS = {
    "tratamientos a llenar y agenda libre": r"tratamientos.*llenar.*agenda|agenda.*tratamientos",
    "valor de un paciente nuevo": r"cuanto os (supone|supuso|deja|dejo)",
    "como llego el ultimo paciente nuevo": r"ultimo paciente nuevo",
    "pacientes nuevos al mes en tramos": r"pacientes nuevos.*(menos de|entre).*(mas de)",
    "que se pregunta en recepcion": r"recepcion.*(pregunta|conoc)",
    "software de reservas": r"(programa|software).*(reserva|citas)",
    "analitica, search console y accesos": r"analitica.*search console.*acceso",
    "quien lleva la web y con que gestor": r"quien lleva la web.*(gestiona|gestor)",
    "agencia, campanas o cambios en 12 semanas": r"(agencia|campanas).*12 semanas|12 semanas.*(agencia|campanas)",
    "gasto en captacion por partida": r"(gasto|gastasteis|invertisteis).*partida",
    "que entienden por posicionamiento en ia": r"posicionamiento en ia",
    "pacientes que mencionan chatgpt": r"paciente.*chatgpt",
    "quien decide y quien aprueba contenidos": r"decide.*aprueba",
    "que contenido pueden aportar": r"precios.*fotos.*profesionales.*preguntas",
    "tratamientos a atraer de fuera de a marina": r"fuera de a marina",
    "ultimo paciente que se desplazo": r"ultimo paciente que vino de fuera",
}
HYPOTHETICAL_RE = re.compile(
    r"\b(pagar|interesar|usar|comprar|contratar|gustar|querer)(ia|ias|iais|iamos)\b"
    r"|\bestar(ia|ias|iais|iamos) dispuest|\bquerr(ia|ias|iais|iamos)\b")


def questions(text: str) -> dict[str, str]:
    return {m.group(1): m.group(2).strip() for m in QUESTION_RE.finditer(text)}


def question_coverage(qs: dict[str, str]) -> dict[str, list[str]]:
    return {topic: [qid for qid, q in qs.items() if re.search(rx, norm_text(q))]
            for topic, rx in QUESTION_TOPICS.items()}


def hypothetical_hits(text: str) -> list[str]:
    return [m.group(0) for m in HYPOTHETICAL_RE.finditer(norm_text(text))]


# ---------------------------------------------------------------- CA-3 proposal

def _plain(text: str) -> str:
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    return re.sub(r"[#*|>`_]+|^\s*[-]{3,}\s*$|^\s*\d+\.\s", " ", text, flags=re.M)


def word_count(text: str) -> int:
    return sum(1 for w in _plain(text).split() if re.search(r"\w", w))


def _sections(text: str) -> list[tuple[str, str]]:
    parts = re.split(r"^##\s+(.+)$", text, flags=re.M)
    return [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts), 2)]


def _negative_guarantees_only(text: str) -> list[str]:
    bad = []
    # Questions ("¿Me garantizas…?") quote the clinic: they are not a promise of ours.
    t = norm_text(re.sub(r"¿[^?\n]*\?", " ", text))
    for m in re.finditer(r"\b(?:garantiz|asegura|promet)\w*", t):
        before = t[max(0, m.start() - 40):m.start()]
        if not re.search(r"\b(no|sin|ni|nadie|nunca)\b", before):
            bad.append(m.group(0))
    return bad


# Amendment (e), ADR-011: the only mention of Galicia allowed in the proposal.
GALICIA_LITERAL = "con margen para ampliarla al resto de Galicia"
# Amendment (e), D-5: the assistants the probe measures, named in the proposal.
ASSISTANTS = ("ChatGPT", "Gemini", "Claude")


def _galicia_issues(text: str, secs: list[tuple[str, str]], obj: int | None) -> list[str]:
    """Exactly one "Galicia", inside GALICIA_LITERAL, in the objective section."""
    t = norm_text(text)
    hits = t.count("galicia")
    if hits == 0:
        return [f"falta en el objetivo el literal: {GALICIA_LITERAL}"]
    if hits > 1:
        return [f"menciona Galicia {hits} veces (solo vale una, en el literal de ampliación)"]
    if obj is None or norm_text(GALICIA_LITERAL) not in norm_text(secs[obj][1]):
        return ["menciona Galicia fuera del literal de ampliación de la sección del objetivo"]
    return []


def proposal_issues(text: str) -> list[str]:
    t = norm_text(text)
    issues = []
    for zone in ("Ferrolterra", "norte e interior de Lugo", "occidente de Asturias",
                 "sin perder la comarca", "ya sois la clinica que la IA recomienda en A Marina"):
        if norm_text(zone) not in t:
            issues.append(f"falta en el objetivo: {zone}")
    secs = _sections(text)
    obj = next((i for i, (h, _) in enumerate(secs) if "objetivo" in norm_text(h)), None)
    if obj is None:
        issues.append("falta la sección de punto de partida y objetivo")
    else:
        near = norm_text(secs[obj][1] + (secs[obj + 1][1] if obj + 1 < len(secs) else ""))
        if "no se garantiza" not in near:
            issues.append("falta 'no se garantiza' junto al objetivo")
    for cond in (r"mas en el area de influencia que al empezar", r"en a marina no perd",
                 r"al menos un paciente"):
        if not re.search(cond, t):
            issues.append(f"falta una condición de 'cómo sabremos': {cond}")
    if "como sabremos si funciona" not in t:
        issues.append("falta 'cómo sabremos si funciona'")
    for need in ("entre 4 y 12 semanas", "12 semanas desde la primera acción", "450 € + iva",
                 "199 €/mes + iva", "iva", "permanencia",
                 # ADR-010 (amendment (e)): prepaid first three months, then monthly, no lock-in.
                 "pagados por adelantado", "a partir del cuarto mes", "en cualquier momento"):
        if norm_text(need) not in t:
            issues.append(f"falta: {need}")
    for old, label in (("pago mensual, 3 meses", "opción mensual de entrada (Pago mensual, 3 meses)"),
                       ("precios sin iva", "frase retirada: Precios sin IVA")):
        if old in t:
            issues.append(label)
    for name in ASSISTANTS:
        if not re.search(rf"\b{norm_text(name)}\b", t):
            issues.append(f"falta el asistente: {name}")
    issues += _galicia_issues(text, secs, obj)
    for line in text.splitlines():
        if ("%" in line or re.search(r"\bpuntos\b", line, re.I)) and not (
                "IVA" in line and "€" in line):
            issues.append(f"porcentaje o puntos fuera del precio: {line.strip()[:60]}")
    for g in _negative_guarantees_only(text):
        issues.append(f"garantía no negativa: {g}")
    for word in ("gratis", "gratuit", "descuento"):
        if word in t:
            issues.append(f"opción gratuita o descuento: {word}")
    return issues


# ---------------------------------------------------------------- CA-4 agreements, CA-6

AGREEMENT_CHECKS = {
    "(a) avisar de cambios": [r"email", r"persistencia|whatsapp|telegram",
                              r"antes de cualquier cambio", r"agencia"],
    "(b) accesos": [r"analitica", r"search console", r"google business profile|ficha de google",
                    r"gestor de la web", r"(rol|permiso) minimo", r"revoca"],
    "(c) nombre en el repositorio": [r"repositorio publico", r"que se publica", r"que no se publica",
                                     r"historial", r"no se borra", r"cualquiera puede (leer|ver)"],
    "(d) sin datos de pacientes": [r"ningun dato (personal )?de pacientes",
                                   r"conteos? semanal", r"prefiero no", r"opcional",
                                   r"no se podra medir"],
    "(e) aprobacion y revision": [r"aprobacion (escrita|por escrito)", r"revision normativa"],
    "dictamen: encargo": [r"encargo del tratamiento", r"antes de (dar|cualquier) acceso"],
    "dictamen: cookies": [r"cookies", r"consentimiento"],
    "dictamen: conservacion": [r"al terminar", r"(borra|suprim)"],
}
PROCESSOR_CONTRACT_CHECKS = (
    r"objeto", r"duracion", r"naturaleza", r"finalidad", r"tipo(s)? de datos",
    r"categorias de interesados", r"instrucciones documentadas", r"confidencialidad",
    r"medidas de seguridad", r"subencargad", r"derechos", r"violacion(es)? de (la )?seguridad",
    r"(devol|supri)\w+ .*al terminar|al terminar.*(devol|supri)", r"auditori|inspeccion",
    r"articulo 28",
)


# ---------------------------------------------------------------- CA-5 support sheet

OBJECTION_RE = re.compile(r"^###\s+(.+)$", re.M)
REQUIRED_OBJECTIONS = (
    "¿me garantizas salir el primero?", "¿cuántos pacientes me vas a traer?",
    "somos amigos, ¿no me lo haces gratis?", "¿por qué no empezamos ya y lo hablamos luego?",
    "la web la lleva otra persona", "¿y si chatgpt cambia?",
    "¿podemos poner precios / antes y después?", "¿esto no es seo?",
    "¿y saldremos cuando alguien de coruña o vigo busque un injerto capilar?",
    "¿y si por buscar pacientes fuera perdemos lo que ya tenemos en a mariña?",
)


def objection_answers(text: str) -> dict[str, str]:
    part = text.split("## Frases para volver a hechos")[0]
    matches = list(OBJECTION_RE.finditer(part))
    out = {}
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(part)
        body = part[m.end():end]
        out[m.group(1).strip()] = " ".join(ln.lstrip("> ").strip() for ln in body.splitlines()
                                           if ln.startswith(">"))
    return out


def objections(text: str) -> list[str]:
    return list(objection_answers(text))


def back_to_facts(text: str) -> list[str]:
    part = text.split("## Frases para volver a hechos", 1)
    if len(part) < 2:
        return []
    return [ln.strip()[2:] for ln in part[1].splitlines() if ln.strip().startswith("- ")]


# ---------------------------------------------------------------- CA-10

COUNT_FIGURE_RE = re.compile(r"\b\d+ de (las )?\d+\b|\d+(?:[.,]\d+)?\s*%|\b\d+\s*pts?\b")
PERSON_RE = re.compile(r"\b(Dra?|Doctora?)\.?\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+")
GALICIA_PROMISE_RE = re.compile(r"(saldr|aparecer|conseguir|llegar)\w*[^.\n]{0,40}galicia")


PRIVATE_ALLOWED = ("email", "teléfono", "persona")


def ca10_issues(text: str) -> list[str]:
    issues = [f"término prohibido: {t}" for t in forbidden_terms(text)]
    issues += [f"garantía no negativa: {g}" for g in _negative_guarantees_only(text)]
    issues += [f"email: {m}" for m in EMAIL_RE.findall(text)]
    issues += [f"teléfono: {m.strip()}" for m in PHONE_RE.findall(text)
               if len(re.sub(r"\D", "", m)) >= 9]
    for line in text.splitlines():
        if "IVA" in line and "€" in line:
            continue
        for m in COUNT_FIGURE_RE.finditer(line):
            issues.append(f"cifra de visibilidad: {m.group(0)}")
    issues += [f"persona: {m.group(0)}" for m in PERSON_RE.finditer(text)]
    t = norm_text(text)
    for m in GALICIA_PROMISE_RE.finditer(t):
        before = t[max(0, m.start() - 40):m.start()]
        if not re.search(r"\b(no|sin|ni|nadie|nunca)\b", before):
            issues.append(f"promesa sobre Galicia: {m.group(0)[:50]}")
    return issues


# ---------------------------------------------------------------- fill

MARKER_RE = re.compile(r"\{([a-z_][a-z0-9_]*)\}")


def fill(text: str, values: dict) -> str:
    return MARKER_RE.sub(lambda m: str(values[m.group(1)]) if m.group(1) in values
                         else m.group(0), text)


def unfilled(text: str) -> list[str]:
    return list(dict.fromkeys(MARKER_RE.findall(text)))


# ---------------------------------------------------------------- markdown subset → HTML

def _inline(s: str) -> str:
    s = html_lib.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)


def md_to_html(text: str) -> str:
    """The subset used by the proposal and its annexes: ## / ### headings, paragraphs,
    - and 1. lists, pipe tables, > quotes, **bold**, *italics*, and the layout markers
    <!-- cols -->, <!-- col -->, <!-- /cols --> and <!-- callout --> (next paragraph)."""
    text = re.sub(r"<!--(?!\s*(?:/?cols|col|callout|lede)\s*-->).*?-->", "", text, flags=re.S)
    out: list[str] = []
    lines = text.splitlines()
    i = 0
    callout = False
    para: list[str] = []

    def flush():
        nonlocal callout
        if para:
            body = _inline(" ".join(para))
            if callout:
                out.append(f'<div class="callout accent">{body}</div>')
                callout = False
            else:
                out.append(f"<p>{body}</p>")
            para.clear()

    while i < len(lines):
        ln = lines[i].rstrip()
        s = ln.strip()
        marker = re.fullmatch(r"<!--\s*(/?cols|col|callout|lede)\s*-->", s)
        if marker:
            flush()
            kind = marker.group(1)
            out.append({"cols": '<div class="cols-2"><div>', "col": "</div><div>",
                        "/cols": "</div></div>"}.get(kind, ""))
            callout = kind == "callout"
            i += 1
            continue
        if re.fullmatch(r"<!--.*?-->", s):
            i += 1
            continue
        if not s:
            flush()
            i += 1
            continue
        h = re.match(r"^(#{2,3})\s+(.+)$", s)
        if h:
            flush()
            level = 3 if len(h.group(1)) == 2 else 4
            out.append(f"<h{level}>{_inline(h.group(2))}</h{level}>")
            i += 1
            continue
        if s.startswith("|"):
            flush()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            head, *body = rows
            th = "".join(f"<th>{_inline(c)}</th>" for c in head)
            trs = "".join("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in r) + "</tr>"
                          for r in body)
            out.append(f'<table class="tbl tight"><thead><tr>{th}</tr></thead>'
                       f"<tbody>{trs}</tbody></table>")
            continue
        lm = re.match(r"^(-|\d+\.)\s+(.+)$", s)
        if lm:
            flush()
            tag = "ul" if lm.group(1) == "-" else "ol"
            items = []
            while i < len(lines):
                m2 = re.match(r"^\s*(-|\d+\.)\s+(.+)$", lines[i])
                if not m2:
                    break
                items.append(f"<li>{_inline(m2.group(2).strip())}</li>")
                i += 1
            out.append(f"<{tag}>{''.join(items)}</{tag}>")
            continue
        if s.startswith(">"):
            flush()
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip().lstrip("> ").strip())
                i += 1
            out.append(f"<blockquote>{_inline(' '.join(quote))}</blockquote>")
            continue
        para.append(s)
        i += 1
    flush()
    return "\n".join(x for x in out if x)


# ---------------------------------------------------------------- document builder

def _split_title(text: str) -> tuple[str, str, str]:
    """(# title, <!-- lede --> paragraph, rest)."""
    m = re.search(r"^#\s+(.+)$", text, re.M)
    title = m.group(1).strip() if m else ""
    rest = text[m.end():] if m else text
    lede = ""
    lm = re.search(r"<!--\s*lede\s*-->\s*\n(.+?)(?:\n\s*\n|$)", rest, re.S)
    if lm:
        lede = " ".join(lm.group(1).split())
        rest = rest[:lm.start()] + rest[lm.end():]
    return title, lede, rest


def _inline_css() -> str:
    parts = []
    for rel in DS_CSS:
        css = (DS_DIR / rel).read_text(encoding="utf-8")
        parts.append(f"/* tremen-ds/{rel} */\n{css}")
    # @import (Google Fonts) must be the first rule of the stylesheet.
    joined = "\n".join(parts)
    # The Google Fonts URL has ";" inside, so match up to the closing parenthesis.
    import_re = r"@import\s+url\([^)]*\)\s*;"
    imports = re.findall(import_re, joined)
    body = re.sub(import_re, "", joined)
    return "\n".join(dict.fromkeys(imports)) + "\n" + body


def build_document(values: dict, draft: bool = False) -> str:
    pending = values.get("_pendiente") or []
    if pending and not draft:
        raise ValueError(f"valores pendientes de la reunión: {pending}; usa --borrador")
    filled = {name: fill((REUNION_DIR / name).read_text(encoding="utf-8"), values)
              for name in PROPOSAL_DOCS}
    missing = sorted({k for t in filled.values() for k in unfilled(t)})
    if missing:
        raise ValueError(f"marcadores sin valor: {missing}")
    esc = html_lib.escape
    running = "Piloto · " + values["clinica"] + " · tremen.dev · confidencial"
    if draft:
        running = "BORRADOR · " + running
    title, lede, body = _split_title(filled["propuesta.md"])
    pages = [f"""<section class="page compact" id="propuesta">
  <div class="section-eyebrow"><span class="num">/ PROPUESTA — UNA PÁGINA</span><span class="ln"></span></div>
  <h2>El piloto <em>en una página</em></h2>
{md_to_html(body)}
</section>"""]
    for n, name in enumerate(PROPOSAL_DOCS[1:], 1):
        t, _, b = _split_title(filled[name])
        pages.append(f"""<section class="page annex" id="anexo-{n}">
  <div class="section-eyebrow"><span class="num">/ ANEXO {n}</span><span class="ln"></span></div>
  <h2>{_inline(t)}</h2>
{md_to_html(b)}
</section>""")
    stamp = "borrador" if draft else "propuesta"
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8" />
<title>{esc(title)} · {esc(values['clinica'])} · tremen.dev</title>
<style>
{_inline_css()}
/* SPEC-009: una página de propuesta; anexos a letra algo menor */
.doc .page.annex {{ font-size: 9.5pt; }}
.doc .page.annex h4 {{ margin-top: 8pt; }}
.doc blockquote {{ margin: 6pt 0; padding-left: 10pt; border-left: 2px solid var(--accent); }}
</style>
<script>window.PagedConfig = {{ auto: false }};</script>
<script src="{PAGED_JS}"></script>
</head>
<body class="v-papel doc" data-running="{esc(running)}">
<section class="cover v-tremendo">
  <div class="cover-top">
    <span class="lockup"><span class="br">{{</span>tremen<span class="dev">.dev</span><span class="br">}}</span></span>
    <div class="stamp">{stamp}<span>{esc(values['fecha'])}</span></div>
  </div>
  <div class="cover-title">
    <div class="eyebrow-row" style="margin-bottom: 0;">
      <span class="eyebrow">/ Piloto de 12 semanas · pacientes que llegan desde los asistentes de IA</span>
      <span class="dot-row"></span>
    </div>
    <h1>{_inline(title)}</h1>
    <p class="lede">{_inline(lede)}</p>
  </div>
  <div class="cover-meta">
    <div><div class="k">Para</div><div class="v">{esc(values['destinatarios'])}<small>{esc(values['clinica'])}</small></div></div>
    <div><div class="k">Preparada por</div><div class="v">{esc(values['autor'])}<small>tremen.dev · {esc(values['email_contacto'])}</small></div></div>
    <div><div class="k">Fecha</div><div class="v">{esc(values['fecha'])}<small>Documento confidencial</small></div></div>
  </div>
</section>
{chr(10).join(pages)}
<script>
  (async () => {{
    try {{
      await Promise.all(['400 14px Geist', '600 14px Geist', '700 14px Geist',
        '400 italic 14px Geist', '500 12px "Geist Mono"'].map((f) => document.fonts.load(f)));
      await document.fonts.ready;
    }} catch (e) {{}}
    try {{ await window.PagedPolyfill.preview(); }} catch (e) {{ console.error('pagedjs', e); }}
    document.documentElement.setAttribute('data-doc-ready', '1');
  }})();
</script>
</body>
</html>
"""


def write_outputs(values: dict, out_dir: Path, draft: bool = False) -> list[Path]:
    out_dir = Path(out_dir).resolve()
    if out_dir == REPO_DIR or REPO_DIR in out_dir.parents:
        raise ValueError("la salida rellenada va al espacio privado, nunca al repo (ADR-004)")
    html_text = build_document(values, draft=draft)
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for name in PROPOSAL_DOCS:
        p = out_dir / name
        p.write_text(fill((REUNION_DIR / name).read_text(encoding="utf-8"), values),
                     encoding="utf-8")
        written.append(p)
    p = out_dir / "propuesta.html"
    p.write_text(html_text, encoding="utf-8")
    written.append(p)
    return written


# ---------------------------------------------------------------- CLI

def check_files(paths: list[Path], private: bool = False) -> list[str]:
    """CA checks; with private=True, names, emails and phones are allowed (private copies)."""
    problems = []
    for p in paths:
        text = p.read_text(encoding="utf-8")
        problems += [f"{p.name}: {i}" for i in ca10_issues(text)
                     if not (private and i.split(":")[0] in PRIVATE_ALLOWED)]
        name = p.name
        if "guion" in name:
            total = sum(b.minutes for b in guion_blocks(text))
            if total > 45:
                problems.append(f"{name}: minutaje {total} > 45")
            qs = questions(text)
            if len(qs) < 12:
                problems.append(f"{name}: {len(qs)} preguntas < 12")
            problems += [f"{name}: sin cubrir: {t}" for t, ids in
                         question_coverage(qs).items() if not ids]
            problems += [f"{name}: hipotética: {h}" for h in hypothetical_hits(text)]
        if "propuesta" in name:
            problems += [f"{name}: {i}" for i in proposal_issues(text)]
            wc = word_count(text)
            if wc > PROPOSAL_MAX_WORDS:
                problems.append(f"{name}: {wc} palabras > {PROPOSAL_MAX_WORDS}")
    return problems


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("files", nargs="*", type=Path)
    c.add_argument("--solo", action="store_true", help="solo los ficheros indicados")
    c.add_argument("--privado", action="store_true",
                   help="copias privadas: admite nombres, emails y teléfonos")
    b = sub.add_parser("build")
    b.add_argument("--valores", type=Path, required=True)
    b.add_argument("--salida", type=Path, required=True)
    b.add_argument("--borrador", action="store_true")
    a = ap.parse_args(argv)
    if a.cmd == "check":
        paths = ([] if a.solo else sorted(REUNION_DIR.glob("*.md"))) + list(a.files)
        problems = check_files(paths, private=a.privado)
        for p in problems:
            print(p)
        print("OK" if not problems else f"{len(problems)} problema(s)")
        return 1 if problems else 0
    values = json.loads(a.valores.read_text(encoding="utf-8"))
    for p in write_outputs(values, a.salida, draft=a.borrador):
        print(p)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
