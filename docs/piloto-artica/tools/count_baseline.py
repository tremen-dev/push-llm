"""Calibration recount of the Clínica Ártica pilot (SPEC-007 CA-7, amendment 2026-09-29 (b)).

Counts ONE manual pass ("antes" or "despues": 15 AV questions in ChatGPT, Gemini and
Google, plus the AM brand questions) and compares it, cell by cell (AV question x
assistant), with the paired AV execution of the probe (results.csv of the Viveiro batch,
written after SPEC-013, i.e. with the searched_urls column). Rules: the sdd-metricas
dictamen (k)-(n) in the SPEC-007 ledger. The same steps are written for a spreadsheet in
docs/piloto-artica/procedimiento-recuento.md; this script is a convenience, not the
definition. Nothing here enters the Go criterion (probe vs probe, SPEC-008 CA-7/CA-9).

    python docs/piloto-artica/tools/count_baseline.py ANTES.csv --probe results.csv \
        [--aliases alias-canonicos.csv] [--out calibracion-antes.md]

Inputs and output live in $PUSHLLM_PRIVADO/piloto-artica/baseline/ (ADR-004): never
point --out inside the repo.
"""
from __future__ import annotations

import argparse
import csv
import statistics
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from baseline_docs import norm  # noqa: E402  (RN-01 normalisation of probe/matching.py)

# Assistants present in both instruments (dictamen k1): manual app -> probe provider.
PAIRED = {"chatgpt": "openai", "gemini": "gemini"}
MAIN_APPS = ("chatgpt", "gemini", "google")
MAIN_PLANS = {"gratuito", "sin_sesion"}
# P-4 (revised by the human, 2026-09-29): every pass, before and after, from Vilaboa. Rows
# taken elsewhere are a location-sensitivity observation, outside the computation.
MAIN_MUNICIPIO = "Vilaboa"
ADJECTIVE_FLAG = "#artica-adjetivo"      # P-1: counts (RN-01), reviewed by hand
DOCTOR_ONLY_FLAG = "#medica-sin-clinica"  # P-2: not a mention, reported apart
CLIENT = "Clínica Ártica"                 # client_brand of probe/batches/viveiro.json

# Thresholds of the dictamen (k)-(m).
MAX_WINDOW_DAYS = 7        # k5: probe AV execution <-> manual pass
MIN_COMPARABLE = 12        # l2b: comparable cells per assistant (of 15)
MIN_AGREEMENT = 0.70       # l2c: same "sale / no sale" (11 of 15)
MAX_SOV_GAP = 0.20         # l2d: |raw SoV app - raw SoV probe| per assistant
POSITION_TOLERANCE = 2     # l2: positions reported as "close" within 2 places; never decides
AIO_CLEAR_CHANGE = 5       # m4: before/after of AI Overviews, searches with the clinic

# Columns of probe/run_probe.py after SPEC-013 (searched_urls last).
PROBE_COLUMNS = ["timestamp_utc", "prompt_id", "specialty", "city", "provider", "run", "model",
                 "status", "input_tokens", "output_tokens", "web_searches", "cost_eur",
                 "brands_mentioned", "directories_mentioned", "cited_urls", "answer",
                 "searched_urls"]


# ------------------------------------------------------------------ reading
def read_rows(paths) -> list[dict]:
    rows = []
    for p in paths:
        with open(p, encoding="utf-8-sig", newline="") as f:
            rows += [{k: (v or "").strip() for k, v in r.items()} for r in csv.DictReader(f)]
    return rows


def read_aliases(path) -> dict[str, str]:
    with open(path, encoding="utf-8-sig", newline="") as f:
        return {norm(r["alias"]): r["canonico"].strip() for r in csv.DictReader(f)}


def read_probe(path) -> list[dict]:
    """results.csv of the probe. Refuses a file written before SPEC-013 (no searched_urls):
    there Gemini's cited_urls meant every grounding chunk (dictamen k)."""
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if "searched_urls" not in (reader.fieldnames or []):
            raise ValueError(f"{path}: results.csv sin la columna searched_urls (anterior a "
                             "SPEC-013); empareja la pasada con una ejecución posterior")
        return [{k: (v or "").strip() for k, v in r.items()} for r in reader]


# ------------------------------------------------------------------ manual pass
def _canonical(name: str, aliases: dict[str, str]) -> str:
    return aliases.get(norm(name), name.strip())


def _split(cell: str) -> list[str]:
    return [x.strip() for x in (cell or "").split(";") if x.strip()]


def _other_place(r: dict) -> bool:
    return bool(r["municipio"]) and norm(r["municipio"]) != norm(MAIN_MUNICIPIO)


