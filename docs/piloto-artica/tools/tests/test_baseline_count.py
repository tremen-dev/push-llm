"""SPEC-007 CA-7 (amendment 2026-09-29 (c)): recount of one manual calibration pass BY
LEVEL and comparison app vs probe, one table and one verdict per level (AV and AR), never
combined. Rules: the CA-2 dictamen (k)-(n) and its third extension (o)-(s) in the SPEC-007
ledger.

Fixtures use a fictitious clinic ("Clínica Norte") and fictitious competitors: no real
figures ever live in the repo (ADR-004).
"""
import csv

import pytest

import baseline_docs as bd
import count_baseline as cb

BASE = {c: "" for c in bd.TEMPLATE_COLUMNS}
CLIENT = "Clínica Norte"
AV = [f"AV{i:02d}" for i in range(1, 16)]
AR = [f"AR{i:02d}" for i in range(1, 6)]
PROV = {"chatgpt": "openai", "gemini": "gemini"}


def row(qid, app, named="no", valid="si", plan="gratuito", clinics="", pos="", domains="",
        resumen=None, obs="", pasada="antes", when="2026-10-06 10:00", municipio="Vilaboa",
        model="x"):
    r = dict(BASE)
    if resumen is None:
        resumen = "no" if app == "google" else "n-a"
    r.update(pasada=pasada, id_pregunta=qid, app=app, plan_cuenta=plan, respuesta_valida=valid,
             artica_nombrada=named if valid == "si" else "", clinicas_nombradas=clinics,
             posicion_artica=pos, dominios_citados=domains, resumen_ia=resumen,
             observaciones=obs, fecha_hora_local=when, modo="temporal", sesion_iniciada="si",
             cuenta="a", modelo_mostrado=model, municipio=municipio,
             ubicacion_dispositivo="si", idioma="es")
    return r


def full_pass(hits=(), when="2026-10-06 10:00", pasada="antes"):
    """The 49 main rows of one pass (bd.EXPECTED_LAYOUT); the clinic appears, at position
    1, in the (app, qid) cells of `hits`."""
    return [row(q, app, "si" if (app, q) in hits else "no",
                pos="1" if (app, q) in hits else "", when=when, pasada=pasada)
            for (app, _), ids in bd.EXPECTED_LAYOUT.items() for q in ids]


def at(rows, qid, app, **kw):
    r = next(r for r in rows if r["id_pregunta"] == qid and r["app"] == app
             and r["plan_cuenta"] == "gratuito" and r["municipio"] == "Vilaboa")
    kw = {"artica_nombrada" if k == "named" else k: v for k, v in kw.items()}
    r.update(kw)
    return r


@pytest.fixture
def rows():
    rs = full_pass()
    # AV chatgpt: 14 valid, 1 mention; clinics in its place canonicalised
    at(rs, "AV01", "chatgpt", named="si", clinicas_nombradas="Clínica Norte;Clínica Sur",
       posicion_artica="1", dominios_citados="doctoralia.es;clinicanorte.es")
    at(rs, "AV02", "chatgpt", clinicas_nombradas="Clínica Sur;Centro Oeste",
       dominios_citados="doctoralia.es")
    at(rs, "AV03", "chatgpt", clinicas_nombradas="clinica sur")
    at(rs, "AV04", "chatgpt", clinicas_nombradas="Sur Estética")
    at(rs, "AV05", "chatgpt", respuesta_valida="no", named="")
    # AV gemini: 15 valid, 2 mentions at positions 2 and 1
    at(rs, "AV01", "gemini", named="si", clinicas_nombradas="Clínica Sur;Clínica Norte",
       posicion_artica="2")
    at(rs, "AV02", "gemini", named="si", clinicas_nombradas="Clínica Norte", posicion_artica="1")
    # AR chatgpt: 2 mentions at positions 3 and 1; a chain with two seats in its place
    at(rs, "AR01", "chatgpt", named="si", posicion_artica="3",
       clinicas_nombradas="Cadena X Ferrol;Clínica Este;Clínica Norte")
    at(rs, "AR02", "chatgpt", named="si", posicion_artica="1", clinicas_nombradas="Clínica Norte")
    at(rs, "AR03", "chatgpt", clinicas_nombradas="Cadena X Lugo")
    at(rs, "AR04", "chatgpt", clinicas_nombradas="Cadena X Ferrol")
    # Google, AR only: 5 valid searches, 2 with AI overview, 1 with the clinic inside
    at(rs, "AR01", "google", resumen_ia="si", named="si", posicion_artica="1",
       clinicas_nombradas="Clínica Norte", dominios_citados="doctoralia.es")
    at(rs, "AR02", "google", resumen_ia="si", clinicas_nombradas="Clínica Este")
    # observation rows never enter the main figures
    rs += [row("AV01", "chatgpt", "si", plan="pago", pos="1"),
           row("AV01", "claude", "si", pos="1"),
           row("AR01", "claude", "si", pos="1")]
    at(rs, "AM01", "chatgpt", observaciones="dirección correcta")
    return rs


