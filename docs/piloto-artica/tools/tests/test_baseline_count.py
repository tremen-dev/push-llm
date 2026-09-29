"""SPEC-007 CA-7: reproducible recount of the manual baseline from the filled CSV.

Fixtures use a fictitious clinic ("Clínica Norte") and fictitious competitors: no real
figures ever live in the repo (ADR-004).
"""
import csv
import io

import pytest

import baseline_docs as bd
import count_baseline as cb

BASE = {c: "" for c in bd.TEMPLATE_COLUMNS}


def row(pasada, qid, app, named, valid="si", plan="gratuito", clinics="", pos="",
        domains="", resumen="n-a", obs=""):
    r = dict(BASE)
    r.update(pasada=pasada, id_pregunta=qid, app=app, plan_cuenta=plan, respuesta_valida=valid,
             artica_nombrada=named, clinicas_nombradas=clinics, posicion_artica=pos,
             dominios_citados=domains, resumen_ia=resumen, observaciones=obs,
             fecha_hora_local="2026-10-01 10:00", modo="temporal", sesion_iniciada="si",
             cuenta="a", modelo_mostrado="x", municipio="Vilaboa", ubicacion_dispositivo="si",
             idioma="es")
    return r


@pytest.fixture
def rows():
    return [
        # chatgpt: 4 valid, 1 mention -> 25 %
        row("p1", "AV01", "chatgpt", "si", clinics="Clínica Norte;Clínica Sur", pos="1",
            domains="doctoralia.es;clinicanorte.es"),
        row("p1", "AV02", "chatgpt", "no", clinics="Clínica Sur;Centro Oeste", domains="doctoralia.es"),
        row("p2", "AV01", "chatgpt", "no", clinics="clinica sur"),
        row("p2", "AV02", "chatgpt", "no", clinics="Sur Estética"),
        row("p2", "AV03", "chatgpt", "", valid="no"),                 # excluded
        # gemini: 2 valid, 2 mentions (positions 2 and 1) -> 100 %
        row("p1", "AV01", "gemini", "si", clinics="Clínica Sur;Clínica Norte", pos="2"),
        row("p2", "AV01", "gemini", "si", clinics="Clínica Norte", pos="1"),
        # google: 3 valid searches, 2 with AI overview, 1 mention
        row("p1", "AV01", "google", "si", resumen="si", clinics="Clínica Norte", pos="1",
            domains="doctoralia.es"),
        row("p1", "AV02", "google", "no", resumen="si", clinics="Clínica Sur"),
        row("p2", "AV01", "google", "no", resumen="no"),
        # observation rows: paid plan and claude never enter the main figures
        row("p1", "AV01", "chatgpt", "si", plan="pago", clinics="Clínica Norte", pos="1"),
        row("p1", "AV01", "claude", "si", clinics="Clínica Norte", pos="1"),
        # brand questions never enter SoV
        row("p1", "AM01", "chatgpt", "si", obs="dirección correcta"),
    ]


ALIASES = {"sur estetica": "Clínica Sur", "clinica sur": "Clínica Sur"}


def test_raw_sov_per_app(rows):
    res = cb.count(rows, ALIASES)
    assert res["apps"]["chatgpt"]["valid"] == 4
    assert res["apps"]["chatgpt"]["mentions"] == 1
    assert res["apps"]["chatgpt"]["sov"] == pytest.approx(0.25)
    assert res["apps"]["chatgpt"]["excluded"] == 1
    assert res["apps"]["gemini"]["sov"] == pytest.approx(1.0)


def test_sov_per_pass(rows):
    res = cb.count(rows, ALIASES)
    assert res["apps"]["chatgpt"]["by_pass"] == {"p1": pytest.approx(0.5), "p2": pytest.approx(0.0)}


def test_weighted_sov_chatgpt_gemini_normalised(rows):
    res = cb.count(rows, ALIASES)
    assert res["weighted"] == pytest.approx((0.25 * 0.55 + 1.0 * 0.25) / 0.80)


def test_weighted_normalises_to_apps_with_valid_answers(rows):
    only_chatgpt = [r for r in rows if r["app"] != "gemini"]
    assert cb.count(only_chatgpt, ALIASES)["weighted"] == pytest.approx(0.25)


def test_mean_position(rows):
    res = cb.count(rows, ALIASES)
    assert res["apps"]["gemini"]["mean_position"] == pytest.approx(1.5)
    assert res["apps"]["chatgpt"]["mean_position"] == pytest.approx(1.0)


