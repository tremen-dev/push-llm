"""CA-6: casos límite del matching según el dictamen de sdd-metricas (ledger)."""
import pytest

import matching

BRANDS = matching.load_brands()


def names(text, specialty=None, city=None):
    return [b["brand"] for b in matching.find_mentions(text, BRANDS, specialty, city)]


# SPEC-001 afirmaba aquí que "IVI" solo no cuenta (RN-01). ADR-002 / RN-11 lo sustituye:
# IVI es sigla corta inequívoca de IVI Vigo (ver CA-3 y CA-4 de SPEC-006 más abajo).

def test_ivi_vigo_counts_via_brand_name():
    assert names("La referencia es IVI Vigo.", "fertility", "Vigo") == ["IVI Vigo"]


def test_short_alias_hits_are_reported_when_brand_not_counted():
    # ADR-002: "IVI" en mayúsculas ya cuenta; "ivi" en minúsculas no, y sigue siendo sesgo.
    text = "Te recomiendo ivi o MIA."
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


# ---------- SPEC-006 (ADR-002 / RN-11): siglas cortas inequívocas ----------

HEADER = "specialty,brand,city,type,aliases,exact_aliases\n"


def write_csv(tmp_path, body, header=HEADER):
    p = tmp_path / "brands.csv"
    p.write_text(header + body, encoding="utf-8")
    return p


def test_spec006_ca1_catalog_exact_aliases_only_ivi():
    by_brand = {b["brand"]: b for b in BRANDS}
    assert {b["brand"]: b["exact_aliases"] for b in BRANDS if b["exact_aliases"]} == {
        "IVI Vigo": ["IVI"]}
    ivi_aliases = [a.strip() for a in by_brand["IVI Vigo"]["aliases"].split(";")]
    assert "IVI" not in ivi_aliases and "IVIRMA" in ivi_aliases
    assert "MIA" in [a.strip() for a in by_brand["Clínica MIA"]["aliases"].split(";")]
    assert by_brand["Clínica MIA"]["exact_aliases"] == []


@pytest.mark.parametrize("bad", ["Ivi", "IVIR", "I", "IV I", "ÍVI"])
def test_spec006_ca2_invalid_form_rejected(tmp_path, bad):
    p = write_csv(tmp_path, f"fertility,Marca X,Vigo,independent,Marca Equis,{bad}\n")
    with pytest.raises(ValueError) as e:
        matching.load_brands(p)
    assert "Marca X" in str(e.value) and bad in str(e.value)


def test_spec006_ca2_sigla_repeated_in_other_brand_exact_aliases(tmp_path):
    p = write_csv(tmp_path, "fertility,Marca X,Vigo,independent,Marca Equis,ABC\n"
                            "dental,Marca Y,Vigo,independent,Marca Ye,ABC\n")
    with pytest.raises(ValueError) as e:
        matching.load_brands(p)
    assert "Marca Y" in str(e.value) and "ABC" in str(e.value)


def test_spec006_ca2_sigla_repeated_as_alias_of_other_brand(tmp_path):
    p = write_csv(tmp_path, "fertility,Marca X,Vigo,independent,Marca Equis,ABC\n"
                            "dental,Marca Y,Vigo,independent,abc;Marca Ye,\n")
    with pytest.raises(ValueError) as e:
        matching.load_brands(p)
    assert "Marca X" in str(e.value) and "ABC" in str(e.value)


def test_spec006_ca2_csv_without_exact_aliases_column_still_loads(tmp_path):
    p = write_csv(tmp_path, "dental,Marca X,Vigo,independent,Marca Equis\n",
                  header="specialty,brand,city,type,aliases\n")
    rows = matching.load_brands(p)
    assert rows[0]["exact_aliases"] == []
    assert names_in("Marca Equis", rows) == ["Marca X"]


def names_in(text, brands, specialty=None, city=None):
    return [b["brand"] for b in matching.find_mentions(text, brands, specialty, city)]


@pytest.mark.parametrize("text", ["Te recomiendo IVI, es la mejor.", "Opciones: (IVI) y NIDA",
                                  "IVI-RMA en Vigo", "Mira IVI."])
def test_spec006_ca3_ivi_uppercase_whole_word_counts(text):
    assert "IVI Vigo" in names(text, "fertility", "Vigo")


@pytest.mark.parametrize("text", ["te recomiendo ivi", "Ivi es buena", "IVIS", "XIVI", "IVI2",
                                  "ÁIVI", "IVIñ"])
def test_spec006_ca3_ivi_not_counted_when_case_or_word_differs(text):
    assert "IVI Vigo" not in names(text, "fertility", "Vigo")


def test_spec006_ca4_mia_still_does_not_count():
    # ADR-002 §5: MIA queda fuera de la excepción ("mía").
    assert names("Te recomiendo MIA", "aesthetic", "Vigo") == []


def test_spec006_ca4_brand_name_and_sigla_count_once():
    assert names("IVI Vigo, también conocida como IVI", "fertility", "Vigo") == ["IVI Vigo"]


def test_spec006_ca4_sigla_keeps_first_appearance_order():
    assert names("Opciones: (IVI) y NIDA", "fertility", "Vigo") == ["IVI Vigo", "Clínica NIDA"]
    assert names("Clínica NIDA o bien IVI.", "fertility", "Vigo") == ["Clínica NIDA", "IVI Vigo"]