ALIASES = {"sur estetica": "Clínica Sur", "clinica sur": "Clínica Sur",
           "cadena x ferrol": "Cadena X", "cadena x lugo": "Cadena X"}


# ------------------------------------------------------------------ layout of one pass
def test_full_pass_is_the_protocol_layout():
    assert len(full_pass()) == bd.CALIBRATION_QUERIES == 49
    cb.count(full_pass())                                   # no error


def test_incomplete_or_extra_layout_fails_loudly(rows):
    """CA-5 (c): 15 AV x (ChatGPT, Gemini) + 5 AR x (ChatGPT, Gemini, Google) + 2 AM x
    (ChatGPT, Gemini). A missing question is an invalid row, never a missing row."""
    missing = [r for r in rows if not (r["id_pregunta"] == "AR03" and r["app"] == "gemini")]
    with pytest.raises(ValueError, match="reparto"):
        cb.count(missing, ALIASES)
    with pytest.raises(ValueError, match="reparto"):
        cb.count(rows + [row("AV16", "chatgpt")], ALIASES)


@pytest.mark.parametrize("qid", ["AV01", "AM01"])
def test_google_av_or_am_rows_are_rejected(rows, qid):
    """Amendment (c): no AV or AM in Google, not even as an observation."""
    with pytest.raises(ValueError, match="Google"):
        cb.count(rows + [row(qid, "google", plan="sin_sesion", municipio="Viveiro")], ALIASES)


def test_ag_rows_are_rejected(rows):
    with pytest.raises(ValueError, match="AG"):
        cb.count(rows + [row("AG01", "claude")], ALIASES)


def test_duplicate_rows_fail_loudly(rows):
    with pytest.raises(ValueError, match="duplicada"):
        cb.count(rows + [rows[0]], ALIASES)


def test_mixed_passes_fail_loudly(rows):
    """Dictamen (n)(b), still in force (s): one pass per recount."""
    other = row("AV06", "claude", pasada="despues")
    with pytest.raises(ValueError, match="una sola pasada"):
        cb.count(rows + [other], ALIASES)


def test_mention_flag_must_be_filled_on_valid_rows(rows):
    at(rows, "AV06", "chatgpt", named="")
    with pytest.raises(ValueError, match="artica_nombrada"):
        cb.count(rows, ALIASES)


# ------------------------------------------------------------------ what the patient sees
def test_raw_sov_per_app_in_av(rows):
    c = cb.count(rows, ALIASES)["levels"]["AV"]["apps"]
    assert (c["chatgpt"]["valid"], c["chatgpt"]["excluded"], c["chatgpt"]["mentions"]) == (14, 1, 1)
    assert c["chatgpt"]["sov"] == pytest.approx(1 / 14)
    assert c["gemini"]["sov"] == pytest.approx(2 / 15)


def test_mean_position_in_av(rows):
    c = cb.count(rows, ALIASES)["levels"]["AV"]["apps"]
    assert c["gemini"]["mean_position"] == pytest.approx(1.5)
    assert c["chatgpt"]["mean_position"] == pytest.approx(1.0)


def test_levels_are_counted_apart(rows):
    """Dictamen (s): AR and AV are never added up; AR rows do not change AV and vice versa."""
    res = cb.count(rows, ALIASES)
    assert res["levels"]["AR"]["apps"]["chatgpt"]["mentions"] == 2
    assert res["levels"]["AV"]["apps"]["chatgpt"]["mentions"] == 1
    for r in rows:
        if r["id_pregunta"].startswith("AR") and r["app"] != "claude":
            r.update(artica_nombrada="si" if r["respuesta_valida"] == "si" else "")
    again = cb.count(rows, ALIASES)
    assert again["levels"]["AV"] == res["levels"]["AV"]
    assert "total" not in res and "global" not in res


def test_ar_positions_are_listed_not_averaged(rows):
    """Dictamen (o.6)/(i): AR positions as a list, never a mean; no SoV figure in AR."""
    c = cb.count(rows, ALIASES)["levels"]["AR"]["apps"]["chatgpt"]
    assert c["positions"] == [3, 1]
    assert "mean_position" not in c and "sov" not in c
    assert (c["valid"], c["mentions"]) == (5, 2)


