"""Offline analysis of a results.csv (SPEC-001 CA-4, CA-5, CA-6; SPEC-008 CA-3).

Recomputes mentions from the stored answer text with the current brands.csv;
never calls a provider. Definitions follow the sdd-metricas dictamen recorded
in the SPEC-001 ledger.

Batches (SPEC-008): rows outside the batch prompt prefixes are ignored and "local clinic"
uses the batch local cities. A batch with `levels` (Clinica Artica pilot, ADR-005) is
reported per level: the client's raw SoV per provider, the weighted SoV of the core level
(condition (D) of the Go) and, since ADR-009 / SPEC-008 CA-11, the weighted SoV of the growth
level AR computed only with AR rows (condition (C)); "x de n" counts elsewhere. No figure
combines levels. `growth_verdict` and `defense_verdict` compare measurements (CA-11 dictamen).
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
    rows_by = {lv["prefix"]: Counter() for lv in levels}  # level -> provider -> rows, any status
    runs_seen = defaultdict(set)            # (level, pid, provider) -> run labels, any status
    growth_level = b.get("go", {}).get("growth", {}).get("level")
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
        rows_by[lv][prov] += 1
        runs_seen[lv, r.get("prompt_id"), prov].add(str(r.get("run")))
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

    def weighted(by_prov):
        return _weighted(by_prov, cfg)

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

    def complete(lv):  # every weighted provider with >= share of its rows ok (CA-9 (a).2)
        return bool(rows_by[lv]) and all(
            rows_by[lv][p] and cells[lv][p]["valid"] / rows_by[lv][p] >= share
            for p in weighted_provs)

    def uniform_runs(lv):  # runs per question x provider when equal everywhere, else None
        counts = {len(v) for (lv2, _, _), v in runs_seen.items() if lv2 == lv}
        return counts.pop() if len(counts) == 1 else None

    growth = None
    if growth_level in cells:
        by_q = defaultdict(dict)
        for (lv, pid, prov), (n_valid, n_hit) in per_cell.items():
            if lv == growth_level:
                by_q[pid][prov] = (n_valid, n_hit)
        growth = {"level": growth_level, "runs": uniform_runs(growth_level),
                  "complete": complete(growth_level), "by_question": dict(by_q),
                  "weighted": weighted({p: (c["valid"], c["with_client"])
                                        for p, c in cells[growth_level].items()})}

    return {"levels": {k: dict(v) for k, v in cells.items()}, "core": core, "client": client,
            "core_weighted": core_weighted,
            "core_weighted_by_run": {run: weighted(bp) for run, bp in sorted(per_run.items())},
            "core_stability": stability, "cells_with_client": with_client_cells,
            "go_complete": complete(core), "core_runs": uniform_runs(core), "growth": growth,
            "bare_client": bare,
            "models": {p: sorted(m) for p, m in models.items()},
            "named": {k: dict(v) for k, v in named.items()},
            "directories": {k: dict(v) for k, v in directories.items()},
            "short_alias": dict(short_alias), "valid": dict(valid),
            "cost_eur": {k: dict(v) for k, v in cost.items()}, "review": review}


def _weighted(by_prov: dict, cfg: dict):
    """RN-03/RN-04: sum of raw SoV x weight, normalised to the providers with valid answers."""
    num = den = 0.0
    for prov, (n_valid, n_hit) in by_prov.items():
        if n_valid:
            w = cfg["providers"].get(prov, {}).get("weight", 0)
            num += n_hit / n_valid * w
            den += w
    return num / den if den else None


def _pooled(by_question: dict, skip=None) -> dict:
    """provider -> (valid, hit) summed over the questions, leaving out `skip`."""
    out = defaultdict(lambda: [0, 0])
    for pid, by_prov in by_question.items():
        if pid == skip:
            continue
        for prov, (n_valid, n_hit) in by_prov.items():
            out[prov][0] += n_valid
            out[prov][1] += n_hit
    return {p: tuple(v) for p, v in out.items()}


EPS = 1e-9  # thresholds are inclusive and compared without rounding


def growth_verdict(before: dict, afters: list[dict], cfg: dict) -> dict:
    """Condition (C) of the Go (ADR-009; SPEC-008 CA-11 dictamen), only with growth-level rows.

    Yes iff, in EACH of the `after_measurements` measurements, the weighted SoV of the level
    rises >= min_rise_pts over the "before" and the rise stays > 0 when any single question
    is left out on both sides. Not decidable (verdict None) unless every measurement is
    complete and has the design runs, and the number of "after" measurements is the one fixed.
    """
    g = _batch(cfg)["go"]["growth"]

    def w(res, skip=None):
        return _weighted(_pooled(res["growth"]["by_question"], skip), cfg) or 0.0

    def valid_design(res):
        gr = res.get("growth") or {}
        return bool(gr.get("complete")) and gr.get("runs") == g["runs"]

    measurements = []
    for a in afters:
        qs = sorted(set(before["growth"]["by_question"]) | set(a["growth"]["by_question"]))
        delta = (w(a) - w(before)) * 100
        loo = min((w(a, q) - w(before, q)) * 100 for q in qs) if len(qs) > 1 else None
        rise = delta >= g["min_rise_pts"] - EPS
        broad = loo is not None and loo > EPS
        measurements.append({"delta_pts": delta, "loo_min_pts": loo, "rise": rise,
                             "broad": broad, "ok": rise and broad,
                             "valid_design": valid_design(a)})
    decidable = (valid_design(before) and len(afters) == g["after_measurements"]
                 and all(m["valid_design"] for m in measurements))
    return {"level": g["level"], "threshold_pts": g["min_rise_pts"], "runs": g["runs"],
            "decidable": decidable, "measurements": measurements,
            "verdict": all(m["ok"] for m in measurements) if decidable else None}


def defense_verdict(baseline: dict, afters: list[dict], cfg: dict) -> dict:
    """Condition (D) of the Go (ADR-009; SPEC-008 CA-11 dictamen), only with core rows.

    The core weighted SoV counts as a significant drop iff it falls >= max_drop_pts against
    the official baseline in EVERY "after" measurement; (D) holds otherwise. Not decidable
    unless every measurement is complete with the core design runs.
    """
    b = _batch(cfg)
    d = b["go"]["defense"]
    runs = next(lv.get("runs") for lv in b["levels"] if lv["prefix"] == d["level"])

    def valid_design(res):
        return bool(res.get("go_complete")) and res.get("core_runs") == runs

    measurements = []
    for a in afters:
        delta = ((a["core_weighted"] or 0.0) - (baseline["core_weighted"] or 0.0)) * 100
        measurements.append({"delta_pts": delta, "drop": delta <= -d["max_drop_pts"] + EPS,
                             "valid_design": valid_design(a)})
    decidable = (valid_design(baseline) and len(afters) == d["after_measurements"]
                 and all(m["valid_design"] for m in measurements))
    return {"level": d["level"], "threshold_pts": d["max_drop_pts"], "runs": runs,
            "decidable": decidable, "measurements": measurements,
            "verdict": (not all(m["drop"] for m in measurements)) if decidable else None}


def _yes_no(v):
    return "no decidible" if v is None else "sí" if v else "no"


def render_go_verdict(growth: dict, defense: dict, cfg: dict) -> str:
    """Go verdict of the pilot: three yes/no conditions reported apart (ADR-009 §1-§2)."""
    gl, dl = growth["level"], defense["level"]
    out = ["# Veredicto del Go del piloto (ADR-009; SPEC-008 CA-11)", "",
           "Tres condiciones sí/no que se exigen a la vez; ninguna cifra combina niveles "
           "(ADR-009 §2). Umbrales inclusivos y sin redondear.", "",
           f"## (C) Crecer — solo filas {gl}", "",
           f"Regla: en cada medición \"después\", Δ del SoV ponderado de {gl} frente al "
           f"\"antes\" ≥ +{growth['threshold_pts']:g} pts y, quitando cualquier pregunta "
           f"{gl} en los dos lados, Δ sigue > 0 ({growth['runs']} runs por pregunta en todas).",
           "", "| Medición | Δ (pts) | Δ mínimo sin una pregunta (pts) | Umbral | Amplitud | "
           "Diseño válido |", "|---|---|---|---|---|---|"]
    for i, m in enumerate(growth["measurements"], 1):
        loo = "—" if m["loo_min_pts"] is None else f"{m['loo_min_pts']:+.1f}"
        out.append(f"| {i} | {m['delta_pts']:+.1f} | {loo} | {_yes_no(m['rise'])} | "
                   f"{_yes_no(m['broad'])} | {_yes_no(m['valid_design'])} |")
    out += ["", f"Condición (C): **{_yes_no(growth['verdict'])}**", "",
            f"## (D) Defender — solo filas {dl}", "",
            "Regla: caída significativa ⇔ Δ del SoV ponderado del núcleo frente al baseline "
            f"oficial ≤ −{defense['threshold_pts']:g} pts en cada medición \"después\" "
            f"({defense['runs']} runs por pregunta en todas).", "",
            "| Medición | Δ (pts) | Caída | Diseño válido |", "|---|---|---|---|"]
    for i, m in enumerate(defense["measurements"], 1):
        out.append(f"| {i} | {m['delta_pts']:+.1f} | {_yes_no(m['drop'])} | "
                   f"{_yes_no(m['valid_design'])} |")
    out += ["", f"Condición (D): **{_yes_no(defense['verdict'])}**", "",
            "## (A) Atribución", "",
            "≥ 1 paciente atribuido al canal IA (RN-07, H3): no sale del probe; lo registra "
            "SPEC-012."]
    return "\n".join(out) + "\n"


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
                "Decidido por el humano el 2026-09-29, antes de la primera acción (ADR-009): el "
                "núcleo es la condición (D) de defensa y el crecimiento se mide en `AR` "
                "(condición (C)). Si vuelve a salir en otra medición, la regla no cambia."]


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
        out += ["", f"Medición completa para la condición (D) del Go: **{verdict}** (cada proveedor "
                    f"con peso tiene ≥ {share * 100:.0f} % de sus filas del núcleo con "
                    "status=ok; si no, `--resume` en la misma semana)."]
    return out


def _growth_lines(res: dict, b: dict, level: str) -> list[str]:
    """Condition (C) figures of one measurement (SPEC-008 CA-11): only the growth level."""
    go = b.get("go", {})
    gr = res.get("growth")
    if not gr or gr["level"] != level:
        return []
    runs = go.get("growth", {}).get("runs")
    if gr["runs"] != runs:
        return ["", f"SoV ponderado de {level}: no se da (esta medición no tiene {runs} runs en "
                    "cada pregunta × proveedor, el diseño de la condición (C) de CA-11; solo "
                    "recuentos)."]
    share = go.get("min_valid_share", 0)
    return ["", f"SoV ponderado de {level} (solo filas {level}; RN-03/RN-04 normalizado a los "
                "proveedores sondeados; runs sumados por proveedor; condición (C) del Go, "
                f"ADR-009; se compara solo con el \"antes\" de {level} de CA-12): "
                f"**{_fmt(gr['weighted'])}**",
            "", "Medición completa para la condición (C) del Go: "
                f"**{'sí' if gr['complete'] else 'no'}** (cada proveedor con peso tiene "
                f"≥ {share * 100:.0f} % de sus filas {level} con status=ok)."]


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
           "Cada nivel se informa por separado (ADR-005 §4, ADR-009 §2): ninguna cifra suma, "
           f"promedia ni pondera niveles. El SoV ponderado del núcleo {core} usa solo sus filas "
           "(condición (D) del Go) y el del área de influencia, solo las suyas (condición (C), "
           "si la medición tiene los runs del diseño). En el resto, solo recuentos \"x de n\" "
           "(dictamen sdd-metricas (j), ledger de SPEC-007)."]
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
            out += _growth_lines(res, b, k)
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
