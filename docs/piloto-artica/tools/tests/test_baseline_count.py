"""SPEC-007 CA-7 (amendment 2026-09-29 (b)): recount of one manual calibration pass and
comparison app vs probe, following the CA-2 dictamen (k)-(n) in the SPEC-007 ledger.

Fixtures use a fictitious clinic ("Clínica Norte") and fictitious competitors: no real
figures ever live in the repo (ADR-004).
"""
import csv

import pytest

import baseline_docs as bd
import count_baseline as cb

BASE = {c: "" for c in bd.TEMPLATE_COLUMNS}
CLIENT = "Clínica Norte"


def row(qid, app, named, valid="si", plan="gratuito", clinics="", pos="", domains="",
        resumen="n-a", obs="", pasada="antes", when="2026-10-06 10:00", municipio="Vilaboa",
        model="x"):
    r = dict(BASE)
    r.update(pasada=pasada, id_pregunta=qid, app=app, plan_cuenta=plan, respuesta_valida=valid,
             artica_nombrada=named, clinicas_nombradas=clinics, posicion_artica=pos,
             dominios_citados=domains, resumen_ia=resumen, observaciones=obs,
             fecha_hora_local=when, modo="temporal", sesion_iniciada="si", cuenta="a",
             modelo_mostrado=model, municipio=municipio, ubicacion_dispositivo="si",
             idioma="es")
    return r


@pytest.fixture
def rows():
    return [
        # chatgpt: 4 valid, 1 mention -> 25 %
        row("AV01", "chatgpt", "si", clinics="Clínica Norte;Clínica Sur", pos="1",
            domains="doctoralia.es;clinicanorte.es"),
        row("AV02", "chatgpt", "no", clinics="Clínica Sur;Centro Oeste", domains="doctoralia.es"),
        row("AV03", "chatgpt", "no", clinics="clinica sur"),
        row("AV04", "chatgpt", "no", clinics="Sur Estética"),
        row("AV05", "chatgpt", "", valid="no"),                    # excluded
        # gemini: 2 valid, 2 mentions (positions 2 and 1) -> 100 %
        row("AV01", "gemini", "si", clinics="Clínica Sur;Clínica Norte", pos="2"),
        row("AV02", "gemini", "si", clinics="Clínica Norte", pos="1"),
        # google: 3 valid searches, 2 with AI overview, 1 mention
        row("AV01", "google", "si", resumen="si", clinics="Clínica Norte", pos="1",
            domains="doctoralia.es"),
        row("AV02", "google", "no", resumen="si", clinics="Clínica Sur"),
        row("AV03", "google", "no", resumen="no"),
        # observation rows: paid plan and claude never enter the main figures
        row("AV01", "chatgpt", "si", plan="pago", clinics="Clínica Norte", pos="1"),
        row("AV01", "claude", "si", clinics="Clínica Norte", pos="1"),
        # brand questions never enter SoV
        row("AM01", "chatgpt", "si", obs="dirección correcta"),
    ]


ALIASES = {"sur estetica": "Clínica Sur", "clinica sur": "Clínica Sur"}


# ------------------------------------------------------------------ one manual pass
def test_raw_sov_per_app(rows):
    res = cb.count(rows, ALIASES)
    assert res["apps"]["chatgpt"]["valid"] == 4
    assert res["apps"]["chatgpt"]["mentions"] == 1
    assert res["apps"]["chatgpt"]["sov"] == pytest.approx(0.25)
    assert res["apps"]["chatgpt"]["excluded"] == 1
    assert res["apps"]["gemini"]["sov"] == pytest.approx(1.0)


def test_no_manual_weighted_figure(rows):
    """Dictamen (n): the manual weighted SoV is not computed (the Go is probe vs probe)."""
    res = cb.count(rows, ALIASES)
    assert "weighted" not in res
    assert "ponderado" not in cb.render_calibration(res, None, ["antes.csv"]).lower()


def test_mean_position(rows):
    res = cb.count(rows, ALIASES)
    assert res["apps"]["gemini"]["mean_position"] == pytest.approx(1.5)
    assert res["apps"]["chatgpt"]["mean_position"] == pytest.approx(1.0)