def _is_main(r: dict) -> bool:
    return r["plan_cuenta"] in MAIN_PLANS and r["app"] in MAIN_APPS and not _other_place(r)


def _check(rows: list[dict]) -> None:
    seen = set()
    for r in rows:
        key = (r["pasada"], r["id_pregunta"], r["app"], r["plan_cuenta"], norm(r["municipio"]))
        if key in seen:
            raise ValueError(f"fila duplicada: {key}")
        seen.add(key)
        if r["respuesta_valida"] == "si" and r["artica_nombrada"] not in {"si", "no"}:
            raise ValueError(f"artica_nombrada vacía o inválida en fila válida: {key}")
    passes = {r["pasada"] for r in rows}
    if len(passes) > 1:
        raise ValueError(f"el recuento es de una sola pasada; hay {sorted(passes)}")


def _core(rows: list[dict]) -> list[dict]:
    return [r for r in rows if r["id_pregunta"].startswith("AV") and _is_main(r)]


def _date(text: str) -> date | None:
    try:
        return date.fromisoformat(text[:10])
    except ValueError:
        return None


def count(rows: list[dict], aliases: dict[str, str] | None = None) -> dict:
    aliases = aliases or {}
    _check(rows)
    av = [r for r in rows if r["id_pregunta"].startswith("AV")]
    main = _core(rows)

    apps = {}
    for app in PAIRED:
        rs = [r for r in main if r["app"] == app]
        valid = [r for r in rs if r["respuesta_valida"] == "si"]
        named = [r for r in valid if r["artica_nombrada"] == "si"]
        positions = [float(r["posicion_artica"]) for r in named if r["posicion_artica"]]
        instead = Counter()
        for r in valid:
            if r["artica_nombrada"] == "no":
                instead.update({_canonical(c, aliases) for c in _split(r["clinicas_nombradas"])})
        apps[app] = {
            "valid": len(valid), "excluded": len(rs) - len(valid), "mentions": len(named),
            "sov": len(named) / len(valid) if valid else None,
            "mean_position": sum(positions) / len(positions) if positions else None,
            "instead": dict(instead.most_common()),
        }

    g_rows = [r for r in main if r["app"] == "google" and r["respuesta_valida"] == "si"]
    g_over = [r for r in g_rows if r["resumen_ia"] == "si"]
    google = {"searches": len(g_rows), "with_overview": len(g_over),
              "mentions": sum(r["artica_nombrada"] == "si" for r in g_over)}

    domains = Counter()
    for r in main:
        if r["respuesta_valida"] == "si":
            domains.update({d.lower().removeprefix("www.") for d in _split(r["dominios_citados"])})

    places = defaultdict(lambda: [0, 0])
    obs = defaultdict(lambda: [0, 0])
    for r in av:
        if r["respuesta_valida"] != "si":
            continue
        if _other_place(r):
            s = places[(r["municipio"], r["app"])]
        elif not _is_main(r):
            s = obs[(r["app"], r["plan_cuenta"])]
        else:
            continue
        s[0] += r["artica_nombrada"] == "si"
        s[1] += 1

    dates = [d for d in (_date(r["fecha_hora_local"]) for r in main) if d]
    return {
        "pasada": next(iter({r["pasada"] for r in rows}), ""),
        "apps": apps, "google": google, "domains": domains.most_common(),
        "observations": [{"key": k, "mentions": m, "valid": n, "sov": m / n}
                         for k, (m, n) in sorted(obs.items())],
        "location_sensitivity": [{"municipio": m, "app": a, "mentions": k, "valid": n}
                                 for (m, a), (k, n) in sorted(places.items())],
        "brand_rows": [r for r in rows if r["id_pregunta"].startswith("AM")],
        "ignored_rows": sum(r["id_pregunta"][:2] in {"AR", "AG"} for r in rows),
        "adjective_flags": sum(ADJECTIVE_FLAG in r["observaciones"] for r in main),
        "doctor_only_flags": sum(DOCTOR_ONLY_FLAG in r["observaciones"] for r in main),
        "dates": (min(dates), max(dates)) if dates else None,
    }


# ------------------------------------------------------------------ probe side
def _probe_position(brands: str, client: str) -> int | None:
    names = [norm(b) for b in _split(brands)]
    return names.index(norm(client)) + 1 if norm(client) in names else None


