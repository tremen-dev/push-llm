"""Calibration recount of the Clínica Ártica pilot (SPEC-007 CA-7, amendment 2026-09-29 (c)).

Counts ONE manual pass ("antes" or "despues") BY LEVEL - AR in ChatGPT, Gemini and Google,
AV and AM in ChatGPT and Gemini (49 rows) - and compares it with the probe, one level at a
time and never combined (ADR-005 §4, ADR-009 §2):

- AV: cell AV question x assistant against the paired AV execution (the official baseline,
  SPEC-008 CA-7), verdict "coinciden de forma razonable en AV" (dictamen (k)-(l), (q));
- AR: cell AR question x assistant against the paired AR execution (the AR "before" of
  SPEC-008 CA-12, 3 runs), weak verdict "sin discrepancia gruesa en AR" (dictamen (o)-(p)).

Google AI Overviews only on the AR searches, as counts (dictamen (r)). Rules: the
sdd-metricas dictamen in the SPEC-007 ledger. The same steps are written for a spreadsheet
in docs/piloto-artica/procedimiento-recuento.md; this script is a convenience, not the
definition. Nothing here enters the Go ((C) and (D) are probe vs probe).

    python docs/piloto-artica/tools/count_baseline.py ANTES.csv         --probe-av .../piloto-artica/probe/results.csv         --probe-ar .../piloto-artica/probe-AR-antes/results.csv         [--aliases alias-canonicos.csv] [--out calibracion-antes.md]

Inputs and output live in $PUSHLLM_PRIVADO/piloto-artica/ (ADR-004): never point --out
inside the repo.
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
from baseline_docs import EXPECTED_LAYOUT, norm  # noqa: E402  (RN-01 normalisation)

# Assistants present in both instruments (dictamen k1, o1): manual app -> probe provider.
PAIRED = {"chatgpt": "openai", "gemini": "gemini"}
LEVELS = ("AV", "AR")
MAIN_APPS = ("chatgpt", "gemini", "google")
MAIN_PLANS = {"gratuito", "sin_sesion"}
# P-4 (revised by the human, 2026-09-29): every pass, before and after, from Vilaboa. Rows
# taken elsewhere are a location-sensitivity observation, outside the computation.
MAIN_MUNICIPIO = "Vilaboa"
ADJECTIVE_FLAG = "#artica-adjetivo"      # P-1: counts (RN-01), reviewed by hand
DOCTOR_ONLY_FLAG = "#medica-sin-clinica"  # P-2: not a mention, reported apart
CLIENT = "Clínica Ártica"                 # client_brand of probe/batches/viveiro.json

# AV thresholds: dictamen (k)-(l), confirmed without changes by (q).
MAX_WINDOW_DAYS = 7        # k5: probe AV execution <-> manual pass
MIN_COMPARABLE = 12        # l2b: comparable cells per assistant (of 15)
MIN_AGREEMENT = 0.70       # l2c: same "sale / no sale" (11 of 15)
MAX_SOV_GAP = 0.20         # l2d: |raw SoV app - raw SoV probe| per assistant
POSITION_TOLERANCE = 2     # l2: positions reported as "close" within 2 places; never decides
# AR thresholds: dictamen (o)-(p). Weak verdict "sin discrepancia gruesa".
AR_MAX_WINDOW_DAYS = 7     # o2: probe AR execution (SPEC-008 CA-12) <-> manual pass
AR_MIN_VALID_RUNS = 2      # o4: a probe cell needs >= 2 valid runs to be comparable
AR_MIN_COMPARABLE = 4      # p3b: comparable cells per assistant (of 5)
AR_MIN_DECISIVE = 3        # p3c: comparable cells unanimous in the probe
AR_MAX_GROSS = 1           # p3d: gross discrepancies allowed per assistant

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


def _level(r: dict) -> str:
    return r["id_pregunta"][:2]


def _check(rows: list[dict]) -> None:
    """One pass, no duplicates, mention flag filled on valid rows, and the layout of
    amendment (c): the main rows are exactly baseline_docs.EXPECTED_LAYOUT (49 rows); no AG
    anywhere and no AV or AM in Google, not even as an observation."""
    seen = set()
    for r in rows:
        key = (r["pasada"], r["id_pregunta"], r["app"], r["plan_cuenta"], norm(r["municipio"]))
        if key in seen:
            raise ValueError(f"fila duplicada: {key}")
        seen.add(key)
        if r["respuesta_valida"] == "si" and r["artica_nombrada"] not in {"si", "no"}:
            raise ValueError(f"artica_nombrada vacía o inválida en fila válida: {key}")
        if _level(r) == "AG":
            raise ValueError(f"fila AG: AG no se pregunta a mano (solo el probe): {key}")
        if r["app"] == "google" and _level(r) in {"AV", "AM"}:
            raise ValueError(f"fila {_level(r)} de Google: en Google solo se pregunta AR: {key}")
    passes = {r["pasada"] for r in rows}
    if len(passes) > 1:
        raise ValueError(f"el recuento es de una sola pasada; hay {sorted(passes)}")
    layout = defaultdict(list)
    for r in rows:
        if _is_main(r):
            layout[(r["app"], _level(r))].append(r["id_pregunta"])
    expected = {k: sorted(v) for k, v in EXPECTED_LAYOUT.items()}
    got = {k: sorted(v) for k, v in layout.items()}
    wrong = sorted(k for k in set(got) | set(expected) if got.get(k) != expected.get(k))
    if wrong:
        raise ValueError("el reparto de la pasada no es el del protocolo (49 filas: AR en "
                         "ChatGPT, Gemini y Google; AV y AM en ChatGPT y Gemini); revisa "
                         f"{wrong}")


def _main_level(rows: list[dict], level: str) -> list[dict]:
    return [r for r in rows if _level(r) == level and _is_main(r)]


def _date(text: str) -> date | None:
    try:
        return date.fromisoformat(text[:10])
    except ValueError:
        return None


def _app_stats(rs: list[dict], level: str, aliases: dict[str, str]) -> dict:
    valid = [r for r in rs if r["respuesta_valida"] == "si"]
    named = [r for r in valid if r["artica_nombrada"] == "si"]
    positions = [int(float(r["posicion_artica"])) for r in named if r["posicion_artica"]]
    instead = Counter()
    for r in valid:
        if r["artica_nombrada"] == "no":
            instead.update({_canonical(c, aliases) for c in _split(r["clinicas_nombradas"])})
    out = {"valid": len(valid), "excluded": len(rs) - len(valid), "mentions": len(named),
           "instead": dict(instead.most_common())}
    if level == "AV":
        out["sov"] = len(named) / len(valid) if valid else None
        out["mean_position"] = sum(positions) / len(positions) if positions else None
    else:                  # AR: counts and a list of places, never a mean (dictamen o.6, p.5)
        out["positions"] = positions
    return out


def count(rows: list[dict], aliases: dict[str, str] | None = None) -> dict:
    aliases = aliases or {}
    _check(rows)
    levels = {}
    for level in LEVELS:
        main = _main_level(rows, level)
        domains = Counter()
        for r in main:
            if r["respuesta_valida"] == "si":
                domains.update({d.lower().removeprefix("www.")
                                for d in _split(r["dominios_citados"])})
        levels[level] = {
            "apps": {app: _app_stats([r for r in main if r["app"] == app], level, aliases)
                     for app in PAIRED},
            "domains": domains.most_common(),
        }

    g_rows = [r for r in _main_level(rows, "AR")
              if r["app"] == "google" and r["respuesta_valida"] == "si"]
    g_over = [r for r in g_rows if r["resumen_ia"] == "si"]
    google = {"searches": len(g_rows), "with_overview": len(g_over),
              "mentions": sum(r["artica_nombrada"] == "si" for r in g_over)}

    places = defaultdict(lambda: [0, 0])
    obs = defaultdict(lambda: [0, 0])
    for r in rows:
        if _level(r) not in LEVELS or r["respuesta_valida"] != "si":
            continue
        if _other_place(r):
            s = places[(_level(r), r["municipio"], r["app"])]
        elif not _is_main(r):
            s = obs[(_level(r), r["app"], r["plan_cuenta"])]
        else:
            continue
        s[0] += r["artica_nombrada"] == "si"
        s[1] += 1

    counted = [r for r in rows if _is_main(r) and _level(r) in LEVELS]
    dates = [d for d in (_date(r["fecha_hora_local"]) for r in rows if _is_main(r)) if d]
    return {
        "pasada": next(iter({r["pasada"] for r in rows}), ""),
        "levels": levels, "google": google,
        "observations": [{"key": k, "mentions": m, "valid": n}
                         for k, (m, n) in sorted(obs.items())],
        "location_sensitivity": [{"level": lv, "municipio": m, "app": a, "mentions": k,
                                  "valid": n}
                                 for (lv, m, a), (k, n) in sorted(places.items())],
        "brand_rows": [r for r in rows if _level(r) == "AM"],
        "adjective_flags": sum(ADJECTIVE_FLAG in r["observaciones"] for r in counted),
        "doctor_only_flags": sum(DOCTOR_ONLY_FLAG in r["observaciones"] for r in counted),
        "dates": (min(dates), max(dates)) if dates else None,
    }


# ------------------------------------------------------------------ probe side
def _probe_position(brands: str, client: str) -> int | None:
    names = [norm(b) for b in _split(brands)]
    return names.index(norm(client)) + 1 if norm(client) in names else None


def summarize_probe(probe_rows: list[dict], client: str = CLIENT, level: str = "AV") -> dict:
    """Per (app, question of `level`): k of n valid runs with the client, majority status,
    median position, positions in the runs where it appears, and whether the cell is
    unanimous (in every valid run or in none, with >= AR_MIN_VALID_RUNS runs). Dictamen
    k3-k4 and o4."""
    by_provider = {p: a for a, p in PAIRED.items()}
    runs = defaultdict(list)
    for r in probe_rows:
        app = by_provider.get(r["provider"])
        if app and r["prompt_id"].startswith(level) and r["status"] == "ok":
            runs[(app, r["prompt_id"])].append(_probe_position(r["brands_mentioned"], client))
    cells = {}
    for key, positions in runs.items():
        hits = [p for p in positions if p is not None]
        k, n = len(hits), len(positions)
        status = "sale" if 2 * k > n else "no sale" if 2 * k < n else "empate"
        cells[key] = {"k": k, "n": n, "status": status, "positions": hits,
                      "position": statistics.median(hits) if hits else None,
                      "unanimous": n >= AR_MIN_VALID_RUNS and k in (0, n)}
    return cells


def _probe_dates(probe_rows: list[dict], level: str) -> tuple[date, date] | None:
    ds = [d for d in (_date(r["timestamp_utc"]) for r in probe_rows
                      if r["prompt_id"].startswith(level) and r["provider"] in PAIRED.values())
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


def _pairing(rows: list[dict], probe_rows: list[dict], level: str, max_days: int):
    """Main rows of the level in the paired apps, and the window against the probe
    execution of that level (each level has its own, dictamen k5 / o2)."""
    main = [r for r in _main_level(rows, level) if r["app"] in PAIRED]
    manual_dates = [d for d in (_date(r["fecha_hora_local"]) for r in main) if d]
    manual_span = (min(manual_dates), max(manual_dates)) if manual_dates else None
    probe_span = _probe_dates(probe_rows, level)
    window = _gap_days(probe_span, manual_span)
    reasons = []
    if window is None or window > max_days:
        reasons.append(f"fuera de la ventana: {window} días entre la ejecución {level} del "
                       f"probe y la pasada (máximo {max_days})")
    return main, {"window_days": window, "window_ok": not reasons,
                  "manual_dates": manual_span, "probe_dates": probe_span}, reasons


def _models(main: list[dict], probe_rows: list[dict], app: str, level: str) -> dict:
    return {"models_app": sorted({r["modelo_mostrado"] for r in main
                                  if r["app"] == app and r["modelo_mostrado"]}),
            "models_probe": sorted({r["model"] for r in probe_rows
                                    if r["provider"] == PAIRED[app]
                                    and r["prompt_id"].startswith(level)
                                    and r["status"] == "ok" and r.get("model")})}


def _app_side(r: dict) -> tuple[str | None, int | None]:
    if r["respuesta_valida"] != "si":
        return None, None
    status = "sale" if r["artica_nombrada"] == "si" else "no sale"
    pos = int(float(r["posicion_artica"])) if r["posicion_artica"] else None
    return status, pos


def compare_av(rows: list[dict], probe_rows: list[dict], client: str = CLIENT) -> dict:
    """AV: app vs probe per AV question x assistant, agreement and the verdict "coinciden de
    forma razonable en AV" (dictamen k-l, confirmed by q). Only AV rows of both sides."""
    _check(rows)
    main, pairing, reasons = _pairing(rows, probe_rows, "AV", MAX_WINDOW_DAYS)
    cells_probe = summarize_probe(probe_rows, client, "AV")
    apps = {}
    for app in PAIRED:
        cells = []
        for r in sorted((r for r in main if r["app"] == app), key=lambda r: r["id_pregunta"]):
            p = cells_probe.get((app, r["id_pregunta"]))
            app_status, app_pos = _app_side(r)
            comparable = app_status is not None and p is not None
            agree = (p["status"] == "empate" or p["status"] == app_status) if comparable else None
            cells.append({"qid": r["id_pregunta"], "app_status": app_status, "app_pos": app_pos,
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
        } | _models(main, probe_rows, app, "AV")
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
    return {"level": "AV", "apps": apps, **pairing, "verdict": not reasons, "reasons": reasons}


def compare_ar(rows: list[dict], probe_rows: list[dict], client: str = CLIENT) -> dict:
    """AR: app vs probe per AR question x assistant and the weak verdict "sin discrepancia
    gruesa en AR" (dictamen o-p). A split probe cell is compatible with any app answer; a
    gross discrepancy is a unanimous probe cell that the app contradicts. No SoV gap."""
    _check(rows)
    main, pairing, reasons = _pairing(rows, probe_rows, "AR", AR_MAX_WINDOW_DAYS)
    cells_probe = summarize_probe(probe_rows, client, "AR")
    apps = {}
    for app in PAIRED:
        cells = []
        for r in sorted((r for r in main if r["app"] == app), key=lambda r: r["id_pregunta"]):
            p = cells_probe.get((app, r["id_pregunta"]))
            app_status, app_pos = _app_side(r)
            comparable = (app_status is not None and p is not None
                          and p["n"] >= AR_MIN_VALID_RUNS)
            decisive = comparable and p["unanimous"]
            gross = decisive and ((p["k"] == p["n"]) != (app_status == "sale"))
            cells.append({"qid": r["id_pregunta"], "app_status": app_status, "app_pos": app_pos,
                          "probe_k": p["k"] if p else None, "probe_n": p["n"] if p else None,
                          "probe_positions": p["positions"] if p else [],
                          "probe_kind": (None if not comparable else
                                         "unánime" if p["unanimous"] else "repartida"),
                          "comparable": comparable, "decisive": decisive, "gross": gross})
        valid_app = [c for c in cells if c["app_status"]]
        res = {
            "cells": cells,
            "comparable": sum(c["comparable"] for c in cells),
            "decisive": sum(c["decisive"] for c in cells),
            "gross": sum(c["gross"] for c in cells),
            "app_valid": len(valid_app),
            "app_mentions": sum(c["app_status"] == "sale" for c in valid_app),
            "probe_k": sum(v["k"] for (a, _), v in cells_probe.items() if a == app),
            "probe_n": sum(v["n"] for (a, _), v in cells_probe.items() if a == app),
        } | _models(main, probe_rows, app, "AR")
        apps[app] = res
        if res["comparable"] < AR_MIN_COMPARABLE:
            reasons.append(f"{app}: {res['comparable']} casillas comparables "
                           f"(mínimo {AR_MIN_COMPARABLE})")
        if res["decisive"] < AR_MIN_DECISIVE:
            reasons.append(f"{app}: {res['decisive']} casillas decisivas, unánimes en el probe "
                           f"(mínimo {AR_MIN_DECISIVE})")
        if res["gross"] > AR_MAX_GROSS:
            reasons.append(f"{app}: {res['gross']} discrepancias gruesas "
                           f"(máximo {AR_MAX_GROSS})")
    return {"level": "AR", "apps": apps, **pairing, "verdict": not reasons, "reasons": reasons}


# ------------------------------------------------------------------ report
def _pct(x):
    return "—" if x is None else f"{x * 100:.1f} %"


def _span(s):
    return "—" if not s else (str(s[0]) if s[0] == s[1] else f"{s[0]} a {s[1]}")


def _yes(v: bool) -> str:
    return "sí" if v else "no"


REVIEW_ORDER = ("revisar, en este orden, la lectura de las casillas en desacuerdo, el "
                "protocolo manual (desviaciones, cuenta, modo, modelo), la configuración del "
                "probe (modelo por defecto, búsqueda, ubicación) y la diferencia de ubicación. "
                "Anotar la causa y la decisión del humano para este nivel en el ledger.")


def _instead_lines(apps: dict) -> list[str]:
    return [f"- {app}: " + ("; ".join(f"{n} ({k})" for n, k in list(c["instead"].items())[:10])
                            or "—")
            for app, c in apps.items()]


def _render_patient(res: dict) -> list[str]:
    av, ar = res["levels"]["AV"], res["levels"]["AR"]
    out = ["## 1. Lo que ve el paciente — núcleo AV (ChatGPT y Gemini)", "",
           "| App | Válidas | Excluidas | Con la clínica | SoV bruto | Posición media |",
           "|---|---|---|---|---|---|"]
    for app, c in av["apps"].items():
        pos = "—" if c["mean_position"] is None else f"{c['mean_position']:.2f}"
        out.append(f"| {app} | {c['valid']} | {c['excluded']} | {c['mentions']} de "
                   f"{c['valid']} | {_pct(c['sov'])} | {pos} |")
    out += ["", "Clínicas que aparecen en su lugar (respuestas sin la clínica):", ""]
    out += _instead_lines(av["apps"])
    out += ["", "## 1b. Lo que ve el paciente — área de influencia AR (ChatGPT y Gemini; "
            "recuentos, sin porcentajes)", "",
            "| App | Válidas | Excluidas | Con la clínica | Puestos donde sale |",
            "|---|---|---|---|---|"]
    for app, c in ar["apps"].items():
        places = ", ".join(str(p) for p in c["positions"]) or "—"
        out.append(f"| {app} | {c['valid']} | {c['excluded']} | {c['mentions']} de "
                   f"{c['valid']} | {places} |")
    out += ["", "Clínicas que aparecen en su lugar (una cadena con varias sedes es una marca):",
            ""]
    out += _instead_lines(ar["apps"])
    g = res["google"]
    out += ["", "## Google, resumen de IA — solo búsquedas AR (canal aparte; fuera de los "
            "veredictos y del Go)", "",
            f"- Búsquedas válidas: {g['searches']} de 5; con resumen de IA: "
            f"{g['with_overview']} de {g['searches']}",
            f"- Con la clínica en el resumen: {g['mentions']} de {g['searches']} búsquedas "
            f"válidas; {g['mentions']} de {g['with_overview']} con resumen",
            f"- Limitación: se busca desde {MAIN_MUNICIPIO}, no desde el lugar que nombra la "
            "búsqueda; Google pesa mucho la ubicación del dispositivo.",
            "- Antes/después (SPEC-012): con 5 búsquedas solo se describe (\"x de 5 antes, "
            "y de 5 después\"), sin objetivo ni promesa.", "",
            "## Dominios más citados, por nivel", ""]
    for level, title in (("AV", "Núcleo AV (ChatGPT y Gemini)"),
                         ("AR", "Área de influencia AR (ChatGPT, Gemini y Google)")):
        out += [f"{title}:", ""]
        out += [f"- {d}: {n}" for d, n in res["levels"][level]["domains"][:15]] or ["- —"]
        out.append("")
    out += ["## Preguntas de marca (AM)", "",
            "Leer cada captura: qué dice el asistente de la clínica (dirección, servicios, "
            "precios) y si es correcto frente a la web y la foto técnica.", "",
            "| Pregunta | App | Captura | Observaciones |", "|---|---|---|---|"]
    out += [f"| {r['id_pregunta']} | {r['app']} | {r['fichero_captura']} | {r['observaciones']} |"
            for r in res["brand_rows"]]
    out += ["", "## Observaciones (no cuentan: Claude, cuentas de pago)", ""]
    out += [f"- {lv} {a} ({plan}): {o['mentions']} de {o['valid']}"
            for o in res["observations"] for lv, a, plan in [o["key"]]] or ["- —"]
    out += ["", f"## Observación de sensibilidad a la ubicación (fuera de {MAIN_MUNICIPIO}; "
            "no cuenta)", ""]
    out += [f"- {s['level']} {s['app']} desde {s['municipio']}: {s['mentions']} de {s['valid']}"
            for s in res["location_sensitivity"]] or ["- —"]
    out += ["", f"Filas marcadas `{ADJECTIVE_FLAG}` (cuentan; revisar a mano): "
            f"{res['adjective_flags']}",
            f"Filas marcadas `{DOCTOR_ONLY_FLAG}` (no cuentan como mención): "
            f"{res['doctor_only_flags']}", ""]
    return out


def _models_line(c: dict) -> str:
    return (f"Modelos: app {', '.join(c['models_app']) or '—'}; probe "
            f"{', '.join(c['models_probe']) or '—'}")


def _render_av(cmp: dict) -> list[str]:
    out = ["## 3. Comparación app frente a probe — AV (casillas AV × ChatGPT y Gemini)", "",
           "- Probe: \"sale\" si la clínica está en más de la mitad de los runs válidos; "
           "\"empate\" si en la mitad (cuenta como acuerdo); posición = mediana.",
           f"- Diferencias conocidas: la manual se hace desde {MAIN_MUNICIPIO} y el probe "
           "envía la ubicación Viveiro; modelo de la app gratuita frente al modelo por "
           "defecto de la API; el probe solo reconoce marcas de su catálogo.", ""]
    for app, c in cmp["apps"].items():
        out += [f"### {app}", "", _models_line(c), "",
                "| Pregunta | App | Posición app | Probe (runs) | Probe | Posición probe | Acuerdo |",
                "|---|---|---|---|---|---|---|"]
        for x in c["cells"]:
            runs = "—" if x["probe_n"] is None else f"{x['probe_k']} de {x['probe_n']}"
            agree = "—" if x["agree"] is None else _yes(x["agree"])
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
    out += [f"**Coinciden de forma razonable en AV: {_yes(cmp['verdict'])}**", ""]
    if cmp["verdict"]:
        out.append("Apoya la frase comercial de SPEC-009 (\"ya sois la clínica que la IA "
                   "recomienda en A Mariña\"). Ninguna cifra manual entra en (D).")
    else:
        out += ["Motivos:"] + [f"- {r}" for r in cmp["reasons"]]
        out += ["", "Qué hacer: " + REVIEW_ORDER + " Hasta entonces no se enseña a la clínica "
                "ninguna cifra AV del probe y se revisa la frase \"ya sois la clínica que la IA "
                "recomienda en A Mariña\" de SPEC-009 antes de enviar la propuesta. Ninguna "
                "cifra manual entra en (D)."]
    return out + [""]


def _render_ar(cmp: dict) -> list[str]:
    out = ["## 4. Comparación app frente a probe — AR (casillas AR × ChatGPT y Gemini; "
           "recuentos, sin porcentajes)", "",
           "- Veredicto débil: con 5 casillas por asistente no se puede afirmar que los dos "
           "instrumentos coinciden; solo se descarta una contradicción clara.",
           "- Probe: casilla unánime (la clínica en todos los runs válidos o en ninguno, con "
           f"{AR_MIN_VALID_RUNS} runs válidos o más) o repartida; una repartida es compatible "
           "con cualquier respuesta de la app; discrepancia gruesa = casilla unánime que la "
           "app contradice.",
           "- Diferencias conocidas: las preguntas AR se formulan desde Ferrolterra, Lugo o "
           f"Asturias; la manual se hace desde {MAIN_MUNICIPIO} y el probe envía la ubicación "
           "Viveiro (al lado de la clínica): aquí la ubicación pesa más que en el núcleo. "
           "Modelo de la app frente al de la API; catálogo cerrado del probe.", ""]
    for app, c in cmp["apps"].items():
        out += [f"### {app}", "", _models_line(c), "",
                "| Pregunta | App | Puesto app | Probe (runs) | Casilla del probe | "
                "Puestos probe | Discrepancia gruesa |",
                "|---|---|---|---|---|---|---|"]
        for x in c["cells"]:
            runs = "—" if x["probe_n"] is None else f"{x['probe_k']} de {x['probe_n']}"
            places = ", ".join(str(p) for p in x["probe_positions"]) or "—"
            gross = _yes(x["gross"]) if x["comparable"] else "—"
            out.append(f"| {x['qid']} | {x['app_status'] or 'no válida'} | "
                       f"{x['app_pos'] or '—'} | {runs} | {x['probe_kind'] or 'no comparable'} "
                       f"| {places} | {gross} |")
        out += ["", f"- Casillas comparables: {c['comparable']} de 5 (mínimo "
                f"{AR_MIN_COMPARABLE}); decisivas: {c['decisive']} (mínimo {AR_MIN_DECISIVE}); "
                f"discrepancias gruesas: {c['gross']} (máximo {AR_MAX_GROSS})",
                f"- Con la clínica: app {c['app_mentions']} de {c['app_valid']} respuestas; "
                f"probe {c['probe_k']} de {c['probe_n']} runs (informativo; no decide)", ""]
    out += [f"**Sin discrepancia gruesa en AR: {_yes(cmp['verdict'])}**", ""]
    if cmp["verdict"]:
        out.append("Basta para contar en la propuesta de SPEC-009 el objetivo de aparecer "
                   "también en el área de influencia, como objetivo, no como dato ni garantía. "
                   "Ninguna cifra manual entra en (C).")
    else:
        out += ["Motivos:"] + [f"- {r}" for r in cmp["reasons"]]
        out += ["", "Qué hacer: " + REVIEW_ORDER + " Hasta entonces no se enseña a la clínica "
                "ninguna cifra AR del probe y se revisa la frase del objetivo de SPEC-009 "
                "antes de enviar la propuesta. El cálculo de (C) no cambia (probe contra "
                "probe); el humano decide si (C) sigue tal cual o con la salvedad escrita. Si "
                "el objetivo se cuenta, va como objetivo, no como dato."]
    return out + [""]


def render_calibration(res: dict, cmp_av: dict | None, cmp_ar: dict | None,
                       sources: list[str]) -> str:
    out = [f"# Calibración \"{res.get('pasada') or 'antes'}\" — piloto Clínica Ártica "
           "(SPEC-007 CA-7)", "",
           "Privado (ADR-004). Generado con `docs/piloto-artica/tools/count_baseline.py` "
           "según el dictamen de CA-2 del ledger de SPEC-007, puntos (k)–(s). Es calibración: "
           "**no entra en el criterio Go** ninguna de sus cifras ((C) y (D) son probe contra "
           "probe). Cada nivel va en su sección, con su veredicto; ninguna cifra ni veredicto "
           "junta los niveles.", "",
           "Fuentes: " + ", ".join(f"`{s}`" for s in sources),
           f"Fechas de la pasada: {_span(res.get('dates'))}", ""]
    out += _render_patient(res)
    if cmp_av is None and cmp_ar is None:
        return "\n".join(out).rstrip() + "\n"
    out += ["## 2. Ejecuciones del probe emparejadas", ""]
    for cmp, max_days in ((cmp_av, MAX_WINDOW_DAYS), (cmp_ar, AR_MAX_WINDOW_DAYS)):
        if cmp is not None:
            out.append(f"- {cmp['level']}: ejecución del probe {_span(cmp['probe_dates'])}; "
                       f"filas {cmp['level']} de la pasada {_span(cmp['manual_dates'])}; "
                       f"distancia {cmp['window_days']} días (ventana máxima {max_days}).")
    out.append("")
    if cmp_av is not None:
        out += _render_av(cmp_av)
    if cmp_ar is not None:
        out += _render_ar(cmp_ar)
    return "\n".join(out).rstrip() + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("csv", help="CSV rellenado de UNA pasada (antes o despues), 49 filas")
    ap.add_argument("--probe-av", help="results.csv de la ejecución AV emparejada (baseline "
                    "oficial, SPEC-008 CA-7; posterior a SPEC-013)")
    ap.add_argument("--probe-ar", help="results.csv de la ejecución AR emparejada (\"antes\" "
                    "de AR, SPEC-008 CA-12, 3 runs)")
    ap.add_argument("--client", default=CLIENT)
    ap.add_argument("--aliases")
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    rows = read_rows([a.csv])
    res = count(rows, read_aliases(a.aliases) if a.aliases else {})
    cmp_av = compare_av(rows, read_probe(a.probe_av), a.client) if a.probe_av else None
    cmp_ar = compare_ar(rows, read_probe(a.probe_ar), a.client) if a.probe_ar else None
    sources = [Path(a.csv).name] + [f"{Path(p).parent.name}/{Path(p).name}"
                                    for p in (a.probe_av, a.probe_ar) if p]
    md = render_calibration(res, cmp_av, cmp_ar, sources)
    if a.out:
        Path(a.out).write_text(md, encoding="utf-8")
    else:
        sys.stdout.write(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
