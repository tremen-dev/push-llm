---
id: SPEC-013
tipo: ledger
epica: EPIC-FIX
---
# Ledger — SPEC-013 Respuesta cruda del proveedor y citas de Claude en el probe

## Resumen
- Fase: <!-- refleja el estado de la spec; la fuente de verdad es el frontmatter de la spec -->
- Rama: `ft/SPEC-013-respuesta-cruda-y-citas-de-claude` (apilada sobre `ft/SPEC-002-…`, aún
  sin merge)

## Matriz de criterios de aceptación
<!-- Escritores: sdd-implementador rellena Implementado y Test; sdd-verificador rellena Verif. y Estado. Nunca al revés. -->
<!-- Estados por CA: ✅ cerrado · ⚠️ parcial/con salvedad · 🚧 en curso · ❌ sin empezar · n-a -->
<!-- Un CA está ✅ solo cuando Implementado + Test + Verif. aplicables están en verde. Una salvedad se marca ⚠️, nunca ✅. -->
| CA | Implementado (fichero) | Test (fichero/caso) | Verif. | Estado |
|---|---|---|---|---|
| CA-1 | `probe/providers.py` (`ProviderResult.request/responses`, `raw_json`, `scrub`, `FORBIDDEN_KEYS`; captura en `_claude`/`_openai`/`_gemini` y `ask`), `probe/run_probe.py` (`RAW_NAME`, `raw_line`, append en el bucle), `probe/README.md` § Output | `probe/tests/test_raw_responses.py`: (a) `test_ca1a_one_line_per_call_with_the_row_keys`; (b) `test_ca1b_pause_turn_line_has_one_response_per_turn`, `test_claude_pause_turn_keeps_one_response_per_turn`; (c) `test_ca1c_no_headers_nor_keys_in_the_file`, `test_gemini_raw_drops_sdk_http_response_and_headers`, `test_real_sdk_objects_serialize_without_http_headers`, `test_forbidden_keys_removed_at_any_depth_case_insensitive`; error: `test_ca1_error_line_has_empty_responses_and_the_message`, `test_error_keeps_request_and_no_responses`; (d) `test_ca1d_resume_appends_and_never_rewrites`; (e) `test_ca1e_analyze_neither_reads_nor_modifies_raw`; (f) `test_ca1f_default_output_raw_file_is_gitignored`; sin recorte: `test_claude_raw_keeps_request_and_full_response`; columnas de `results.csv`: aserción en (a) | | ❌ |
| CA-2 | Llamada real del orquestador (2026-09-29); forma copiada en § "Evidencia CA-2" de este ledger. Comando comprobado offline (1 llamada) | `test_raw_responses.py::test_ca2_diagnostic_command_makes_exactly_one_claude_call` | | ❌ |
| CA-3 | `probe/providers.py` (`ProviderResult.searched_urls`; `_claude` + `_close_span`; `_openai` + `OPENAI_INCLUDE`; `_gemini` + `_gemini_urls`), `probe/run_probe.py` (`COLUMNS` + `searched_urls`, `results_header`, rechazo de `--resume`), `probe/tests/fakes.py` (`ns`, `load_fixture`, `sources=`, `supports=`), `probe/tests/fixtures/claude_web_search_20260209.json` (nuevo, sanitizado), `probe/README.md` § Output | `probe/tests/test_searched_urls.py`: forma `test_fixture_has_the_ca2_shape`; (a) `test_ca3a_claude_fixture_has_no_cited_urls` + `test_providers.py::test_claude_ok_collects_usage_urls_and_served_model` (sin cambios); (b) `test_ca3b_claude_searched_urls_from_top_level_search_results`, `…_across_pause_turn_with_and_without_caller` (incl. inclusión), `…_search_error_block_adds_nothing_and_does_not_break`; (c) `test_ca3c_claude_fixture_text_is_exact`, `test_ca3c_consecutive_text_blocks_join_without_separator_spans_with_blank_line`, `test_providers.py::test_claude_pause_turn_accumulates_usage_and_text` (actualizado); (d) `test_ca3d_reprocess_the_real_ca2_response_offline` (se salta sin `PUSHLLM_PRIVADO`; recuentos en § "Cómo retomar"); (e–g) `test_ca3ef_gemini_cited_are_supported_chunks_searched_are_all` (índice repetido, inclusión), `test_ca3f_gemini_without_supports_cites_nothing`, `test_ca3f_gemini_out_of_range_index_is_ignored`, `test_ca3f_gemini_chunk_without_web_counts_in_neither_list`, `test_ca3g_gemini_redirects_are_kept_as_they_are`; (h) `test_ca3h_openai_asks_for_action_sources`; (i) `test_ca3i_openai_searched_urls_from_sources_skipping_feeds` (feed `oai-weather` sin url, inclusión), `test_ca3i_openai_action_without_sources_adds_nothing`; (j) `test_ca3j_openai_citation_outside_sources_stays_cited_only`, `test_providers.py::test_openai_ok`; error: `test_error_leaves_both_url_lists_empty`; (k) `test_ca3k_searched_urls_is_the_last_column_and_filled_for_each_provider`; (l) `test_ca3l_resume_refuses_an_old_results_csv[True/False]`, `test_ca3l_resume_on_a_new_results_csv_still_appends`, `test_ca3l_analyze_same_summary_with_or_without_the_column` | | ❌ |
| CA-4 | Sin cambios en `probe/analysis.py`, `vigo_results.csv` ni `vigo_summary_before.md`. `pytest probe/tests`: 213 passed, 1 skipped (CA-3 d sin `PUSHLLM_PRIVADO`; con él, 214 passed); `pytest docs/piloto-artica/tools/tests`: 143 passed; `ruff check probe`: OK | Expectativas cambiadas (y solo estas): `test_providers.py::test_claude_pause_turn_accumulates_usage_and_text` (`"Parte 1.\nParte 2."` → `"Parte 1.\n\nParte 2."`, CA-3 c); `test_providers.py::test_gemini_ok_sums_thoughts_and_tool_tokens` (`cited_urls` `["https://v.es"]` → `[]`, y `searched_urls == ["https://v.es"]`); `test_providers.py::test_openai_ok` (aserción nueva de `include`); `test_raw_responses.py::test_ca1a_one_line_per_call_with_the_row_keys` (solo el comentario: la aserción `== run_probe.COLUMNS` ya incluye `searched_urls`). Golden `test_pilot_batch.py::test_ca4_vigo_summary_identical_to_before_the_change` en verde sin tocar | | ❌ |
| CA-5 | `probe/providers.py` (`_openai`: `include`; `_claude`/`_gemini`: petición intacta). Dictamen sdd-probe: § "Dictamen sdd-probe (CA-5)" | `test_searched_urls.py::test_ca5_claude_and_gemini_send_exactly_the_same_openai_only_adds_include` (kwargs completos de los tres clientes falsos frente a la petición anterior escrita a mano) | | ❌ |
| CA-6 | Llamada real del orquestador, 2026-09-29 (3 llamadas, 0,1216 €; tope 0,40 €), precedida de `pytest -q tests` con 214 passed. Evidencia y análisis de la alerta de coste de OpenAI en § "Evidencia CA-6" |  `test_searched_urls.py::test_ca6_confirmation_command_makes_exactly_three_calls` | | ❌ |
| CA-7 | Dictamen sdd-metricas: § "Dictamen sdd-metricas (CA-7)". Confirma (1) y (5); no pide cambios de columna, significado, §4 ni RN | `test_ca3l_analyze_same_summary_with_or_without_the_column` + golden de Vigo (apoyan el punto 5) | | ❌ |

