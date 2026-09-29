"""Checks for the SPEC-007 pilot documents (Clínica Ártica manual baseline).

Pure functions over text, used by the tests and runnable by the verifier:

    python docs/piloto-artica/tools/baseline_docs.py            # repo documents
    python docs/piloto-artica/tools/baseline_docs.py FILE.md    # + forbidden terms of CA-10

Normalisation is the one of the probe (probe/matching.py, RN-01) so that "Ártica" and
"Artica" are the same string here and there.
"""
from __future__ import annotations

import csv
import io
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
PILOT_DIR = HERE.parent
REPO_DIR = PILOT_DIR.parent.parent
if str(REPO_DIR / "probe") not in sys.path:
    sys.path.insert(0, str(REPO_DIR / "probe"))

from matching import norm  # noqa: E402  (RN-01 normalisation, single definition)

LINES = ("facial", "corporal", "capilar", "cirugia_facial", "general")
INTENTS = ("discovery", "price", "comparison", "urgent", "trust", "specific")
MARIÑA_PLACES = ("mariña", "burela", "foz", "ribadeo")
# ADR-005 geography of the three levels (municipalities as they appear in patient questions).
MARIÑA_MUNICIPALITIES = ("mariña", "viveiro", "o vicedo", "vicedo", "xove", "cervo",
                         "burela", "foz", "alfoz", "barreiros", "ribadeo", "trabada",
                         "lourenza", "mondoñedo", "o valadouro", "valadouro", "a pontenova",
                         "pontenova", "ourol")
FERROLTERRA = ("ferrol", "ferrolterra", "naron", "neda", "fene", "mugardos", "ares",
               "cabanas", "pontedeume", "as pontes", "cedeira", "valdoviño",
               "san sadurniño", "moeche", "as somozas", "ortigueira", "cariño", "mañon",
               "cerdido", "monfero", "a capela")
NORTH_LUGO_OUTSIDE_MARIÑA = ("vilalba", "terra cha", "abadin", "muras", "xermade",
                             "guitiriz", "begonte", "cospeito", "castro de rei",
                             "a pastoriza", "meira", "riotorto", "outeiro de rei")
INTERIOR_LUGO = ("sarria", "a fonsagrada", "fonsagrada", "becerrea", "navia de suarna",
                 "baleira", "monforte", "chantada", "o incio")
WEST_ASTURIAS = ("asturias", "navia", "tapia de casariego", "vegadeo", "castropol",
                 "el franco", "coaña", "luarca", "valdes", "boal", "taramundi",
                 "san tirso de abres")
CITIES_AND_COMARCAS = ("vigo", "santiago", "coruña", "pontevedra", "ourense", "lugo",
                       "vilagarcia") + MARIÑA_MUNICIPALITIES + FERROLTERRA     + NORTH_LUGO_OUTSIDE_MARIÑA + INTERIOR_LUGO + WEST_ASTURIAS
KNOWN_PLACES = ("lugo", "galicia", "coruña") + MARIÑA_MUNICIPALITIES + FERROLTERRA     + NORTH_LUGO_OUTSIDE_MARIÑA + INTERIOR_LUGO + WEST_ASTURIAS
OPENNESS_RE = re.compile(r"\b(vivo en|vivo entre|cerca de|por la zona|pola zona|preto de|"
                         r"aunque tenga que desplazarme|ainda que tena que desprazarme)\b")
MEASUREMENT_HEADING = "Preguntas de medición (cuentan para el SoV)"
REGIONAL_HEADING = "Área de influencia — AR (indicador aparte, no cuenta para el criterio Go)"
GALICIA_HEADING = "Galicia — AG (indicador aparte, no cuenta para el criterio Go)"
BRAND_HEADING = "Preguntas de marca (no cuentan para el SoV)"

# CA-3: mandatory fields per row, in template order (plantilla-captura.csv).
PROTOCOL_FIELDS = [
    "fecha_hora_local", "pasada", "id_pregunta", "app", "modo", "sesion_iniciada",
    "cuenta", "plan_cuenta", "modelo_mostrado", "municipio", "ubicacion_dispositivo",
    "idioma",
]
# Extra fields of CA-4 plus those the CA-2 dictamen adds (respuesta_valida, resumen_ia).
TEMPLATE_EXTRA_FIELDS = [
    "respuesta_valida", "resumen_ia", "clinicas_nombradas", "artica_nombrada",
    "posicion_artica", "dominios_citados", "enlace_compartido", "fichero_captura",
    "observaciones",
]
TEMPLATE_COLUMNS = PROTOCOL_FIELDS + TEMPLATE_EXTRA_FIELDS

