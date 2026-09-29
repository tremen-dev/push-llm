"""Offline analysis of a results.csv (SPEC-001 CA-4, CA-5, CA-6; SPEC-008 CA-3).

Recomputes mentions from the stored answer text with the current brands.csv;
never calls a provider. Definitions follow the sdd-metricas dictamen recorded
in the SPEC-001 ledger.

Batches (SPEC-008): rows outside the batch prompt prefixes are ignored and "local clinic"
uses the batch local cities. A batch with `levels` (Clinica Artica pilot, ADR-005) is
reported per level: the client's raw SoV per provider, the weighted SoV only for the core
level and only "x de n" counts outside the core (sdd-metricas (g)-(j), SPEC-007 ledger).
"""
from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

import matching
import settings

DEFAULT_TITLE = "Resumen del probe Vigo/Pontevedra"


def read_results(path: str | Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _pct(n, d):
    return n / d if d else None


def _batch(cfg: dict) -> dict:
    return cfg.get("batch") or {}


def _in_batch(rows: list[dict], cfg: dict) -> tuple[list[dict], int]:
    b = _batch(cfg)
    if not b.get("prompt_prefixes"):
        return rows, 0
    in_batch = settings.prompt_matcher(b)
    kept = [r for r in rows if in_batch(r.get("prompt_id"))]
    return kept, len(rows) - len(kept)


def analyze(rows: list[dict], brands: list[dict], cfg: dict) -> dict:
    rows, ignored = _in_batch(rows, cfg)
    if _batch(cfg).get("levels"):
        res = analyze_levels(rows, brands, cfg)
    else:
        res = _analyze_specialties(rows, brands, cfg)
    res["ignored_rows"] = ignored
    return res


def _analyze_specialties(rows: list[dict], brands: list[dict], cfg: dict) -> dict:
    local_cities = _batch(cfg).get("local_cities")
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
        if any(matching.is_local_clinic(b, local_cities) for b in hits):
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
    if "levels" in res:
        return render_levels(res, cfg)
    out = [f"# {_batch(cfg).get('title', DEFAULT_TITLE)}", "",
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
    out += _ignored_note(res)
    return "\n".join(out) + "\n"


def _ignored_note(res: dict) -> list[str]:
    n = res.get("ignored_rows", 0)
    return ["", f"Filas de results.csv fuera de este lote, ignoradas: {n}."] if n else []


# ---------------------------------------------------------------- levels (SPEC-008)

def _level_of(pid: str, levels: list[dict]) -> str | None:
    for lv in levels:
        if settings.prompt_matcher([lv["prefix"]])(pid):
            return lv["prefix"]
    return None


def analyze_levels(rows: list[dict], brands: list[dict], cfg: dict) -> dict:
    """Per level x provider: valid answers, answers naming the client, local clinics,
    excluded rows; named clinics and directories per level; weighted SoV of the core only."""
    b = _batch(cfg)
    levels = b["levels"]
    core = next(lv["prefix"] for lv in levels if lv.get("core"))
    client = b["client_brand"]
    local_cities = b.get("local_cities")

    def new_cell():
        return {"valid": 0, "with_client": 0, "with_local": 0, "excluded": {}}

    cells = {lv["prefix"]: defaultdict(new_cell) for lv in levels}
    named = {lv["prefix"]: Counter() for lv in levels}  # clinic -> answers naming it
    directories = {lv["prefix"]: Counter() for lv in levels}
    cost = {lv["prefix"]: defaultdict(float) for lv in levels}
    short_alias, valid = Counter(), Counter()
    terms = [matching.norm(t) for t in b.get("review_terms", [])]
    review = []
    per_cell = defaultdict(lambda: [0, 0])  # (level, pid, provider) -> [valid runs, with client]
    per_run = defaultdict(lambda: defaultdict(lambda: [0, 0]))  # core run -> prov -> [valid, hit]
    rows_core = Counter()                   # core rows per provider, any status
    models = defaultdict(set)
    bare = {lv["prefix"]: [] for lv in levels}
    client_row = next((x for x in brands if x["brand"] == client), None)
    review_pats = {matching.norm(a) for a in b.get("client_review_aliases", [])}
    strong_pats = [p for p in (client_row or {}).get("patterns", []) if p not in review_pats]

    for r in rows:
        lv = _level_of(r.get("prompt_id", ""), levels)
        if lv is None:
            continue
        prov, status = r["provider"], r.get("status", "ok")
        cell = cells[lv][prov]
        if r.get("model"):
            models[prov].add(r["model"])
        if lv == core:
            rows_core[prov] += 1
        try:
            cost[lv][prov] += float(r.get("cost_eur") or 0)
        except ValueError:
            pass
        if status != "ok":
            cell["excluded"][status] = cell["excluded"].get(status, 0) + 1
            continue
        cell["valid"] += 1
        valid[lv] += 1
        hits = matching.find_mentions(r.get("answer", ""), brands, r.get("specialty"),
                                      r.get("city"))
        has_client = any(h["brand"] == client for h in hits)
        pc = per_cell[lv, r.get("prompt_id"), prov]
        pc[0] += 1
        if lv == core:
            pr = per_run[str(r.get("run"))][prov]
            pr[0] += 1
            pr[1] += has_client
        if has_client:
            cell["with_client"] += 1
            pc[1] += 1
            padded = f" {matching.norm(r.get('answer', ''))} "
            if review_pats and not any(f" {p} " in padded for p in strong_pats):
                bare[lv].append((r.get("prompt_id"), prov, str(r.get("run"))))
        if any(matching.is_local_clinic(h, local_cities) for h in hits):
            cell["with_local"] += 1
        for h in hits:
            (directories if h["type"] == "directory" else named)[lv][h["brand"]] += 1
        if matching.short_alias_hits(r.get("answer", ""), brands, hits):
            short_alias[lv] += 1
        review += _review_hits(r, lv, brands, terms)

    for lv_cells in cells.values():
        for cell in lv_cells.values():
            cell["pct"] = _pct(cell["with_client"], cell["valid"])

    def weighted(by_prov):  # RN-03 normalised to the providers with valid answers
        num = den = 0.0
        for prov, (n_valid, n_hit) in by_prov.items():
            if n_valid:
                w = cfg["providers"].get(prov, {}).get("weight", 0)
                num += n_hit / n_valid * w
                den += w
        return num / den if den else None

    # RN-03 on the core level only (ADR-005 §4); runs pooled per provider (CA-9 (b))
    core_weighted = weighted({p: (c["valid"], c["with_client"]) for p, c in cells[core].items()})
    stability = {"all": 0, "some": 0, "none": 0, "cells": 0}
    with_client_cells = {lv["prefix"]: [] for lv in levels}
    for (lv, pid, prov), (n_valid, n_hit) in sorted(per_cell.items()):
        if lv == core:
            stability["cells"] += 1
            stability["all" if n_hit == n_valid else "some" if n_hit else "none"] += 1
        elif n_hit:
            with_client_cells[lv].append((pid, prov, n_hit, n_valid))
    share = b.get("go", {}).get("min_valid_share", 0)
    weighted_provs = [p for p, pc in cfg["providers"].items() if pc.get("weight", 0) > 0]
    complete = bool(rows_core) and all(
        rows_core[p] and cells[core][p]["valid"] / rows_core[p] >= share for p in weighted_provs)

    return {"levels": {k: dict(v) for k, v in cells.items()}, "core": core, "client": client,
            "core_weighted": core_weighted,
            "core_weighted_by_run": {run: weighted(bp) for run, bp in sorted(per_run.items())},
            "core_stability": stability, "cells_with_client": with_client_cells,
            "go_complete": complete, "bare_client": bare,
            "models": {p: sorted(m) for p, m in models.items()},
            "named": {k: dict(v) for k, v in named.items()},
            "directories": {k: dict(v) for k, v in directories.items()},
            "short_alias": dict(short_alias), "valid": dict(valid),
            "cost_eur": {k: dict(v) for k, v in cost.items()}, "review": review}


SENTENCE_RE = re.compile(r"(?<=[.!?;])\s+|\n+")


def _review_hits(row: dict, level: str, brands: list[dict], terms: list[str]) -> list[dict]:
    """Sentences of a valid answer that name a clinic next to a "no doctor" expression
    (human decision 2026-09-29, SPEC-008 ledger). Only for manual review, never counted."""
    if not terms:
        return []
    out = []
    for sentence in SENTENCE_RE.split(row.get("answer", "") or ""):
        padded = f" {matching.norm(sentence)} "
        found = [t for t in terms if f" {t} " in padded]
        if not found:
            continue
        clinics = [b["brand"] for b in matching.find_mentions(sentence, brands)
                   if b["type"] != "directory"]
        if clinics:
            out.append({"level": level, "prompt_id": row.get("prompt_id"),
                        "provider": row.get("provider"), "run": row.get("run"),
                        "brands": clinics, "terms": found})
    return out


def _of(n, d):
    return f"{n} de {d}"


def _ceiling_warning(res: dict, b: dict) -> list[str]:
    """CA-10: the core weighted SoV is within 15 pts of its ceiling (only AV, only the probe)."""
    ceiling = b.get("go", {}).get("ceiling")
    w = res["core_weighted"]
    if ceiling is None or w is None or round(w, 9) < ceiling:
        return []
    return ["", f"> **Aviso de techo (SPEC-008 CA-10)**: el SoV ponderado del núcleo es "
                f"≥ {ceiling * 100:.0f} %, a menos de {100 - ceiling * 100:.0f} pts de su techo. "
                "Antes de la primera acción, el humano decide y deja registrado en el ledger si "
                "se mantiene el criterio Go, se mide sobre un subconjunto de `AV` o se cambia el "
                "umbral; nunca después de ver el efecto."]


def _core_go_lines(res: dict, b: dict, client: str) -> list[str]:
    """Noise and validity of a Go measurement (SPEC-008 CA-9 (b), (e), (f))."""
    out = ["", "SoV ponderado del núcleo por run (ruido entre runs del mismo día; el criterio "
               "Go usa la cifra de arriba, con los runs sumados):", "",
           "| Run | SoV ponderado |", "|---|---|"]
    for run, w in res["core_weighted_by_run"].items():
        out.append(f"| {run} | {_fmt(w)} |")
    st = res["core_stability"]
    n = st["cells"]
    out += ["", f"Estabilidad por pregunta × proveedor del núcleo: {client} en todos sus runs "
                f"válidos: {_of(st['all'], n)}; en alguno: {_of(st['some'], n)}; en ninguno: "
                f"{_of(st['none'], n)}."]
    share = b.get("go", {}).get("min_valid_share")
    if share is not None:
        verdict = "sí" if res["go_complete"] else "no"
        out += ["", f"Medición completa para el criterio Go: **{verdict}** (cada proveedor "
                    f"con peso tiene ≥ {share * 100:.0f} % de sus filas del núcleo con "
                    "status=ok; si no, `--resume` en la misma semana)."]
    return out


def _bare_lines(res: dict, level: str, client: str, aliases: list[str]) -> list[str]:
    """F-SPEC-008-3 / CA-9 (h): answers naming the client only through a common-word alias."""
    if not aliases:
        return []
    bare = res.get("bare_client", {}).get(level, [])
    listed = "; ".join(f"{pid} × {prov} (run {run})" for pid, prov, run in bare) or "ninguna"
    quoted = " o ".join(f'"{a}"' for a in aliases)
    return ["", f"Respuestas con {client} solo por {quoted} suelta (cuentan, RN-01; revisar "
                f"a mano si es adjetivo, F-SPEC-008-3): {listed}."]


def render_levels(res: dict, cfg: dict) -> str:
    b = _batch(cfg)
    core, client = res["core"], res["client"]
    weights = ", ".join(f"{n} {p['weight']:.2f}" for n, p in cfg["providers"].items())
    out = [f"# {b.get('title', DEFAULT_TITLE)}", "",
           "Recalculado offline desde results.csv con el brands.csv actual y solo las marcas "
           "del lote. Solo cuentan las respuestas con status=ok; las demás se listan como "
           "excluidas.", "",
           "Cada nivel se informa por separado (ADR-005 §4): ninguna cifra suma, promedia ni "
           f"pondera niveles. El SoV ponderado es solo del núcleo {core} (criterio Go). Fuera "
           "del núcleo, solo recuentos \"x de n\" (dictamen sdd-metricas (j), ledger de "
           "SPEC-007)."]
    for lv in b["levels"]:
        k = lv["prefix"]
        is_core = k == core
        out += ["", f"## Nivel {k} — {lv['label']}", ""]
        if is_core:
            out += [f"| Proveedor | Válidas | Con {client} | SoV bruto | Con clínica local | "
                    "Excluidas |", "|---|---|---|---|---|---|"]
        else:
            out += [f"| Proveedor | Válidas | Con {client} | Excluidas |", "|---|---|---|---|"]
        for prov, c in sorted(res["levels"][k].items()):
            excl = ", ".join(f"{s}: {n}" for s, n in sorted(c["excluded"].items())) or "0"
            mid = (f" {_fmt(c['pct'])} | {_of(c['with_local'], c['valid'])} |" if is_core
                   else "")
            out.append(f"| {prov} | {c['valid']} | {_of(c['with_client'], c['valid'])} |"
                       f"{mid} {excl} |")
        if is_core:
            out += ["", "SoV ponderado del núcleo (RN-03/RN-04, normalizado a los proveedores "
                        f"sondeados; pesos: {weights}; runs sumados por proveedor): "
                        f"**{_fmt(res['core_weighted'])}**"]
            out += _ceiling_warning(res, b)
            out += _core_go_lines(res, b, client)
        else:
            cw = res["cells_with_client"].get(k, [])
            listed = "; ".join(f"{pid} × {prov} ({_of(h, v)} runs)" for pid, prov, h, v in cw)
            out += ["", f"Casillas pregunta × proveedor con {client} (para comparar periodos "
                        f"a mano, dictamen CA-9 (g) del ledger de SPEC-008): {listed or 'ninguna'}."]
        out += _bare_lines(res, k, client, b.get("client_review_aliases", []))
        n = res["valid"].get(k, 0)
        out += ["", f"Clínicas nombradas en {k} (respuestas válidas que la nombran):", "",
                "| Marca | Respuestas |", "|---|---|"]
        for brand, cnt in sorted(res["named"][k].items(), key=lambda x: (-x[1], x[0])):
            out.append(f"| {brand} | {_of(cnt, n)} |")
        out += ["", f"Directorios en {k}:", "", "| Directorio | Respuestas |", "|---|---|"]
        for d, cnt in sorted(res["directories"][k].items(), key=lambda x: (-x[1], x[0])):
            out.append(f"| {d} | {_of(cnt, n)} |")
        out += ["", f"Respuestas con alias < 4 caracteres no contados (sesgo RN-01) en {k}: "
                    f"{_of(res['short_alias'].get(k, 0), n)}."]
    out += ["", "## Coste estimado (€) — operativo, no es una cifra de visibilidad", "",
            "| Nivel | Proveedor | € |", "|---|---|---|"]
    total = 0.0
    for lv in b["levels"]:
        for prov, eur in sorted(res["cost_eur"][lv["prefix"]].items()):
            out.append(f"| {lv['prefix']} | {prov} | {eur:.2f} |")
            total += eur
    out.append(f"| lote | total | {total:.2f} |")
    out += ["", "## Modelos servidos (columna model; D-5/RN-10, dictamen CA-9 (f))", "",
            "| Proveedor | Modelo(s) |", "|---|---|"]
    for prov, ms in sorted(res.get("models", {}).items()):
        out.append(f"| {prov} | {'; '.join(ms)} |")
    if b.get("review_terms"):
        out += ["", "## Observaciones para revisar a mano (no es una métrica)", "",
                "Frases de respuestas válidas que nombran una clínica junto a expresiones como "
                "\"sin médico\", \"esteticista\" o \"no sanitario\". Coincidencia literal: puede "
                "haber falsos positivos (p. ej. la frase habla de otra clínica); leer la "
                "respuesta completa. Decisión del humano del 2026-09-29 (ledger de SPEC-008).",
                "", "| Nivel | Pregunta | Proveedor | Run | Clínicas en la frase | Expresión |",
                "|---|---|---|---|---|---|"]
        for o in res.get("review", []):
            out.append(f"| {o['level']} | {o['prompt_id']} | {o['provider']} | {o['run']} | "
                       f"{'; '.join(o['brands'])} | {'; '.join(o['terms'])} |")
    out += _ignored_note(res)
    return "\n".join(out) + "\n"
