"""Recount of the manual "before" baseline of the Clínica Ártica pilot (SPEC-007 CA-7).

Implements, from the filled capture CSVs, the counting rules of the sdd-metricas dictamen
recorded in the SPEC-007 ledger (CA-2). The same steps are written for a spreadsheet in
docs/piloto-artica/procedimiento-recuento.md; this script is a convenience, not the
definition.

    python docs/piloto-artica/tools/count_baseline.py P1.csv P2.csv \
        [--aliases alias-canonicos.csv] [--out recuento-antes.md]

Inputs and output live in $PUSHLLM_PRIVADO/piloto-artica/baseline/ (ADR-004): never
point --out inside the repo.
"""
from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import baseline_docs as bd  # noqa: E402  (also puts probe/ on sys.path)
from matching import norm  # noqa: E402

# RN-04 starting weights, normalised to the apps actually measured (RN-03). Claude is an
# observation in the manual baseline (CA-2 dictamen): it never enters the weighted figure.
WEIGHTS = {"chatgpt": 0.55, "gemini": 0.25}
MAIN_PLANS = {"gratuito", "sin_sesion"}
# P-4 (revised by the human, 2026-09-29): every pass, before and after, from Vilaboa. Rows
# taken elsewhere are a location-sensitivity observation, outside the computation.
MAIN_MUNICIPIO = "Vilaboa"
ADJECTIVE_FLAG = "#artica-adjetivo"      # P-1: counts (RN-01), reviewed by hand
DOCTOR_ONLY_FLAG = "#medica-sin-clinica"  # P-2: not a mention, reported apart


def read_rows(paths) -> list[dict]:
    rows = []
    for p in paths:
        with open(p, encoding="utf-8-sig", newline="") as f:
            rows += [{k: (v or "").strip() for k, v in r.items()} for r in csv.DictReader(f)]
    return rows


def read_aliases(path) -> dict[str, str]:
    with open(path, encoding="utf-8-sig", newline="") as f:
        return {norm(r["alias"]): r["canonico"].strip() for r in csv.DictReader(f)}


def _canonical(name: str, aliases: dict[str, str]) -> str:
    return aliases.get(norm(name), name.strip())


def _split(cell: str) -> list[str]:
    return [x.strip() for x in cell.split(";") if x.strip()]


def _other_place(r: dict) -> bool:
    return bool(r["municipio"]) and norm(r["municipio"]) != norm(MAIN_MUNICIPIO)


def _is_main(r: dict) -> bool:
    return (r["plan_cuenta"] in MAIN_PLANS and r["app"] in ({"google"} | set(WEIGHTS))
            and not _other_place(r))


def _check(rows: list[dict]) -> None:
    seen = set()
    for r in rows:
        key = (r["pasada"], r["id_pregunta"], r["app"], r["plan_cuenta"], norm(r["municipio"]))
        if key in seen:
            raise ValueError(f"fila duplicada: {key}")
        seen.add(key)
        if r["respuesta_valida"] == "si" and r["artica_nombrada"] not in {"si", "no"}:
            raise ValueError(f"artica_nombrada vacía o inválida en fila válida: {key}")


LEVELS = ("AR", "AG")
LEVEL_APPS = ("chatgpt", "gemini", "google")
AR_MIN_STABLE_CELLS = 2   # CA-2 (g): "aparece con cierta regularidad"


def count_level(rows: list[dict], prefix: str, aliases: dict[str, str]) -> dict:
    """Indicator of a non-core level (CA-2 g-j, ADR-005 §4): counts "x de n" per app and
    pass, never percentages nor weighted, never mixed with the core."""
    main = [r for r in rows if r["id_pregunta"].startswith(prefix) and _is_main(r)
            and r["respuesta_valida"] == "si"]
    apps, cells = {}, defaultdict(lambda: [0, 0])
    instead, domains = Counter(), Counter()
    for app in LEVEL_APPS:
        rs = [r for r in main if r["app"] == app]
        by_pass = defaultdict(lambda: [0, 0])
        for r in rs:
            by_pass[r["pasada"]][0] += r["artica_nombrada"] == "si"
            by_pass[r["pasada"]][1] += 1
            c = cells[(app, r["id_pregunta"])]
            c[0] += r["artica_nombrada"] == "si"
            c[1] += 1
        apps[app] = {
            "by_pass": {p: tuple(v) for p, v in sorted(by_pass.items())},
            "positions": sorted(int(float(r["posicion_artica"])) for r in rs
                                if r["artica_nombrada"] == "si" and r["posicion_artica"]),
        }
        if app == "google":
            apps[app]["with_overview"] = sum(r["resumen_ia"] == "si" for r in rs)
    for r in main:
        if r["artica_nombrada"] == "no":
            instead.update({_canonical(c, aliases) for c in _split(r["clinicas_nombradas"])})
        domains.update({d.lower().removeprefix("www.") for d in _split(r["dominios_citados"])})
    stable = [k for k, (m, n) in cells.items() if n >= 2 and m == n]
    mentions = sum(m for m, _ in cells.values())
    indicator = (len(stable) >= AR_MIN_STABLE_CELLS) if prefix == "AR" else mentions >= 1
    return {"apps": apps, "stable_cells": stable, "mentions": mentions,
            "valid": sum(n for _, n in cells.values()), "indicator": indicator,
            "instead": dict(instead.most_common()), "domains": domains.most_common()}