## Evidencia CA-2 (forma de la respuesta; sin texto, URLs ni nombres de clínica)
Copiada por sdd-implementador el 2026-09-29 de la spec (§ "Evidencia de CA-2") y
comprobada contra `results.csv` y `raw_responses.jsonl` del directorio privado
`$PUSHLLM_PRIVADO/diagnostico/spec-013` (solo claves y recuentos).
- Fecha y hora: **2026-09-29T13:57:58Z** (UTC). Modelo servido: `claude-sonnet-5-5`.
  Coste de la fila: **0,072869 €** (30 425 tokens de entrada, 1 206 de salida).
  Búsquedas: **1** (`server_tool_use.web_search_requests=1`, `web_fetch_requests=0`).
- `request.tools`: `web_search_20260209`, `max_uses=5`, **sin `allowed_callers`** (por
  defecto `["code_execution_20260120"]`: filtrado dinámico).
- 1 turno, `stop_reason=end_turn`. 9 bloques de primer nivel:
  1. `server_tool_use` (`name=code_execution`, `caller=null`)
  2. `server_tool_use` (`name=web_search`, `caller={type: code_execution_20260120, tool_id}`)
  3. `web_search_tool_result` (`caller={type: code_execution_20260120, tool_id}`)
  4. `code_execution_tool_result` (`encrypted_code_execution_result`)
  5. `server_tool_use` (`code_execution`, `caller=null`)
  6. `code_execution_tool_result` (`code_execution_result`)
  7. `server_tool_use` (`code_execution`, `caller=null`)
  8. `code_execution_tool_result` (`code_execution_result`)
  9. `text`
  `caller` es un objeto `{type, tool_id}`, no una cadena.
