"""CA-4 (errores fuera del denominador) y CA-5 (análisis offline) con cifras a mano."""
import csv

import pytest

import analysis
import matching
import settings

CFG = settings.load_config()
BRANDS = matching.load_brands()


def row(pid, spec, provider, run, status, answer, city="Vigo"):
    return {"prompt_id": pid, "specialty": spec, "city": city, "provider": provider,
            "run": str(run), "status": status, "answer": answer}


FIXTURE = [
    # dental
    row("D01", "dental", "openai", 1, "ok", "Te recomiendo Clínica Torres y Vitaldent."),
    row("D01", "dental", "openai", 2, "ok", "Busca en Doctoralia."),
    row("D01", "dental", "openai", 3, "error", "[error] RateLimitError: Clínica Bastida"),
    row("D01", "dental", "claude", 1, "ok", "Clínica Torres, Clínica Torres otra vez; mira Top Doctors"),
    row("D01", "dental", "claude", 2, "refusal", "No puedo recomendar Clínica Bastida"),
    row("D01", "dental", "gemini", 1, "ok", "No conozco ninguna."),
    row("D01", "dental", "gemini", 2, "empty", ""),
    # fertility
    row("F01", "fertility", "openai", 1, "ok", "IVI Vigo es la referencia, también IVI."),
    row("F01", "fertility", "openai", 2, "ok", "IVI es la mejor opción."),  # counts: RN-11/ADR-002
    row("F01", "fertility", "claude", 1, "ok", "Clínica NIDA y reproduccionasistida.org"),
    # aesthetic / ophthalmology: shared alias "Villoria"
    row("E01", "aesthetic", "openai", 1, "ok", "Villoria."),
    row("E01", "aesthetic", "openai", 2, "ok", "Te recomiendo MIA."),  # MIA: bias, not a mention
    row("O01", "ophthalmology", "openai", 1, "ok",
        "Clínica Villoria es la referencia; Villoria opera también en Pontevedra."),
]


@pytest.fixture(scope="module")
def result():
    return analysis.analyze(FIXTURE, BRANDS, CFG)


# ---------- CA-4 ----------

def test_ca4_non_ok_rows_out_of_numerator_and_denominator(result):
    c = result["cells"]
    assert (c["dental", "openai"]["valid"], c["dental", "openai"]["with_clinic"]) == (2, 1)
    assert (c["dental", "claude"]["valid"], c["dental", "claude"]["with_clinic"]) == (1, 1)
    assert (c["dental", "gemini"]["valid"], c["dental", "gemini"]["with_clinic"]) == (1, 0)


def test_ca4_excluded_counts_by_provider_and_specialty(result):
    c = result["cells"]
    assert c["dental", "openai"]["excluded"] == {"error": 1}
    assert c["dental", "claude"]["excluded"] == {"refusal": 1}
    assert c["dental", "gemini"]["excluded"] == {"empty": 1}
    assert c["fertility", "openai"]["excluded"] == {}


def test_ca4_summary_shows_excluded_counts(result, tmp_path):
    md = analysis.render_summary(result, CFG)
    assert "error: 1" in md and "refusal: 1" in md and "empty: 1" in md


# ---------- CA-5 ----------

def test_ca5_coverage_percentages(result):
    c = result["cells"]
    assert c["dental", "openai"]["pct"] == pytest.approx(0.5)
    assert c["dental", "claude"]["pct"] == pytest.approx(1.0)
    assert c["dental", "gemini"]["pct"] == pytest.approx(0.0)
    # SPEC-006: "IVI" alone now counts (RN-11/ADR-002) -> 2/2 (was 1/2 under SPEC-001)
    assert c["fertility", "openai"]["pct"] == pytest.approx(1.0)


def test_ca5_weighted_aggregate_normalised_to_probed_providers(result):
    # dental: (0.5*0.55 + 1.0*0.10 + 0.0*0.25) / (0.55+0.10+0.25)
    assert result["weighted"]["dental"] == pytest.approx(0.375 / 0.90)
    # fertility: gemini not probed -> (1.0*0.55 + 1.0*0.10) / (0.55+0.10) = 1.0 (SPEC-006)
    assert result["weighted"]["fertility"] == pytest.approx(0.65 / 0.65)


