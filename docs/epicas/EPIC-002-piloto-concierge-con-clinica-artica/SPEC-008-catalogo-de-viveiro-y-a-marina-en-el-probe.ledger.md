---
id: SPEC-008
tipo: ledger
epica: EPIC-002
---
# Ledger — SPEC-008 Catálogo de Viveiro y A Mariña en el probe

## Resumen
- Fase: <!-- refleja el estado de la spec; la fuente de verdad es el frontmatter de la spec -->
- Rama: `ft/SPEC-008-catalogo-de-viveiro-y-a-marina-en-el-probe` (sale de
  `ft/SPEC-007-…`, que aún no está en `main`)

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
| CA-5 | Dictamen `sdd-probe` y cálculo en este ledger ("Dictamen sdd-probe (CA-5)"); cadencia aceptada por el humano; runs por nivel en `probe/batches/viveiro.json` y `--levels` en `probe/run_probe.py` | Cálculo reproducible en el propio dictamen; `test_pilot_batch.py::test_ca5_*` | Intermedia 2026-09-29: recalculado: 72 p×e → 8,9/16,2 €; mes normal 9,2/16,8 €; baseline 102 p×e alto 22,97 € → regla de 2 runs 19,6 €; precios coinciden con `probe_config.json`; `AR/AG` a menor cadencia que `AV` | ✅ |
| CA-6 | `probe/README.md` §"Batches" (lote Vigo = defecto; comandos del lote piloto con `.\.venv\Scripts\python`; runs por nivel; salida) y docstring de `run_probe.py` | `test_pilot_batch.py::test_ca6_readme_documents_pilot_batch_with_working_commands` y `::test_ca6_ledger_human_commands_within_budget_and_use_venv_python` (los comandos del README y del ledger se ejecutan offline: lote piloto y ≤ 54 llamadas por proveedor) | Intermedia 2026-09-29: sección "Batches" presente, lote Vigo = defecto, salida y comandos válidos. Salvedad: el comando de baseline del README (24 × 3 runs, 216 llamadas) no sigue la cadencia de CA-5 (`AR/AG` 1 run; regla 2/3 runs) que sí siguen las instrucciones del ledger | ⚠️ |
| CA-7 | [Humano] pendiente de claves. Comandos exactos en "Instrucciones para el humano (CA-7)" | — (fechas frente a la primera acción de SPEC-012) | Pendiente [Humano]: no ejecutado en verificación intermedia; comandos del ledger revisados | ❌ |
| CA-8 | [Verificador]. Ninguna salida en el repo: tests con `tmp_path`; la salida por defecto del lote es `$PUSHLLM_PRIVADO/piloto-artica/probe` y el respaldo `probe/out/piloto-artica/probe` está bajo `probe/out/` (ignorado); `run_probe.py` rechaza `--out` vacío o raíz de unidad (`unsafe_out`) | `test_run_probe.py::test_ca8_default_inside_repo_is_gitignored` (sin cambios); `test_pilot_batch.py::test_ca8_out_empty_or_root_is_refused`, `::test_ca8_unsafe_out_rules` | Intermedia 2026-09-29: `git ls-files` solo lista fixtures sintéticos de test (`probe/tests/fixtures/vigo_results.csv`, `vigo_summary_before.md`), ninguna salida de lote; `git status --ignored` sin `probe/out/` (no existe); `probe/out/` en `.gitignore`. Repetir al cierre tras CA-7 | ✅ |

Tests (2026-09-29, tras los findings): `python -m pytest -q probe/tests` → 156 en verde;
`python -m pytest -q docs/piloto-artica/tools/tests` → 143 en verde; `ruff check probe` limpio.

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

## Dependencias
- **Set congelado (SPEC-007 CA-8)**: CA-1 pide el set "congelado". El texto de los tres
  niveles es el definitivo y se ha copiado tal cual, pero la fecha de congelación es el
  inicio de la pasada 1 manual, que aún no ha empezado. Dependencia pendiente, **no
  bloqueo**: se cumple cuando el humano fije esa fecha en el ledger de SPEC-007. Si el set
  cambiara antes, `test_ca1_pilot_prompts_equal_to_frozen_set_id_and_literal_text` falla y
  obliga a sincronizar `prompts.csv`.