- Bloques `text`: **1**, con `citations: null`. **0** con citas, así que no hay ningún
  `type` de cita ni campo con URL.
- `web_search_tool_result.content`: **10** `web_search_result` (claves `encrypted_content`,
  `page_age`, `title`, `type`, `url`), con 10 `url` distintos. Están en primer nivel, no
  anidados en `code_execution_tool_result`.
- **Caso B** (hay URLs consultadas y ninguna citada). Documentación: *Web search tool*,
  *Server tools* y *Citations* de platform.claude.com, consultadas el 2026-09-29 (citas
  literales en la spec, § "Problema").

## Dictamen sdd-probe (CA-5), 2026-09-29
Rol advisory, consultado por sdd-implementador. Fuentes del proyecto: FOUNDATION D-5,
reglas.md RN-10, `06-models-costs-and-usage-share.md`, `probe/probe_config.json` (openai:
`gpt-5.6-luna`, tool `web_search`, effort `low`, `search_usd` 0,01). Fuentes oficiales
consultadas el 2026-09-29.
1. **Correcto.** `include` solo cambia lo que devuelve la API.
   - Referencia de la Responses API: "Specify additional output data to include in the
     model response"; `web_search_call.action.sources`: "Include the sources of the web
     search tool call".
     https://developers.openai.com/api/reference/resources/responses/methods/create
   - Guía: "sources returns the complete list of URLs the model consulted when forming its
     response". https://developers.openai.com/api/docs/guides/tools-web-search
   - El modelo, la tool, `user_location`, el effort y las instructions no cambian, así que
     D-5 y RN-10 siguen intactos.
   - Salvedad: la documentación no dice de forma expresa que `include` no altere la
     búsqueda; se deduce de su definición.
2. **Correcto, por inferencia.** El coste no cambia.
   - Precios: "$10.00 / 1k calls + Search content tokens billed at model rates".
     https://developers.openai.com/api/docs/pricing
   - Nada de eso depende de `include`. Impacto estimado: 0 €.
   - Hay que contrastarlo con la fila de OpenAI de CA-6: una desviación de más del 20 %
     respecto a unos 0,012 € sería una alerta.