def test_ar_chains_are_one_brand(rows):
    c = cb.count(rows, ALIASES)["levels"]["AR"]["apps"]["chatgpt"]
    assert c["instead"] == {"Cadena X": 2}


def test_clinics_in_its_place_are_canonicalised(rows):
    c = cb.count(rows, ALIASES)["levels"]["AV"]["apps"]["chatgpt"]
    assert c["instead"] == {"Clínica Sur": 3, "Centro Oeste": 1}


def test_google_overviews_only_in_ar(rows):
    """Dictamen (r): Google AI Overviews only on the 5 AR searches, apart from any verdict."""
    res = cb.count(rows, ALIASES)
    g = res["google"]
    assert (g["searches"], g["with_overview"], g["mentions"]) == (5, 2, 1)
    assert "google" not in res["levels"]["AV"]["apps"]
    assert "google" not in res["levels"]["AR"]["apps"]


def test_top_domains_per_level(rows):
    res = cb.count(rows, ALIASES)
    assert res["levels"]["AV"]["domains"][0] == ("doctoralia.es", 2)
    assert res["levels"]["AR"]["domains"] == [("doctoralia.es", 1)]


def test_no_manual_weighted_figure(rows):
    """Dictamen (n)(c), in both levels (s)."""
    res = cb.count(rows, ALIASES)
    assert "weighted" not in res
    assert "ponderado" not in cb.render_calibration(res, None, None, ["antes.csv"]).lower()


def test_observation_and_brand_rows_apart(rows):
    res = cb.count(rows, ALIASES)
    assert {o["key"] for o in res["observations"]} == {
        ("AV", "chatgpt", "pago"), ("AV", "claude", "gratuito"), ("AR", "claude", "gratuito")}
    assert [r["id_pregunta"] for r in res["brand_rows"]] == ["AM01", "AM02", "AM01", "AM02"]


def test_adjective_flag_is_reported(rows):
    at(rows, "AV01", "chatgpt", observaciones="#artica-adjetivo")
    assert cb.count(rows, ALIASES)["adjective_flags"] == 1


def test_doctor_without_clinic_flag_is_reported_apart(rows):
    at(rows, "AV02", "chatgpt", observaciones="#medica-sin-clinica")
    res = cb.count(rows, ALIASES)
    assert res["doctor_only_flags"] == 1
    assert res["levels"]["AV"]["apps"]["chatgpt"]["mentions"] == 1
    assert "#medica-sin-clinica" in cb.render_calibration(res, None, None, ["antes.csv"])


def test_rows_from_another_municipality_are_location_sensitivity_observations(rows):
    extra = row("AR01", "google", "no", resumen="si", municipio="Viveiro", plan="sin_sesion")
    res = cb.count(rows + [extra], ALIASES)
    assert res["google"]["searches"] == 5 and res["google"]["mentions"] == 1
    assert res["location_sensitivity"] == [
        {"level": "AR", "municipio": "Viveiro", "app": "google", "mentions": 0, "valid": 1}]
    assert "sensibilidad a la ubicación" in cb.render_calibration(res, None, None, ["antes.csv"])


def test_main_municipality_is_vilaboa():
    assert cb.MAIN_MUNICIPIO == "Vilaboa"


def test_reads_csv_files(tmp_path, rows):
    p = tmp_path / "antes.csv"
    with open(p, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=bd.TEMPLATE_COLUMNS)
        w.writeheader()
        w.writerows(rows)
    assert len(cb.read_rows([p])) == len(rows)


def test_alias_file(tmp_path):
    p = tmp_path / "alias.csv"
    p.write_text("alias,canonico\nSur Estética,Clínica Sur\n", encoding="utf-8")
    assert cb.read_aliases(p) == {"sur estetica": "Clínica Sur"}


# ------------------------------------------------------------------ probe results.csv
def prow(qid, provider, run, brands="", status="ok", ts="2026-10-04T09:00:00Z", model="m-1"):
    return {c: "" for c in cb.PROBE_COLUMNS} | {
        "timestamp_utc": ts, "prompt_id": qid, "provider": provider, "run": str(run),
        "status": status, "brands_mentioned": brands, "model": model,
        "specialty": "aesthetic", "city": "Viveiro"}


def test_read_probe_refuses_results_without_searched_urls(tmp_path):
    old = tmp_path / "old.csv"
    cols = [c for c in cb.PROBE_COLUMNS if c != "searched_urls"]
    old.write_text(",".join(cols) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="searched_urls"):
        cb.read_probe(old)