def test_clinics_in_its_place_are_canonicalised(rows):
    res = cb.count(rows, ALIASES)
    # answers without the clinic, per app: who appears instead (answers naming each)
    assert res["apps"]["chatgpt"]["instead"] == {"Clínica Sur": 3, "Centro Oeste": 1}


def test_google_ai_overviews_apart(rows):
    g = cb.count(rows, ALIASES)["google"]
    assert g["searches"] == 3 and g["with_overview"] == 2 and g["mentions"] == 1
    assert g["sov_all"] == pytest.approx(1 / 3)
    assert g["sov_with_overview"] == pytest.approx(1 / 2)


def test_google_never_weighted(rows):
    res = cb.count(rows, ALIASES)
    assert "google" not in res["apps"]


def test_top_domains(rows):
    res = cb.count(rows, ALIASES)
    assert res["domains"][0] == ("doctoralia.es", 3)


def test_observation_and_brand_rows_apart(rows):
    res = cb.count(rows, ALIASES)
    assert {o["key"] for o in res["observations"]} == {("chatgpt", "pago"), ("claude", "gratuito")}
    assert [r["id_pregunta"] for r in res["brand_rows"]] == ["AM01"]


def test_stability_per_question(rows):
    res = cb.count(rows, ALIASES)
    assert res["stability"][("chatgpt", "AV01")] == (1, 2)
    assert res["stability"][("gemini", "AV01")] == (2, 2)


def test_duplicate_rows_fail_loudly(rows):
    with pytest.raises(ValueError, match="duplicada"):
        cb.count(rows + [rows[0]], ALIASES)


def test_mention_flag_must_be_filled_on_valid_rows(rows):
    rows[0]["artica_nombrada"] = ""
    with pytest.raises(ValueError, match="artica_nombrada"):
        cb.count(rows, ALIASES)


def test_adjective_flag_is_reported(rows):
    rows[0]["observaciones"] = "#artica-adjetivo"
    assert cb.count(rows, ALIASES)["adjective_flags"] == 1


def test_render_is_markdown_with_all_sections(rows):
    md = cb.render(cb.count(rows, ALIASES), sources=["p1.csv", "p2.csv"])
    for heading in ("Por app", "ponderado", "Google", "Dominios", "Estabilidad",
                    "Observaciones", "Preguntas de marca"):
        assert heading in md


def test_reads_csv_files(tmp_path, rows):
    p = tmp_path / "p1.csv"
    with open(p, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=bd.TEMPLATE_COLUMNS)
        w.writeheader()
        w.writerows(rows)
    assert len(cb.read_rows([p])) == len(rows)


def test_alias_file(tmp_path):
    p = tmp_path / "alias.csv"
    p.write_text("alias,canonico\nSur Estética,Clínica Sur\n", encoding="utf-8")
    assert cb.read_aliases(p) == {"sur estetica": "Clínica Sur"}


def test_doctor_without_clinic_flag_is_reported_apart(rows):
    """P-2 (human, 2026-09-29): the doctor's name without the clinic is not a mention;
    it is tagged in observaciones and reported apart."""
    rows[1]["observaciones"] = "#medica-sin-clinica"
    res = cb.count(rows, ALIASES)
    assert res["doctor_only_flags"] == 1
    assert res["apps"]["chatgpt"]["mentions"] == 1   # unchanged: not a mention
    assert "#medica-sin-clinica" in cb.render(res, sources=["p1.csv"])


def test_rows_from_another_municipality_are_location_sensitivity_observations(rows):
    """P-4 revised (2026-09-29): the pilot measures from Vilaboa. Google/Maps rows taken
    elsewhere (e.g. Viveiro) are a location-sensitivity observation, never counted, and do
    not collide with the main row of the same question."""
    extra = dict(rows[7])          # p1 AV01 google, mention
    extra.update(municipio="Viveiro", artica_nombrada="no", resumen_ia="si")
    res = cb.count(rows + [extra], ALIASES)
    assert res["google"]["searches"] == 3 and res["google"]["mentions"] == 1
    assert res["location_sensitivity"] == [
        {"municipio": "Viveiro", "app": "google", "mentions": 0, "valid": 1}]
    assert "sensibilidad a la ubicación" in cb.render(res, sources=["p1.csv"])


def test_main_municipality_is_vilaboa():
    assert cb.MAIN_MUNICIPIO == "Vilaboa"


