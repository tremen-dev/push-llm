"""Offline analysis of a results.csv (SPEC-001 CA-4, CA-5, CA-6).

Recomputes mentions from the stored answer text with the current brands.csv;
never calls a provider. Definitions follow the sdd-metricas dictamen recorded
in the SPEC-001 ledger.
"""
from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path

import matching


def read_results(path: str | Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _pct(n, d):
    return n / d if d else None


def analyze(rows: list[dict], brands: list[dict], cfg: dict) -> dict:
    cells = defaultdict(lambda: {"valid": 0, "with_clinic": 0, "excluded": {}})
    brand_answers = defaultdict(Counter)   # specialty -> brand -> answers naming it
    directories = defaultdict(Counter)     # specialty -> directory -> answers naming it
    short_alias = Counter()                # specialty -> answers with an uncounted short alias
    valid_by_spec = Counter()
    cost = defaultdict(float)
    spec_of = {b["brand"]: b["specialty"] for b in brands}

    for r in rows:
        sp, prov, status = r["specialty"], r["provider"], r.get("status", "ok")
        cell = cells[sp, prov]
        try:
            cost[prov] += float(r.get("cost_eur") or 0)
        except ValueError:
            pass
        if status != "ok":
            cell["excluded"][status] = cell["excluded"].get(status, 0) + 1
            continue
        cell["valid"] += 1
        valid_by_spec[sp] += 1
        hits = matching.find_mentions(r.get("answer", ""), brands, sp, r.get("city"))
        if any(matching.is_local_clinic(b) for b in hits):
            cell["with_clinic"] += 1
        for b in hits:
            if b["type"] == "directory":
                directories[sp][b["brand"]] += 1
            else:
                brand_answers[sp][b["brand"]] += 1
        if matching.short_alias_hits(r.get("answer", ""), brands, hits):
            short_alias[sp] += 1

    for cell in cells.values():
        cell["pct"] = _pct(cell["with_clinic"], cell["valid"])

    weighted = {}
    for sp in {sp for sp, _ in cells}:
        num = den = 0.0
        for (sp2, prov), cell in cells.items():
            if sp2 != sp or not cell["valid"]:
                continue
            w = cfg["providers"].get(prov, {}).get("weight", 0)
            num += cell["pct"] * w
            den += w
        weighted[sp] = num / den if den else None

    leaders = {}
    for sp in {sp for sp, _ in cells}:
        own = {b: n for b, n in brand_answers[sp].items() if spec_of.get(b) == sp}
        top = max(own.values(), default=0)
        leaders[sp] = {"brands": sorted(b for b, n in own.items() if n == top and top > 0),
                       "count": top, "valid": valid_by_spec[sp],
                       "pct": _pct(top, valid_by_spec[sp])}

    return {"cells": dict(cells), "weighted": weighted, "leaders": leaders,
            "directories": {sp: dict(c) for sp, c in directories.items()},
            "short_alias": dict(short_alias), "valid_by_spec": dict(valid_by_spec),
            "cost_eur": dict(cost),
            "exact_aliases": [(a, b["brand"]) for b in brands for a in b.get("exact_aliases", [])]}


def _fmt(p):
    return "—" if p is None else f"{p * 100:.1f} %"


def render_summary(res: dict, cfg: dict) -> str:
    out = ["# Resumen del probe Vigo/Pontevedra", "",
           "Recalculado offline desde results.csv con el brands.csv actual. Solo cuentan las "
           "respuestas con status=ok; las demás se listan como excluidas (SPEC-001 CA-4).", "",
           "## Cobertura por especialidad × proveedor", "",
           "| Especialidad | Proveedor | Válidas | Con clínica local | % | Excluidas |",
           "|---|---|---|---|---|---|"]
    for (sp, prov), c in sorted(res["cells"].items()):
        excl = ", ".join(f"{k}: {v}" for k, v in sorted(c["excluded"].items())) or "0"
        out.append(f"| {sp} | {prov} | {c['valid']} | {c['with_clinic']} | {_fmt(c['pct'])} | {excl} |")
    weights = ", ".join(f"{n} {p['weight']:.2f}" for n, p in cfg["providers"].items())
    out += ["", f"## Agregado ponderado (RN-03/RN-04; pesos: {weights})", "",
            "| Especialidad | % ponderado de respuestas con clínica local |", "|---|---|"]
    for sp in sorted(res["weighted"]):
        out.append(f"| {sp} | {_fmt(res['weighted'][sp])} |")
    out += ["", "## Marca líder por especialidad (solo marcas de la especialidad)", "",
            "| Especialidad | Marca(s) | Respuestas | Válidas | % |", "|---|---|---|---|---|"]
    for sp in sorted(res["leaders"]):
        L = res["leaders"][sp]
        out.append(f"| {sp} | {'; '.join(L['brands']) or '—'} | {L['count']} | {L['valid']} | {_fmt(L['pct'])} |")
    out += ["", "## Menciones de directorios", "",
            "| Especialidad | Directorio | Respuestas | % de válidas |", "|---|---|---|---|"]
    for sp in sorted(res["directories"]):
        for d, n in sorted(res["directories"][sp].items(), key=lambda x: (-x[1], x[0])):
            out.append(f"| {sp} | {d} | {n} | {_fmt(_pct(n, res['valid_by_spec'][sp]))} |")
    active = ", ".join(f"{a} → {b}" for a, b in res.get("exact_aliases", [])) or "ninguna"
    out += ["", "## Sesgo RN-01: respuestas con alias < 4 caracteres no contados (p. ej. \"MIA\")", "",
            f"Siglas cortas que sí cuentan (RN-11/ADR-002, columna exact_aliases, solo en "
            f"mayúsculas y como palabra completa): {active}.", "",
            "| Especialidad | Respuestas |", "|---|---|"]
    for sp in sorted(res["short_alias"]):
        out.append(f"| {sp} | {res['short_alias'][sp]} |")
    out += ["", "## Coste estimado (€)", "", "| Proveedor | € |", "|---|---|"]
    for prov in sorted(res["cost_eur"]):
        out.append(f"| {prov} | {res['cost_eur'][prov]:.2f} |")
    out.append(f"| total | {sum(res['cost_eur'].values()):.2f} |")
    return "\n".join(out) + "\n"