def test_read_probe_reads_new_results(tmp_path):
    p = tmp_path / "results.csv"
    with open(p, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cb.PROBE_COLUMNS)
        w.writeheader()
        w.writerow(prow("AV01", "openai", 1, brands=CLIENT))
    assert cb.read_probe(p)[0]["brands_mentioned"] == CLIENT


def test_probe_cell_majority_of_runs():
    probe = [prow("AV01", "openai", 1, brands=CLIENT), prow("AV01", "openai", 2, brands=CLIENT),
             prow("AV01", "openai", 3, brands="Clínica Sur"),
             prow("AV02", "openai", 1, brands=CLIENT), prow("AV02", "openai", 2),
             prow("AV02", "openai", 3)]
    cells = cb.summarize_probe(probe, CLIENT)
    assert (cells[("chatgpt", "AV01")]["k"], cells[("chatgpt", "AV01")]["n"]) == (2, 3)
    assert cells[("chatgpt", "AV01")]["status"] == "sale"
    assert cells[("chatgpt", "AV02")]["status"] == "no sale"


def test_probe_cell_tie_with_two_runs():
    probe = [prow("AV01", "gemini", 1, brands=CLIENT), prow("AV01", "gemini", 2)]
    assert cb.summarize_probe(probe, CLIENT)[("gemini", "AV01")]["status"] == "empate"


def test_probe_cell_ignores_errors_other_levels_and_claude():
    probe = [prow("AV01", "openai", 1, brands=CLIENT, status="error"),
             prow("AV01", "openai", 2),
             prow("AR01", "openai", 1, brands=CLIENT),
             prow("AV01", "claude", 1, brands=CLIENT)]
    cells = cb.summarize_probe(probe, CLIENT)
    assert set(cells) == {("chatgpt", "AV01")}
    assert (cells[("chatgpt", "AV01")]["k"], cells[("chatgpt", "AV01")]["n"]) == (0, 1)
    assert set(cb.summarize_probe(probe, CLIENT, level="AR")) == {("chatgpt", "AR01")}


def test_probe_position_is_median_of_runs_where_it_appears():
    probe = [prow("AV01", "openai", 1, brands=f"Clínica Sur;{CLIENT}"),
             prow("AV01", "openai", 2, brands=f"A;B;C;{CLIENT}"),
             prow("AV01", "openai", 3, brands=CLIENT)]
    assert cb.summarize_probe(probe, CLIENT)[("chatgpt", "AV01")]["position"] == 2


def test_probe_client_match_ignores_accents_and_case():
    probe = [prow("AV01", "openai", 1, brands="clinica norte")]
    assert cb.summarize_probe(probe, CLIENT)[("chatgpt", "AV01")]["k"] == 1


@pytest.mark.parametrize("k,n,unanimous", [(0, 3, True), (3, 3, True), (1, 3, False),
                                           (2, 3, False), (1, 2, False), (2, 2, True),
                                           (1, 1, False), (0, 1, False)])
def test_ar_probe_cell_unanimous_or_split(k, n, unanimous):
    """Dictamen (o.4): unanimous = in every valid run or in none, with >= 2 valid runs."""
    probe = [prow("AR01", "openai", i + 1, brands=CLIENT if i < k else "Clínica Sur")
             for i in range(n)]
    cell = cb.summarize_probe(probe, CLIENT, level="AR")[("chatgpt", "AR01")]
    assert cell["unanimous"] is unanimous
    assert cell["positions"] == [1] * k


# ------------------------------------------------------------------ AV comparison and verdict
def scenario_av(app_hits, probe_hits, runs=3, app_date="2026-10-06 10:00",
                probe_ts="2026-10-04T09:00:00Z"):
    """app_hits / probe_hits: {app: set of AV qids with the clinic}. The probe puts the
    clinic in every run of its qids (or in none)."""
    rows = full_pass({(a, q) for a, qs in app_hits.items() for q in qs}, when=app_date)
    probe = [prow(q, PROV[app], run, brands=CLIENT if q in probe_hits[app] else "Clínica Sur",
                  ts=probe_ts)
             for app in PROV for q in AV for run in range(1, runs + 1)]
    return rows, probe


NONE = {"chatgpt": set(), "gemini": set()}


def test_agreement_counts_same_status_cells():
    hits = {"chatgpt": {"AV01", "AV02"}, "gemini": {"AV01"}}
    probe_hits = {"chatgpt": {"AV01", "AV03"}, "gemini": {"AV01"}}
    rows, probe = scenario_av(hits, probe_hits)
    cmp = cb.compare_av(rows, probe, CLIENT)
    c = cmp["apps"]["chatgpt"]
    assert c["comparable"] == 15 and c["agree"] == 13
    assert c["agreement"] == pytest.approx(13 / 15)
    assert cmp["apps"]["gemini"]["agree"] == 15