# ------------------------------------------------ amendment 2026-09-29: levels AR / AG (ADR-005)
@pytest.fixture
def level_rows():
    return [
        # AR01 chatgpt: clinic in both passes -> stable cell
        row("p1", "AR01", "chatgpt", "si", clinics="Clínica Norte;Clínica Lejana", pos="1",
            domains="doctoralia.es"),
        row("p2", "AR01", "chatgpt", "si", clinics="Clínica Lejana;Clínica Norte", pos="2"),
        # AR01 gemini: only p1
        row("p1", "AR01", "gemini", "si", clinics="Clínica Norte", pos="1"),
        row("p2", "AR01", "gemini", "no", clinics="Cadena Sede Ferrol"),
        # AR02 google: overview with clinic in both passes -> stable cell
        row("p1", "AR02", "google", "si", resumen="si", clinics="Clínica Norte", pos="1"),
        row("p2", "AR02", "google", "si", resumen="si", clinics="Clínica Norte", pos="1"),
        row("p1", "AR03", "google", "no", resumen="no"),
        # AG: never
        row("p1", "AG01", "chatgpt", "no", clinics="Cadena Sede Vigo;Clínica Lejana",
            domains="topdoctors.es"),
        row("p2", "AG01", "chatgpt", "no", clinics="Cadena Sede Coruña"),
        row("p1", "AG01", "google", "no", resumen="si", clinics="Clínica Lejana"),
        # paid plan in a level: observation, not counted
        row("p1", "AG02", "chatgpt", "si", plan="pago", clinics="Clínica Norte", pos="1"),
    ]


CHAIN = dict(ALIASES, **{"cadena sede ferrol": "Cadena", "cadena sede vigo": "Cadena",
                         "cadena sede coruna": "Cadena"})


def test_core_unchanged_when_level_rows_removed(rows, level_rows):
    with_levels = cb.count(rows + level_rows, CHAIN)
    without = cb.count(rows, CHAIN)
    for key in ("apps", "weighted", "google", "domains", "stability"):
        assert with_levels[key] == without[key], key


def test_level_counts_per_app_and_pass(rows, level_rows):
    ar = cb.count(rows + level_rows, CHAIN)["levels"]["AR"]
    assert ar["apps"]["chatgpt"]["by_pass"] == {"p1": (1, 1), "p2": (1, 1)}
    assert ar["apps"]["gemini"]["by_pass"] == {"p1": (1, 1), "p2": (0, 1)}
    assert ar["apps"]["google"]["by_pass"] == {"p1": (1, 2), "p2": (1, 1)}
    assert ar["apps"]["google"]["with_overview"] == 2   # p1 AR02, p2 AR02


def test_level_positions_are_listed_not_averaged(rows, level_rows):
    ar = cb.count(rows + level_rows, CHAIN)["levels"]["AR"]
    assert ar["apps"]["chatgpt"]["positions"] == [1, 2]


def test_regularity_definition_ar(rows, level_rows):
    ar = cb.count(rows + level_rows, CHAIN)["levels"]["AR"]
    assert sorted(ar["stable_cells"]) == [("chatgpt", "AR01"), ("google", "AR02")]
    assert ar["indicator"] is True          # >= 2 stable cells


def test_regularity_needs_two_stable_cells(rows, level_rows):
    fewer = [r for r in level_rows if not (r["id_pregunta"] == "AR02")]
    assert cb.count(rows + fewer, CHAIN)["levels"]["AR"]["indicator"] is False


def test_galicia_indicator_is_at_least_once(rows, level_rows):
    res = cb.count(rows + level_rows, CHAIN)
    assert res["levels"]["AG"]["indicator"] is False       # paid-plan row does not count
    level_rows[7]["artica_nombrada"] = "si"
    assert cb.count(rows + level_rows, CHAIN)["levels"]["AG"]["indicator"] is True


def test_chains_are_one_brand_in_levels(rows, level_rows):
    ag = cb.count(rows + level_rows, CHAIN)["levels"]["AG"]
    assert ag["instead"] == {"Clínica Lejana": 2, "Cadena": 2}
    assert ag["domains"] == [("topdoctors.es", 1)]


def test_render_levels_as_counts_without_percentages(rows, level_rows):
    md = cb.render(cb.count(rows + level_rows, CHAIN), sources=["p1.csv"])
    for heading in ("## Área de influencia (AR)", "## Galicia (AG)"):
        section = md.split(heading, 1)[1].split("\n## ", 1)[0]
        assert "%" not in section
        assert " de " in section
