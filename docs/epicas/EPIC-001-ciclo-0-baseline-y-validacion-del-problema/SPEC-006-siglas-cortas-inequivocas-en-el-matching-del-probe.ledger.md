---
id: SPEC-006
tipo: ledger
epica: EPIC-001
---
# Ledger — SPEC-006 Siglas cortas inequívocas en el matching del probe

## Resumen
- Fase: en-revision <!-- refleja el estado de la spec; la fuente de verdad es el frontmatter de la spec -->
- Rama: `ft/SPEC-006-siglas-cortas-inequivocas-en-el-matching-del-probe`

## Matriz de criterios de aceptación
<!-- Escritores: sdd-implementador rellena Implementado y Test; sdd-verificador rellena Verif. y Estado. Nunca al revés. -->
<!-- Estados por CA: ✅ cerrado · ⚠️ parcial/con salvedad · 🚧 en curso · ❌ sin empezar · n-a -->
<!-- Un CA está ✅ solo cuando Implementado + Test + Verif. aplicables están en verde. Una salvedad se marca ⚠️, nunca ✅. -->
| CA | Implementado (fichero) | Test (fichero/caso) | Verif. | Estado |
|---|---|---|---|---|
| CA-0 | Dictamen sdd-metricas en este ledger (Notas); ADR-002 `estado: aprobada` | n-a (evidencia documental: sección Notas + frontmatter de ADR-002) | | ❌ |
| CA-1 | `probe/brands.csv` (columna `exact_aliases`; IVI Vigo `aliases=IVIRMA`, `exact_aliases=IVI`; Clínica MIA conserva `MIA` en `aliases`), `probe/matching.py` (`load_brands`, `_exact_aliases`) | `probe/tests/test_matching.py::test_spec006_ca1_catalog_exact_aliases_only_ivi` | | ❌ |
| CA-2 | `probe/matching.py` (`_check_exact_aliases`, `EXACT_ALIAS_RE`; compatibilidad con `row.get`) | `test_matching.py::test_spec006_ca2_invalid_form_rejected[Ivi,IVIR,I,IV I,ÍVI]`, `::test_spec006_ca2_sigla_repeated_in_other_brand_exact_aliases`, `::test_spec006_ca2_sigla_repeated_as_alias_of_other_brand`, `::test_spec006_ca2_csv_without_exact_aliases_column_still_loads` | | ❌ |
| CA-3 | `probe/matching.py` (`_exact_occurrences`: regex sensible a mayúsculas con fronteras `(?<![^\W_])…(?![^\W_])` sobre el texto original; integrado en `find_mentions`) | `test_matching.py::test_spec006_ca3_ivi_uppercase_whole_word_counts` (4 textos del CA) y `::test_spec006_ca3_ivi_not_counted_when_case_or_word_differs` (5 textos del CA + `ÁIVI`, `IVIñ`) | | ❌ |
| CA-4 | `probe/matching.py` (las ocurrencias de sigla entran en la regla de solapes y la deduplicación; posición traducida a coordenadas del texto normalizado) | `test_matching.py::test_spec006_ca4_mia_still_does_not_count`, `::test_spec006_ca4_brand_name_and_sigla_count_once`, `::test_spec006_ca4_sigla_keeps_first_appearance_order`; test SPEC-001 `test_short_alias_alone_does_not_count_rn01` sustituido por comentario con referencia a ADR-002; `test_short_alias_hits_are_reported_when_brand_not_counted` pasa a usar `ivi` en minúsculas; resto de SPEC-001 sin cambios | | ❌ |
| CA-5 | `probe/analysis.py` (`analyze` devuelve `exact_aliases`; `render_summary` añade la línea «Siglas cortas que sí cuentan (RN-11/ADR-002…): IVI → IVI Vigo» bajo el título de la sección de sesgo, cuyo ejemplo pasa a "MIA") | `test_analysis.py::test_spec006_ca5_ivi_alone_counts_and_mia_alone_is_bias`, `::test_spec006_ca5_summary_lists_active_exact_aliases`; fixture de SPEC-001 recalculado (ver Notas: recálculo a mano) en `test_ca5_coverage_percentages`, `test_ca5_weighted_aggregate_normalised_to_probed_providers`, `test_ca5_leader_per_specialty`, `test_ca6_short_alias_bias_reported` | | ❌ |
| CA-6 | `probe/run_probe.py` sin cambios (usa `matching.find_mentions`) | `test_run_probe.py::test_spec006_ca6_ivi_alone_goes_to_brands_mentioned` (falla con `matching.py`/`brands.csv` anteriores, comprobado) | | ❌ |
| CA-7 | `probe/README.md` (sección *Brand matching (RN-01, RN-11)* y descripción de `summary.md`), docstring de `probe/matching.py` | `python -m pytest probe/tests` → 94 passed (2026-09-24, sin claves ni red: 0 variables `*API_KEY*` en el entorno); `ruff check probe` → All checks passed | | ❌ |