def test_av_comparison_ignores_ar_rows_of_both_instruments():
    rows, probe = scenario_av(NONE, NONE)
    at(rows, "AR01", "chatgpt", named="si", posicion_artica="1")
    probe.append(prow("AR01", "openai", 1, brands=CLIENT))
    c = cb.compare_av(rows, probe, CLIENT)["apps"]["chatgpt"]
    assert [x["qid"] for x in c["cells"]] == AV and c["sov_app"] == 0 and c["sov_probe"] == 0


def test_agreement_tie_counts_as_agreement():
    rows, probe = scenario_av(NONE, NONE, runs=2)
    probe[0]["brands_mentioned"] = CLIENT      # chatgpt AV01: 1 of 2 runs -> tie
    cmp = cb.compare_av(rows, probe, CLIENT)
    cell = next(x for x in cmp["apps"]["chatgpt"]["cells"] if x["qid"] == "AV01")
    assert cell["probe_status"] == "empate" and cell["agree"] is True


def test_sov_app_and_probe_per_assistant():
    rows, probe = scenario_av({"chatgpt": {"AV01", "AV02", "AV03"}, "gemini": set()},
                              {"chatgpt": {"AV01"}, "gemini": set()})
    c = cb.compare_av(rows, probe, CLIENT)["apps"]["chatgpt"]
    assert c["sov_app"] == pytest.approx(3 / 15)
    assert c["sov_probe"] == pytest.approx(3 / 45)
    assert c["sov_gap"] == pytest.approx(3 / 15 - 3 / 45)


def test_verdict_yes_when_instruments_agree():
    hits = {"chatgpt": {"AV01", "AV02"}, "gemini": {"AV01"}}
    rows, probe = scenario_av(hits, hits)
    cmp = cb.compare_av(rows, probe, CLIENT)
    assert cmp["verdict"] is True and cmp["reasons"] == []


def test_verdict_no_below_seventy_percent_agreement():
    rows, probe = scenario_av({"chatgpt": {"AV01", "AV02", "AV03", "AV04", "AV05"},
                               "gemini": set()}, NONE)
    cmp = cb.compare_av(rows, probe, CLIENT)
    assert cmp["verdict"] is False
    assert any("acuerdo" in r and "chatgpt" in r for r in cmp["reasons"])


def test_verdict_threshold_is_eleven_of_fifteen():
    four = {"AV01", "AV02", "AV03", "AV04"}           # 11/15 = 73 % agreement
    rows, probe = scenario_av({"chatgpt": four, "gemini": set()}, NONE)
    cmp = cb.compare_av(rows, probe, CLIENT)
    assert cmp["apps"]["chatgpt"]["agreement"] >= cb.MIN_AGREEMENT
    assert cmp["verdict"] is False                   # but the SoV gap is 26.7 pts > 20
    assert [r for r in cmp["reasons"] if "acuerdo" in r] == []
    assert any("SoV" in r for r in cmp["reasons"])


def test_verdict_no_when_sov_gap_above_twenty_points():
    rows, probe = scenario_av(NONE, {"chatgpt": {"AV01", "AV02", "AV03", "AV04"},
                                     "gemini": set()})
    cmp = cb.compare_av(rows, probe, CLIENT)
    assert cmp["apps"]["chatgpt"]["sov_gap"] == pytest.approx(-4 / 15)
    assert cmp["verdict"] is False


def test_verdict_no_with_fewer_than_twelve_comparable_cells():
    rows, probe = scenario_av(NONE, NONE)
    for q in AV[:4]:
        at(rows, q, "chatgpt", respuesta_valida="no", named="")
    cmp = cb.compare_av(rows, probe, CLIENT)
    assert cmp["apps"]["chatgpt"]["comparable"] == 11
    assert cmp["verdict"] is False
    assert any("comparables" in r for r in cmp["reasons"])


def test_window_distance_between_probe_and_manual_dates():
    rows, probe = scenario_av(NONE, NONE, app_date="2026-10-11 10:00",
                              probe_ts="2026-10-04T09:00:00Z")
    cmp = cb.compare_av(rows, probe, CLIENT)
    assert cmp["window_days"] == 7 and cmp["window_ok"] is True


def test_window_beyond_seven_days_gives_no():
    rows, probe = scenario_av(NONE, NONE, app_date="2026-10-12 10:00",
                              probe_ts="2026-10-04T09:00:00Z")
    cmp = cb.compare_av(rows, probe, CLIENT)
    assert cmp["window_days"] == 8 and cmp["verdict"] is False
    assert any("ventana" in r for r in cmp["reasons"])