3. **Correcto, con matiz.** El nombre exacto es `"web_search_call.action.sources"` (guía y
   referencia).
   - La referencia documenta las entradas de `sources` de la acción `search` como
     `{type: "url", url}`.
   - En la práctica llegan también entradas `{type: "api", name: "oai-weather" | …}` sin
     `url` (https://github.com/openai/openai-python/issues/2636; la guía nombra los feeds
     `oai-sports`, `oai-weather` y `oai-finance`).
   - La forma exacta de la entrada `api` queda como **dudosa** en la documentación oficial.
     El parser debe tolerar entradas sin `url`: cubierto por
     `test_ca3i_openai_searched_urls_from_sources_skipping_feeds`, con un feed
     `{type: api, name: oai-weather}`.
4. **Dudoso.** `open_page` ("Opens a specific URL from search results") y `find_in_page`
   (lleva `url`) solo existen en modelos de razonamiento, y `gpt-5.6-luna` lo es.
   - Son páginas que el modelo abrió de verdad, así que conceptualmente cuentan como
     consultadas.
   - La documentación no dice si esas URLs aparecen también en `sources`.
   - Recomienda un follow-up: F-SPEC-013-3.
- **Invariantes:** D-5, RN-10, el no-negociable de coste y `probe_config.json` sin cambio.
  `request` refleja el `include` (07 §6).
- **Veredicto global: FAVORABLE al `include`**, condicionado a que el parser tolere
  entradas `api` sin `url` (hecho, con test) y a contrastar el coste real de OpenAI en CA-6.

## Dictamen sdd-metricas (CA-7), 2026-09-29
Rol advisory, consultado por sdd-implementador. Fuentes: `07-mvp-product-spec.md` §3
(Source) y §4 (*Source citation weight*, *Coverage of cited sources*, *Gap analysis*);
`docs/fundacion/reglas.md` RN-03, RN-04 y RN-08; `docs/fundacion/dominio.md`
(Probe/ProbeRun "URLs citadas", Source "página citada"); FOUNDATION D-6; `probe/analysis.py`
(leído el 2026-09-29); SPEC-011 CA-1.
1. **Correcto.** El peso de fuente es "Σ over answers **citing** the source of the provider
   weight", Source es la "página citada", RN-08 ordena por peso de citación y Coverage usa
   el top-10 "by citation weight". Todo se calcula solo con `cited_urls`; una URL solo
   consultada suma 0.
   - **Claude:** mientras no cite, su 10 % de RN-04 aporta 0. El ranking sale de ChatGPT
     (55 %) y Gemini (25 %). No hay sesgo de escala: el peso es una suma sin normalizar.
     Pero las fuentes de Claude quedan invisibles en el ranking, y el informe tiene que
     decirlo ("Claude: 0 citas en el periodo"). No se redistribuye su peso: eso cambiaría
     RN-04 y D-6.
   - **Gemini:** bajan sus citadas respecto a los humos anteriores. Es la medida correcta,
     no una pérdida: antes se inflaba el peso de fuentes solo consultadas. No se compara
     con los rankings anteriores.
2. **Dudoso: la comparación entre proveedores es parcial.**
   - Claude: resultados antes del filtrado dinámico, una cota superior de lo que leyó el
     modelo.
   - OpenAI: "complete list of URLs the model consulted", sin `open_page`/`find_in_page`.
   - Gemini: chunks de grounding, ya seleccionados, como redirecciones.
   - Vale como **marca por fuente** ("¿la consultó el proveedor X?") y como recuento dentro
     de un mismo proveedor a lo largo del tiempo.
   - No vale comparar recuentos absolutos entre proveedores.
   - Gemini no se cruza por dominio con los otros hasta resolver las redirecciones
     (F-SPEC-001-2).