def test_clinics_in_its_place_are_canonicalised(rows):
    res = cb.count(rows, ALIASES)
    assert res["apps"]["chatgpt"]["instead"] == {"Clínica Sur": 3, "Centro Oeste": 1}


def test_google_ai_overviews_apart(rows):
    res = cb.count(rows, ALIASES)
    g = res["google"]
    assert (g["searches"], g["with_overview"], g["mentions"]) == (3, 2, 1)
    assert "google" not in res["apps"]


def test_render_google_as_counts_without_percentages(rows):
    md = cb.render_calibration(cb.count(rows, ALIASES), None, ["antes.csv"])
    section = md.split("## Google", 1)[1].split("\n## ", 1)[0]
    assert "%" not in section
    assert "1 de 3" in section and "1 de 2" in section


def test_top_domains(rows):
    assert cb.count(rows, ALIASES)["domains"][0] == ("doctoralia.es", 3)


def test_observation_and_brand_rows_apart(rows):
    res = cb.count(rows, ALIASES)
    assert {o["key"] for o in res["observations"]} == {("chatgpt", "pago"), ("claude", "gratuito")}
    assert [r["id_pregunta"] for r in res["brand_rows"]] == ["AM01"]


def test_duplicate_rows_fail_loudly(rows):
    with pytest.raises(ValueError, match="duplicada"):
        cb.count(rows + [rows[0]], ALIASES)


def test_mixed_passes_fail_loudly(rows):
    """Dictamen (n)(b): one pass per recount; 'antes' and 'despues' are never joined."""
    other = row("AV06", "chatgpt", "no", pasada="despues")
    with pytest.raises(ValueError, match="una sola pasada"):
        cb.count(rows + [other], ALIASES)


def test_mention_flag_must_be_filled_on_valid_rows(rows):
    rows[0]["artica_nombrada"] = ""
    with pytest.raises(ValueError, match="artica_nombrada"):
        cb.count(rows, ALIASES)


def test_adjective_flag_is_reported(rows):
    rows[0]["observaciones"] = "#artica-adjetivo"
    assert cb.count(rows, ALIASES)["adjective_flags"] == 1


def test_doctor_without_clinic_flag_is_reported_apart(rows):
    rows[1]["observaciones"] = "#medica-sin-clinica"
    res = cb.count(rows, ALIASES)
    assert res["doctor_only_flags"] == 1
    assert res["apps"]["chatgpt"]["mentions"] == 1
    assert "#medica-sin-clinica" in cb.render_calibration(res, None, ["antes.csv"])


def test_rows_from_another_municipality_are_location_sensitivity_observations(rows):
    extra = dict(rows[7])          # AV01 google, mention
    extra.update(municipio="Viveiro", artica_nombrada="no", resumen_ia="si")
    res = cb.count(rows + [extra], ALIASES)
    assert res["google"]["searches"] == 3 and res["google"]["mentions"] == 1
    assert res["location_sensitivity"] == [
        {"municipio": "Viveiro", "app": "google", "mentions": 0, "valid": 1}]
    assert "sensibilidad a la ubicación" in cb.render_calibration(res, None, ["antes.csv"])


def test_main_municipality_is_vilaboa():
    assert cb.MAIN_MUNICIPIO == "Vilaboa"


def test_level_rows_are_ignored(rows):
    """Dictamen (n)(g-j): AR/AG are not asked by hand; stray rows never enter any figure."""
    stray = [row("AR01", "chatgpt", "si", pos="1"), row("AG01", "google", "si", resumen="si")]
    with_stray = cb.count(rows + stray, ALIASES)
    without = cb.count(rows, ALIASES)
    for key in ("apps", "google", "domains"):
        assert with_stray[key] == without[key], key
    assert with_stray["ignored_rows"] == 2


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
def prow(qid, provider, run, brands="", status="ok", ts="2026-10-04T09:00:00Z", model="m-1",
         cited="", searched=""):
    return {c: "" for c in cb.PROBE_COLUMNS} | {
        "timestamp_utc": ts, "prompt_id": qid, "provider": provider, "run": str(run),
        "status": status, "brands_mentioned": brands, "model": model, "cited_urls": cited,
        "searched_urls": searched, "specialty": "aesthetic", "city": "Viveiro"}