## Veredicto del verificador
<!-- GREEN/RED + fecha + resumen. Lo escribe SOLO sdd-verificador. -->

## Evidencia visual
<!-- Tabla CA → captura en _qa/SPEC-006/. Informe HTML opcional: _qa/SPEC-006/informe.html -->

## Notas

### Dictamen sdd-metricas (2026-09-24) — ADR-002 reglas 1–5 (CA-0)
Emitido por sdd-implementador aplicando `.ai-context/skills/sdd-metricas.md`.
Veredicto global: **correcto**. Nada de lo que sigue cambia la regla ni el ADR; las notas
son de implementación o de documentación. Invariantes: RN-01, RN-02, RN-03, RN-06, RN-11,
D-6. Fuentes: `docs/fundacion/reglas.md` (RN-01, RN-11), `docs/fundacion/dominio.md`
(Mention), dictamen sdd-metricas de SPEC-001 (puntos 3–5), ADR-002.

1. **Definición de sigla corta inequívoca (§1)** — *correcto*. Los cuatro requisitos
   preservan el objetivo de RN-01 (evitar falsos positivos con palabras comunes) y (d)
   mantiene la atribución a una sola marca, así que una sigla nunca pasa por la resolución
   de alias compartidos (punto 4 del dictamen de SPEC-001). Para `IVI`: (b) es la forma con
   la que la marca se nombra públicamente (IVI / IVIRMA); (c) "ivi" no es palabra en
   castellano ni gallego ni sigla sanitaria de uso general (la de interrupción del
   embarazo es IVE); (d) ninguna otra marca de `brands.csv` la usa.
2. **Marcado en catálogo (§2)** — *correcto*. La sigla es dato de la marca; fallar al cargar
   si incumple (a) o (d) evita contar siglas no juzgadas en silencio.
3. **Comparación (§3)** — *correcto*. Sensible a mayúsculas y por palabra completa sobre el
   texto original; "palabra completa" debe tratar como letra cualquier letra Unicode
   (acentuada incluida) y los dígitos, y como frontera todo lo demás (espacio, puntuación,
   guion, paréntesis). Así "IVI-RMA" y "(IVI)" cuentan e "IVIS", "XIVI", "IVI2", "ÁIVI" no.
4. **Qué cuenta (§4)** — *correcto*. Una coincidencia de sigla es una Mention a efectos de
   cobertura (RN-02), agregado ponderado (RN-03) y líder. Nota de implementación: la
   ocurrencia de sigla debe entrar en la misma deduplicación por marca (punto 5 de SPEC-001)
   y en la regla de solapes (punto 4): si está contenida en un nombre más largo que también
   coincide ("IVI" dentro de "IVI Vigo"), cuenta la larga; el resultado es la misma marca
   una sola vez. El orden de aparición (RN-06, Position) no se calcula en Ciclo 0; basta con
   que el orden sea determinista.
5. **Alcance (§5)** — *correcto*. `MIA` incumple (c) ("mía"); en mayúsculas de énfasis o
   título sería falso positivo. Debe seguir sin contar y seguir apareciendo en el recuento
   de sesgo de `summary.md`. Ese recuento debe seguir incluyendo también las apariciones de
   `IVI` que no cuentan (minúsculas o capitalizada, p. ej. "ivi", "Ivi"), porque ADR-002
   (Consecuencias) confía en él para medir el acierto perdido.