3. **Propuesta para SPEC-011 y sdd-producto**, sin crear métrica aquí.
   - Por cada Source, un indicador aparte **"consultada por"** para ChatGPT, Gemini y
     Claude: respuestas con la fuente en `searched_urls` sobre las respuestas válidas del
     proveedor, o una marca sí/no.
   - Sin ponderar con RN-04 y sin entrar en el top-10, en Coverage ni en RN-08.
   - Texto al cliente, igual para todos: "Consultada: el asistente la leyó al buscar.
     Citada: la enlazó en su respuesta. Solo las citadas cuentan en el peso de fuentes."
   - Una nota por proveedor con los límites del punto 2.
   - Dar peso a las consultadas sería una definición nueva de §4: la deciden sdd-producto y
     el humano.
4. **Ficheros anteriores a SPEC-013** (su cabecera no tiene `searched_urls`).
   - SPEC-011 CA-1 usa **solo** el baseline posterior a SPEC-013.
   - Si se usan ficheros antiguos, se reclasifican al leerlos, sin reescribirlos:
     - OpenAI: `cited_urls` vale como citadas;
     - Gemini: `cited_urls` pasa a consultadas, y las citadas son desconocidas;
     - Claude: citadas vacías y consultadas desconocidas.
   - Nunca se mezclan en un mismo ranking filas de Gemini con los dos significados.
5. **Correcto.** `analysis.py` solo lee `prompt_id`, `provider`, `specialty`, `city`,
   `status`, `cost_eur`, `answer` y `run`. SoV (RN-02/03), menciones (RN-01/11) y posición
   (RN-06) no dependen de URLs, así que el golden de Vigo no puede cambiar.
- **Invariantes:** ninguno roto. Queda pendiente revisar SPEC-011 CA-1 con los puntos 2–4 y
  añadir "URLs consultadas" a Probe/ProbeRun en `dominio.md`, sin peso de citación.
- **¿Confirma (1) y (5) sin pedir cambios de columna, significado, §4 ni RN? SÍ.**

## Evidencia CA-6 (solo recuentos; sin URLs ni texto)
Llamada real ejecutada por el orquestador el 2026-09-29, con autorización del humano. Comando:
`--providers claude,openai,gemini --only D01 --runs 1 --out "$env:PUSHLLM_PRIVADO\diagnostico\spec-013-post"`.
Resultado: la cabecera de `results.csv` termina en `searched_urls`, hay 3 filas y 3 líneas en
`raw_responses.jsonl`, y la de OpenAI lleva `include=["web_search_call.action.sources"]` en
`request` (comprobado por sdd-implementador).

| Proveedor | Modelo servido | Estado | Búsquedas | Consultadas | Citadas | Citadas ⊆ consultadas | Coste |
|---|---|---|---|---|---|---|---|
| claude | `claude-sonnet-5-5` | ok | 1 | 10 | 0 | sí | 0,0696 € |
| openai | `gpt-5.6-luna` | ok | 2 | 50 | 4 | sí | 0,0218 € |
| gemini | `gemini-3.6-flash` | ok | 2 | 5 | 5 | sí | 0,0302 € |

Total: 0,1216 €.

**Alerta del dictamen de CA-5, punto 2: el coste de OpenAI se desvía más de un 20 %.**
Análisis de sdd-implementador a partir de `results.csv` y `raw_responses.jsonl` de
`spec-013-post` y de las filas de openai de `$PUSHLLM_PRIVADO/probe-smoke/results.csv`
(humo de SPEC-002). Los precios salen de `probe_config.json`: 0,20 $/Mtok de entrada,
1,20 $/Mtok de salida, 0,01 $ por búsqueda y 1,1378 $/€, así que una búsqueda cuesta
0,00879 €.