def test_read_probe_refuses_results_without_searched_urls(tmp_path):
    """Dictamen (k): only a results.csv written after SPEC-013 (with searched_urls; the
    meaning of Gemini's cited_urls changed there) is paired with the manual pass."""
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
    assert cells[("chatgpt", "AV01")]["k"] == 2 and cells[("chatgpt", "AV01")]["n"] == 3
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


def test_probe_position_is_median_of_runs_where_it_appears():
    probe = [prow("AV01", "openai", 1, brands=f"Clínica Sur;{CLIENT}"),
             prow("AV01", "openai", 2, brands=f"A;B;C;{CLIENT}"),
             prow("AV01", "openai", 3, brands=CLIENT)]
    assert cb.summarize_probe(probe, CLIENT)[("chatgpt", "AV01")]["position"] == 2


def test_probe_client_match_ignores_accents_and_case():
    probe = [prow("AV01", "openai", 1, brands="clinica norte")]
    assert cb.summarize_probe(probe, CLIENT)[("chatgpt", "AV01")]["k"] == 1


# ------------------------------------------------------------------ comparison and verdict
QIDS = [f"AV{i:02d}" for i in range(1, 16)]


def scenario(app_hits, probe_hits, runs=3, app_date="2026-10-06 10:00",
             probe_ts="2026-10-04T09:00:00Z"):
    """app_hits / probe_hits: {app: set of qids where the clinic appears}. The probe puts
    the clinic in every run of its qids (or in none)."""
    rows, probe = [], []
    prov = {"chatgpt": "openai", "gemini": "gemini"}
    for app in ("chatgpt", "gemini"):
        for q in QIDS:
            hit = q in app_hits[app]
            rows.append(row(q, app, "si" if hit else "no", pos="1" if hit else "",
                            when=app_date))
            for run in range(1, runs + 1):
                probe.append(prow(q, prov[app], run,
                                  brands=CLIENT if q in probe_hits[app] else "Clínica Sur",
                                  ts=probe_ts))
    return rows, probe


def test_agreement_counts_same_status_cells():
    hits = {"chatgpt": {"AV01", "AV02"}, "gemini": {"AV01"}}
    probe_hits = {"chatgpt": {"AV01", "AV03"}, "gemini": {"AV01"}}
    rows, probe = scenario(hits, probe_hits)
    cmp = cb.compare_with_probe(rows, probe, CLIENT)
    c = cmp["apps"]["chatgpt"]
    assert c["comparable"] == 15 and c["agree"] == 13
    assert c["agreement"] == pytest.approx(13 / 15)
    assert cmp["apps"]["gemini"]["agree"] == 15


def test_agreement_tie_counts_as_agreement():
    rows, probe = scenario({"chatgpt": set(), "gemini": set()},
                           {"chatgpt": set(), "gemini": set()}, runs=2)
    probe[0]["brands_mentioned"] = CLIENT      # chatgpt AV01: 1 of 2 runs -> tie
    cmp = cb.compare_with_probe(rows, probe, CLIENT)
    cell = next(x for x in cmp["apps"]["chatgpt"]["cells"] if x["qid"] == "AV01")
    assert cell["probe_status"] == "empate" and cell["agree"] is True


def test_sov_app_and_probe_per_assistant():
    rows, probe = scenario({"chatgpt": {"AV01", "AV02", "AV03"}, "gemini": set()},
                           {"chatgpt": {"AV01"}, "gemini": set()})
    c = cb.compare_with_probe(rows, probe, CLIENT)["apps"]["chatgpt"]
    assert c["sov_app"] == pytest.approx(3 / 15)
    assert c["sov_probe"] == pytest.approx(3 / 45)
    assert c["sov_gap"] == pytest.approx(3 / 15 - 3 / 45)