# CA-10 (same criterion as SPEC-004 CA-12): words the meeting sheet must not contain.
FORBIDDEN_MEETING_TERMS = ["LLM", "SoV", "share of voice", "AEO", "GEO",
                           "visibilidad en IA", "posicionamiento garantizado"]


# ---------------------------------------------------------------- CA-1 question set
def _table_rows(section: str) -> list[list[str]]:
    rows = []
    for line in section.splitlines():
        line = line.strip()
        if not line.startswith("|") or set(line) <= set("|-: "):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        rows.append(cells)
    return rows[1:]  # drop header


def _section(md: str, heading: str) -> str:
    m = re.search(rf"^##\s+{re.escape(heading)}\s*$(.*?)(?=^##\s|\Z)", md, re.M | re.S)
    return m.group(1) if m else ""


def _questions(md: str, heading: str) -> list[dict]:
    return [{"id": c[0], "text": c[1], "line": c[2], "intent": c[3], "scope": c[4],
             "language": c[5]}
            for c in _table_rows(_section(md, heading)) if len(c) >= 6]


def _has_heading(md: str, heading: str) -> str | None:
    return heading if re.search(rf"^##\s+{re.escape(heading)}\s*$", md, re.M) else None


def parse_prompts_doc(md: str) -> dict:
    measurement = _questions(md, MEASUREMENT_HEADING)
    brand = [{"id": c[0], "text": c[1], "language": c[2]}
             for c in _table_rows(_section(md, BRAND_HEADING)) if len(c) >= 3]
    brand_heading = BRAND_HEADING if re.search(
        rf"^##\s+{re.escape(BRAND_HEADING)}\s*$", md, re.M) else None
    return {"measurement": measurement, "brand": brand, "brand_heading": brand_heading,
            "regional": _questions(md, REGIONAL_HEADING),
            "regional_heading": _has_heading(md, REGIONAL_HEADING),
            "galicia": _questions(md, GALICIA_HEADING),
            "galicia_heading": _has_heading(md, GALICIA_HEADING)}


def _has_word(text: str, word: str) -> bool:
    return re.search(rf"\b{re.escape(norm(word))}\b", norm(text)) is not None


def names_a_place(text: str) -> bool:
    return any(_has_word(text, p) for p in KNOWN_PLACES)


def names_any(text: str, places) -> bool:
    return any(_has_word(text, p) for p in places)


def coverage_regional(questions: list[dict]) -> dict:
    return {
        "total": len(questions),
        "ferrolterra": sum(names_any(q["text"], FERROLTERRA) for q in questions),
        "north_lugo": sum(names_any(q["text"], NORTH_LUGO_OUTSIDE_MARIÑA) for q in questions),
        "interior_lugo": sum(names_any(q["text"], INTERIOR_LUGO) for q in questions),
        "west_asturias": sum(names_any(q["text"], WEST_ASTURIAS) for q in questions),
        "mariña_or_viveiro": sum(names_any(q["text"], MARIÑA_MUNICIPALITIES) for q in questions),
        "openness": sum(bool(OPENNESS_RE.search(norm(q["text"]))) for q in questions),
        "lines": sorted({q["line"] for q in questions}),
        "intents": sorted({q["intent"] for q in questions}),
        "gl": sum(q["language"] == "gl" for q in questions),
    }


def render_coverage_regional(cov: dict) -> str:
    return (f"Cobertura AR: {cov['total']} preguntas; {cov['ferrolterra']} nombran Ferrolterra, "
            f"{cov['north_lugo']} el norte de Lugo fuera de A Mariña, {cov['interior_lugo']} el "
            f"interior de Lugo, {cov['west_asturias']} el occidente de Asturias; "
            f"{cov['mariña_or_viveiro']} nombran Viveiro o A Mariña; {cov['openness']} desde el "
            f"lugar del paciente con apertura a desplazarse; líneas {', '.join(cov['lines'])}; "
            f"intents {', '.join(cov['intents'])}; {cov['gl']} en gallego.")