def count(rows: list[dict], aliases: dict[str, str] | None = None) -> dict:
    aliases = aliases or {}
    _check(rows)
    av = [r for r in rows if r["id_pregunta"].startswith("AV")]
    main = [r for r in av if _is_main(r)]

    apps = {}
    for app in WEIGHTS:
        rs = [r for r in main if r["app"] == app]
        valid = [r for r in rs if r["respuesta_valida"] == "si"]
        named = [r for r in valid if r["artica_nombrada"] == "si"]
        positions = [float(r["posicion_artica"]) for r in named if r["posicion_artica"]]
        by_pass = defaultdict(lambda: [0, 0])
        for r in valid:
            by_pass[r["pasada"]][0] += r["artica_nombrada"] == "si"
            by_pass[r["pasada"]][1] += 1
        instead = Counter()
        for r in valid:
            if r["artica_nombrada"] == "no":
                instead.update({_canonical(c, aliases) for c in _split(r["clinicas_nombradas"])})
        apps[app] = {
            "valid": len(valid), "excluded": len(rs) - len(valid), "mentions": len(named),
            "sov": len(named) / len(valid) if valid else None,
            "by_pass": {p: m / n for p, (m, n) in sorted(by_pass.items())},
            "mean_position": sum(positions) / len(positions) if positions else None,
            "instead": dict(instead.most_common()),
        }

    measured = {a: WEIGHTS[a] for a, c in apps.items() if c["valid"]}
    weighted = (sum(apps[a]["sov"] * w for a, w in measured.items()) / sum(measured.values())
                if measured else None)

    g_rows = [r for r in main if r["app"] == "google" and r["respuesta_valida"] == "si"]
    g_over = [r for r in g_rows if r["resumen_ia"] == "si"]
    g_named = [r for r in g_over if r["artica_nombrada"] == "si"]
    google = {
        "searches": len(g_rows), "with_overview": len(g_over), "mentions": len(g_named),
        "sov_all": len(g_named) / len(g_rows) if g_rows else None,
        "sov_with_overview": len(g_named) / len(g_over) if g_over else None,
    }

    domains = Counter()
    for r in main:
        if r["respuesta_valida"] == "si":
            domains.update({d.lower().removeprefix("www.") for d in _split(r["dominios_citados"])})

    stability = defaultdict(lambda: [0, 0])
    for r in main:
        if r["respuesta_valida"] == "si" and r["app"] in WEIGHTS:
            s = stability[(r["app"], r["id_pregunta"])]
            s[0] += r["artica_nombrada"] == "si"
            s[1] += 1

    places = defaultdict(lambda: [0, 0])
    for r in av:
        if _other_place(r) and r["respuesta_valida"] == "si":
            s = places[(r["municipio"], r["app"])]
            s[0] += r["artica_nombrada"] == "si"
            s[1] += 1

    obs = defaultdict(lambda: [0, 0])
    for r in av:
        if not _is_main(r) and not _other_place(r) and r["respuesta_valida"] == "si":
            o = obs[(r["app"], r["plan_cuenta"])]
            o[0] += r["artica_nombrada"] == "si"
            o[1] += 1

    return {
        "apps": apps, "weighted": weighted, "weights_used": measured, "google": google,
        "domains": domains.most_common(), "stability": {k: tuple(v) for k, v in stability.items()},
        "observations": [{"key": k, "mentions": m, "valid": n, "sov": m / n}
                         for k, (m, n) in sorted(obs.items())],
        "location_sensitivity": [{"municipio": m, "app": a, "mentions": k, "valid": n}
                                 for (m, a), (k, n) in sorted(places.items())],
        "levels": {lv: count_level(rows, lv, aliases) for lv in LEVELS},
        "brand_rows": [r for r in rows if r["id_pregunta"].startswith("AM")],
        "adjective_flags": sum(ADJECTIVE_FLAG in r["observaciones"] for r in main),
        "doctor_only_flags": sum(DOCTOR_ONLY_FLAG in r["observaciones"] for r in main),
    }


def _pct(x):
    return "—" if x is None else f"{x * 100:.1f} %"


