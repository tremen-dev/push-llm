"""CA-6: casos límite del matching según el dictamen de sdd-metricas (ledger)."""
import pytest

import matching

BRANDS = matching.load_brands()


def names(text, specialty=None, city=None):
    return [b["brand"] for b in matching.find_mentions(text, BRANDS, specialty, city)]


def test_short_alias_alone_does_not_count_rn01():
    assert names("Te recomiendo IVI, es la mejor.", "fertility", "Vigo") == []


def test_ivi_vigo_counts_via_brand_name():
    assert names("La referencia es IVI Vigo.", "fertility", "Vigo") == ["IVI Vigo"]


def test_short_alias_hits_are_reported_when_brand_not_counted():
    text = "Te recomiendo IVI o MIA."
    matched = matching.find_mentions(text, BRANDS, "fertility", "Vigo")
    assert matching.short_alias_hits(text, BRANDS, matched) == ["IVI Vigo", "Clínica MIA"]


def test_short_alias_hit_not_reported_when_brand_already_counted():
    text = "IVI Vigo, también conocida como IVI."
    matched = matching.find_mentions(text, BRANDS, "fertility", "Vigo")
    assert matching.short_alias_hits(text, BRANDS, matched) == []


def test_shared_alias_villoria_in_aesthetic_answer():
    assert names("Para bótox, Villoria.", "aesthetic", "Vigo") == ["Clínica Villoria L'Essence"]


def test_shared_alias_villoria_in_ophthalmology_answer():
    assert names("Para cataratas, Villoria.", "ophthalmology", "Vigo") == ["Clínica Villoria"]


def test_shared_alias_resolved_by_city_within_specialty():
    assert names("Vitaldent tiene buenos precios.", "dental", "Pontevedra") == ["Vitaldent Pontevedra"]


def test_shared_alias_without_matching_specialty_keeps_all_candidates():
    assert sorted(names("Povisa es un buen hospital.", "hospital", "Vigo")) == [
        "Ribera Povisa", "Ribera Povisa Oftalmología"]


def test_longer_overlapping_name_wins():
    assert names("Clínica Villoria L'Essence en Vigo.", "ophthalmology", "Vigo") == [
        "Clínica Villoria L'Essence"]


def test_brand_repeated_counts_once_per_answer():
    assert names("Clínica Torres. Repito: Clínica Torres. clinica torres!", "dental", "Vigo") == [
        "Clínica Torres"]


def test_order_is_first_appearance():
    assert names("Primero Clínica Bastida, luego Clínica Torres y Doctoralia.", "dental", "Vigo") == [
        "Clínica Bastida", "Clínica Torres", "Doctoralia"]


def test_accent_and_case_insensitive_whole_words():
    assert names("GRANDIO PAZOS", "dental", "Vigo") == ["Clínica Dental Grandío Pazos"]
    assert names("Torresvigo no es una marca", "dental", "Vigo") == []


@pytest.mark.parametrize("brand,expected", [("Clínica Torres", True), ("Doctoralia", False),
                                            ("IVI Vigo", True)])
def test_is_local_clinic(brand, expected):
    b = next(x for x in BRANDS if x["brand"] == brand)
    assert matching.is_local_clinic(b) is expected