def test_window_is_zero_when_dates_overlap():
    rows, probe = scenario_av(NONE, NONE, app_date="2026-10-04 18:00",
                              probe_ts="2026-10-04T09:00:00Z")
    assert cb.compare_av(rows, probe, CLIENT)["window_days"] == 0


def test_positions_are_reported_but_do_not_decide():
    hits = {"chatgpt": {"AV01", "AV02"}, "gemini": set()}
    rows, probe = scenario_av(hits, hits)
    at(rows, "AV02", "chatgpt", posicion_artica="5")  # app 5, probe 1
    cmp = cb.compare_av(rows, probe, CLIENT)
    c = cmp["apps"]["chatgpt"]
    assert c["positions_both"] == 2 and c["positions_close"] == 1
    assert cmp["verdict"] is True


def test_observation_rows_do_not_enter_the_comparison():
    hits = {"chatgpt": {"AV01"}, "gemini": set()}
    rows, probe = scenario_av(hits, hits)
    rows.append(row("AV02", "chatgpt", "si", plan="pago", pos="1"))
    assert cb.compare_av(rows, probe, CLIENT)["apps"]["chatgpt"]["agree"] == 15


def test_models_of_both_instruments_are_reported():
    rows, probe = scenario_av(NONE, NONE)
    cmp = cb.compare_av(rows, probe, CLIENT)
    assert cmp["apps"]["chatgpt"]["models_app"] == ["x"]
    assert cmp["apps"]["chatgpt"]["models_probe"] == ["m-1"]


# ------------------------------------------------------------------ AR comparison and verdict
def scenario_ar(app_hits, probe_k, runs=3, app_date="2026-10-06 10:00",
                probe_ts="2026-10-04T09:00:00Z"):
    """app_hits: {app: set of AR qids with the clinic}; probe_k: {(app, qid): runs with the
    clinic} (0 when absent)."""
    rows = full_pass({(a, q) for a, qs in app_hits.items() for q in qs}, when=app_date)
    probe = [prow(q, PROV[app], run,
                  brands=CLIENT if run <= probe_k.get((app, q), 0) else "Clínica Sur",
                  ts=probe_ts)
             for app in PROV for q in AR for run in range(1, runs + 1)]
    return rows, probe


def test_ar_verdict_yes_without_gross_discrepancy():
    """Split cells are compatible with any app answer (dictamen p.2)."""
    rows, probe = scenario_ar({"chatgpt": {"AR01", "AR02"}, "gemini": {"AR03"}},
                              {("chatgpt", "AR01"): 3, ("chatgpt", "AR02"): 1,
                               ("chatgpt", "AR03"): 2, ("gemini", "AR03"): 3})
    cmp = cb.compare_ar(rows, probe, CLIENT)
    c = cmp["apps"]["chatgpt"]
    assert (c["comparable"], c["decisive"], c["gross"]) == (5, 3, 0)
    assert cmp["verdict"] is True and cmp["reasons"] == []


def test_ar_verdict_allows_one_gross_discrepancy_per_assistant():
    rows, probe = scenario_ar({"chatgpt": {"AR01"}, "gemini": set()}, {})
    cmp = cb.compare_ar(rows, probe, CLIENT)
    assert cmp["apps"]["chatgpt"]["gross"] == 1 and cmp["verdict"] is True


def test_ar_verdict_no_with_two_gross_discrepancies():
    rows, probe = scenario_ar({"chatgpt": set(), "gemini": {"AR01"}},
                              {("gemini", "AR02"): 3})
    cmp = cb.compare_ar(rows, probe, CLIENT)
    assert cmp["apps"]["gemini"]["gross"] == 2
    assert cmp["verdict"] is False
    assert any("gemini" in r and "discrepancias gruesas" in r for r in cmp["reasons"])


def test_ar_verdict_no_with_fewer_than_three_decisive_cells():
    split = {("chatgpt", q): 1 for q in ("AR01", "AR02", "AR03")}
    rows, probe = scenario_ar(NONE, split)
    cmp = cb.compare_ar(rows, probe, CLIENT)
    assert cmp["apps"]["chatgpt"]["decisive"] == 2
    assert cmp["verdict"] is False
    assert any("decisivas" in r for r in cmp["reasons"])


def test_ar_verdict_no_with_fewer_than_four_comparable_cells():
    rows, probe = scenario_ar(NONE, {})
    for q in ("AR01", "AR02"):
        at(rows, q, "chatgpt", respuesta_valida="no", named="")
    cmp = cb.compare_ar(rows, probe, CLIENT)
    assert cmp["apps"]["chatgpt"]["comparable"] == 3
    assert cmp["verdict"] is False
    assert any("comparables" in r for r in cmp["reasons"])