| Fila | Tokens entrada | Tokens salida | Búsquedas | Coste por tokens | Coste por búsquedas | Coste total | Total / búsqueda | Entrada / búsqueda |
|---|---|---|---|---|---|---|---|---|
| humo D01 | 12 799 | 902 | 1 | 0,0032 € | 0,0088 € | 0,0120 € | 0,0120 € | 12 799 |
| humo F01 | 12 663 | 822 | 1 | 0,0031 € | 0,0088 € | 0,0119 € | 0,0119 € | 12 663 |
| humo O01 | 12 925 | 763 | 1 | 0,0031 € | 0,0088 € | 0,0119 € | 0,0119 € | 12 925 |
| humo E01 | 12 397 | 616 | 1 | 0,0028 € | 0,0088 € | 0,0116 € | 0,0116 € | 12 397 |
| **CA-6 D01** | 18 630 | 863 | **2** | 0,0042 € | 0,0176 € | **0,0218 €** | **0,0109 €** | **9 315** |

- **Diferencia frente a la media del humo:** 0,0218 − 0,0119 = +0,0099 €, un +84 %.
  - La búsqueda extra explica +0,0088 €, un 89 % de la diferencia.
  - Los tokens explican +0,0012 €, un 12 %: la entrada pasa de unos 12 700 a 18 630 tokens
    (+47 %) y la salida no cambia (863 frente a 616–902).
- **Normalizado por búsqueda,** esta llamada cuesta menos que el humo: 0,0109 € frente a
  0,0116–0,0120 €. También tiene menos tokens de entrada por búsqueda: 9 315 frente a
  12 400–12 900.
- **La observación del orquestador se confirma con los datos.** El humo hizo 1 búsqueda por
  llamada (4 en 4) y esta llamada hizo 2. La subida de entrada encaja con meter en el
  contexto el contenido de una segunda búsqueda, porque la entrada por búsqueda baja.
- **Lo que este dato no permite separar:**
  - Es una sola llamada, así que no se puede distinguir si la segunda búsqueda es variación
    normal del modelo o un efecto de `include`.
  - El dictamen de CA-5 sostiene que `include` solo añade datos de salida. No hay evidencia
    en contra, pero tampoco se puede probar con n = 1.
  - `usage` no desglosa tokens atribuibles a `sources`. Sí indica
    `cache_write_tokens=4436`, `cached_tokens=0` y `reasoning_tokens=204`.
- **Sin decidir:** si la alerta se cierra lo decide el verificador (o sdd-probe y el
  humano). Una forma de acotarlo sin gasto nuevo es comparar las búsquedas por llamada de
  OpenAI en el primer humo de SPEC-008 CA-7, que ya lleva `include`, con las del humo de
  SPEC-002.
- **F-SPEC-013-3 (dato para ese follow-up):** en esta respuesta de OpenAI no hay acciones
  `open_page` ni `find_in_page`; los 2 `web_search_call` son de tipo `search`. Las 50
  entradas de `sources` son todas `type=url` con `url`, sin feeds `oai-*`. Todavía no se
  puede comprobar si esas URLs aparecen en `sources`.

## Veredicto del verificador
<!-- GREEN/RED + fecha + resumen. Lo escribe SOLO sdd-verificador. -->

## Evidencia visual
<!-- Tabla CA → captura en _qa/SPEC-013/. Informe HTML opcional: _qa/SPEC-013/informe.html -->

## Salvedades / follow-ups
<!-- IDs F-SPEC-013-1, F-SPEC-013-2… con destino (spec futura o EPIC-MEJORA). -->
- **F-SPEC-013-1** (sdd-arquitecto, 2026-09-29), `searched_urls` de OpenAI: **resuelto dentro
  de la spec** por la enmienda (c). CA-3 (h–j) añade `include`, con el dictamen de sdd-probe
  de CA-5.
- **F-SPEC-013-2** (sdd-arquitecto, 2026-09-29), significado de `cited_urls` en Gemini:
  **resuelto dentro de la spec** por la enmienda (c). CA-3 (e–g): `searched_urls` son todos
  los chunks y `cited_urls` los referenciados por `grounding_supports`. Resolver las
  redirecciones `vertexaisearch` sigue en F-SPEC-001-2.