Specs/documentos a revisar (sin bloquear): `docs/fundacion/dominio.md` (entidad Mention)
solo cita el umbral de ≥ 4 caracteres y no la excepción RN-11 → F-SPEC-006-1. El texto de
RN-01/RN-11 en `reglas.md` aún dice "ADR-002 en borrador" aunque ADR-002 está aprobada →
F-SPEC-006-2. SPEC-002 (veredicto) debe anotar la limitación "IVI cadena → IVI Vigo".

### Recálculo a mano del fixture de SPEC-001 (CA-5, 2026-09-24)
Cambio: la fila F01/openai/2 "IVI es la mejor opción." pasa a contar (RN-11); se añade la fila
E01/openai/2 "Te recomiendo MIA." (MIA sigue sin contar).
- fertility × openai: 2 válidas, 2 con clínica local → **100 %** (antes 1/2 = 50 %).
- fertility × claude: 1/1 = 100 % (sin cambio).
- fertility ponderado: (1,0 × 0,55 + 1,0 × 0,10) / (0,55 + 0,10) = 0,65 / 0,65 = **100 %** (antes 0,375/0,65 = 57,7 %).
- Líder fertility: IVI Vigo en 2 de 3 respuestas válidas → **IVI Vigo, 2, 66,7 %** (antes empate NIDA/IVI Vigo 1/3).
- Sesgo alias cortos: fertility **0** (antes 1); aesthetic **1** (fila MIA).
- aesthetic × openai: 2 válidas, 1 con clínica local (50 %); líder sigue siendo Clínica Villoria L'Essence.
- dental, ophthalmology y directorios: sin cambio (41,7 % ponderado dental).

## Salvedades / follow-ups
<!-- IDs F-SPEC-006-1, F-SPEC-006-2… con destino (spec futura o EPIC-MEJORA). -->
- **F-SPEC-006-1** (drift de dominio): `docs/fundacion/dominio.md`, entidad Mention, no menciona la excepción RN-11 (siglas cortas). Destino: sdd-arquitecto / humano (documento de verdad, no lo edita el implementador).
- **F-SPEC-006-2** (drift de reglas): RN-01 y RN-11 en `docs/fundacion/reglas.md` dicen "ADR-002 en borrador"; ADR-002 está `aprobada`. Destino: sdd-arquitecto / humano.
- **F-SPEC-006-4** (validación no pedida por los CA): `load_brands` no rechaza que una sigla de `exact_aliases` figure también en `aliases` de su propia marca (ADR-002 §2 lo prohíbe como convención del catálogo; CA-2 solo exige forma y exclusividad entre marcas). El catálogo actual lo cumple (test CA-1). Destino: spec futura si se quiere forzar.
- **F-SPEC-006-5** (limitación de juicio, ya en ADR-002): "IVI" de la cadena se atribuye a IVI Vigo; y una sigla en mayúsculas de énfasis ("MIA") no cuenta por diseño. Destino: veredicto de SPEC-002 (CA-5).
- **F-SPEC-006-3** (historial): en SPEC-006 y ADR-002 la entrada `aprobada` (2026-09-23) tiene fecha anterior a la de `borrador` (2026-09-24). No afecta al código; revisar fechas. Destino: sdd-arquitecto / humano.

## Cómo retomar (handoff)
<!-- Estado real del trabajo para la siguiente sesión: qué está hecho, qué falta, dónde seguir. -->
- 2026-09-24, sdd-implementador: CA-0…CA-7 implementados en la rama `ft/SPEC-006-siglas-cortas-inequivocas-en-el-matching-del-probe` (commits 943ff93, 235e184, 1a956b4, a6b78f4 y el de cierre; sin push). Spec en `en-revision`. Pendiente: verificación (sdd-verificador).
- Verificar: `python -m pytest probe/tests` desde la raíz (94 passed); `python -m pytest probe/tests -k spec006 -v`; `ruff check probe`. No hace falta ninguna clave ni red; no se ha ejecutado el probe contra proveedores.