def test_ar_one_run_rows_are_not_comparable():
    """Dictamen (o.2)/(o.4): the 1-run AR rows of the official baseline are not the paired
    AR execution; with one valid run no cell is comparable, so the verdict is "no"."""
    rows, probe = scenario_ar(NONE, {}, runs=1)
    cmp = cb.compare_ar(rows, probe, CLIENT)
    assert cmp["apps"]["chatgpt"]["comparable"] == 0 and cmp["verdict"] is False


def test_ar_verdict_ignores_sov():
    """Dictamen (p.5): no SoV gap in AR; a large difference of counts made only of split
    cells is not a gross discrepancy."""
    rows, probe = scenario_ar({"chatgpt": set(), "gemini": set()},
                              {("chatgpt", "AR01"): 2, ("chatgpt", "AR02"): 2})
    cmp = cb.compare_ar(rows, probe, CLIENT)
    c = cmp["apps"]["chatgpt"]
    assert (c["app_mentions"], c["app_valid"], c["probe_k"], c["probe_n"]) == (0, 5, 4, 15)
    assert "sov_gap" not in c and cmp["verdict"] is True


def test_ar_window_is_checked_against_the_ar_execution():
    rows, probe = scenario_ar(NONE, {}, app_date="2026-10-06 10:00",
                              probe_ts="2026-09-29T17:43:00Z")
    cmp = cb.compare_ar(rows, probe, CLIENT)
    assert cmp["window_days"] == 7 and cmp["window_ok"] is True


def test_ar_window_beyond_seven_days_gives_no():
    rows, probe = scenario_ar(NONE, {}, app_date="2026-10-07 10:00",
                              probe_ts="2026-09-29T17:43:00Z")
    cmp = cb.compare_ar(rows, probe, CLIENT)
    assert cmp["window_days"] == 8 and cmp["verdict"] is False
    assert any("ventana" in r for r in cmp["reasons"])


def test_ar_window_uses_only_ar_rows_of_the_probe():
    rows, probe = scenario_ar(NONE, {}, probe_ts="2026-10-04T09:00:00Z")
    probe.append(prow("AV01", "openai", 1, ts="2026-09-01T09:00:00Z"))
    assert cb.compare_ar(rows, probe, CLIENT)["window_days"] == 2


def test_ar_positions_are_listed_on_both_sides():
    rows, probe = scenario_ar({"chatgpt": {"AR01"}, "gemini": set()}, {("chatgpt", "AR01"): 3})
    at(rows, "AR01", "chatgpt", posicion_artica="2")
    cell = cb.compare_ar(rows, probe, CLIENT)["apps"]["chatgpt"]["cells"][0]
    assert cell["app_pos"] == 2 and cell["probe_positions"] == [1, 1, 1]


def test_thresholds_of_the_dictamen():
    assert (cb.MAX_WINDOW_DAYS, cb.MIN_COMPARABLE, cb.MIN_AGREEMENT, cb.MAX_SOV_GAP,
            cb.POSITION_TOLERANCE) == (7, 12, 0.70, 0.20, 2)                   # (k)-(l), (q)
    assert (cb.AR_MAX_WINDOW_DAYS, cb.AR_MIN_VALID_RUNS, cb.AR_MIN_COMPARABLE,
            cb.AR_MIN_DECISIVE, cb.AR_MAX_GROSS) == (7, 2, 4, 3, 1)            # (o)-(p)
    assert not hasattr(cb, "AIO_CLEAR_CHANGE")                                 # (r.4)


# ------------------------------------------------------------------ calibration report
def both(av_app=None, av_probe=None, ar_app=None, ar_k=None):
    rows, probe_av = scenario_av(av_app or NONE, av_probe or av_app or NONE)
    _, probe_ar = scenario_ar(NONE, ar_k or {})
    for app, qs in (ar_app or {}).items():
        for q in qs:
            at(rows, q, app, named="si", posicion_artica="1")
    return rows, probe_av, probe_ar


def report(rows, probe_av, probe_ar):
    return cb.render_calibration(cb.count(rows), cb.compare_av(rows, probe_av, CLIENT),
                                 cb.compare_ar(rows, probe_ar, CLIENT),
                                 ["antes.csv", "probe/results.csv", "probe-AR-antes/results.csv"])


def _section(md, start, end=None):
    part = md.split(start, 1)[1]
    return part.split(end, 1)[0] if end else part