- **F-SPEC-013-3** (sdd-implementador, 2026-09-29, por el punto 4 del dictamen de sdd-probe),
  URLs de las acciones `open_page`/`find_in_page` de OpenAI: fuera de esta spec (§ Fuera de
  alcance). Primero hay que comprobar en la respuesta cruda de CA-6 si esas URLs ya están
  en `sources`. Si no están, se propone añadirlas a `searched_urls`, sin duplicados. Destino:
  una spec futura del probe (EPIC-FIX) o SPEC-011.
- **F-SPEC-013-4** (sdd-implementador, 2026-09-29, del dictamen de sdd-metricas), para el
  arquitecto, sin código:
  - añadir "URLs consultadas" a Probe/ProbeRun en `docs/fundacion/dominio.md`, sin peso de
    citación;
  - dejar en SPEC-011 una nota con los puntos 2–4 del dictamen.
  Lo prevé CA-7 ("el arquitecto añade…").

## Cómo retomar (handoff)
<!-- Estado real del trabajo para la siguiente sesión: qué está hecho, qué falta, dónde seguir. -->
- **2026-09-29 (sdd-arquitecto)**: spec en `borrador`, bajo EPIC-FIX (creada hoy). Origen:
  F-SPEC-002-7 (ledger de SPEC-002). Siguiente: gate humano (spec + gasto de CA-2). Tras la
  aprobación: sdd-implementador hace CA-1; [Orquestador] lanza la llamada de CA-2 (comando
  en la spec); sdd-implementador sigue con CA-3/CA-4 según caso A o B. Pendiente del
  orquestador: enlazar SPEC-013 desde F-SPEC-002-7 (ledger de SPEC-002) y desde SPEC-008
  CA-7 cuando el verificador los suelte.