def summarize_probe(probe_rows: list[dict], client: str = CLIENT) -> dict:
    """Per (app, AV question): k of n valid runs with the client, majority status and the
    median of its positions (dictamen k3-k4)."""
    by_provider = {p: a for a, p in PAIRED.items()}
    runs = defaultdict(list)
    for r in probe_rows:
        app = by_provider.get(r["provider"])
        if app and r["prompt_id"].startswith("AV") and r["status"] == "ok":
            runs[(app, r["prompt_id"])].append(_probe_position(r["brands_mentioned"], client))
    cells = {}
    for key, positions in runs.items():
        hits = [p for p in positions if p is not None]
        k, n = len(hits), len(positions)
        status = "sale" if 2 * k > n else "no sale" if 2 * k < n else "empate"
        cells[key] = {"k": k, "n": n, "status": status,
                      "position": statistics.median(hits) if hits else None}
    return cells


def _probe_dates(probe_rows: list[dict]) -> tuple[date, date] | None:
    ds = [d for d in (_date(r["timestamp_utc"]) for r in probe_rows
                      if r["prompt_id"].startswith("AV") and r["provider"] in PAIRED.values())
          if d]
    return (min(ds), max(ds)) if ds else None


def _gap_days(a: tuple[date, date] | None, b: tuple[date, date] | None) -> int | None:
    if not a or not b:
        return None
    if a[1] < b[0]:
        return (b[0] - a[1]).days
    if b[1] < a[0]:
        return (a[0] - b[1]).days
    return 0


def compare_with_probe(rows: list[dict], probe_rows: list[dict], client: str = CLIENT) -> dict:
    """App vs probe per AV question x assistant, agreement and the verdict "coinciden de
    forma razonable" (dictamen k-l)."""
    _check(rows)
    main = [r for r in _core(rows) if r["app"] in PAIRED]
    cells_probe = summarize_probe(probe_rows, client)
    manual_dates = [d for d in (_date(r["fecha_hora_local"]) for r in main) if d]
    manual_span = (min(manual_dates), max(manual_dates)) if manual_dates else None
    probe_span = _probe_dates(probe_rows)
    window = _gap_days(probe_span, manual_span)

    apps, reasons = {}, []
    if window is None or window > MAX_WINDOW_DAYS:
        reasons.append(f"fuera de la ventana: {window} días entre probe y pasada "
                       f"(máximo {MAX_WINDOW_DAYS})")
    for app, provider in PAIRED.items():
        cells = []
        for r in sorted((r for r in main if r["app"] == app), key=lambda r: r["id_pregunta"]):
            p = cells_probe.get((app, r["id_pregunta"]))
            valid = r["respuesta_valida"] == "si"
            app_status = ("sale" if r["artica_nombrada"] == "si" else "no sale") if valid else None
            comparable = valid and p is not None
            agree = None
            if comparable:
                agree = p["status"] == "empate" or p["status"] == app_status
            cells.append({"qid": r["id_pregunta"], "app_status": app_status,
                          "app_pos": int(float(r["posicion_artica"])) if valid and r["posicion_artica"] else None,
                          "probe_k": p["k"] if p else None, "probe_n": p["n"] if p else None,
                          "probe_status": p["status"] if p else None,
                          "probe_pos": p["position"] if p else None,
                          "comparable": comparable, "agree": agree})
        comp = [c for c in cells if c["comparable"]]
        agree_n = sum(c["agree"] for c in comp)
        valid_app = [c for c in cells if c["app_status"]]
        sov_app = (sum(c["app_status"] == "sale" for c in valid_app) / len(valid_app)
                   if valid_app else None)
        k = sum(v["k"] for (a, _), v in cells_probe.items() if a == app)
        n = sum(v["n"] for (a, _), v in cells_probe.items() if a == app)
        sov_probe = k / n if n else None
        gap = sov_app - sov_probe if sov_app is not None and sov_probe is not None else None
        both = [c for c in comp if c["app_status"] == "sale" and c["probe_pos"] is not None
                and c["app_pos"] is not None]
        res = {
            "cells": cells, "comparable": len(comp), "agree": agree_n,
            "agreement": agree_n / len(comp) if comp else None,
            "sov_app": sov_app, "sov_probe": sov_probe, "sov_gap": gap,
            "positions_both": len(both),
            "positions_close": sum(abs(c["app_pos"] - c["probe_pos"]) <= POSITION_TOLERANCE
                                   for c in both),
            "models_app": sorted({r["modelo_mostrado"] for r in main
                                  if r["app"] == app and r["modelo_mostrado"]}),
            "models_probe": sorted({r["model"] for r in probe_rows
                                    if r["provider"] == provider and r["prompt_id"].startswith("AV")
                                    and r["status"] == "ok" and r.get("model")}),
        }
        apps[app] = res
        if res["comparable"] < MIN_COMPARABLE:
            reasons.append(f"{app}: {res['comparable']} casillas comparables "
                           f"(mínimo {MIN_COMPARABLE})")
        if res["agreement"] is None or res["agreement"] < MIN_AGREEMENT:
            reasons.append(f"{app}: acuerdo {agree_n} de {len(comp)} "
                           f"(mínimo {MIN_AGREEMENT:.0%})")
        if gap is None or abs(gap) > MAX_SOV_GAP + 1e-9:
            shown = "—" if gap is None else f"{abs(gap) * 100:.1f} pts"
            reasons.append(f"{app}: diferencia de SoV bruto {shown} "
                           f"(máximo {MAX_SOV_GAP * 100:.0f} pts)")
    return {"apps": apps, "window_days": window,
            "window_ok": window is not None and window <= MAX_WINDOW_DAYS,
            "manual_dates": manual_span, "probe_dates": probe_span,
            "verdict": not reasons, "reasons": reasons}