def render_coverage_galicia(questions: list[dict]) -> str:
    lines = Counter(q["line"] for q in questions)
    intents = Counter(q["intent"] for q in questions)
    return (f"Cobertura AG: {len(questions)} preguntas; líneas "
            + ", ".join(f"{k} {lines[k]}" for k in sorted(lines))
            + "; intents " + ", ".join(f"{k} {intents[k]}" for k in sorted(intents))
            + f"; {sum(q['language'] == 'gl' for q in questions)} en gallego; ninguna nombra "
            "ciudad ni comarca.")


def coverage(questions: list[dict]) -> dict:
    return {
        "total": len(questions),
        "lines": {k: sum(q["line"] == k for q in questions) for k in LINES},
        "intents": Counter(q["intent"] for q in questions),
        "viveiro": sum(_has_word(q["text"], "viveiro") for q in questions),
        "mariña": sum(any(_has_word(q["text"], p) for p in MARIÑA_PLACES) for q in questions),
        "lugo": sum(_has_word(q["text"], "lugo") for q in questions),
        "gl": sum(q["language"] == "gl" for q in questions),
    }


def render_coverage(cov: dict) -> str:
    lines = ", ".join(f"{k} {cov['lines'][k]}" for k in LINES)
    intents = ", ".join(f"{k} {cov['intents'][k]}" for k in INTENTS if cov["intents"][k])
    return (f"Cobertura: {cov['total']} preguntas; líneas {lines}; intents {intents}; "
            f"{cov['viveiro']} nombran Viveiro, {cov['mariña']} nombran A Mariña, Burela, "
            f"Foz o Ribadeo, {cov['lugo']} nombran Lugo; {cov['gl']} en gallego.")


# ---------------------------------------------------------------- CA-4 template
def template_header(csv_text: str) -> tuple[list[str], int]:
    """Header of the template and number of non-empty lines in the file."""
    lines = [ln for ln in csv_text.splitlines() if ln.strip()]
    header = next(csv.reader(io.StringIO(lines[0]))) if lines else []
    return header, len(lines)


# ---------------------------------------------------------------- CA-10 / CA-11
def forbidden_terms(text: str, terms=FORBIDDEN_MEETING_TERMS) -> list[str]:
    """Forbidden terms present as whole words (case-insensitive, accents folded)."""
    return [t for t in terms if _has_word(text, t)]


EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
PHONE_RE = re.compile(r"(?<!\d)(?:\+34[\s.]?)?[6789]\d{2}[\s.]?\d{2,3}[\s.]?\d{2,3}[\s.]?\d{0,2}(?!\d)")
FIGURE_RE = re.compile(r"\d+(?:[.,]\d+)?\s*(?:%|pts?\b|puntos\b)")


def brand_names(brands_csv: Path | None = None) -> list[str]:
    path = brands_csv or REPO_DIR / "probe" / "brands.csv"
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    names = {"Clínica Ártica", "Ártica"}
    for r in rows:
        names.add(r["brand"])
        names.update(a for a in r["aliases"].split(";") if len(norm(a)) >= 4)
    return sorted(names)


def frontier_issues(text: str, names: list[str]) -> list[str]:
    """ADR-001/ADR-004 pass rule on a repo document: no emails, no phone numbers, and no
    figure (percentage or points) on the same line as a catalogue brand name."""
    issues = [f"email: {m}" for m in EMAIL_RE.findall(text)]
    issues += [f"teléfono: {m.strip()}" for m in PHONE_RE.findall(text)
               if len(re.sub(r"\D", "", m)) >= 9]
    for n, line in enumerate(text.splitlines(), 1):
        if FIGURE_RE.search(line) and any(_has_word(line, b) for b in names):
            issues.append(f"cifra junto a marca, línea {n}: {line.strip()[:80]}")
    return issues


def main(argv: list[str]) -> int:
    names = brand_names()
    bad = 0
    for p in sorted(PILOT_DIR.glob("*.*")):
        if p.suffix not in {".md", ".csv"}:
            continue
        for issue in frontier_issues(p.read_text(encoding="utf-8"), names):
            print(f"{p.name}: {issue}")
            bad += 1
    for extra in argv:
        found = forbidden_terms(Path(extra).read_text(encoding="utf-8"))
        for t in found:
            print(f"{extra}: término prohibido: {t}")
            bad += 1
    print("OK" if not bad else f"{bad} problema(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