- **2026-09-29 (sdd-implementador, fase 1)**: spec a `en-progreso`. **CA-1 implementado** con
  TDD (tests en `probe/tests/test_raw_responses.py`, primero en rojo). `raw_responses.jsonl`
  junto a `results.csv`: una línea JSON compacta (UTF-8) por llamada con `timestamp_utc`,
  `prompt_id`, `provider`, `run`, `model` (los de la fila), `status`, `error`, `request` y
  `responses` (una por turno, JSON completo vía `model_dump(mode="json")` de los SDK; sin
  recortar `encrypted_*`). Se eliminan a cualquier profundidad, sin distinguir mayúsculas,
  las claves `headers`, `sdk_http_response`, `api_key`, `authorization`, `x-api-key`. Una
  llamada con error deja `responses: []` (también si falla un turno de continuación tras
  `pause_turn`: la spec pide `responses` vacía). Tamaño: se guarda `encrypted_content`
  completo, como decide la spec (decenas de KB por llamada). `results.csv` sin cambios de
  columnas. La rama real es `ft/SPEC-013-respuesta-cruda-y-citas-de-claude` (el Resumen dice
  otro slug; no lo toco, es texto del arquitecto).
  **Siguiente**: [Orquestador] CA-2 desde `probe\`:
  `.\.venv\Scripts\python run_probe.py --providers claude --only D01 --runs 1 --out "$env:PUSHLLM_PRIVADO\diagnostico\spec-013"`
  (1 llamada, comprobado offline); después sdd-implementador sigue con CA-3 (fixture
  sanitizado con la forma anotada en CA-2) y CA-4.
- **2026-09-29 (sdd-arquitecto, enmienda (b))**: CA-2 ejecutado por el orquestador (forma
  en la spec, § "Evidencia de CA-2": caso B, 0 citas, 10 `web_search_result` con `url`,
  0,0729 €, 1 búsqueda). **Queda por pasar al ledger** (sdd-implementador) la fila de CA-2
  con esos datos. El humano eligió **B1**. La spec pasa de `en-progreso` a `bloqueada` y a
  `borrador`, y espera **re-aprobación**. Cambian CA-1 (texto sobre columnas), CA-3
  (B1: `searched_urls` al final de `results.csv`, solo en Claude; compatibilidad con CSV
  antiguos), CA-4, CA-6, y hay un CA-7 nuevo (dictamen de sdd-metricas). CA-1 sigue valiendo
  tal cual. Tras la re-aprobación: sdd-implementador hace CA-3/CA-4 (la aserción de columnas
  de `test_raw_responses.py` (a) pasará a incluir `searched_urls`: citarlo); el orquestador
  pide el dictamen de CA-7 a sdd-metricas y después la llamada de CA-6.
- **2026-09-29 (sdd-arquitecto, enmienda (c))**: el humano no aprobó la (b) y pidió
  `searched_urls` en los tres proveedores. La spec sigue en `borrador` y espera
  aprobación. Cambian:
  - CA-3: Gemini (chunks y supports) y OpenAI (`include=["web_search_call.action.sources"]`).
    Hay corrección del significado de `cited_urls` en Gemini;
  - CA-4: cambian las expectativas de `test_gemini_ok_sums_thoughts_and_tool_tokens` y de
    `test_openai_ok`;
  - CA-5: el dictamen de sdd-probe pasa a ser obligatorio;
  - CA-6: 3 llamadas, ≈ 0,11 €, tope 0,40 €;
  - CA-7: el dictamen de sdd-metricas cubre los tres proveedores.
  F-SPEC-013-1 y F-SPEC-013-2 quedan resueltos dentro de la spec.
- **2026-09-29 (sdd-implementador, fase 2)**: spec re-aprobada (enmiendas (b) y (c)) y pasada a
  `en-progreso`. Hechos con TDD (tests en rojo antes de tocar el código) **CA-2** (evidencia
  copiada), **CA-3** (B1 en los tres proveedores), **CA-4**, **CA-5** (test de parámetros y
  dictamen favorable de sdd-probe) y **CA-7** (el dictamen de sdd-metricas confirma los
  puntos 1 y 5).
  **CA-3 (d), reprocesado offline** de la respuesta real de CA-2 con el adaptador nuevo:
  - `status=ok`;
  - `cited_urls`: 0;
  - `searched_urls`: 10 (10 `web_search_result`, con 10 `url` distintos);
  - todas las citadas están en las consultadas;
  - 1 bloque `text`, así que el texto sale igual que antes: 2 141 caracteres, acaba en
    signo de puntuación, sin cortes a mitad de frase y sin separadores al principio ni al
    final.
  No se ha copiado ninguna URL ni texto.
  **Pendiente: CA-6** (orquestador; tope 0,40 €). Desde `probe\`:
  `.\.venv\Scripts\python run_probe.py --providers claude,openai,gemini --only D01 --runs 1 --out "$env:PUSHLLM_PRIVADO\diagnostico\spec-013-post"`
  Hace **3 llamadas**, una por proveedor (comprobado offline con
  `test_ca6_confirmation_command_makes_exactly_three_calls`). Al anotar CA-6 hay que:
  - contrastar el coste de OpenAI con los ≈ 0,012 € del humo (dictamen de CA-5, punto 2);
  - revisar F-SPEC-013-3 en la respuesta cruda de OpenAI.
  Después, el gate del verificador. La spec se queda en `en-progreso`.
- **2026-09-29 (sdd-implementador, cierre)**:
  - CA-6 lo ejecutó el orquestador. La evidencia y el análisis de la alerta de coste de
    OpenAI están en § "Evidencia CA-6". La alerta queda abierta para el verificador.
  - Los CA de agente están cubiertos: CA-1, CA-3, CA-4, CA-5 (con test y dictamen) y CA-7
    (dictamen). CA-2 y CA-6 son del orquestador y tienen su evidencia en el ledger.
  - La spec pasa a `en-revision`. Siguiente paso: el gate de sdd-verificador. Pendientes
    fuera del código: F-SPEC-013-3 y F-SPEC-013-4 (este, para el arquitecto).