# ------------------------------------------------------------------ report
def _pct(x):
    return "—" if x is None else f"{x * 100:.1f} %"


def _span(s):
    return "—" if not s else (str(s[0]) if s[0] == s[1] else f"{s[0]} a {s[1]}")


def render_calibration(res: dict, cmp: dict | None, sources: list[str]) -> str:
    out = [f"# Calibración \"{res.get('pasada') or 'antes'}\" — piloto Clínica Ártica "
           "(SPEC-007 CA-7)", "",
           "Privado (ADR-004). Generado con `docs/piloto-artica/tools/count_baseline.py` "
           "según el dictamen de CA-2 (k)–(n) del ledger de SPEC-007. Es calibración: **no "
           "entra en el criterio Go** ninguna de sus cifras (el Go es probe contra probe).", "",
           "Fuentes: " + ", ".join(f"`{s}`" for s in sources),
           f"Fechas de la pasada: {_span(res.get('dates'))}", "",
           "## 1. Lo que ve el paciente — núcleo AV (cuentas gratuitas, desde "
           f"{MAIN_MUNICIPIO})", "",
           "| App | Válidas | Excluidas | Con la clínica | SoV bruto | Posición media |",
           "|---|---|---|---|---|---|"]
    for app, c in res["apps"].items():
        pos = "—" if c["mean_position"] is None else f"{c['mean_position']:.2f}"
        out.append(f"| {app} | {c['valid']} | {c['excluded']} | {c['mentions']} de "
                   f"{c['valid']} | {_pct(c['sov'])} | {pos} |")
    out += ["", "### Clínicas que aparecen en su lugar (respuestas sin la clínica)", ""]
    for app, c in res["apps"].items():
        top = "; ".join(f"{n} ({k})" for n, k in list(c["instead"].items())[:10]) or "—"
        out.append(f"- {app}: {top}")
    g = res["google"]
    out += ["", "## Google, resumen de IA (canal aparte; fuera del acuerdo y del Go)", "",
            f"- Búsquedas válidas: {g['searches']}; con resumen de IA: {g['with_overview']} "
            f"de {g['searches']}",
            f"- Con la clínica en el resumen: {g['mentions']} de {g['searches']} búsquedas "
            f"válidas; {g['mentions']} de {g['with_overview']} con resumen",
            f"- Lectura antes/después (SPEC-012): cambio claro solo con ≥ {AIO_CLEAR_CHANGE} "
            "búsquedas de diferencia con la clínica; sin objetivo.", "",
            "## Dominios más citados (ChatGPT, Gemini y Google)", ""]
    out += [f"- {d}: {n}" for d, n in res["domains"][:15]] or ["- —"]
    out += ["", "## Preguntas de marca (AM)", "",
            "Leer cada captura: qué dice el asistente de la clínica (dirección, servicios, "
            "precios) y si es correcto frente a la web y la foto técnica.", "",
            "| Pregunta | App | Captura | Observaciones |", "|---|---|---|---|"]
    out += [f"| {r['id_pregunta']} | {r['app']} | {r['fichero_captura']} | {r['observaciones']} |"
            for r in res["brand_rows"]]
    out += ["", "## Observaciones (no cuentan: Claude, cuentas de pago)", ""]
    out += [f"- {a} ({plan}): {o['mentions']} de {o['valid']}"
            for o in res["observations"] for a, plan in [o["key"]]] or ["- —"]
    out += ["", f"## Observación de sensibilidad a la ubicación (fuera de {MAIN_MUNICIPIO}; "
            "no cuenta)", ""]
    out += [f"- {s['app']} desde {s['municipio']}: {s['mentions']} de {s['valid']}"
            for s in res["location_sensitivity"]] or ["- —"]
    out += ["", f"Filas marcadas `{ADJECTIVE_FLAG}` (cuentan; revisar a mano): "
            f"{res['adjective_flags']}",
            f"Filas marcadas `{DOCTOR_ONLY_FLAG}` (no cuentan como mención): "
            f"{res['doctor_only_flags']}"]
    if res.get("ignored_rows"):
        out.append(f"Filas `AR`/`AG` ignoradas (no se preguntan a mano): {res['ignored_rows']}")
    if cmp is None:
        return "\n".join(out) + "\n"

    out += ["", "## 2. Comparación app frente a probe (ChatGPT y Gemini, casillas AV)", "",
            f"- Ejecución del probe: {_span(cmp['probe_dates'])}; pasada manual: "
            f"{_span(cmp['manual_dates'])}; distancia: {cmp['window_days']} días "
            f"(ventana máxima {MAX_WINDOW_DAYS}).",
            "- Probe: \"sale\" si la clínica está en más de la mitad de los runs válidos; "
            "\"empate\" si en la mitad (cuenta como acuerdo); posición = mediana.",
            f"- Diferencias conocidas: la manual se hace desde {MAIN_MUNICIPIO} y el probe "
            "envía la ubicación Viveiro; modelo de la app gratuita frente al modelo por "
            "defecto de la API; el probe solo reconoce marcas de su catálogo.", ""]
    for app, c in cmp["apps"].items():
        out += [f"### {app}", "",
                f"Modelos: app {', '.join(c['models_app']) or '—'}; probe "
                f"{', '.join(c['models_probe']) or '—'}", "",
                "| Pregunta | App | Posición app | Probe (runs) | Probe | Posición probe | Acuerdo |",
                "|---|---|---|---|---|---|---|"]
        for x in c["cells"]:
            runs = "—" if x["probe_n"] is None else f"{x['probe_k']} de {x['probe_n']}"
            agree = "—" if x["agree"] is None else ("sí" if x["agree"] else "no")
            out.append(f"| {x['qid']} | {x['app_status'] or 'no válida'} | "
                       f"{x['app_pos'] or '—'} | {runs} | {x['probe_status'] or '—'} | "
                       f"{'—' if x['probe_pos'] is None else x['probe_pos']} | {agree} |")
        gap = "—" if c["sov_gap"] is None else f"{c['sov_gap'] * 100:+.1f} pts"
        out += ["", f"- Acuerdo: {c['agree']} de {c['comparable']} casillas comparables "
                f"({_pct(c['agreement'])}; mínimo {MIN_AGREEMENT:.0%} y {MIN_COMPARABLE} "
                "comparables)",
                f"- SoV bruto: app {_pct(c['sov_app'])}, probe {_pct(c['sov_probe'])}; "
                f"diferencia {gap} (máximo ± {MAX_SOV_GAP * 100:.0f} pts)",
                f"- Posición (informativa): parecida (± {POSITION_TOLERANCE}) en "
                f"{c['positions_close']} de {c['positions_both']} casillas donde sale en los dos",
                ""]
    out.append(f"**Coinciden de forma razonable: {'sí' if cmp['verdict'] else 'no'}**")
    if not cmp["verdict"]:
        out += ["", "Motivos:"] + [f"- {r}" for r in cmp["reasons"]]
        out += ["", "Qué hacer: revisar, en este orden, la lectura de las casillas en "
                "desacuerdo, el protocolo manual (desviaciones, cuenta, modo, modelo), la "
                "configuración del probe (modelo por defecto, búsqueda, ubicación) y la "
                "diferencia de ubicación. Anotar la causa y la decisión del humano en el "
                "ledger. Hasta entonces no se enseña a la clínica ninguna cifra del probe ni "
                "se envía la propuesta (SPEC-009)."]
    return "\n".join(out) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("csv", help="CSV rellenado de UNA pasada (antes o despues)")
    ap.add_argument("--probe", help="results.csv del probe (lote Viveiro, posterior a SPEC-013)")
    ap.add_argument("--client", default=CLIENT)
    ap.add_argument("--aliases")
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    rows = read_rows([a.csv])
    res = count(rows, read_aliases(a.aliases) if a.aliases else {})
    cmp = compare_with_probe(rows, read_probe(a.probe), a.client) if a.probe else None
    sources = [Path(a.csv).name] + ([Path(a.probe).name] if a.probe else [])
    md = render_calibration(res, cmp, sources)
    if a.out:
        Path(a.out).write_text(md, encoding="utf-8")
    else:
        sys.stdout.write(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
