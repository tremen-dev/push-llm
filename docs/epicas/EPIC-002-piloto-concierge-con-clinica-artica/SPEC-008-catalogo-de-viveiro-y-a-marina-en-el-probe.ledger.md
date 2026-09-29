---
id: SPEC-008
tipo: ledger
epica: EPIC-002
---
# Ledger — SPEC-008 Catálogo de Viveiro y A Mariña en el probe

## Resumen
- Fase: <!-- refleja el estado de la spec; la fuente de verdad es el frontmatter de la spec -->
- Rama: `ft/SPEC-008-catalogo-de-viveiro-y-a-marina-en-el-probe` (CA-1…CA-8, sale de
  `ft/SPEC-007-…`). Enmienda (b), CA-9/CA-10 y baseline oficial:
  `ft/SPEC-008-baseline-oficial`, apilada sobre `ft/SPEC-013-…` (PR #4), sin push.

## Matriz de criterios de aceptación
<!-- Escritores: sdd-implementador rellena Implementado y Test; sdd-verificador rellena Verif. y Estado. Nunca al revés. -->
<!-- Estados por CA: ✅ cerrado · ⚠️ parcial/con salvedad · 🚧 en curso · ❌ sin empezar · n-a -->
<!-- Un CA está ✅ solo cuando Implementado + Test + Verif. aplicables están en verde. Una salvedad se marca ⚠️, nunca ✅. -->
| CA | Implementado (fichero) | Test (fichero/caso) | Verif. | Estado |
|---|---|---|---|---|
| CA-1 | `probe/prompts.csv`: `AV01`–`AV15`, `AR01`–`AR05`, `AG01`–`AG04` (24), texto literal e intent de `docs/piloto-artica/prompts-baseline.md`, `specialty=aesthetic`, `city=Viveiro`; sin `AM`; sin columna nueva. Dependencia: el set aún no tiene fecha de congelación (ver "Dependencias") | `probe/tests/test_pilot_batch.py::test_ca1_pilot_prompts_equal_to_frozen_set_id_and_literal_text`, `::test_ca1_brand_questions_am_are_not_in_the_probe`, `::test_ca1_prompt_ids_unique` | Intermedia 2026-09-29: comparación propia (parser independiente) id+texto+intent de los 24 `AV/AR/AG` contra `prompts-baseline.md` → 0 diferencias; `AM` ausentes; 44 preguntas Vigo intactas. Salvedad: set aún sin fecha de congelación (SPEC-007 CA-8) | ⚠️ |
| CA-2 | `probe/brands.csv`: Clínica Ártica (alias del dictamen `sdd-metricas` de SPEC-007 (a1)) + 15 competidoras verificadas + directorio Páxinas Galegas; Clínica Villoria L'Essence y Clínica Villoria (filas existentes) reutilizadas por pertenencia; ninguna sigla nueva. Tabla "Competidores verificados" y pendientes en este ledger | `test_pilot_batch.py::test_ca2_brands_csv_loads_and_has_the_client`, `::test_ca2_no_bare_common_word_alias_for_pilot_brands`, `::test_ca2_new_aliases_do_not_collide_with_existing_ones` (colisiones = ∅), `::test_ca2_no_alias_shared_between_two_brands_of_the_pilot_batch`, `::test_ca2_no_new_exact_aliases`, `::test_ca2_every_pilot_competitor_is_verified_in_the_ledger`, `::test_ca2_villoria_mentions_go_to_the_right_row_in_pilot_batch`, `::test_ca2_virxe_da_marina_domain_forms` | Intermedia 2026-09-29: `brands.csv` carga; 15 competidoras con URL+fecha en la tabla; muestreo propio de 3 fuentes (gaiaproaging.com, clinicamartaprieto.com/ferrol, medicalhair.es/vigo) confirma oferta y ciudad; patrones compartidos en todo el CSV solo los previos (vitaldent, povisa, villoria); sin siglas nuevas. Salvedad: en el lote piloto "Clínica Villoria" (oftalmología, fuera del lote) se atribuye a Villoria L'Essence por el alias "villoria" (riesgo en `AG03/AG04` blefaroplastia) + F-SPEC-008-2 | ⚠️ |
| CA-3 | `probe/batches/viveiro.json` (`extends` de `probe_config.json`; `user_location` Viveiro; `batch`: prefijos `AV/AR/AG`, niveles, cliente, ciudades locales de A Mariña, marcas miembro, `output_subdir`); `probe/settings.py` (`extends`, `batch`, `prompt_matcher`); `probe/matching.py` (`batch_brands`, `is_local_clinic(…, local_cities)`); `probe/run_probe.py` (`batch_prompts`, `output_dir(…, batch)`, `--only` fuera del lote rechazado); `probe/analysis.py` (`analyze_levels`, `render_levels`; filas fuera del lote ignoradas) | `test_pilot_batch.py::test_ca3_*` (ubicación en peticiones Claude/OpenAI, Gemini solo por texto, solo preguntas del lote, salida `piloto-artica/probe`, marca del piloto con ciudad Vigo participa, ponderado del núcleo igual sin filas `AR`/`AG`, resumen por nivel sin `%` fuera del núcleo, `--analyze` del lote) | Intermedia 2026-09-29: tests en verde y revisión de código: ubicación Viveiro en Claude/OpenAI, Gemini solo texto; 24 preguntas del lote; marcas por pertenencia (`batch_brands`, nombre desconocido falla); ponderado solo con celdas del núcleo (`analysis.py` bucle sobre `cells[core]`); `AR/AG` sin `%`; salida `$PUSHLLM_PRIVADO/piloto-artica/probe` | ✅ |
| CA-4 | `probe/probe_config.json`: sección `batch` del lote Vigo (prefijos `D F O E P H`, locales Vigo+Pontevedra, lista explícita de sus 52 marcas, salida `probe`). Golden generado con el código anterior (commit 8fe5132): `probe/tests/fixtures/vigo_results.csv` (incluye respuestas que nombran a Novoa, Medical Hair, Dorsia, Ártica, Hospital Capilar…) y `vigo_summary_before.md` | `test_pilot_batch.py::test_ca4_vigo_summary_identical_to_before_the_change`, `::test_ca4_default_batch_is_vigo`, `::test_ca4_default_run_never_executes_pilot_prompts`, `::test_ca4_pilot_brand_based_in_vigo_is_not_in_vigo_batch`, `::test_ca4_every_brand_belongs_to_some_batch`; todos los tests previos en verde (`python -m pytest -q probe/tests`: 156) | Intermedia 2026-09-29: regenerado el golden con el código de `8fe5132^` (git archive) → idéntico a `vigo_summary_before.md` (salvo CRLF); el mismo código viejo con el `brands.csv` nuevo da otro resumen (estética openai 25→50 %, ponderado 54,2→69,4 %), así que el test tiene dientes; lista Vigo = las 52 marcas previas; filas previas de `brands.csv`, `prompts.csv` y `probe_config.json` (salvo `batch`) sin cambios; `pytest probe/tests` 133 verde, `ruff` limpio | ✅ |
| CA-5 | Dictamen `sdd-probe` y cálculo en este ledger ("Dictamen sdd-probe (CA-5)"); cadencia aceptada por el humano; runs por nivel en `probe/batches/viveiro.json` (`AV` 3 desde la enmienda (b)) y `--levels` en `probe/run_probe.py`. Enmienda (b): "Mes del cierre y mes del baseline (enmienda (b))" con `c` = 0,1142 € y umbrales de `c'`. Enmienda (d): "Opción A y diseño de CA-11" con `c` real 0,1245 €, `AR` ≈ 5,6 € en el piloto, cierre sin palancas 20,5/22,2 € y palancas 1–4 en orden (la 1, del humano: `AG` cada 8 semanas) → 19,6/19,2 € | Cálculo reproducible en el propio dictamen; `test_pilot_batch.py::test_ca5_*` (`test_ca5_simple_pilot_command_uses_runs_per_level`: 15 × 3 + 9 = 54 llamadas por proveedor) | Intermedia 2026-09-29: recalculado: 72 p×e → 8,9/16,2 €; mes normal 9,2/16,8 €; baseline 102 p×e alto 22,97 € → regla de 2 runs 19,6 €; precios coinciden con `probe_config.json`; `AR/AG` a menor cadencia que `AV` | ✅ |
| CA-6 | `probe/README.md` §"Batches" (lote Vigo = defecto; comandos del lote piloto con `.\.venv\Scripts\python`; runs por nivel; salida). Enmienda (b): comando simple = baseline oficial (`AV` 3, `AR`/`AG` 1; cierra el finding 1), medición "después" con `--levels AV`, humo en directorio nuevo, orden sin pasada manual, líneas del Go en `summary.md` | `test_pilot_batch.py::test_ca6_readme_documents_pilot_batch_with_working_commands` y `::test_ca6_ledger_human_commands_within_budget_and_use_venv_python` (los comandos del README y del ledger se ejecutan offline: lote piloto y ≤ 54 llamadas por proveedor; el ledger sigue el orden de la enmienda (b)) | Intermedia 2026-09-29: sección "Batches" presente, lote Vigo = defecto, salida y comandos válidos. Salvedad: el comando de baseline del README (24 × 3 runs, 216 llamadas) no sigue la cadencia de CA-5 (`AR/AG` 1 run; regla 2/3 runs) que sí siguen las instrucciones del ledger | ⚠️ |
| CA-7 | **Ejecutado el 2026-09-29** (orquestador, con autorización del humano), en el orden de las instrucciones: humo de seguimiento (F-SPEC-013-5 cerrado sin reabrir) → congelación (2026-09-29T15:30:43Z, `60863af`) → baseline oficial `run_probe.py --config batches/viveiro.json`, 15:31:12Z–16:15:10Z. 162 llamadas, 162 `ok` (54 por proveedor, 0 excluidas); modelos servidos = `probe_config.json` (`claude-sonnet-5-5`, `gemini-3.6-flash`, `gpt-5.6-luna`); coste 6,73 € (c real 0,1245 € ≤ 0,1307: CA-5 sin cambios); "Medición completa": sí; **Aviso de techo (CA-10): sí** (decisión del humano pendiente, paso 5). Cifras de visibilidad y revisión de "Ártica" suelta solo en privado (ADR-004 §2): `$PUSHLLM_PRIVADO\piloto-artica\ca7-baseline-evidencia.md`; salida en `…\piloto-artica\probe\`, log en `…\baseline-run.log`. Nada en el repo | Congelación: `test_pilot_batch.py::test_ca7_pilot_prompts_equal_to_set_frozen_at_official_baseline` con `probe/tests/fixtures/pilot-set-frozen.tsv` (24 `id`/`prompt` del commit `60863af`). Fechas: SPEC-013 `hecho` (`0ed5384`) y dictamen CA-9 antes de la congelación; congelación 29 s antes de la primera fila; primera acción de SPEC-012 aún no ocurrida | Pendiente [Humano]: no ejecutado en verificación intermedia; comandos del ledger revisados | ❌ |
| CA-8 | [Verificador]. Ninguna salida en el repo: tests con `tmp_path`; la salida por defecto del lote es `$PUSHLLM_PRIVADO/piloto-artica/probe` y el respaldo `probe/out/piloto-artica/probe` está bajo `probe/out/` (ignorado); `run_probe.py` rechaza `--out` vacío o raíz de unidad (`unsafe_out`) | `test_run_probe.py::test_ca8_default_inside_repo_is_gitignored` (sin cambios); `test_pilot_batch.py::test_ca8_out_empty_or_root_is_refused`, `::test_ca8_unsafe_out_rules` | Intermedia 2026-09-29: `git ls-files` solo lista fixtures sintéticos de test (`probe/tests/fixtures/vigo_results.csv`, `vigo_summary_before.md`), ninguna salida de lote; `git status --ignored` sin `probe/out/` (no existe); `probe/out/` en `.gitignore`. Repetir al cierre tras CA-7 | ✅ |
| CA-9 | Dictamen `sdd-metricas` fechado 2026-09-29 en "Dictamen sdd-metricas (CA-9)" con tabla condición → cambio; `probe/batches/viveiro.json` (`AV` 3 runs, `go.min_valid_share` 0,9, `client_review_aliases`); `probe/analysis.py` (`analyze_levels`: ponderado por run, estabilidad por casilla, medición completa, respuestas solo por "Ártica", casillas `AR`/`AG` con la clínica, modelos servidos; `_core_go_lines`, `_bare_lines`); README; instrucciones de este ledger | `test_pilot_batch.py::test_ca9_config_fixes_the_go_instrument`, `::test_ca9_weighted_sov_per_run_and_pooled`, `::test_ca9_stability_per_question_and_provider`, `::test_ca9_go_measurement_complete_only_with_enough_valid_rows_per_provider`, `::test_ca9_bare_artica_answers_are_counted_and_flagged_for_review`, `::test_ca9_levels_outside_core_list_cells_with_client_without_percentages`, `::test_ca9_models_served_are_reported`; golden de Vigo intacto (`test_ca4_vigo_summary_identical_to_before_the_change`) | | |
| CA-10 | `probe/batches/viveiro.json` (`go.ceiling` 0,85); `probe/analysis.py` (`_ceiling_warning`: línea "Aviso de techo (SPEC-008 CA-10)" en la sección `AV` de `summary.md` si el ponderado del núcleo es ≥ 85 %, solo con `AV`). Decisión humana, si aplica, tras el baseline (paso 5 de las instrucciones). **Aviso saltado en el baseline oficial; decisión del humano del 2026-09-29, antes de la primera acción, registrada en "Decisiones del humano" (c) (ADR-009)**; el texto del aviso en `summary.md` recoge la decisión | `test_pilot_batch.py::test_ca10_ceiling_warning_only_from_core_weighted` (20/20, 17/20 = 85 % avisa; 16/20 no; 0 no), `::test_ca10_ceiling_ignores_other_levels` (`AR` al 100 % no avisa) | | |
| CA-11 | Dictamen `sdd-metricas` fechado 2026-09-29 en "Dictamen sdd-metricas (CA-11)" (opción A; (i)–(v); 5 preguntas bastan con condiciones) con tabla condición → cambio; `probe/batches/viveiro.json` (`AR` 3 runs; `go.growth` +12 pts, 2 "después"; `go.defense` −10 pts en las dos; etiquetas (C)/(D)); `probe/analysis.py` (`analyze_levels` → `growth`, `core_runs`; `_growth_lines`; `growth_verdict`, `defense_verdict`, `render_go_verdict`; completitud por nivel); `probe/README.md` "Batches"; CA-5 recalculado ("Opción A y diseño de CA-11") | `test_pilot_batch.py::test_ca11_config_fixes_growth_and_defense`, `::test_ca11_ar_weighted_uses_only_ar_rows`, `::test_ca11_ar_summary_gives_its_own_weighted_only_with_design_runs`, `::test_ca11_ar_measurement_incomplete_with_errors`, `::test_ca11_growth_needs_rise_in_both_afters_and_more_than_one_question`, `::test_ca11_growth_threshold_is_inclusive_and_unrounded`, `::test_ca11_growth_not_decidable_with_other_design_or_incomplete`, `::test_ca11_defense_fails_only_with_a_drop_in_both_afters`, `::test_ca11_verdicts_do_not_mix_levels`, `::test_ca11_go_verdict_report_gives_c_and_d_apart`; ajustados `test_ca9_config_fixes_the_go_instrument`, `test_ca5_simple_pilot_command_uses_runs_per_level` (64 por proveedor) y `test_ca9_go_measurement_complete_…` (rótulo (D)); golden de Vigo intacto | | |
| CA-12 | **Preparado, sin ejecutar** ([Humano] lanza). "Instrucciones para el humano (CA-12)": `--config batches/viveiro.json --levels AR --runs 3 --out "$env:PUSHLLM_PRIVADO\piloto-artica\probe-AR-antes"`; 45 llamadas (15 por proveedor), ≈ 1,9 €; comprobación previa del modelo por defecto (CA-11 (iv)). Falta: ejecución, fecha, llamadas por estado, coste, modelos y "Medición completa (C)" | `test_pilot_batch.py::test_ca12_ledger_command_is_the_ar_before_with_the_design_of_ca11` (ejecuta offline el comando del ledger: 45 llamadas, solo `AR01`–`AR05`, runs 1–3, medición completa con 3 runs) | | |

Tests (2026-09-29, tras los findings): `python -m pytest -q probe/tests` → 156 en verde;
`python -m pytest -q docs/piloto-artica/tools/tests` → 143 en verde; `ruff check probe` limpio.
Tests (2026-09-29, enmienda (b), CA-9/CA-10, con `PUSHLLM_PRIVADO` en el entorno):
`pytest probe/tests` → 226 en verde; `pytest docs/piloto-artica/tools/tests` → 143 en verde;
`ruff check probe` limpio.
Tests (2026-09-29, registro de CA-7 y congelación): `pytest probe/tests` → 227 en verde;
`pytest docs/piloto-artica/tools/tests` → 143 en verde; `py -m ruff check probe` limpio.
Tests (2026-09-29, enmienda (d), CA-11/CA-12): `pytest probe/tests` → 238 en verde;
`pytest docs/piloto-artica/tools/tests` → 143 en verde; `py -m ruff check probe` limpio.

## Diseño (mecanismo de CA-3, propuesto por el implementador)
- **Lote = fichero de configuración** pasado con `--config`. `batches/viveiro.json` hereda
  de `probe_config.json` con `"extends"` (fusión superficial: cada clave de primer nivel del
  lote sustituye entera a la del fichero base). Precios, modelos, pesos y cambio viven solo
  en `probe_config.json`.
- **Preguntas del lote**: prefijos de id (`prompt_prefixes`) seguidos de dígitos. Vigo:
  `D F O E P H`; piloto: `AV AR AG`. El nivel se lee del prefijo (sin columna nueva).
- **Marcas del lote por pertenencia declarada** (`batch.brands`), no por ciudad (enmienda
  CA-3 (i), ADR-005 §5). El lote Vigo lista explícitamente sus 52 marcas de antes, así que
  una marca nueva de `brands.csv` nunca entra en Vigo por accidente. Un test exige que toda
  marca pertenezca al menos a un lote y que no haya nombres desconocidos.
- **Resumen por nivel** (enmienda CA-3 (ii)): con `batch.levels`, `summary.md` da por nivel
  y proveedor válidas, "x de n" con Clínica Ártica y excluidas; SoV bruto, clínica local y
  ponderado (RN-03) **solo en `AV`**; en `AR`/`AG` solo recuentos, sin porcentajes
  (dictamen `sdd-metricas` (g)–(j) de SPEC-007). El coste se da por nivel y proveedor y un
  total del lote, rotulado como operativo (no es cifra de visibilidad).
- **Filas ajenas al lote** en un `results.csv` se ignoran en el análisis (y, solo si hay
  alguna, una línea lo dice), para que un lote nunca cuente preguntas del otro.

## Competidores (CA-2)

### Alias de Clínica Ártica
Del dictamen `sdd-metricas` del ledger de SPEC-007, punto (a1), confirmado por el humano el
2026-09-29 (P-1) y recogido en F-SPEC-007-2: nombre "Clínica Ártica"; alias "Ártica",
"Ártica Medicina Estética" y "clinicaartica" (dominio en el texto). "Ártica" sola cuenta
también como adjetivo (RN-01 literal): el probe no marca `#artica-adjetivo`; se revisa a
mano si el recuento lo pide (F-SPEC-008-3). Sin sigla (RN-11 no aplica). Sin alias de la
médica titular (a4/P-2).

### Competidores verificados
Todas las fuentes consultadas el 2026-09-29 (búsqueda pública; página abierta, no solo el
fragmento del buscador). Criterio: la página muestra que la marca ofrece hoy medicina
estética, capilar o blefaroplastia en la ciudad indicada. Alias: nombre + forma distintiva
+ dominio; nunca una palabra común o un apellido suelto.

| Marca (brands.csv) | Ciudad (sedes) | Fuente | Fecha | Qué muestra | Nivel |
|---|---|---|---|---|---|
| Luxury Clínica Médico Estética | Viveiro | https://luxuryclinica.com | 2026-09-29 | "Tratamientos de medicina estética" (láser, facial, corporal); Páxinas Galegas la lista entre clínicas de medicina estética de Viveiro. No nombra médico ni bótox/hialurónico (salvedad F-SPEC-008-2) | AV |
| Clínica Virxe da Mariña | Burela | https://xn--clinicavirxedamaria-d4b.com/consultations | 2026-09-29 | "Medicina Estética" entre sus especialidades, con médica. Alias de dominio: `clinicavirxedamariña` (forma con eñe) y `clinicavirxedamaria` (la que aparece en el dominio punycode `xn--clinicavirxedamaria-d4b`, finding 3) | AV |
| Gaia Pro Aging | Lugo | https://gaiaproaging.com | 2026-09-29 | "Una clínica de medicina estética en Lugo" | AV |
| Clínica Pío Vila Ayán | Lugo (y Monforte de Lemos) | https://clinicapiovila.com | 2026-09-29 | "Apostamos por la medicina estética…"; clínica sobre todo dental (salvedad F-SPEC-008-2) | AV |
| Dorsia | Lugo (cadena; también Vigo, A Coruña, Santiago, Ourense, Pontevedra) | https://dorsia.es/clinicas-dorsia/lugo | 2026-09-29 | Medicina y cirugía estética, incluida blefaroplastia; las otras cinco sedes gallegas cargan en `dorsia.es/clinicas-dorsia/{vigo,coruna,santiago-compostela,ourense,pontevedra}` | AV, AG |
| Avance Capilar | Vilagarcía de Arousa | https://avancecapilar.com | 2026-09-29 | "Trasplante y Medicina Capilar en Galicia" (DHI); Ourense y A Coruña no confirmadas en su web | AG |
| Medical Hair | Vigo (cadena nacional) | https://medicalhair.es/vigo/ | 2026-09-29 | "Clínica Capilar en Vigo — Injerto Capilar Vigo" | AG |
| Hospital Capilar | Vigo (y Pontevedra, solo por directorios) | https://hospitalcapilar.com/injerto-capilar-vigo/ | 2026-09-29 | Injerto capilar FUE con sede propia en Vigo | AG |
| Clínica Novoa | Vigo (y Santiago, A Coruña) | https://clinicanovoa.es/tratamientos-capilares.aspx | 2026-09-29 | Tratamientos capilares médicos (mesoterapia, PRP); **no** anuncia trasplante | AG |
| Clínica Dr. Torres | A Coruña | https://injertocapilarcoruna.es | 2026-09-29 | "Primera clínica de microtrasplante capilar en Galicia" | AG |
| Clínica Villoria L'Essence | Vigo (y Pontevedra) | https://clinicaesteticavilloria.es/blefaroplastia-y-su-precio-vigo-pontevedra/ | 2026-09-29 | "Blefaroplastia superior con láser". Fila ya existente en `brands.csv` (lote Vigo); entra en el piloto por pertenencia, sin fila nueva | AG |
| Clínica Villoria | Vigo | https://www.clinicavilloria.es/blefaroplastia-y-su-precio/ | 2026-09-29 | "Somos el centro pionero … de Galicia en blefaroplastia con tecnología láser CO2". Fila ya existente (oftalmología, lote Vigo); entra en el piloto por pertenencia para que "Clínica Villoria" no se cuente como L'Essence (finding 2 de la verificación intermedia) | AG |
| Clínica Ulloa | A Coruña | https://cirugiaulloa.com | 2026-09-29 | "Blefaroplastias" en cirugía estética facial | AG |
| Clínica Dr. Cerqueiro | A Coruña | https://cerqueiro.es | 2026-09-29 | "Párpados / blefaroplastia" en cirugía facial | AG |
| Clínica Marta Prieto | Ferrol (y Madrid) | https://clinicamartaprieto.com/ferrol/ | 2026-09-29 | Dermatología y medicina estética en Ferrol | AR |
| Clínicas Médicas Dr Luna | Ferrol | https://clinicasdrluna.es/clinica-estetica-ferrol | 2026-09-29 | "Médico especialista en estética" en Ferrol | AR |

Directorio añadido (sin verificación de oferta, es plataforma): Páxinas Galegas
(`paxinasgalegas`), que lista clínicas de medicina estética de Viveiro. El lote piloto usa
además Doctoralia, Top Doctors, Multiestetica, SaludOnNet y ClinicPoint (ya existentes).

### Candidatas pendientes (no entran en `brands.csv`)
| Candidata | Motivo (2026-09-29) |
|---|---|
| Clínica Ribera Polusa Viveiro | La noticia de 2024 (riberasalud.com; aquidiario.com 18-06-2024) anunciaba medicina estética; la ficha actual de la clínica (https://riberasalud.com/polusa/clinicaviveiro/) tiene otra dirección y **no** lista medicina estética. Vigencia no verificada |
| CapMédica | https://capmedica.com/lugo es una página de captación: la única clínica está en Las Palmas. No está en Lugo → descartada |
| Clínica de medicina estética en Ribadeo (médica de familia) | Artículo de elprogreso.es (04-06-2026) sin nombre comercial de la clínica |
| Centro Clínico Ribadeo | La página de medicina estética da 404; solo un fragmento de 2018 |
| Medicina estética en Foz ("JS") | Sin web; solo un fragmento de directorio y una cuenta de red social |
| Centro Médico Ábaton (A Coruña) | Cirugía plástica en su web; la blefaroplastia solo figura en directorios |
| Clínica Dra. Mosquera (Ferrol) | Web inaccesible (error de certificado); solo ficha de directorio |
| Centro Médico Estético MM (Vegadeo) | Web sin médico ni tratamientos médicos: puede ser estética no médica |
| Biothecare Estétika (Navia) | Solo fragmento de buscador; parece centro de belleza |
| Luarca, Tapia de Casariego, Castropol | Nada encontrado (sin socios SEME en el occidente de Asturias) |
| todoestetica.com, miclinicacapilar.com (directorios) | No comprobados; se valoran con las respuestas reales |
Se reconsideran con las competidoras que salgan en las pasadas manuales (SPEC-007) y en el
humo/baseline del probe (F-SPEC-008-1).

### Colisiones de alias
Ningún alias nuevo coincide (normalizado) con uno existente del lote Vigo
(`test_ca2_new_aliases_…`). En el lote piloto solo se comparte **"villoria"**, justificado
(`JUSTIFIED_SHARED_IN_PILOT` en `test_ca2_no_alias_shared_…`): tras el finding 2 de la
verificación intermedia (2026-09-29), las dos filas existentes de Villoria son miembros del
lote piloto. "Clínica Villoria" casa con la fila de oftalmología (nombre más largo gana) y
"Villoria L'Essence" con la de estética; "Villoria" suelta se resuelve por especialidad
(`aesthetic`) a L'Essence, como en el lote Vigo. Ninguna fila de `brands.csv` de Vigo cambia;
el golden de Vigo sigue idéntico. Test
`test_ca2_villoria_mentions_go_to_the_right_row_in_pilot_batch`. Decisiones de alias:
- Apellidos y palabras comunes sin alias suelto: "Luxury", "Novoa", "Ulloa", "Torres",
  "Luna", "Gaia", "Avance".
- "Dr. Cerqueiro" y "Pío Vila" sí entran: nombre y apellido/tratamiento + apellido poco
  común referidos a la clínica.
- Ninguna sigla nueva en `exact_aliases` (ADR-002 §6 no se invoca).

## Dictamen sdd-probe (CA-5)
- **Fecha**: 2026-09-29. **Emisor**: sdd-implementador aplicando
  `.ai-context/skills/sdd-probe.md` (advisory; no cambia reglas). **Invariantes**: RN-10,
  D-5, No-negociable "coste del probe ≤ 20 € por clínica y mes".
- **Fuentes**: `probe/probe_config.json` (precios del 2026-09-23, fuentes dentro);
  dictamen sdd-probe del ledger de SPEC-001 (estimación 396 llamadas ≈ 20–30 €);
  https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool y
  https://developers.openai.com/api/docs/guides/tools-web-search (consultadas el
  2026-09-29).

**Ubicación Viveiro por proveedor — correcto.**
- Claude: `user_location` `{type: approximate, city, region, country, timezone}`; `city` es
  texto libre y `country` ISO-3166 (ES admitido): Viveiro/Galicia/ES/Europe/Madrid es válido.
- OpenAI: `user_location` approximate; "city y region son texto libre": válido.
- Gemini: sin parámetro de ubicación en el grounding con Google Search; como hoy, la
  ubicación va solo en el texto de la pregunta (todas las `AV`/`AR` nombran el lugar; las
  `AG` dicen "Galicia"). Salvedad RN-10 ya conocida (F-SPEC-001-1).
- Nota: en `AR` el paciente vive en Ferrol, Vilalba, Asturias…, pero todo el lote usa la
  ubicación Viveiro (Fuera de alcance de la spec); el lugar va en el texto.

**Coste por pregunta × ejecución (los 3 proveedores), supuestos por llamada:**
| Proveedor | Típico | Alto |
|---|---|---|
| Claude Sonnet 5 (2/10 $ por M; 0,01 $/búsqueda) | 20k entrada, 0,8k salida, 3 búsquedas → 0,078 $ | 40k, 1,5k, 5 → 0,145 $ |
| GPT-5.6 Luna (0,20/1,20 $ por M; 0,01 $/búsqueda) | 10k, 1k, 2 → 0,023 $ | 20k, 2k, 3 → 0,040 $ |
| Gemini 3.6 Flash (0,75/3,75 $ por M; 0,014 $/consulta) | 6k, 1,5k, 2 → 0,040 $ | 10k, 3k, 3 → 0,072 $ |
| **Total** (1 EUR = 1,1411 USD) | **0,141 $ ≈ 0,124 €** | **0,257 $ ≈ 0,225 €** |

Contraste: con el típico, las 132 preguntas × ejecución del lote Vigo (396 llamadas) salen
≈ 16 € y con el alto ≈ 30 €: coherente con los 20–30 € estimados en SPEC-001.

**Una ejecución completa del lote** (24 preguntas × 3 runs × 3 proveedores = 216 llamadas,
72 preguntas × ejecución): **≈ 8,9 € típico / 16,2 € alto**. Humo (3 preguntas × 1 run × 3
= 9 llamadas): ≈ 0,4–0,7 €.

**Cadencia para SPEC-012 (≤ 20 €/mes) — aceptada por el humano el 2026-09-29 (ver
"Decisiones del humano"):**
| Bloque | Cadencia | Preguntas × ejecución al mes | € típico | € alto |
|---|---|---|---|---|
| `AV` (15), 1 run × 3 proveedores | semanal (52/12 al mes) | 65 | 8,0 | 14,6 |
| `AR` + `AG` (9), 1 run × 3 proveedores | cada 4 semanas (13/12 al mes) | 9,75 | 1,2 | 2,2 |
| **Mes normal** | | 74,75 | **9,2** | **16,8** |

- Cabe en ≤ 20 €/mes incluso con el supuesto alto. `AR`/`AG` van a menor frecuencia que
  `AV`, nunca al revés (enmienda CA-5).
- **Mes del baseline** (CA-7): baseline `AV` con 3 runs + `AR`/`AG` con 1 run (54
  preguntas × ejecución) + humo (3) + 3 semanas de `AV` semanal (45) = 102 → 12,6 € típico,
  22,9 € alto. **Condición**: tras el humo, calcular el coste real por pregunta × ejecución
  `c` = total del humo ÷ 3 (sale en la tabla de coste de su `summary.md`). Si `c ≤ 0,19 €`,
  baseline con 3 runs en `AV` (102 × 0,19 ≤ 19,4 €); si `c > 0,19 €`, baseline con 2 runs en
  `AV`, que con el alto da 87 × 0,225 ≈ 19,6 €. `AR`/`AG` del baseline, 1 run.
  El baseline sustituye a la ejecución `AV` semanal de su semana.
- **Runs por nivel en el lote** (finding 1): `batches/viveiro.json` fija `runs` por nivel
  (`AV` 2, `AR` 1, `AG` 1), así que el comando simple es la variante segura del baseline
  (39 preguntas × ejecución por proveedor; ≈ 8,8 € con el supuesto alto). `--runs N` pisa
  todos los niveles seleccionados y `--levels AV` / `--levels AR,AG` elige niveles. Tests:
  `test_ca5_simple_pilot_command_uses_runs_per_level`,
  `test_ca5_levels_option_selects_levels_and_runs_override`; los comandos del README y de
  este ledger se ejecutan offline en `test_ca6_*` y ninguno pasa de 54 llamadas por
  proveedor.
- Mismo instrumento (dictamen sdd-metricas (e) de SPEC-007): la comparación probe antes /
  probe después usa el mismo número de runs en ambos lados; el "después" del cierre repite
  la forma del baseline.
- Palanca si los precios suben: bajar `AR`/`AG` a cada 8 semanas antes que tocar `AV`.
  Quitar Claude del probe (peso 10 %) abarataría ~55 %, pero cambia el instrumento: no se
  propone; lo decidiría el humano con `sdd-metricas`.
- **Antes del humo**: re-verificar el modelo por defecto de cada app (GPT-6 Luna,
  F-SPEC-001-3) y los precios; si cambian, se actualiza `probe_config.json` (vale para los
  dos lotes) y se rehace este cálculo.

**Mes del cierre y mes del baseline (enmienda (b), 2026-09-29)** — mismo emisor y fuentes,
más el dictamen CA-9. `c` medido en el humo de Viveiro = 0,3425 € ÷ 3 = **0,1142 €** por
pregunta × ejecución (los 3 proveedores), con precios de `probe_config.json`.
| Mes | Composición (preguntas × ejecución) | Total | € con `c` = 0,1142 |
|---|---|---|---|
| Baseline (peor caso) | humo antiguo 3 + humo de seguimiento 3 + baseline 54 (`AV` 15 × 3 + `AR`/`AG` 9) + 4 semanas de `AV` semanal 60 + 1 `AR`/`AG` 9 | 129 | **14,7** |
| Normal (SPEC-012) | ver tabla de cadencia | 74,75 | 8,5 |
| Cierre, típico (4,33 semanas) | 2 mediciones "después" 90 (`AV` 15 × 3 cada una, sustituyen a su semanal) + 2,33 semanales 35 + 1,08 `AR`/`AG` 9,75 | 134,75 | **15,4** |
| Cierre, peor mes natural | 2 "después" 90 + 3 semanales 45 + 2 `AR`/`AG` 18 (semanas 8 y 12 en el mismo mes) | 153 | **17,5** |

- **Cabe en ≤ 20 €** con el `c` medido, sin bajar los runs del Go (3) por debajo de los del
  baseline.
- **Condición** (el humo de seguimiento da `c'`, ya con `include` en OpenAI):
  - `c' ≤ 0,1307 €` (20 ÷ 153): nada cambia.
  - `0,1307 € < c' ≤ 0,155 €`: palancas para el mes del cierre, en este orden, sin tocar las
    mediciones del Go:
    1. una sola ejecución `AR`/`AG` en ese mes (la de la semana 8 se adelanta a la 7):
       144 preguntas × ejecución, `c' ≤ 0,139 €`;
    2. sin `AV` semanal en la semana anterior a la primera medición "después": 129,
       `c' ≤ 0,155 €`.
    El mes del baseline (129) también cabe hasta 0,155 €.
  - `c' > 0,155 €`: no se lanza el baseline. Vuelve a `sdd-probe` y al humano.
  - `c' > 0,19 €`: además, la regla de CA-7 daría 2 runs, lo que cambia la forma del Go
    (dictamen CA-9 (a)).
- Un humo de 3 preguntas es una muestra pequeña. El baseline da el `c` real, que se recalcula
  al cerrar CA-7.
- Si SPEC-007 necesitara una ejecución `AV` extra para su ventana de calibración (15
  preguntas × ejecución con 1 run), el mes del baseline sube a 144 → 16,4 €.

**Opción A y diseño de CA-11 (enmienda (d), 2026-09-29)**. Mismo emisor y mismas fuentes,
más el dictamen CA-11 y la regla de recorte del humano (ver "Decisiones del humano" (e)).
- `c` real del baseline oficial = 6,7252 € ÷ 54 = **0,1245 €** por pregunta × ejecución (los
  3 proveedores). Solo `AR`: ≈ 0,126 €.
- **Coste de `AR` en el piloto**: el "antes" (CA-12) y cada "después" son 5 preguntas ×
  3 runs = 15 preguntas × ejecución (45 llamadas) ≈ **1,9 €**. Son tres ejecuciones:
  **≈ 5,6 €** en todo el piloto.
- Cada medición "después" = `--levels AV,AR` = 60 preguntas × ejecución (180 llamadas)
  ≈ 7,5 €. Sustituye a la `AV` semanal de su semana. En la semana 12 sustituye también al
  `AR` de 1 run; ahí `AG`, si toca, se lanza solo con `--levels AG --runs 1`.

| Mes | Composición (preguntas × ejecución) | Total | € con `c` = 0,1245 |
|---|---|---|---|
| Septiembre (baseline y, si se lanza ya, CA-12) | humos 0,34 € + 0,36 € + baseline 6,73 € + CA-12 15 | — | **≈ 9,3** |
| Arranque (CA-12 en el mes de la primera acción) | CA-12 15 + 5 semanales `AV` 75 + 1 `AR`/`AG` 9 | 99 | 12,3 |
| Normal (SPEC-012) | tabla de cadencia (sin cambios) | 74,75 | 9,3 |
| Cierre típico (4,33 semanas), sin palancas | 2 "después" 120 + 2,33 semanales 35 + 1,08 `AR`/`AG` 9,75 | 164,75 | **20,5** ✗ |
| Cierre, peor mes natural (semanas 8–12), sin palancas | 2 "después" 120 + 3 semanales (8, 9, 10) 45 + `AR`/`AG` semana 8: 9 + `AG` semana 12: 4 | 178 | **22,2** ✗ |

- **No cabe sin palancas.** El orden de las palancas es fijo. La primera la decidió el humano;
  las demás las propone `sdd-probe`. Nunca se bajan los runs de las mediciones del Go (3 en
  `AV` y en `AR`) ni el número de mediciones "después":
  1. **`AG` cada 8 semanas** (semanas 0 y 8), decisión del humano. Peor mes 174 → 21,7 €;
     típico 162,6 → 20,2 €. No basta.
  2. **Sin `AR` de 1 run en el mes del cierre** (la de la semana 8): las mediciones `AR` del Go
     ya lo miden. Peor mes 169 → 21,0 €; típico 157,2 → **19,6 €** ✓.
  3. **Sin `AV` semanal en la semana anterior a la primera medición "después"** (semana 10),
     la palanca 2 del cálculo (b). Peor mes 154 → **19,2 €** ✓.
- **Con las palancas 1–3, el cierre cabe hasta `c` ≤ 0,1299 €** (20 ÷ 154). Si el `c` medido
  antes del cierre supera ese valor, se añade:
  4. sin `AV` semanal en la semana 9: 139, `c` ≤ 0,1439 €.
  Por encima de 0,1439 €, PARA: vuelve a `sdd-probe` y al humano.
- Las palancas se deciden **al planificar el mes del cierre** (SPEC-012), no después de ver
  datos. No tocan el Go: las `AV` semanales y el `AR` de 1 run son solo seguimiento.
- Opción A con 5 runs (descartada en CA-11 (v)): cada ejecución `AR` ≈ 3,1 €. El peor mes
  no cabría ni con las palancas 1–4.
- **CA-12 en concreto**: 5 preguntas × 3 runs × 3 proveedores = **45 llamadas** (15 por
  proveedor), **≈ 1,9 €** (1,87 € con `c` = 0,1245; 1,89 € con el `c` de `AR`). Si se lanza en
  septiembre, el mes queda en ≈ 9,3 € ≤ 20 €.


## Dictamen sdd-metricas (CA-9)
- **Fecha**: 2026-09-29, **antes del baseline oficial** (CA-7 sin lanzar: no existe
  `$PUSHLLM_PRIVADO/piloto-artica/probe/`). **Emisor**: sdd-implementador aplicando
  `.ai-context/skills/sdd-metricas.md` (advisory; no implementa ni cambia reglas).
  **Fuentes**: `docs/fundacion/reglas.md` RN-01–RN-06, RN-10, RN-11; EPIC-002, criterios 1 y 4;
  ADR-005 §4 (vigente según ADR-008 §6); dictámenes `sdd-metricas` del ledger de SPEC-007
  ((a)–(j); P-1, P-3) y de SPEC-013 (CA-7, URLs consultadas y citadas); `probe/analysis.py`,
  `probe/batches/viveiro.json` y `probe/probe_config.json` (leídos el 2026-09-29); humo de
  Viveiro (c = 0,1142 €) y evidencia CA-6 de SPEC-013.
- **¿Cambia alguna regla de negocio? No.** Todo lo de abajo son condiciones de medición y
  lectura del criterio Go. RN-01, RN-02, RN-03, RN-04, RN-05, RN-06 y RN-10 se aplican tal
  cual. Si alguna condición llegara a exigir cambiar una RN, se devuelve al arquitecto; no ha
  hecho falta.

### (a) Forma del baseline — **correcto con condiciones**
- Una sola ejecución del lote: `AV` con **3 runs** (regla de CA-7: c = 0,1142 € ≤ 0,19 €),
  `AR` y `AG` con **1 run**. En total, 54 preguntas × ejecución × 3 proveedores = 162 llamadas.
  Es el comando simple de `batches/viveiro.json`.
- **No hacen falta dos ejecuciones en semanas distintas.** El ruido del baseline es común a
  las dos comparaciones "después", así que una segunda ejecución solo baja el error típico de
  cada diferencia de √2·σ a √1,5·σ (≈ −13 %). A cambio, retrasaría la primera acción al
  menos 7 días. La protección frente al ruido la da la regla (d), que exige la subida en
  **cada** medición "después".
- **Condiciones**:
  1. Se lanza en un directorio nuevo con la columna `searched_urls`.
  2. Queda **completa**: cada proveedor con peso tiene ≥ 90 % de sus filas `AV` con
     `status=ok`. Si no, `--resume` en la misma semana. `summary.md` lo dice ("Medición
     completa para el criterio Go: sí/no").
  3. Su inicio **congela el set** (SPEC-007 CA-8).
  4. Ninguna acción del piloto empieza antes de que termine y se haya leído el aviso de
     techo (CA-10).

### (b) Cómo se agregan los runs — **correcto**
- SoV bruto (RN-02) por proveedor = respuestas válidas con Clínica Ártica ÷ respuestas
  válidas, sumando todos los runs de la ejecución. Es lo que hace `analysis.py`: 45 respuestas
  por proveedor si no hay exclusiones.
- SoV ponderado del núcleo (RN-03/RN-04) = Σ SoV bruto × peso ÷ Σ pesos de los proveedores con
  respuestas válidas. Con ChatGPT 0,55, Gemini 0,25 y Claude 0,10, la suma es 0,90 y los pesos
  normalizados quedan en 0,611, 0,278 y 0,111.
- Claude **sí** entra: en el probe se sondea en todas las mediciones (a diferencia de la
  manual).
- La media de los SoV por run coincide con la cifra agregada cuando los runs tienen las
  mismas respuestas válidas. El Go usa **la cifra agregada**. `summary.md` da además el
  ponderado por run, que es solo lectura de ruido.
- Solo `AV` (ADR-005 §4).

### (c) Forma de las dos mediciones "después" — **correcto con condiciones**
- Misma forma que el baseline en `AV`: **3 runs**, con `--levels AV`, que toma los runs del
  lote.
- Semana 0 = semana de la primera acción. Primera medición en la **semana 11** y segunda en
  la **12**, cada una ± 1. Entre sus inicios, **≥ 7 días**. Las dos, antes del cierre del
  piloto.
- Cada una **sustituye** a la ejecución `AV` semanal de 1 run de su semana.
- La ejecución `AR`/`AG` que toque en la semana 12 se lanza aparte con `--levels AR,AG` y
  1 run. No entra en el Go.
- Cada medición debe quedar **completa** (condición (a).2). Si una no se completa en su
  semana, se repite entera la semana siguiente, siempre dentro de la ventana ± 1 y con los
  7 días de separación.

### (d) Regla de estabilidad del Go — **correcto** (P-3 del humano)
- **Go de visibilidad ⇔ Δ₁ ≥ +15,0 pts y Δ₂ ≥ +15,0 pts**. Δᵢ = ponderado del núcleo de la
  medición "después" i − ponderado del núcleo del baseline. Se calcula sin redondear y con
  las dos mediciones completas.
- **No se usa la media** de las dos: una sola medición alta no basta.
- Se decide con sí/no desde los tres `results.csv`:
  1. Al emitir el veredicto se recalculan los tres `summary.md` con `--analyze`, con el
     **mismo** `brands.csv` y el **mismo** `probe_config.json` (mismos pesos: si RN-05 los
     refresca, se aplican iguales a los dos lados).
  2. Se lee la línea "SoV ponderado del núcleo".
- El criterio Go completo exige además ≥ 1 paciente atribuido (EPIC-002, criterio 4;
  SPEC-012). Eso no es de este dictamen.

### (e) Ruido esperable frente a +15 pts — **correcto con condiciones**
- Error típico del ponderado del núcleo (binomial; Σw² = 0,463):
  - con n = 45 respuestas por proveedor (3 runs independientes);
  - entre paréntesis, con n efectivo = 15, si los 3 runs del mismo día salen iguales.
- La realidad cae entre los dos. El cálculo **no** incluye la deriva de semana a semana
  (índice de búsqueda, modelo), así que es una cota inferior.

| SoV "antes" | Error típico | Margen 95 % de una diferencia | P(Go falso) con Δ real 0 y la regla (d) | P(Go) con Δ real +20 |
|---|---|---|---|---|
| 5 % | 2,2 pts (3,8) | ± 6 (± 11) | < 0,1 % | 55–73 % |
| 10 % | 3,0 (5,3) | ± 8 (± 15) | 0,4 % | — |
| 20 % | 4,1 (7,0) | ± 11 (± 19) | 0,05–1,8 % | 51–65 % |
| 35 % | 4,8 (8,4) | ± 13 (± 23) | 0,2–3,4 % | — |
| 50 % | 5,1 (8,8) | ± 14 (± 24) | 0,3–3,9 % | — |

- **Lectura**: con la regla (d), un Go falso es improbable (≤ 4 %). La regla es
  **conservadora**: una subida real de +20 pts pasa en 51–73 % de los casos, y una de +25 o
  +30 en 69–100 %. Es la contrapartida de exigir estabilidad (P-3), y se acepta.
- **Las ejecuciones `AV` semanales de 1 run no sirven como medida del ruido del Go**:
  - tras la primera acción mezclan efecto y ruido;
  - tienen n = 15 por proveedor, con un margen de ± 15–24 pts frente al baseline.
  - Sirven para ver la tendencia y fechar movimientos (registro acción → efecto, SPEC-012),
    nunca para decidir el Go.
- **Medida del ruido**: en cada medición, `summary.md` da el ponderado por run (ruido del
  mismo día) y la estabilidad por pregunta × proveedor (en todos, en alguno o en ningún run).
  El veredicto informa además |Δ₁ − Δ₂| como ruido de semana a semana observado al final. Es
  informativo: no cambia el sí/no.

### (f) Mismo instrumento; cambio de modelo por defecto — **correcto con condiciones**
- **Idéntico entre el baseline y las mediciones "después"**:
  - el set congelado (CA-8);
  - los runs de `AV` (3);
  - la ubicación Viveiro/Galicia/ES;
  - los prompts de sistema e instrucciones;
  - la configuración de búsqueda y de la petición: herramienta y versión, `max_uses`,
    `include` de OpenAI, `effort`, `max_tokens`.
  - Se comprueba con el `request` de `raw_responses.jsonl`: mismos campos salvo `model`.
- Un cambio en `probe/` que altere la petición entre el baseline y una medición "después" es
  **cambio de instrumento**: no se hace sin un dictamen nuevo anterior a esa medición.
- En particular, si el seguimiento **F-SPEC-013-5** del humo reabre el `include` de OpenAI,
  se decide **antes** del baseline. Cambiarlo después rompe el instrumento.
- **Modelo por defecto (D-5, RN-10)**:
  - El probe debe usar el modelo por defecto de cada app. `summary.md` lista los modelos
    servidos. Antes del baseline y antes de cada medición "después", `sdd-probe` vuelve a
    comprobar el modelo por defecto y los precios; si cambian, se actualiza
    `probe_config.json` con fecha.
  - Si cambia **entre el baseline y la primera acción**, se **repite el baseline** con el
    modelo nuevo, en un directorio nuevo y antes de la primera acción. Cuesta unos 6 €. La
    fecha de congelación no cambia.
  - Si cambia **después de la primera acción**, la comparación **sigue valiendo**. RN-10
    manda medir lo que contesta el modelo que ve el paciente: el cambio forma parte del
    entorno, como un cambio del índice de búsqueda.
  - En ese caso el veredicto anota el proveedor, el modelo anterior y el nuevo, y la fecha.
    No se rehace el baseline ni se descarta ninguna medición.
  - Se fija ahora, antes de ver datos.
- **Pesos y alias**: los dos lados se calculan con los mismos (condición (d).1). Los alias de
  Clínica Ártica no cambian durante el piloto. Añadir competidoras no cambia la cifra del Go.

### (g) Indicadores `AR` y `AG` con el probe — **correcto con condiciones**
- Se trasladan las definiciones de SPEC-007 (g)–(j) con la cadencia de CA-5: `AR`/`AG` cada
  4 semanas, 1 run. Las ejecuciones son en las semanas 0 (el baseline), 4, 8 y 12.
- **Casilla** = pregunta × proveedor (ChatGPT, Gemini, Claude). Solo recuentos "x de n",
  nunca porcentajes ni ponderado. Nada se suma al núcleo.
- **Periodo "antes"** = la ejecución de la semana 0. **Periodo "después"** = semanas 8 y 12
  para `AR`, y semanas 4, 8 y 12 para `AG`.
- `AR`:
  - "No aparece" antes ⇔ 0 casillas con la clínica en la semana 0.
  - "Aparece con cierta regularidad" después ⇔ **≥ 2 casillas** con la clínica **en las
    dos** ejecuciones (8 y 12).
  - Si ya aparecía antes, se informa tal cual.
- `AG`:
  - "Aparece alguna vez" en un periodo ⇔ **≥ 1** respuesta válida con la clínica en alguna
    de sus ejecuciones.
  - Nivel sin objetivo y que no se promete (ADR-005 §6).
- **Asimetría conocida**: el "antes" de `AR` es una sola ejecución de 1 run. Se acepta: no
  es criterio Go.
- **Posición** (RN-06): puesto de la clínica en `brands_mentioned`, que ya excluye
  directorios. Se da como **lista de puestos**, sin media.
- Una cadena es una marca: ya es así en `brands.csv` (Dorsia, Medical Hair…).
- `summary.md` lista por nivel las casillas con la clínica. La comparación entre
  ejecuciones la hace SPEC-012 (F-SPEC-008-10).

### (h) "Ártica" como adjetivo — **correcto con condiciones** (P-1, F-SPEC-008-3)
- RN-01 literal: "Ártica" suelta **cuenta** en el probe, igual que en la manual. No se
  descuenta nada a mano, ni en el baseline ni en las mediciones "después".
- `summary.md` lista las respuestas en que la clínica aparece **solo** por "Ártica" suelta
  (sin "Clínica Ártica", "Ártica Medicina Estética" ni `clinicaartica`), por nivel. Así se
  pueden leer y anotar como adjetivo en el ledger. Configuración: `client_review_aliases`.
- El veredicto informa cuántas hay en cada medición. También dice si quitar las de uso
  adjetivo cambiaría el sí/no de alguna Δ. Es sensibilidad **informativa**: la cifra del Go
  es la literal, fijada antes de ver datos.

### (i) URLs consultadas y citadas (SPEC-013) — **correcto**
- El SoV del Go usa solo el texto de la respuesta (RN-01/RN-02).
- `searched_urls` y `cited_urls` **no** son mención: una URL de la clínica en esas columnas
  sin su nombre en el texto no cuenta. Sí cuenta el dominio `clinicaartica` si está en el
  texto, que es el alias de siempre.
- El baseline oficial es el primer fichero del piloto con las dos columnas y significado
  homogéneo en los tres proveedores. Es el que usa SPEC-011 CA-1 para fuentes (dictamen
  SPEC-013, punto 4). No se mezcla con el humo antiguo de Viveiro, sin `searched_urls` y con
  `cited_urls` de Gemini en el significado anterior.
- El directorio nuevo garantiza que `--resume` no mezcle ficheros.
- Si la web de la clínica aparece entre las consultadas o las citadas, es un indicador de
  fuentes de SPEC-011 ("consultada por"), sin peso. No entra en el Go.

### Tabla condición → cambio
| Condición | Cambio | Dónde |
|---|---|---|
| (a) baseline `AV` 3 runs, `AR`/`AG` 1, una ejecución | `levels[].runs` = 3/1/1; comando simple = baseline | `probe/batches/viveiro.json`; README "Batches"; instrucciones CA-7 paso 3; `test_ca9_config_fixes_the_go_instrument`, `test_ca5_simple_pilot_command_uses_runs_per_level` |
| (a)/(c) medición completa (≥ 90 % `ok` por proveedor con peso) | `go.min_valid_share`; línea "Medición completa para el criterio Go" | `viveiro.json`; `analysis.py` (`analyze_levels`, `_core_go_lines`); `test_ca9_go_measurement_complete_only_with_enough_valid_rows_per_provider` |
| (a) congelación al inicio del baseline | Registro previo al comando del baseline | Instrucciones CA-7 paso 3; "Registro de la congelación del set" |
| (b) runs sumados por proveedor; ponderado normalizado con Claude | Sin cambio de cálculo; rótulo "runs sumados por proveedor" | `analysis.py`; `test_ca9_weighted_sov_per_run_and_pooled`, `test_ca3_core_weighted_sov_uses_only_av` |
| (c) "después" = `AV` 3 runs, semanas 11 y 12 ± 1, ≥ 7 días | Comando `--levels AV` con directorio fechado | README "Batches"; F-SPEC-008-5 (→ SPEC-012) |
| (d) Δ ≥ +15 en cada "después", mismos `brands.csv`/pesos | Regla para el veredicto; `--analyze` de los tres | F-SPEC-008-5 y F-SPEC-008-10 (→ SPEC-012 CA-7) |
| (e) ruido: ponderado por run y estabilidad por casilla | Tabla "por run" y línea de estabilidad en `AV` | `analysis.py` (`_core_go_lines`); `test_ca9_weighted_sov_per_run_and_pooled`, `test_ca9_stability_per_question_and_provider` |
| (f) mismo instrumento; modelos servidos | Tabla "Modelos servidos"; revisión de `request` y del modelo por defecto antes de cada medición | `analysis.py`; `test_ca9_models_served_are_reported`; instrucciones CA-7 pasos 0 y 2 |
| (f) F-SPEC-013-5 antes del baseline | Humo de seguimiento y umbral antes del paso 3 | Instrucciones CA-7 pasos 1–2 |
| (g) `AR`/`AG`: casillas con la clínica | Línea "Casillas pregunta × proveedor con Clínica Ártica" por nivel, sin % | `analysis.py`; `test_ca9_levels_outside_core_list_cells_with_client_without_percentages` |
| (h) "Ártica" suelta cuenta y se lista | `client_review_aliases`; línea por nivel | `viveiro.json`; `analysis.py` (`_bare_lines`); `test_ca9_bare_artica_answers_are_counted_and_flagged_for_review` |
| (i) URLs no son mención; directorio nuevo | Sin cambio de cálculo; baseline en `piloto-artica/probe` (nuevo) | README "Batches"; instrucciones CA-7 |
| CA-10 aviso de techo ≥ 85 %, solo `AV` | `go.ceiling`; línea "Aviso de techo" | `viveiro.json`; `analysis.py` (`_ceiling_warning`); `test_ca10_*` |

**Enmienda (d) (ADR-009)**: siguen valiendo (a), (b), (c), (e), (f), (h) e (i). El punto (d)
(Δ ≥ +15 pts en el núcleo) queda sustituido por CA-11 (ii) y (iii), y el punto (g), en lo que
toca a `AR`, por CA-11 (i) y (ii). En `AG`, (g) sigue igual.

## Dictamen sdd-metricas (CA-11)
- **Fecha**: 2026-09-29. Es anterior al "antes" de `AR` (CA-12, sin lanzar: no existe
  `$PUSHLLM_PRIVADO/piloto-artica/probe-AR-antes/`) y a la primera acción del piloto.
  **Emisor**: sdd-implementador aplicando `.ai-context/skills/sdd-metricas.md` (advisory: no
  cambia reglas).
- **Fuentes**:
  - ADR-009 (§1–§6), ADR-005 §4 y §6, EPIC-002 criterio 4;
  - `docs/fundacion/reglas.md` RN-01–RN-04, RN-07, RN-10, RN-11;
  - dictámenes CA-9 (arriba) y (g)–(j) de SPEC-007;
  - el baseline oficial (CA-7) y su evidencia privada
    (`$PUSHLLM_PRIVADO/piloto-artica/probe/summary.md`, `ca7-baseline-evidencia.md`), leídos
    solo para estimar el ruido. Aquí van solo reglas, umbrales y probabilidades, sin cifras de
    visibilidad (ADR-004 §2).
  - Simulación Monte Carlo propia (binomial por casilla, con y sin deriva semanal) para las
    probabilidades de (ii) y (iii). No se guarda en el repo: es un cálculo de apoyo.
- **Opción de medición: A**, decidida por el humano el 2026-09-29 (ver "Decisiones del
  humano"): más runs con las mismas 5 preguntas `AR`. No se reabre la congelación.
- **¿Cambia alguna regla de negocio? No.**
  - (C) aplica la fórmula de RN-03/RN-04 a las filas `AR` solas, como permite ADR-009 §5.
  - Las reglas de mención (RN-01, RN-02, RN-11) son las del núcleo.
  - Ninguna cifra combina niveles (ADR-009 §2).
  - La cifra de `AR` es interna del Go. Cómo se cuenta a la clínica es de SPEC-009.

### (i) Diseño de medición de `AR` — **correcto con condiciones**
- **Preguntas**: las 5 `AR` congeladas (`AR01`–`AR05`, sin cambios de id ni de texto).
- **Runs**: **3 por pregunta × proveedor**, en el "antes" y en cada "después". Son los mismos
  runs que el núcleo, así que el instrumento es uno solo.
- **Cifra**: el **SoV ponderado de `AR`**. Se calcula como el del núcleo, pero solo con filas
  `AR`:
  - SoV bruto por proveedor = respuestas válidas con la clínica ÷ respuestas válidas, con los
    3 runs sumados;
  - después se pondera con RN-04 (ChatGPT 0,55, Gemini 0,25, Claude 0,10), normalizado a los
    proveedores con respuestas válidas.
  - Se elige frente al recuento de casillas porque respeta RN-03 (pesa por uso). Además, con
    el mismo riesgo de Go falso, detectó más subidas reales en la simulación.
- **"Antes"**: una ejecución `--levels AR --runs 3` en un directorio nuevo, **antes de la
  primera acción** (CA-12).
  - Las filas `AR` de 1 run del baseline oficial **no** sirven como base de (C): tienen otro
    diseño.
  - Siguen siendo la ejecución de la semana 0 del seguimiento.
- **"Después"**: **dos** mediciones, en las mismas semanas que las del núcleo (CA-9 (c)):
  - semanas 11 y 12 desde la primera acción, ± 1, con ≥ 7 días entre sus inicios;
  - cada una es una sola ejecución `--levels AV,AR` con 3 runs en los dos niveles;
  - si una no queda completa, se repite entera dentro de la ventana, como en CA-9 (c).
- **Seguimiento**: `AR` con 1 run cada 4 semanas (semanas 4 y 8). Es solo tendencia: su
  cifra nunca se compara con el "antes" ni entra en (C). Por eso `summary.md` solo da el
  ponderado de `AR` cuando la medición tiene los 3 runs del diseño.
- **Medición completa** de `AR`: cada proveedor con peso tiene ≥ 90 % de sus filas `AR` con
  `status=ok` (misma regla que CA-9 (a).2). Si no, `--resume` en la misma semana.
- La regularidad de `AR` del dictamen CA-9 (g) ("≥ 2 casillas en las dos ejecuciones") queda
  sustituida por (C). Para `AG`, CA-9 (g) sigue igual.

### (ii) Umbral de crecimiento y regla de estabilidad, condición (C) — **correcto con condiciones**
- **(C) ⇔ en cada una de las dos mediciones "después"** (no en su media) se cumplen las dos
  cosas:
  1. **Subida**: Δᵢ = ponderado `AR` después i − ponderado `AR` antes **≥ +12,0 pts**.
  2. **Amplitud**: al quitar **cualquier** pregunta `AR` (sus filas, en el antes y en el
     después) y recalcular, Δᵢ sigue **> 0**. Es decir, la subida no depende de una sola
     pregunta.
- La regla se calcula sin redondear y solo con mediciones completas y con 3 runs. Si falta
  algo, la condición es "no decidible" y la medición se repite.
- **Por qué +12**: con 5 preguntas, una pregunta que pasa entera a mencionar la clínica en
  ChatGPT mueve el ponderado +12,2 pts; en Gemini, +5,6; en Claude, +2,2. +12 pide como mínimo
  el equivalente a una pregunta entera en ChatGPT. La amplitud obliga a que haya al menos una
  segunda pregunta que suba.
- **Ruido y probabilidades** (simulación con casillas desde estables hasta 6 de 15
  inestables, p = 0,35–0,5, con y sin deriva semanal, en la que el 10 % de las casillas cambia
  de probabilidad cada semana):
  - **Go falso** (sin cambio real): **0–4 %**.
  - **Detectar una subida real** de 2 preguntas en ChatGPT y Gemini (p = 0,8): **49–97 %**.
    Si la subida es de 2 preguntas en ChatGPT y 1 en Gemini: **34–87 %**. Los valores bajos
    corresponden a muchas casillas inestables y deriva.
  - Una subida de **una sola pregunta** en los 3 proveedores pasa solo en el 18–32 % de los
    casos, y siempre por ruido de otras preguntas: la amplitud la frena a propósito.
  - Igual que la regla del núcleo (CA-9 (e)), la regla es **conservadora**: se prefiere no
    dar un Go falso a detectar toda subida real.
- **Informativo** (no cambia el sí/no): el veredicto da |Δ₁ − Δ₂| (deriva de semana a
  semana), las casillas que ganan o pierden a la clínica y la sensibilidad a "Ártica" adjetivo
  (CA-9 (h)).

### (iii) Umbral de defensa del núcleo, condición (D) — **correcto con condiciones**
- **Caída significativa ⇔ Δᵢ ≤ −10,0 pts en las dos mediciones "después"**.
  - Δᵢ = ponderado del núcleo después i − ponderado del núcleo del baseline oficial (CA-7).
  - Se calcula sin redondear, con las dos mediciones de CA-9 (c): `AV`, 3 runs, completas.
- **(D) se cumple ⇔ no hay caída significativa.** Una sola medición con caída no basta para
  romper (D). Es la misma exigencia de estabilidad que en (C), en sentido contrario.
- **Por qué −10 y en las dos**: se estimó con las cifras privadas del baseline.
  - La dispersión entre runs del mismo día es menor que el umbral.
  - El error típico de una diferencia queda entre ≈ 4 pts (runs independientes) y ≈ 7 pts
    (runs idénticos del mismo día).
  - **Caída falsa** (sin cambio real): 0,1–2,4 %.
  - **Detectar una caída real** de −15 pts: 63–82 %; de −20 pts: 86–99 %. Una caída real de
    −10 pts se detecta en torno a un tercio de las veces.
  - Exigir la caída en **una** sola medición subiría la caída falsa hasta ≈ 15 %: el Go
    fallaría por ruido.
- Con el núcleo por encima del umbral de techo, una subida no aporta nada a (D). (D) solo
  mira caídas.
- **Informativo**: Δ de cada medición y ponderado por run (CA-9 (e)).

### (iv) Mismo instrumento en `AR` — **correcto con condiciones**
- Se aplica entero CA-9 (f). Son idénticos entre el "antes" de `AR` y los "después":
  - el set congelado;
  - los runs (3);
  - la ubicación Viveiro/Galicia/ES;
  - los prompts y la configuración de la petición;
  - los pesos y los alias. El veredicto recalcula los `summary` con el **mismo**
    `brands.csv` y `probe_config.json`.
  - Se comprueba con el `request` de `raw_responses.jsonl`: mismos campos salvo `model`.
- **Modelo por defecto**:
  - Antes de lanzar CA-12, `sdd-probe` comprueba que el modelo por defecto y los precios de
    cada app siguen siendo los de `probe_config.json`.
  - Si **no** han cambiado, CA-12 se lanza. Su petición es la del baseline oficial.
  - Si **han** cambiado antes de la primera acción, CA-12 se lanza con el modelo nuevo
    (RN-10) y, como dice CA-9 (f), se repite también el baseline del núcleo antes de la
    primera acción. Así las bases de (C) y de (D) usan el mismo modelo.
  - Si cambia **después** de la primera acción, la comparación sigue valiendo, se anota y no
    se rehace nada (CA-9 (f)).
- CA-12 va días después del baseline del núcleo. Se acepta (ADR-009 §4): sigue siendo
  anterior a la primera acción.

### (v) ¿Bastan 5 preguntas? — **sí, con condiciones**
- **Sí** para fijar (ii) con una regla decidible:
  - con 3 runs, un Go falso queda en ≤ 4 % en todos los escenarios de ruido simulados;
  - la amplitud impide que el Go descanse en una sola pregunta, que es la salvedad del
    arquitecto.
- **Límites que se aceptan** (lo que la opción A no arregla):
  1. **Potencia moderada**: una subida real de 2 preguntas puede no verse en el 3–66 % de
     los casos. El (C) de este piloto puede dar "no" con una mejora real pequeña.
  2. **Alcance**: (C) habla de las 5 preguntas y de sus zonas (Ferrolterra, norte e interior
     de Lugo, occidente de Asturias), no de "todo el área de influencia".
  3. Más runs (5) apenas mejoran la potencia en la simulación (+3–13 pts) y no caben en el
     mes del cierre. La potencia la limitan las 5 preguntas y la deriva semanal, no los runs.
- **No se recomienda la opción B.** Si el humano quiere más potencia o más alcance, la
  palanca es la opción B (más preguntas), que decide él. Así no hace falta para decidir.

### Tabla condición → cambio (CA-11)
| Condición | Cambio | Dónde |
|---|---|---|
| (i) `AR` 3 runs en "antes" y "después" | `levels[AR].runs` = 3; `go.growth.runs` = 3; comando CA-12 `--levels AR --runs 3` | `probe/batches/viveiro.json`; README "Batches"; "Instrucciones para el humano (CA-12)"; `test_ca11_config_fixes_growth_and_defense`, `test_ca5_simple_pilot_command_uses_runs_per_level`, `test_ca12_ledger_command_is_the_ar_before_with_the_design_of_ca11` |
| (i) cifra = ponderado de `AR` solo con filas `AR`; solo con los runs del diseño | `analyze_levels` → `growth`; línea "SoV ponderado de AR" (o "no se da" con otros runs) | `probe/analysis.py` (`_growth_lines`); `test_ca11_ar_weighted_uses_only_ar_rows`, `test_ca11_ar_summary_gives_its_own_weighted_only_with_design_runs` |
| (i) medición `AR` completa (≥ 90 % `ok`) | "Medición completa para la condición (C)" | `analysis.py`; `test_ca11_ar_measurement_incomplete_with_errors` |
| (i) "después" = `--levels AV,AR`, semanas 11 y 12 ± 1 | Comando del README; cadencia | README "Batches"; F-SPEC-008-5 y F-SPEC-008-14 (→ SPEC-012) |
| (ii) Δ ≥ +12 en cada "después" + amplitud (quitar una pregunta, Δ > 0); no decidible sin diseño | `go.growth.min_rise_pts` = 12, `after_measurements` = 2; `growth_verdict` | `viveiro.json`; `analysis.py`; `test_ca11_growth_needs_rise_in_both_afters_and_more_than_one_question`, `test_ca11_growth_threshold_is_inclusive_and_unrounded`, `test_ca11_growth_not_decidable_with_other_design_or_incomplete` |
| (iii) caída ⇔ Δ ≤ −10 en las dos; (D) se cumple si no | `go.defense.max_drop_pts` = 10; `defense_verdict` | `viveiro.json`; `analysis.py`; `test_ca11_defense_fails_only_with_a_drop_in_both_afters` |
| ADR-009 §2: (C) y (D) por separado, sin mezclar niveles | `render_go_verdict` con secciones (C), (D) y (A) separadas; etiquetas de nivel | `analysis.py`; `test_ca11_verdicts_do_not_mix_levels`, `test_ca11_go_verdict_report_gives_c_and_d_apart`; `test_ca3_core_weighted_sov_uses_only_av` (sigue en verde) |
| (iv) mismo instrumento; modelo por defecto antes de CA-12 | Comprobación de `sdd-probe` antes del comando | "Instrucciones para el humano (CA-12)" paso 0 |
| CA-10 decidido | Texto del aviso de techo con la decisión (ADR-009) | `analysis.py` (`_ceiling_warning`); `test_ca10_*` |
| Veredicto entre ejecuciones (lectura de los `results.csv` y el comando) | Funciones listas; el comando y el informe son de SPEC-012 | F-SPEC-008-10 (→ SPEC-012) |

## Dependencias
Reescrito el 2026-09-29 por la enmienda (b) (F-SPEC-008-9.5). CA-7 (baseline oficial del Go)
depende de:
- **SPEC-013 en `hecho`**: **cumplido** el 2026-09-29 (commit `0ed5384`, veredicto GREEN).
  El probe escribe `searched_urls` y `raw_responses.jsonl`.
- **Dictamen CA-9**: **cumplido** el 2026-09-29 (arriba), antes del baseline.
- **Claves (SPEC-002 CA-1)**: cumplido. Están en el `.env` de la raíz y el humo de Viveiro
  del 2026-09-29 dio 9/9 `ok`.
- **Set congelado (SPEC-007 CA-8)**: se congela **al empezar el baseline oficial**, salvo que
  el humano fije antes otra fecha en el ledger de SPEC-007. El texto de los tres niveles es el
  de `docs/piloto-artica/prompts-baseline.md`. Si cambiara antes de la congelación,
  `test_ca1_pilot_prompts_equal_to_frozen_set_id_and_literal_text` falla y obliga a
  sincronizar `prompts.csv`. Registro: "Registro de la congelación del set", abajo.
- **Ya no depende** de ninguna pasada manual de SPEC-007. La pasada "antes" de calibración va
  **después** del baseline y emparejada con él (ventana del dictamen (k) de SPEC-007).

## Instrucciones para el humano (CA-7)
Reescritas el 2026-09-29 (enmienda (b)). **Ejecutadas el 2026-09-29.** Desde CA-11, el
comando simple del paso 3 lanza `AR` con 3 runs: no se repite. El siguiente paso es CA-12.
**Orden**:
1. humo de seguimiento (F-SPEC-013-5);
2. SPEC-013 `hecho` (ya) y dictamen CA-9 (ya);
3. congelación del set, que se registra justo antes del baseline;
4. **baseline oficial**;
5. revisión del Aviso de techo (CA-10);
6. primera acción del piloto (SPEC-012).
Ninguna acción del piloto antes del paso 5.

`PUSHLLM_PRIVADO` ya es variable de usuario: no se fija aquí. Sin activar el venv: se llama
a `.\.venv\Scripts\python` directamente. **Claves** (ADR-006, ADR-007): en el `.env` de la
raíz del repo. El probe lo carga solo, nunca pisa una variable ya definida en la sesión y
nunca escribe los valores. En PowerShell, desde la raíz del repo:

```powershell
cd probe
if (-not $env:PUSHLLM_PRIVADO) { throw "PUSHLLM_PRIVADO no está definida" }

# 0) Comprobación offline (sin claves ni red): todo en verde
.\.venv\Scripts\python -m pytest -q tests

# 1) HUMO DE SEGUIMIENTO (F-SPEC-013-5): 3 preguntas x 1 run x 3 proveedores = 9 llamadas, ~0,35 EUR
#    Directorio NUEVO: el humo antiguo (probe-smoke) no tiene searched_urls
.\.venv\Scripts\python run_probe.py --config batches/viveiro.json --only AV01,AR01,AG01 --runs 1 --out "$env:PUSHLLM_PRIVADO\piloto-artica\probe-smoke-spec013"
Select-String "lote \| total" "$env:PUSHLLM_PRIVADO\piloto-artica\probe-smoke-spec013\summary.md"
Import-Csv "$env:PUSHLLM_PRIVADO\piloto-artica\probe-smoke-spec013\results.csv" | Where-Object provider -eq "openai" | Measure-Object -Property web_searches,cost_eur -Average | Select-Object Property,Average

# 2) Decide con el paso 1 (umbrales abajo). Si alguno salta, PARA y avisa: no hay baseline.

# 3) BASELINE OFICIAL DEL GO: AV 3 runs + AR/AG 1 run = 54 preguntas x 3 proveedores = 162 llamadas, ~6,2 EUR
#    Registra la congelación del set JUSTO ANTES (su inicio congela el set, SPEC-007 CA-8)
if (git status --porcelain -- prompts.csv ..\docs\piloto-artica\prompts-baseline.md) { throw "el set tiene cambios sin commit" }
"congelacion_set_utc=$((Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')) commit=$(git rev-parse --short HEAD)" | Tee-Object -FilePath "$env:PUSHLLM_PRIVADO\piloto-artica\congelacion-set.txt"
.\.venv\Scripts\python run_probe.py --config batches/viveiro.json

# 4) Si se corta: repite la MISMA línea del paso 3 añadiendo --resume (solo llama lo que falta; misma semana)
# 5) Aviso de techo (CA-10) y validez: léelo antes de cualquier acción
Select-String "Aviso de techo|SoV ponderado del núcleo \(|Medición completa|lote \| total" "$env:PUSHLLM_PRIVADO\piloto-artica\probe\summary.md"

# 6) Recuento offline cuando quieras (sin llamadas)
.\.venv\Scripts\python run_probe.py --config batches/viveiro.json --analyze
```

**Umbrales del paso 2** (decídelos con los números del paso 1; `c'` = "lote | total" ÷ 3):
- **F-SPEC-013-5 (OpenAI)**: se compara con dos referencias.
  - Humo de SPEC-002: 1 búsqueda por llamada, 0,0119 € de media.
  - Humo antiguo de Viveiro, **mismas 3 preguntas** y sin `include`: 1,33 búsquedas por
    llamada (1, 1, 2) y 0,0146 € de media.
  - Si la media de `web_searches` de OpenAI es **≥ 1,67** (≈ 2) **y** su coste medio por
    llamada supera **0,0144 €** (+20 % sobre 0,012 €), se reabre con `sdd-probe` y el humano
    decide sobre el `include` **antes** del baseline (dictamen CA-9 (f): cambiarlo después
    rompe el instrumento).
  - Ojo: el humo antiguo de Viveiro ya pasaba de 0,0144 € con 1,33 búsquedas. La señal que
    importa es la subida de búsquedas por llamada frente a las mismas preguntas.
- **Coste (CA-5)**:
  - `c' ≤ 0,1307 €`: sigue.
  - `0,1307 € < c' ≤ 0,155 €`: sigue, y en el mes del cierre se aplican las palancas de CA-5.
  - `c' > 0,155 €`: PARA.
- **Modelos**: la tabla "Modelos servidos" del `summary.md` del humo debe coincidir con
  `probe_config.json` (dictamen vigente de `sdd-probe`). Si no, PARA.

**Qué avisar después del paso 5**:
- la línea de `congelacion-set.txt`;
- fecha y hora de inicio y fin;
- nº de llamadas por estado (tablas de `summary.md`);
- coste total;
- modelos servidos;
- "Medición completa" sí/no;
- si aparece el **Aviso de techo**.
Con eso el agente rellena CA-7 y el registro de congelación.

**Si sale el Aviso de techo** (ponderado del núcleo ≥ 85 %): antes de la primera acción, el
humano decide y se registra aquí, con fecha, una de estas opciones:
- mantener el criterio;
- medir sobre un subconjunto de `AV` (p. ej. Lugo o capilar);
- cambiar el umbral.
Nunca se decide después de ver el efecto (CA-10).

- Salida: `$env:PUSHLLM_PRIVADO\piloto-artica\probe\` con `results.csv` (con
  `searched_urls`), `raw_responses.jsonl` y `summary.md`. Es un directorio nuevo: no existía
  el 2026-09-29. Nada al repo (ADR-001/ADR-004). El probe rechaza un `--out` vacío o raíz de
  unidad, y `--resume` sobre un `results.csv` anterior a SPEC-013.
- Si la primera acción ya hubiera ocurrido sin baseline del probe, no hay criterio Go
  (CA-7): avisa y no lances nada.
- Antes del paso 1, `sdd-probe` (orquestador) confirma que el modelo por defecto de cada app
  y los precios siguen siendo los de `probe_config.json` (dictamen CA-9 (f)).

### Registro de la congelación del set (SPEC-007 CA-8)
Preparado el 2026-09-29. Lo rellena el agente con lo que avise el humano tras el paso 3:
| Campo | Valor |
|---|---|
| Fecha y hora UTC de congelación (inicio del baseline, `congelacion-set.txt`) | **2026-09-29T15:30:43Z** |
| Commit del repo en ese momento (`prompts.csv` y `prompts-baseline.md` sin cambios pendientes) | **`60863af`** (sin cambios pendientes en el set; `git diff 60863af HEAD` de los dos ficheros vacío el 2026-09-29) |
| Preguntas congeladas | `AV01`–`AV15`, `AR01`–`AR05`, `AG01`–`AG04` (24), texto literal de `docs/piloto-artica/prompts-baseline.md`; copia en `probe/tests/fixtures/pilot-set-frozen.tsv` |
| Primera fila `timestamp_utc` de `piloto-artica/probe/results.csv` | **2026-09-29T15:31:12Z** (última 16:15:10Z) |

Registrado el 2026-09-29 por sdd-implementador. Hecho el paso 1 de abajo (fixture y
`test_ca7_pilot_prompts_equal_to_set_frozen_at_official_baseline`); el paso 2 queda para el
orquestador: fecha **2026-09-29T15:30:43Z**, commit `60863af`, al ledger de SPEC-007 CA-8.

- Tras el registro, el agente:
  1. copia en `probe/tests/fixtures/pilot-set-frozen.tsv` las 24 filas (`id`, `prompt`) del
     commit registrado, con un test que compare `prompts.csv` con esa copia (patrón de
     `docs/piloto-artica/tools/tests/av-2026-09-29.tsv`);
  2. pasa la fecha al orquestador para el ledger de SPEC-007 CA-8. Este implementador no
     edita ese ledger.
- Desde esa fecha, una pregunta nueva lleva id nuevo, se informa aparte y no cuenta para
  el Go.

## Instrucciones para el humano (CA-12)
Preparadas el 2026-09-29 (sdd-implementador) con el diseño del dictamen CA-11. Es el "antes"
de `AR` de la condición (C). Se lanza **antes de la primera acción** del piloto y en un
directorio nuevo. Comprobado offline con `test_ca12_ledger_command_is_the_ar_before_with_the_design_of_ca11`:
lanza 45 llamadas (15 por proveedor), solo `AR01`–`AR05`, runs 1–3, y la medición sale
completa con 3 runs. Coste ≈ 1,9 € (CA-5).

Orden:
0. `sdd-probe` (orquestador) confirma que el modelo por defecto y los precios de cada app
   siguen siendo los de `probe_config.json` (CA-11 (iv)). Si han cambiado, PARA: se aplica
   CA-11 (iv) (CA-12 con el modelo nuevo y repetición del baseline del núcleo).
1. Lanzar el comando de abajo.
2. Leer las líneas de validez.
3. Avisar al agente, que rellena CA-12 en la matriz.
4. Después, primera acción del piloto (SPEC-012).

En PowerShell, desde `probe\` (claves en el `.env` de la raíz; `PUSHLLM_PRIVADO` como variable
de usuario):

```powershell
if (-not $env:PUSHLLM_PRIVADO) { throw "PUSHLLM_PRIVADO no está definida" }
if (Test-Path "$env:PUSHLLM_PRIVADO\piloto-artica\probe-AR-antes\results.csv") { throw "ya existe: no repetir sin --resume" }

# CA-12: "antes" de AR del Go (opción A): 5 preguntas x 3 runs x 3 proveedores = 45 llamadas, ~1,9 EUR
.\.venv\Scripts\python run_probe.py --config batches/viveiro.json --levels AR --runs 3 --out "$env:PUSHLLM_PRIVADO\piloto-artica\probe-AR-antes"

# Si se corta: repite la MISMA línea añadiendo --resume (misma semana)
# Validez: medición completa de (C), runs, coste y modelos
Select-String "SoV ponderado de AR|Medición completa para la condición \(C\)|lote \| total" "$env:PUSHLLM_PRIVADO\piloto-artica\probe-AR-antes\summary.md"
```

**Qué avisar**:
- fecha y hora de inicio y fin;
- número de llamadas por estado (tablas de `summary.md`);
- coste total;
- la tabla "Modelos servidos";
- "Medición completa para la condición (C)": sí/no.
La línea "SoV ponderado de AR" debe salir con cifra, no con "no se da"; si sale "no se da",
faltan runs. Las cifras de visibilidad se quedan en el espacio privado (ADR-004): al ledger
solo van los veredictos.

## Decisiones del humano
Del 2026-09-29, **decidido por el humano (Alberto Fojo)**:
- **(a) Competidoras sin médico visible**: Luxury Clínica y Clínica Pío Vila Ayán **sí
  cuentan** como competidoras (cierra la pregunta de F-SPEC-008-2). Añade: "sería
  destacable que la IA explicitase que no tienen médico". Aplicado así: el `summary.md` del
  lote Viveiro termina con "Observaciones para revisar a mano (no es una métrica)", que
  lista las frases de respuestas válidas que nombran una clínica junto a expresiones de
  `batch.review_terms` ("sin médico", "no médico", "esteticista", "no sanitario"…). Es
  coincidencia literal por frase, barata y con falsos positivos posibles (la frase puede
  hablar de otra clínica), por eso solo se lista para leer a mano y no cuenta en ninguna
  cifra. Tests `test_review_observations_*`. Follow-up F-SPEC-008-7.
- **(b) Cadencia**: **aceptada**: `AV` semanal con 1 run; `AR` y `AG` cada 4 semanas; en el
  baseline, 3 runs en `AV` si el humo da `c ≤ 0,19 €` y 2 si no (F-SPEC-008-5).
- ~~**Orden**: el baseline del probe va después de la pasada 1 manual de SPEC-007; el humo
  puede ir antes.~~ **Sustituida** por la enmienda (b), re-aprobada por el humano el
  2026-09-29. El probe es el instrumento del Go. Orden: humo → baseline oficial (congela el
  set) → aviso de techo → primera acción. La pasada manual "antes" va después del baseline,
  emparejada con él (SPEC-007).
- **(c) CA-10, aviso de techo (2026-09-29, decidido por el humano)**: en el baseline oficial
  saltó el aviso de techo. El humano decidió, **antes de la primera acción**, cambiar el
  criterio Go a "crecer fuera, defender dentro": (C) crecer en `AR`, (D) defender `AV`
  frente al baseline oficial y (A) ≥ 1 paciente atribuido (ADR-009, aprobado el 2026-09-29;
  EPIC-002, criterio 4). No eligió ninguna de las tres opciones de CA-10. Cierra
  F-SPEC-008-12.
- **(d) Medición de `AR`: opción A (2026-09-29, decidido por el humano)**: más runs con las
  mismas 5 preguntas `AR`. **No se reabre la congelación** del set. Los runs, los umbrales y
  la regla los fija el dictamen CA-11.
- **(e) Recorte de coste (2026-09-29, decidido por el humano)**: si el mes del cierre supera
  20 €, lo primero es pasar `AG` a **cada 8 semanas**. Las palancas siguientes, en orden,
  están en el dictamen `sdd-probe` (CA-5, "Opción A y diseño de CA-11").

## Veredicto del verificador
<!-- GREEN/RED + fecha + resumen. Lo escribe SOLO sdd-verificador. -->

**Verificación intermedia 2026-09-29, CA-7 pendiente** (sin transición de estado; no es el
veredicto de cierre). Parte offline apta para que el humano lance humo y baseline: CA-3,
CA-4, CA-5, CA-8 ✅; CA-1, CA-2, CA-6 ⚠️ con salvedades no bloqueantes para la ejecución.
Gates: `pytest probe/tests` 133 verde, `pytest docs/piloto-artica/tools/tests` 143 verde,
`ruff check probe` limpio. Ningún test llama a `main` sin `env` y `ask` falsos ni a
`providers.ask` sin cliente falso: `pytest` con las claves puestas no hace llamadas de pago.
Findings: (1) media — README "Batches": el comando de baseline lanza 24 × 3 runs (216
llamadas), fuera de la cadencia de CA-5; usar las instrucciones de este ledger. (2) baja —
alias "villoria" de Villoria L'Essence recoge en el lote piloto menciones de "Clínica
Villoria" (oftalmología), posible sobreconteo en `AG03/AG04`. (3) baja — alias
`clinicavirxedamariña` no casa con el dominio punycode `xn--clinicavirxedamaria-d4b`. (4)
baja — si `PUSHLLM_PRIVADO` está vacío, el `--out "$env:PUSHLLM_PRIVADO\piloto-artica\..."`
del humo apunta a la raíz de la unidad; comprobar la variable antes. (5) dependencia — el
set no está congelado (SPEC-007 CA-8): si el baseline del probe se lanza antes de la
pasada 1 y el set cambia después, el baseline no sirve. Al cierre: CA-7 y repetir CA-8.

**Re-verificación offline 2026-09-29 en la punta de la rama SPEC-002** (sdd-verificador;
sin transición de estado: CA-7, baseline real, sigue pendiente). Cambios revisados desde
`01cb09d`: modelos del dictamen vigente de SPEC-002 (Claude `claude-sonnet-5-5`), effort
`medium` y `max_tokens` 16000 de Claude, cambio BCE 1,1378, carga del `.env` en
`run_probe.py` (con `conftest.py` autouse) y la nota de la spec que remite a ADR-008 (no
cambia CA). Sin cambios desde `01cb09d` en `prompts.csv`, `brands.csv`, `batches/`,
fixtures ni en la sección `batch` de `probe_config.json`. Gates: `pytest probe/tests
docs/piloto-artica/tools/tests` → 317 passed (`test_pilot_batch.py` 50 passed); `ruff
check probe` limpio. CA-1…CA-6 se siguen cumpliendo como en la intermedia (mismas
salvedades de CA-1, CA-2 y CA-6). CA-4: golden de Vigo regenerado por el verificador
(`--analyze` con `env={}`, sin `.env`, sobre `tests/fixtures/vigo_results.csv`) →
**idéntico** a `vigo_summary_before.md` (salvo CRLF). CA-5: el cambio de tipo (+0,3 %) y
el effort `medium` no rompen el dictamen; humo de Viveiro medido c = 0,1142 € ≤ 0,19 €.
**CA-8 ahora no se cumple en el árbol local**: `git status --ignored` muestra `probe/out/`
con `piloto-artica/probe/{results.csv,summary.md}` sintéticos (2026-09-29 12:58, modelo
`claude-sonnet-5`, F-SPEC-002-5); la suite actual no los regenera (mtime intacto tras
`pytest`). `git ls-files` sigue sin salidas del lote. Borrar `probe/out/` antes del cierre.
Humo de Viveiro (informativo para CA-7): 9/9 `ok`, modelos = dictamen, Claude 0 de 3
`cited_urls` (F-SPEC-002-7, a arreglar antes del baseline en spec aparte).

## Evidencia visual
<!-- Tabla CA → captura en _qa/SPEC-008/. Informe HTML opcional: _qa/SPEC-008/informe.html -->

## Salvedades / follow-ups
- **F-SPEC-008-1** (→ sdd-implementador, tras la pasada 1 de SPEC-007 y el humo): añadir,
  con la misma verificación, las competidoras que aparezcan en las respuestas reales
  (sobre todo `AR`/`AG`) y reconsiderar las pendientes. Al añadirlas, listarlas en
  `batches/viveiro.json` (y nunca en el lote Vigo).
- **F-SPEC-008-2** (cerrado 2026-09-29): Luxury Clínica y Clínica Pío Vila Ayán no nombran
  médico en su web; el humano decidió que **sí cuentan** ("Decisiones del humano" (a)).
- **F-SPEC-008-3** (→ sdd-metricas / SPEC-012): el probe cuenta "Ártica" también como
  adjetivo (P-1) y no marca `#artica-adjetivo` como el recuento manual; para el probe se
  revisa a mano leyendo las respuestas con la clínica si la cifra lo pide.
- **F-SPEC-008-4** (→ SPEC-002 / quien mantenga el lote Vigo): desde este cambio, una marca
  nueva del lote Vigo se añade en `brands.csv` **y** en `batch.brands` de
  `probe_config.json`; si falta en ambos lotes, `test_ca4_every_brand_belongs_to_some_batch`
  falla. No afecta a la ejecución de SPEC-002 (mismos comandos, misma salida).
- **F-SPEC-008-5** (→ SPEC-012, **aceptada por el humano el 2026-09-29**): cadencia del
  probe del piloto: `AV` semanal con 1 run
  (`--levels AV --runs 1 --out "$env:PUSHLLM_PRIVADO\piloto-artica\probe-AAAA-MM-DD"`);
  `AR` y `AG` cada 4 semanas con 1 run (`--levels AR,AG`); baseline con 3 runs en `AV` si
  el humo da `c ≤ 0,19 €` y 2 si no; el "después" del cierre repite la forma del baseline.
  Los runs por nivel viven en `batches/viveiro.json` (`AV` 2, `AR` 1, `AG` 1).
  **Actualizado 2026-09-29 (enmienda (b), dictamen CA-9)**:
  - El baseline ya no espera a la pasada manual. Es el baseline oficial del Go.
  - `AV` pasa a 3 runs en `batches/viveiro.json` (c = 0,1142 €).
  - Las dos mediciones "después" (semanas 11 y 12 ± 1, ≥ 7 días) repiten los 3 runs con
    `--levels AV --out "$env:PUSHLLM_PRIVADO\piloto-artica\probe-go-AAAA-MM-DD"`.
  - El `AV` semanal lleva `--runs 1` explícito.
  - `AR`/`AG` cada 4 semanas (0, 4, 8, 12).
  - Regla del Go: dictamen CA-9 (d).
- **F-SPEC-008-6** (→ sdd-documentalista): la matriz de este ledger venía con `\n`
  literales (como F-SPEC-007-3); se ha rehecho sin tocar el contenido de Verif./Estado.

- **F-SPEC-008-7** (→ SPEC-011 y SPEC-012; decisión del humano (a)): que una IA diga que
  una competidora no tiene médico es un argumento de confianza a favor de Ártica (médica
  titular). SPEC-011 lo usa en el diagnóstico; SPEC-012 lo revisa en cada informe con la
  sección "Observaciones para revisar a mano" del `summary.md` del probe y, en la medición
  manual, con una marca en `observaciones`. No es métrica ni se promete.
- **F-SPEC-008-9** — **hecho el 2026-09-29 (sdd-implementador)**, salvo la ejecución real
  de CA-7 (humano). Commits en `ft/SPEC-008-baseline-oficial`. El dictamen CA-9 y el mes del
  cierre están arriba; configuración, análisis, README e instrucciones están cambiados; CA-9
  y CA-10 están en la matriz.
  (→ sdd-implementador, **tras la re-aprobación humana** de la enmienda
  2026-09-29 (b); sdd-arquitecto). El probe es el instrumento del Go. **No tocar nada de
  esta lista antes de la re-aprobación.** Después, en este orden:
  1. **Dictamen CA-9**: pedir a `sdd-metricas` el dictamen (a)–(h) y añadirlo a este ledger
     con tabla condición → cambio, con fecha anterior al baseline.
  2. **CA-5**: añadir al dictamen de `sdd-probe` el cálculo del mes del cierre (dos
     mediciones "después" con los runs del baseline + `AV` semanal del resto del mes +
     `AR`/`AG`) con el `c` medido (0,1142 €); si el dictamen CA-9 pide dos ejecuciones de
     baseline, recalcular también el mes del baseline.
  3. **Configuración y análisis** (`probe/batches/viveiro.json`, `probe/analysis.py`): lo
     que pida CA-9 (runs del baseline y de las mediciones "después"; agregación de runs;
     indicadores `AR`/`AG` con la cadencia de 4 semanas) y una línea de **aviso de techo** en
     `summary.md` cuando el ponderado del núcleo sea ≥ 85 % (CA-10), solo con `AV`. Tests
     en `probe/tests/test_pilot_batch.py`; el golden de Vigo (CA-4) no cambia.
  4. **README** `probe/README.md` §"Batches": el comando de baseline con la forma de CA-9
     (cierra también el finding 1 de la verificación intermedia).
  5. **Este ledger**: reescribir "Dependencias" e "Instrucciones para el humano (CA-7)" con
     el orden humo → SPEC-013 `hecho` → dictamen CA-9 → congelación del set (fecha en el
     ledger de SPEC-007) → baseline oficial → aviso de techo (CA-10) → primera acción;
     quitar "después de la pasada 1 manual"; añadir CA-9 y CA-10 a la matriz; actualizar
     "Decisiones del humano" (Orden) y F-SPEC-008-5 (el baseline ya no espera a la manual).
  La comparación app frente a probe no se implementa aquí: es SPEC-007 CA-7 (F-SPEC-007-8).
- **F-SPEC-008-10** (→ SPEC-012, sdd-arquitecto): comparación **entre ejecuciones**, que no
  hace `analysis.py`, porque cada `summary.md` es de un solo `results.csv`:
  - Δ₁/Δ₂ del Go y |Δ₁ − Δ₂| (dictamen CA-9 (d)–(e));
  - regularidad `AR` (≥ 2 casillas con la clínica en las ejecuciones de las semanas 8 y 12);
  - `AG` alguna vez;
  - lista de puestos (CA-9 (g));
  - sensibilidad de "Ártica" adjetivo (CA-9 (h));
  - anotación de cambios de modelo (CA-9 (f)).
  SPEC-012 decide si lo hace a mano desde los `summary.md` o con una herramienta.
  **Actualizado 2026-09-29 (CA-11)**: la regla del Go ya no es Δ ≥ +15 en el núcleo, sino
  (C) y (D) del dictamen CA-11. `probe/analysis.py` ya tiene `growth_verdict`,
  `defense_verdict` y `render_go_verdict`, con tests. Reciben el resultado de
  `analysis.analyze` de cada `results.csv`. Falta el comando o procedimiento que los lee y
  escribe el veredicto en el espacio privado: es de SPEC-012. La regularidad `AR` de CA-9 (g)
  queda sustituida por (C).
- **F-SPEC-008-11** (→ orquestador, antes del paso 3 de CA-7): SPEC-007 dice que P-5
  (Mondoñedo) debe resolverse antes de la congelación. El dictamen (k) de SPEC-007, en su
  worktree, la da por "cerrada", pero el set publicado no cambia. Si la decisión añadiera o
  cambiara preguntas, hay que sincronizar `prompts.csv` (el test CA-1 lo exige) **antes** del
  baseline. Una vez congelado el set, no se toca.
- **F-SPEC-008-8** (verificación intermedia, 2026-09-29): findings 1–4 corregidos: runs por
  nivel y `--levels` (1), Clínica Villoria como miembro del lote piloto (2), alias punycode
  de Virxe da Mariña (3), `--out` vacío o raíz rechazado y comprobación de
  `PUSHLLM_PRIVADO` en los pasos del humano (4).
- **F-SPEC-013-5 — cerrado sin reabrir el 2026-09-29** (humo de seguimiento, paso 1 de
  CA-7, `…\piloto-artica\probe-smoke-spec013`): 9/9 `ok`; OpenAI 1,00 búsquedas por llamada
  (umbral 1,67) y 0,0116 € por llamada (umbral 0,0144 €), por debajo de los dos, así que el
  `include` de OpenAI no se toca y el instrumento del Go queda fijado (dictamen CA-9 (f));
  total 0,3646 €, c' = 0,1215 € ≤ 0,1307 € (CA-5 sin cambios); modelos servidos = configuración;
  la cabecera de `results.csv` termina en `searched_urls`.
- **F-SPEC-008-3 — revisión a mano del baseline oficial (2026-09-29, sdd-implementador)**: se
  leyeron en privado todas las respuestas del núcleo que `summary.md` lista con la clínica solo
  por "Ártica" suelta. **Todas se refieren a Clínica Ártica** (nombre comercial con su
  dirección o su oferta); ninguna usa "ártica" como adjetivo, así que la sensibilidad del
  dictamen CA-9 (h) no cambia nada en el baseline. Cuántas y cuáles, en privado
  (`ca7-baseline-evidencia.md`, ADR-004 §2). Se repite en cada medición "después".
- **F-SPEC-008-12** — **cerrado el 2026-09-29**: el baseline oficial dio el **Aviso de
  techo** y el humano decidió antes de la primera acción ("Decisiones del humano" (c);
  ADR-009).
- **F-SPEC-008-13** (→ sdd-implementador / verificador): `ruff` no está en el venv del probe
  (`probe\.venv`); se ejecutó con `py -m ruff`. Valorar añadirlo a las dependencias de
  desarrollo.
- **F-SPEC-008-14** (→ SPEC-012, sdd-arquitecto; dictamen CA-11 y CA-5 de la enmienda (d)):
  la cadencia del piloto cambia.
  - Cada medición "después" del Go es `--levels AV,AR` con 3 runs, en las semanas 11 y
    12 ± 1, con ≥ 7 días entre ellas.
  - En la semana 12 sustituye al `AR` de 1 run. `AG`, si toca, va aparte con
    `--levels AG --runs 1`.
  - El seguimiento `AR`/`AG` lleva `--runs 1` explícito: sin él, `--levels AR,AG` lanzaría
    `AR` con 3 runs.
  - Las palancas de coste 1–4 del mes del cierre se deciden al planificarlo.
  - SPEC-012 CA-3 y CA-7 deben recoger esto (ADR-009, Consecuencias).
- **F-SPEC-008-15** (→ sdd-documentalista): `docs/fundacion/contexto.md` todavía dice "Go
  solo con `AV`". Se actualiza con ADR-009 (ADR-009, Consecuencias). Este implementador no
  edita documentos de verdad.
- **F-SPEC-008-16** (→ sdd-arquitecto, informativo): el comando simple del lote (sin
  `--levels`) lanza ahora `AV` 3 + `AR` 3 + `AG` 1 = 64 preguntas × ejecución por
  proveedor. Ya no es la forma del baseline oficial, que se ejecutó con `AR` 1. Nadie debe
  relanzarlo como baseline. El README lo documenta.

## Cómo retomar (handoff)
- **2026-09-29 (e) (sdd-implementador, tras la re-aprobación de la enmienda (d) y ADR-009)**:
  spec en `en-progreso`. Hecho:
  - decisiones del humano (c) CA-10, (d) opción A y (e) recorte, anotadas; F-SPEC-008-12
    cerrado;
  - dictamen CA-11 con tabla condición → cambio;
  - `AR` a 3 runs; `go.growth` y `go.defense`;
  - veredictos (C) y (D) por separado en `analysis.py`, con TDD;
  - README; CA-5 recalculado;
  - instrucciones de CA-12 comprobadas offline.
  Tests con `PUSHLLM_PRIVADO` en el entorno: `pytest probe/tests` → 238 en verde;
  `pytest docs/piloto-artica/tools/tests` → 143 en verde; `py -m ruff check probe` limpio;
  `valida.mjs` OK. Sin commit.
  Falta:
  - CA-12 ([Humano], tras la comprobación de `sdd-probe`); después, el agente anota CA-12
    (solo veredictos en el repo; cifras en privado);
  - verificación de CA-7, CA-9, CA-10, CA-11 y CA-12 y repetición de CA-8
    (sdd-verificador);
  - F-SPEC-008-14 a SPEC-012 (arquitecto).
- **2026-09-29 (d) (sdd-implementador, tras la ejecución de CA-7)**: CA-7 registrado en la
  matriz (mi mitad), registro de la congelación relleno, fixture
  `probe/tests/fixtures/pilot-set-frozen.tsv` con su test, F-SPEC-013-5 cerrado y revisión de
  "Ártica" suelta hecha (todas son la clínica). Cifras en
  `$PUSHLLM_PRIVADO\piloto-artica\ca7-baseline-evidencia.md` (ADR-004). Sin commit.
  Falta: decisión del humano sobre el Aviso de techo (F-SPEC-008-12) antes de la primera
  acción; fecha de congelación al ledger de SPEC-007 CA-8 (orquestador); verificación de
  CA-7, CA-9, CA-10 y repetición de CA-8 (sdd-verificador).
- **2026-09-29 (c) (sdd-implementador, tras la re-aprobación de la enmienda (b))**: spec en
  `en-progreso`. F-SPEC-008-9 hecho.
  - Dictamen CA-9 fechado antes del baseline.
  - CA-10 (aviso de techo) con TDD.
  - `AV` a 3 runs.
  - Líneas del Go en `summary.md`.
  - CA-5 del mes del cierre y del baseline.
  - README.
  - Dependencias, instrucciones CA-7 (humo de seguimiento F-SPEC-013-5 → baseline oficial)
    y registro de congelación preparado.
  Falta: CA-7 ([Humano]: pasos 1–5); después, el agente rellena CA-7, el registro de
  congelación, el fixture del set congelado y, si sale el aviso, la decisión del humano
  (CA-10). Revisar F-SPEC-008-11 antes del paso 3.
- **2026-09-29 (b) (sdd-arquitecto)**: la spec vuelve a `borrador` por la enmienda "el probe
  es el instrumento del Go": CA-7 pasa a baseline oficial (depende de SPEC-013 `hecho` y de
  CA-9, ya no de la pasada manual), CA-9 (dictamen del Go con el probe) y CA-10 (techo)
  nuevos, CA-5 amplía el cálculo al mes del cierre. CA-1 a CA-4, CA-6 y CA-8 siguen como
  estaban (implementados y verificados en intermedia). Tras la re-aprobación: F-SPEC-008-9.
- **2026-09-29 (sdd-implementador, tras la verificación intermedia)**: findings 1–4
  corregidos con tests; decisiones del humano (a) y (b) y el orden humo → pasada 1 →
  baseline registrados. Spec en `en-progreso`; falta CA-7 ([Humano]).
- **2026-09-29 (sdd-implementador)**: CA-1 a CA-6 hechos offline, con tests; CA-8 preparado
  para el verificador. Spec en `en-progreso` porque falta CA-7 ([Humano], claves). Pendiente
  además la fecha de congelación del set (dependencia de SPEC-007 CA-8, no bloqueo).
- Siguiente: verificación de CA-1–CA-6 y CA-8 por `sdd-verificador`; cuando haya claves, el
  humano lanza humo y baseline con las instrucciones de arriba; luego el agente anota CA-7
  (fecha, llamadas, estado, coste) y F-SPEC-008-1.
- Comprobar: `python -m pytest -q probe/tests`, `python -m pytest -q
  docs/piloto-artica/tools/tests`, `ruff check probe`.