- **Claves (SPEC-002 CA-1)**: solo para CA-7.

## Instrucciones para el humano (CA-7)
**Orden**: el humo puede lanzarse ya; el **baseline va después de la pasada 1 manual de
SPEC-007** (su inicio congela el set, SPEC-007 CA-8) y **antes de la primera acción del
piloto** (SPEC-012). `PUSHLLM_PRIVADO` ya es variable de usuario: no se fija aquí. Sin
activar el venv: se llama a `.\.venv\Scripts\python` directamente. En PowerShell, desde
`probe/` (venv instalado según `probe/README.md`, "Install"):

```powershell
cd probe
if (-not $env:PUSHLLM_PRIVADO) { throw "PUSHLLM_PRIVADO no está definida" }
$env:ANTHROPIC_API_KEY = Read-Host "Anthropic key"
$env:OPENAI_API_KEY    = Read-Host "OpenAI key"
$env:GEMINI_API_KEY    = Read-Host "Gemini key"

# 0) Comprobación offline (sin claves ni red): todo en verde
.\.venv\Scripts\python -m pytest -q tests

# 1) HUMO (se puede ya): 3 preguntas x 1 run x 3 proveedores = 9 llamadas
.\.venv\Scripts\python run_probe.py --config batches/viveiro.json --only AV01,AR01,AG01 --runs 1 --out "$env:PUSHLLM_PRIVADO\piloto-artica\probe-smoke"
Select-String "lote \| total" "$env:PUSHLLM_PRIVADO\piloto-artica\probe-smoke\summary.md"
# c = "lote | total" / 3  (coste por pregunta x ejecución, los 3 proveedores)

# 2) BASELINE (solo después de la pasada 1 manual de SPEC-007)
#    Si c > 0,19 EUR: un solo comando (AV 2 runs, AR/AG 1 run)
.\.venv\Scripts\python run_probe.py --config batches/viveiro.json
#    Si c <= 0,19 EUR: en su lugar, estos dos (AV 3 runs; después AR/AG 1 run)
.\.venv\Scripts\python run_probe.py --config batches/viveiro.json --levels AV --runs 3
.\.venv\Scripts\python run_probe.py --config batches/viveiro.json --levels AR,AG --resume

# 3) Si se corta: repetir la misma línea añadiendo --resume (solo llama lo que falta)
# 4) Recuento offline cuando quieras (sin llamadas)
.\.venv\Scripts\python run_probe.py --config batches/viveiro.json --analyze
```

- Salida: `$env:PUSHLLM_PRIVADO\piloto-artica\probe\results.csv` y `summary.md`. Nada al
  repo (ADR-001/ADR-004). El probe rechaza un `--out` vacío o raíz de unidad.
- Después, avisa con: fecha y hora de inicio y fin, nº de llamadas por estado (tabla de
  `summary.md`) y coste total. Con eso el agente rellena CA-7 aquí y revisa el resumen.
- Si las claves llegan **después** de la primera acción, no lances el baseline como tal:
  CA-7 pasa a n-a y el probe solo sirve para tendencia.

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
- **Orden**: el baseline del probe va después de la pasada 1 manual de SPEC-007; el humo
  puede ir antes (instrucciones de arriba).

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
- **F-SPEC-008-6** (→ sdd-documentalista): la matriz de este ledger venía con `\n`
  literales (como F-SPEC-007-3); se ha rehecho sin tocar el contenido de Verif./Estado.

- **F-SPEC-008-7** (→ SPEC-011 y SPEC-012; decisión del humano (a)): que una IA diga que
  una competidora no tiene médico es un argumento de confianza a favor de Ártica (médica
  titular). SPEC-011 lo usa en el diagnóstico; SPEC-012 lo revisa en cada informe con la
  sección "Observaciones para revisar a mano" del `summary.md` del probe y, en la medición
  manual, con una marca en `observaciones`. No es métrica ni se promete.
- **F-SPEC-008-8** (verificación intermedia, 2026-09-29): findings 1–4 corregidos: runs por
  nivel y `--levels` (1), Clínica Villoria como miembro del lote piloto (2), alias punycode
  de Virxe da Mariña (3), `--out` vacío o raíz rechazado y comprobación de
  `PUSHLLM_PRIVADO` en los pasos del humano (4).

## Cómo retomar (handoff)
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
