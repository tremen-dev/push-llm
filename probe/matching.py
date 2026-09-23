"""Brand mention matching (RN-01) with the sdd-metricas dictamen of SPEC-001 CA-6.

- Accent/case-insensitive, whole-word matching on normalised text.
- Only names/aliases of >= 4 normalised characters count (RN-01).
- An occurrence contained in a longer overlapping occurrence is dropped.
- An alias shared by several brands goes to the candidates of the prompt's
  specialty, then of the prompt's city; if none (or several) remain, to all.
- A brand counts at most once per answer; order = first appearance.

Exception RN-11 (ADR-002): the `exact_aliases` column of brands.csv lists short
unambiguous acronyms (2-3 chars, only A-Z/0-9, exclusive to one brand; today only
IVI -> IVI Vigo). They are matched on the ORIGINAL answer text, case-sensitively and
as a whole word (not glued to any letter, accented or not, nor to a digit): "IVI",
"(IVI)", "IVI-RMA" count; "ivi", "Ivi", "IVIS", "XIVI", "IVI2" do not. A match is a
mention like any other (overlap, dedup and order rules above apply). MIA is not an
exact alias ("mía"): it stays in `aliases` and is only reported as RN-01 bias.
"""
from __future__ import annotations

import csv
import re
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
MIN_ALIAS_LEN = 4
EXACT_ALIAS_RE = re.compile(r"[A-Z0-9]{2,3}")
LOCAL_CITIES = {"Vigo", "Pontevedra"}


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def _names(row: dict) -> list[str]:
    return [row["brand"]] + [a for a in row["aliases"].split(";") if a.strip()]


def _exact_aliases(row: dict) -> list[str]:
    return [a.strip() for a in (row.get("exact_aliases") or "").split(";") if a.strip()]


def _check_exact_aliases(rows: list[dict]) -> None:
    """ADR-002 §1 (a) form, (d) exclusivity and §2 (not also in own aliases); fails loudly.

    Every brand using a normalised name/alias/acronym is recorded, so the check does not
    depend on the order of the rows.
    """
    users: dict[str, set[str]] = {}   # normalised name/alias/acronym -> brands using it
    for r in rows:
        for n in _names(r) + r["exact_aliases"]:
            users.setdefault(norm(n), set()).add(r["brand"])
    for r in rows:
        own_aliases = {norm(a) for a in _names(r)[1:]}
        for a in r["exact_aliases"]:
            if not EXACT_ALIAS_RE.fullmatch(a):
                raise ValueError(f"brands.csv: exact alias {a!r} of {r['brand']!r} must be "
                                 "2-3 characters, only uppercase A-Z or digits (ADR-002)")
            key = norm(a)
            if key in own_aliases:
                raise ValueError(f"brands.csv: exact alias {a!r} of {r['brand']!r} must not "
                                 "also be in its own aliases (ADR-002 §2)")
            others = sorted(users[key] - {r["brand"]})
            if others:
                raise ValueError(f"brands.csv: exact alias {a!r} of {r['brand']!r} repeats a "
                                 f"name, alias or acronym of {others[0]!r} (ADR-002)")


def load_brands(path: str | Path | None = None) -> list[dict]:
    with open(path or HERE / "brands.csv", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["exact_aliases"] = _exact_aliases(r)
        normed = [norm(n) for n in _names(r)]
        r["patterns"] = list(dict.fromkeys(n for n in normed if len(n) >= MIN_ALIAS_LEN))
        # exact aliases also feed the bias report when they appear but do not count
        r["short_patterns"] = list(dict.fromkeys(
            n for n in normed + [norm(a) for a in r["exact_aliases"]] if 0 < len(n) < MIN_ALIAS_LEN))
    _check_exact_aliases(rows)
    return rows


def is_local_clinic(brand: dict) -> bool:
    return brand["type"] != "directory" and brand["city"] in LOCAL_CITIES


def _occurrences(t: str, pattern: str):
    """Character spans of whole-word occurrences of pattern in normalised text t."""
    padded = f" {t} "
    start = padded.find(f" {pattern} ")
    while start != -1:
        yield (start, start + len(pattern))  # span in t coordinates (padding offset cancels)
        start = padded.find(f" {pattern} ", start + 1)


def _exact_occurrences(text: str, acronym: str):
    """Spans, in norm(text) coordinates, of case-sensitive whole-word matches in raw text.

    The text is NFC-composed first so an accented letter written as letter + combining
    mark (NFD) is one letter, not a word boundary (ADR-002 §3). Any combining mark (Unicode
    category M*) left next to the acronym also glues it to a letter. norm() is unaffected.
    """
    text = unicodedata.normalize("NFC", text)

    def is_mark(i: int) -> bool:
        return 0 <= i < len(text) and unicodedata.category(text[i]).startswith("M")

    for m in re.finditer(rf"(?<![^\W_]){re.escape(acronym)}(?![^\W_])", text):
        if is_mark(m.start() - 1) or is_mark(m.end()):
            continue
        prefix = norm(text[:m.start()])
        start = len(prefix) + 1 if prefix else 0
        yield (start, start + len(norm(acronym)))


def _resolve(candidates: list[dict], specialty, city) -> list[dict]:
    if len(candidates) <= 1:
        return candidates
    by_spec = [b for b in candidates if b["specialty"] == specialty]
    if not by_spec:
        return candidates
    if len(by_spec) == 1:
        return by_spec
    by_city = [b for b in by_spec if b["city"] == city]
    return by_city if len(by_city) == 1 else by_spec


def find_mentions(text: str, brands: list[dict], specialty=None, city=None) -> list[dict]:
    t = norm(text or "")
    if not t:
        return []
    by_pattern: dict[str, list[dict]] = {}
    for b in brands:
        for p in b["patterns"]:
            by_pattern.setdefault(p, []).append(b)
    occ = [(s, e, p) for p in by_pattern for (s, e) in _occurrences(t, p)]
    for b in brands:  # RN-11: exclusive acronyms, keyed apart from normalised patterns
        for a in b["exact_aliases"]:
            key = f"={a}"
            by_pattern[key] = [b]
            occ += [(s, e, key) for (s, e) in _exact_occurrences(text, a)]
    kept = [o for o in occ
            if not any(o2[0] <= o[0] and o[1] <= o2[1] and (o2[1] - o2[0]) > (o[1] - o[0])
                       for o2 in occ)]
    kept.sort()
    seen, out = set(), []
    for _, _, p in kept:
        for b in _resolve(by_pattern[p], specialty, city):
            if id(b) not in seen:
                seen.add(id(b))
                out.append(b)
    return out


def short_alias_hits(text: str, brands: list[dict], matched: list[dict]) -> list[str]:
    """Brands whose < 4-char alias appears as a whole word but that were not counted.

    Only for reporting the RN-01 measurement bias; never counted as a mention.
    """
    t = norm(text or "")
    matched_ids = {id(b) for b in matched}
    hits = []
    for b in brands:
        if id(b) in matched_ids:
            continue
        if any(next(_occurrences(t, p), None) for p in b["short_patterns"]):
            hits.append(b["brand"])
    return hits