def test_verdict_yes_when_instruments_agree():
    hits = {"chatgpt": {"AV01", "AV02"}, "gemini": {"AV01"}}
    rows, probe = scenario(hits, hits)
    cmp = cb.compare_with_probe(rows, probe, CLIENT)
    assert cmp["verdict"] is True and cmp["reasons"] == []


def test_verdict_no_below_seventy_percent_agreement():
    # 5 disagreeing cells of 15 -> 66.7 % < 70 %; SoV gap 5/15 - 0 = 33 pts too
    rows, probe = scenario({"chatgpt": {"AV01", "AV02", "AV03", "AV04", "AV05"}, "gemini": set()},
                           {"chatgpt": set(), "gemini": set()})
    cmp = cb.compare_with_probe(rows, probe, CLIENT)
    assert cmp["verdict"] is False
    assert any("acuerdo" in r and "chatgpt" in r for r in cmp["reasons"])


def test_verdict_threshold_is_eleven_of_fifteen():
    four = {"AV01", "AV02", "AV03", "AV04"}           # 11/15 = 73 % agreement
    rows, probe = scenario({"chatgpt": four, "gemini": set()},
                           {"chatgpt": set(), "gemini": set()})
    cmp = cb.compare_with_probe(rows, probe, CLIENT)
    assert cmp["apps"]["chatgpt"]["agreement"] >= cb.MIN_AGREEMENT
    # but the SoV gap is 4/15 = 26.7 pts > 20: still "no", for that reason only
    assert cmp["verdict"] is False
    assert [r for r in cmp["reasons"] if "acuerdo" in r] == []
    assert any("SoV" in r for r in cmp["reasons"])


def test_verdict_no_when_sov_gap_above_twenty_points():
    # probe: clinic in every run of 4 questions where the app agrees 11/15 -> gap check
    rows, probe = scenario({"chatgpt": set(), "gemini": set()},
                           {"chatgpt": {"AV01", "AV02", "AV03", "AV04"}, "gemini": set()})
    cmp = cb.compare_with_probe(rows, probe, CLIENT)
    assert cmp["apps"]["chatgpt"]["sov_gap"] == pytest.approx(-4 / 15)
    assert cmp["verdict"] is False


def test_verdict_no_with_fewer_than_twelve_comparable_cells():
    rows, probe = scenario({"chatgpt": set(), "gemini": set()},
                           {"chatgpt": set(), "gemini": set()})
    for r in rows[:4]:                                  # chatgpt AV01-AV04 invalid
        r.update(respuesta_valida="no", artica_nombrada="")
    cmp = cb.compare_with_probe(rows, probe, CLIENT)
    assert cmp["apps"]["chatgpt"]["comparable"] == 11
    assert cmp["verdict"] is False
    assert any("comparables" in r for r in cmp["reasons"])


def test_window_distance_between_probe_and_manual_dates():
    rows, probe = scenario({"chatgpt": set(), "gemini": set()},
                           {"chatgpt": set(), "gemini": set()},
                           app_date="2026-10-11 10:00", probe_ts="2026-10-04T09:00:00Z")
    cmp = cb.compare_with_probe(rows, probe, CLIENT)
    assert cmp["window_days"] == 7 and cmp["window_ok"] is True


def test_window_beyond_seven_days_gives_no():
    rows, probe = scenario({"chatgpt": set(), "gemini": set()},
                           {"chatgpt": set(), "gemini": set()},
                           app_date="2026-10-12 10:00", probe_ts="2026-10-04T09:00:00Z")
    cmp = cb.compare_with_probe(rows, probe, CLIENT)
    assert cmp["window_days"] == 8 and cmp["verdict"] is False
    assert any("ventana" in r for r in cmp["reasons"])


def test_window_is_zero_when_dates_overlap():
    rows, probe = scenario({"chatgpt": set(), "gemini": set()},
                           {"chatgpt": set(), "gemini": set()},
                           app_date="2026-10-04 18:00", probe_ts="2026-10-04T09:00:00Z")
    assert cb.compare_with_probe(rows, probe, CLIENT)["window_days"] == 0