def test_render_has_one_section_and_one_verdict_per_level():
    md = report(*both(av_app={"chatgpt": {"AV01"}, "gemini": set()}))
    for heading in ("Lo que ve el paciente — núcleo AV", "Lo que ve el paciente — área de "
                    "influencia AR", "Google", "Dominios", "Preguntas de marca",
                    "Comparación app frente a probe — AV",
                    "Comparación app frente a probe — AR"):
        assert heading in md, heading
    low = md.lower()
    assert low.count("coinciden de forma razonable en av: sí") == 1
    assert low.count("sin discrepancia gruesa en ar: sí") == 1
    assert "coinciden de forma razonable en ar" not in low
    assert "| AV01 |" in md and "| AR01 |" in md


def test_render_never_combines_levels():
    """Dictamen (s): no figure or verdict adds up AR and AV; no 'global' verdict."""
    md = report(*both())
    low = md.lower()
    assert "global" not in low and "combinad" not in low and "total" not in low
    av = _section(md, "## 3. Comparación app frente a probe — AV", "## 4.")
    ar = _section(md, "## 4. Comparación app frente a probe — AR")
    assert "AR0" not in av and "AV0" not in ar
    assert [ln for ln in md.splitlines() if "AV" in ln and "AR" in ln and any(
        ch.isdigit() for ch in ln.replace("AV", "").replace("AR", ""))] == []


def test_render_ar_sections_without_percentages():
    """Dictamen (p.5)/(j): AR, app and probe, only as counts."""
    md = report(*both(ar_app={"chatgpt": {"AR01"}}, ar_k={("chatgpt", "AR01"): 2}))
    assert "%" not in _section(md, "## 1b.", "## 2.")
    assert "%" not in _section(md, "## 4. Comparación app frente a probe — AR")
    assert "1 de 5" in _section(md, "## 1b.", "## 2.")


def test_render_google_as_counts_without_percentages(rows):
    md = cb.render_calibration(cb.count(rows, ALIASES), None, None, ["antes.csv"])
    section = _section(md, "## Google", "\n## ")
    assert "%" not in section and "AR" in section
    assert "1 de 5" in section and "1 de 2" in section
    assert "solo se describe" in section and "cambio claro" not in section


def test_render_ar_writes_its_limits():
    md = report(*both()).lower()
    ar = _section(md, "## 4. comparación app frente a probe — ar")
    assert "veredicto débil" in ar and "vilaboa" in ar and "viveiro" in ar
    assert "como objetivo, no como dato" in ar


def test_render_says_what_each_no_blocks():
    rows, probe_av, probe_ar = both(av_app={"chatgpt": {"AV01", "AV02", "AV03", "AV04", "AV05"},
                                            "gemini": set()},
                                    av_probe=NONE, ar_app={"gemini": {"AR01", "AR02"}})
    md = report(rows, probe_av, probe_ar).lower()
    av = _section(md, "## 3. comparación app frente a probe — av", "## 4.")
    ar = _section(md, "## 4. comparación app frente a probe — ar")
    assert "coinciden de forma razonable en av: no" in av
    assert "ya sois la clínica que la ia recomienda en a mariña" in av
    assert "ninguna cifra av del probe" in av
    assert "sin discrepancia gruesa en ar: no" in ar
    assert "frase del objetivo" in ar and "ninguna cifra ar del probe" in ar
    assert "(c)" in ar


def test_render_calibration_never_enters_the_go():
    md = report(*both()).lower()
    assert "no entra en el criterio go" in md


def test_cli_writes_two_tables_and_two_verdicts(tmp_path):
    rows, probe_av, probe_ar = both(av_app={"chatgpt": {"AV01"}, "gemini": set()})
    manual = tmp_path / "antes.csv"
    with open(manual, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=bd.TEMPLATE_COLUMNS)
        w.writeheader()
        w.writerows(rows)
    paths = {}
    for name, probe in (("av", probe_av), ("ar", probe_ar)):
        paths[name] = tmp_path / f"results-{name}.csv"
        with open(paths[name], "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cb.PROBE_COLUMNS)
            w.writeheader()
            w.writerows(probe)
    out = tmp_path / "calibracion-antes.md"
    assert cb.main([str(manual), "--probe-av", str(paths["av"]), "--probe-ar",
                    str(paths["ar"]), "--client", CLIENT, "--out", str(out)]) == 0
    md = out.read_text(encoding="utf-8").lower()
    assert "coinciden de forma razonable en av: sí" in md
    assert "sin discrepancia gruesa en ar: sí" in md
    assert "results-av.csv" in md and "results-ar.csv" in md