def test_ca5_leader_per_specialty(result):
    L = result["leaders"]
    assert L["dental"] == {"brands": ["Clínica Torres"], "count": 2, "valid": 4, "pct": 0.5}
    # SPEC-006: IVI Vigo named in 2 of 3 valid fertility answers (was a 1-1 tie with NIDA)
    assert L["fertility"]["brands"] == ["IVI Vigo"]
    assert L["fertility"]["count"] == 2 and L["fertility"]["pct"] == pytest.approx(2 / 3)
    assert L["aesthetic"]["brands"] == ["Clínica Villoria L'Essence"]
    assert L["ophthalmology"] == {"brands": ["Clínica Villoria"], "count": 1, "valid": 1, "pct": 1.0}


def test_ca5_directory_distribution(result):
    assert result["directories"]["dental"] == {"Doctoralia": 1, "Top Doctors": 1}
    assert result["directories"]["fertility"] == {"reproduccionasistida.org": 1}


def test_ca6_short_alias_bias_reported(result):
    # SPEC-006: "IVI" now counts, so fertility has no bias left; "MIA" still does not.
    assert result["short_alias"].get("fertility", 0) == 0
    assert result["short_alias"]["aesthetic"] == 1
    assert result["short_alias"].get("dental", 0) == 0


# ---------- SPEC-006 CA-5 ----------

def test_spec006_ca5_ivi_alone_counts_and_mia_alone_is_bias():
    rows = [row("F01", "fertility", "openai", 1, "ok", "IVI es la mejor opción."),
            row("E01", "aesthetic", "openai", 1, "ok", "Te recomiendo MIA.")]
    res = analysis.analyze(rows, BRANDS, CFG)
    assert res["cells"]["fertility", "openai"]["with_clinic"] == 1
    assert res["leaders"]["fertility"]["brands"] == ["IVI Vigo"]
    assert res["short_alias"].get("fertility", 0) == 0
    assert res["cells"]["aesthetic", "openai"]["with_clinic"] == 0
    assert res["short_alias"]["aesthetic"] == 1


def test_spec006_ca5_summary_lists_active_exact_aliases(result):
    md = analysis.render_summary(result, CFG)
    lines = md.splitlines()
    bias = next(i for i, l in enumerate(lines) if l.startswith("## Sesgo RN-01"))
    active = next(i for i, l in enumerate(lines) if "IVI → IVI Vigo" in l)
    assert "RN-11" in lines[active] and "ADR-002" in lines[active]
    assert 0 < active - bias <= 3  # right next to the short-alias bias section


def test_ca5_recomputes_from_text_ignoring_stored_mention_columns():
    rows = [dict(FIXTURE[1], brands_mentioned="Clínica Torres")]  # stale column
    res = analysis.analyze(rows, BRANDS, CFG)
    assert res["cells"]["dental", "openai"]["with_clinic"] == 0


def test_ca5_render_summary_contains_tables(result):
    md = analysis.render_summary(result, CFG)
    assert "| dental | openai | 2 | 1 | 50.0 %" in md
    assert "41.7 %" in md  # weighted dental
    assert "Clínica Torres" in md and "Doctoralia" in md


def test_read_results_roundtrip(tmp_path):
    path = tmp_path / "results.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(FIXTURE[0]))
        w.writeheader()
        w.writerows(FIXTURE)
    assert analysis.read_results(path) == FIXTURE


def test_cost_totals_per_provider_from_rows():
    rows = [dict(FIXTURE[0], cost_eur="0.10"), dict(FIXTURE[2], cost_eur="0.05"),
            dict(FIXTURE[3], cost_eur="0.20")]
    res = analysis.analyze(rows, BRANDS, CFG)
    assert res["cost_eur"] == {"openai": pytest.approx(0.15), "claude": pytest.approx(0.20)}
    assert "| total | 0.35 |" in analysis.render_summary(res, CFG)