def test_positions_are_reported_but_do_not_decide():
    hits = {"chatgpt": {"AV01", "AV02"}, "gemini": set()}
    rows, probe = scenario(hits, hits)
    rows[1]["posicion_artica"] = "5"                  # chatgpt AV02: app 5, probe 1
    cmp = cb.compare_with_probe(rows, probe, CLIENT)
    c = cmp["apps"]["chatgpt"]
    assert c["positions_both"] == 2 and c["positions_close"] == 1
    assert cmp["verdict"] is True


def test_observation_rows_do_not_enter_the_comparison():
    hits = {"chatgpt": {"AV01"}, "gemini": set()}
    rows, probe = scenario(hits, hits)
    rows.append(row("AV02", "chatgpt", "si", plan="pago", pos="1"))
    assert cb.compare_with_probe(rows, probe, CLIENT)["apps"]["chatgpt"]["agree"] == 15


def test_models_of_both_instruments_are_reported():
    rows, probe = scenario({"chatgpt": set(), "gemini": set()},
                           {"chatgpt": set(), "gemini": set()})
    cmp = cb.compare_with_probe(rows, probe, CLIENT)
    assert cmp["apps"]["chatgpt"]["models_app"] == ["x"]
    assert cmp["apps"]["chatgpt"]["models_probe"] == ["m-1"]


def test_thresholds_of_the_dictamen():
    assert (cb.MAX_WINDOW_DAYS, cb.MIN_COMPARABLE, cb.MIN_AGREEMENT, cb.MAX_SOV_GAP,
            cb.POSITION_TOLERANCE, cb.AIO_CLEAR_CHANGE) == (7, 12, 0.70, 0.20, 2, 5)


# ------------------------------------------------------------------ calibration report
def test_render_calibration_has_both_parts_and_verdict():
    hits = {"chatgpt": {"AV01", "AV02"}, "gemini": {"AV01"}}
    rows, probe = scenario(hits, hits)
    md = cb.render_calibration(cb.count(rows), cb.compare_with_probe(rows, probe, CLIENT),
                               ["antes.csv", "results.csv"])
    for heading in ("Lo que ve el paciente", "Google", "Dominios", "Preguntas de marca",
                    "Comparación app frente a probe"):
        assert heading in md
    assert "coinciden de forma razonable: sí" in md.lower()
    assert "| AV01 |" in md


def test_render_calibration_says_what_to_do_if_no():
    rows, probe = scenario({"chatgpt": {"AV01", "AV02", "AV03", "AV04", "AV05"}, "gemini": set()},
                           {"chatgpt": set(), "gemini": set()})
    md = cb.render_calibration(cb.count(rows), cb.compare_with_probe(rows, probe, CLIENT),
                               ["antes.csv", "results.csv"])
    assert "coinciden de forma razonable: no" in md.lower()
    assert "ninguna cifra del probe" in md.lower()


def test_render_calibration_never_enters_the_go():
    rows, probe = scenario({"chatgpt": set(), "gemini": set()},
                           {"chatgpt": set(), "gemini": set()})
    md = cb.render_calibration(cb.count(rows), cb.compare_with_probe(rows, probe, CLIENT),
                               ["antes.csv"])
    assert "no entra en el criterio go" in md.lower()


def test_cli_writes_the_calibration_report(tmp_path):
    hits = {"chatgpt": {"AV01"}, "gemini": set()}
    rows, probe = scenario(hits, hits)
    manual = tmp_path / "antes.csv"
    with open(manual, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=bd.TEMPLATE_COLUMNS)
        w.writeheader()
        w.writerows(rows)
    results = tmp_path / "results.csv"
    with open(results, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cb.PROBE_COLUMNS)
        w.writeheader()
        w.writerows(probe)
    out = tmp_path / "calibracion-antes.md"
    assert cb.main([str(manual), "--probe", str(results), "--client", CLIENT,
                    "--out", str(out)]) == 0
    assert "coinciden de forma razonable: sí" in out.read_text(encoding="utf-8").lower()
