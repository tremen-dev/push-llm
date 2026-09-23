"""Brand mention matching (RN-01) with the sdd-metricas dictamen of SPEC-001 CA-6.

- Accent/case-insensitive, whole-word matching on normalised text.
- Only names/aliases of >= 4 normalised characters count (RN-01).
- An occurrence contained in a longer overlapping occurrence is dropped.
- An alias shared by several brands goes to the candidates of the prompt's
  specialty, then of the prompt's city; if none (or several) remain, to all.
- A brand counts at most once per answer; order = first appearance.
"""
from __future__ import annotations

import csv
import re
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
MIN_ALIAS_LEN = 4
LOCAL_CITIES = {"Vigo", "Pontevedra"}


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def _names(row: dict) -> list[str]:
    return [row["brand"]] + [a for a in row["aliases"].split(";") if a.strip()]


def load_brands(path: str | Path | None = None) -> list[dict]:
    with open(path or HERE / "brands.csv", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        normed = [norm(n) for n in _names(r)]
        r["patterns"] = list(dict.fromkeys(n for n in normed if len(n) >= MIN_ALIAS_LEN))
        r["short_patterns"] = list(dict.fromkeys(n for n in normed if 0 < len(n) < MIN_ALIAS_LEN))
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