def render(res: dict, sources: list[str]) -> str:
    out = ["# Recuento \"antes\" — piloto Clínica Ártica (SPEC-007 CA-7)", "",
           "Privado (ADR-004). Generado con `docs/piloto-artica/tools/count_baseline.py` "
           "según el dictamen de CA-2 del ledger de SPEC-007.", "",
           "Fuentes: " + ", ".join(f"`{s}`" for s in sources), "",
           "## Núcleo (AV) — Por app (solo cuentas gratuitas; único nivel del criterio Go)", "",
           "| App | Válidas | Excluidas | Con la clínica | SoV bruto | Por pasada | Posición media |",
           "|---|---|---|---|---|---|---|"]
    for app, c in res["apps"].items():
        by_pass = ", ".join(f"{p} {_pct(v)}" for p, v in c["by_pass"].items()) or "—"
        pos = "—" if c["mean_position"] is None else f"{c['mean_position']:.2f}"
        out.append(f"| {app} | {c['valid']} | {c['excluded']} | {c['mentions']} | "
                   f"{_pct(c['sov'])} | {by_pass} | {pos} |")
    w = ", ".join(f"{a} {v:.2f}" for a, v in res["weights_used"].items())
    out += ["", f"## SoV ponderado ChatGPT + Gemini (RN-03/RN-04; pesos {w}, normalizados)", "",
            f"**{_pct(res['weighted'])}**", "",
            "## Clínicas que aparecen en su lugar (respuestas sin la clínica)", ""]
    for app, c in res["apps"].items():
        top = "; ".join(f"{n} ({k})" for n, k in list(c["instead"].items())[:10]) or "—"
        out.append(f"- {app}: {top}")
    g = res["google"]
    out += ["", "## Google, resumen de IA (canal aparte, sin ponderar; RN-04)", "",
            f"- Búsquedas válidas: {g['searches']}; con resumen de IA: {g['with_overview']}; "
            f"con la clínica en el resumen: {g['mentions']}",
            f"- Sobre todas las búsquedas: {_pct(g['sov_all'])}; sobre las que tuvieron "
            f"resumen: {_pct(g['sov_with_overview'])}", "",
            "## Dominios más citados (todas las apps)", ""]
    out += [f"- {d}: {n}" for d, n in res["domains"][:15]] or ["- —"]
    out += ["", "## Estabilidad por pregunta (pasadas con la clínica / pasadas válidas)", "",
            "| App | Pregunta | Con la clínica |", "|---|---|---|"]
    out += [f"| {a} | {q} | {m} de {n} |" for (a, q), (m, n) in sorted(res["stability"].items())]
    names = {"AR": ("Área de influencia (AR)", "aparece con cierta regularidad "
                    f"(≥ {AR_MIN_STABLE_CELLS} casillas pregunta × app con la clínica en las "
                    "dos pasadas)"),
             "AG": ("Galicia (AG)", "aparece alguna vez (≥ 1 respuesta válida con la clínica)")}
    for lv, lres in res["levels"].items():
        title, definition = names[lv]
        out += ["", f"## {title}", "",
                "Indicador aparte (ADR-005 §4): recuentos \"x de n\", sin ponderar y sin "
                "sumarse al núcleo.", "",
                f"- {definition}: **{'sí' if lres['indicator'] else 'no'}** "
                f"({lres['mentions']} de {lres['valid']} respuestas válidas con la clínica)"]
        for app, a in lres["apps"].items():
            passes = ", ".join(f"{p}: {m} de {n}" for p, (m, n) in a["by_pass"].items()) or "sin filas"
            extra = f"; con resumen de IA: {a['with_overview']}" if "with_overview" in a else ""
            pos = ", ".join(str(x) for x in a["positions"]) or "—"
            out.append(f"- {app}: {passes}{extra}; puestos: {pos}")
        stable = ", ".join(f"{a} {q}" for a, q in sorted(lres["stable_cells"])) or "—"
        out.append(f"- Casillas con la clínica en las dos pasadas: {stable}")
        top = "; ".join(f"{n} ({k})" for n, k in list(lres["instead"].items())[:10]) or "—"
        out.append(f"- En su lugar: {top}")
        doms = "; ".join(f"{d} ({k})" for d, k in lres["domains"][:10]) or "—"
        out.append(f"- Dominios citados: {doms}")
    out += ["", "## Observaciones (no cuentan: Claude, cuentas de pago)", ""]
    out += [f"- {a} ({plan}): {o['mentions']} de {o['valid']} ({_pct(o['sov'])})"
            for o in res["observations"] for a, plan in [o["key"]]] or ["- —"]
    out += ["", f"## Observación de sensibilidad a la ubicación (fuera de {MAIN_MUNICIPIO}; no cuenta)", ""]
    out += [f"- {s['app']} desde {s['municipio']}: {s['mentions']} de {s['valid']}"
            for s in res["location_sensitivity"]] or ["- —"]
    out += ["", f"Filas marcadas `{ADJECTIVE_FLAG}` (cuentan; revisar a mano): "
            f"{res['adjective_flags']}",
            f"Filas marcadas `{DOCTOR_ONLY_FLAG}` (no cuentan como mención): "
            f"{res['doctor_only_flags']}", "",
            "## Preguntas de marca (AM)", "",
            "| Pasada | Pregunta | App | Captura | Observaciones |", "|---|---|---|---|---|"]
    out += [f"| {r['pasada']} | {r['id_pregunta']} | {r['app']} | {r['fichero_captura']} | "
            f"{r['observaciones']} |" for r in res["brand_rows"]]
    return "\n".join(out) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("csv", nargs="+")
    ap.add_argument("--aliases")
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    res = count(read_rows(a.csv), read_aliases(a.aliases) if a.aliases else {})
    md = render(res, [Path(p).name for p in a.csv])
    if a.out:
        Path(a.out).write_text(md, encoding="utf-8")
    else:
        sys.stdout.write(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
