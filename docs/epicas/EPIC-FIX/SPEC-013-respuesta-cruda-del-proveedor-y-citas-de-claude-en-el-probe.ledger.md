---
id: SPEC-013
tipo: ledger
epica: EPIC-FIX
---
# Ledger — SPEC-013 Respuesta cruda del proveedor y citas de Claude en el probe

## Resumen
- Fase: <!-- refleja el estado de la spec; la fuente de verdad es el frontmatter de la spec -->
- Rama: `ft/SPEC-013-respuesta-cruda-del-proveedor-y-citas-de-claude-en-el-probe` (apilada
  sobre `ft/SPEC-002-…`, aún sin merge)

## Matriz de criterios de aceptación
<!-- Escritores: sdd-implementador rellena Implementado y Test; sdd-verificador rellena Verif. y Estado. Nunca al revés. -->
<!-- Estados por CA: ✅ cerrado · ⚠️ parcial/con salvedad · 🚧 en curso · ❌ sin empezar · n-a -->
<!-- Un CA está ✅ solo cuando Implementado + Test + Verif. aplicables están en verde. Una salvedad se marca ⚠️, nunca ✅. -->
| CA | Implementado (fichero) | Test (fichero/caso) | Verif. | Estado |
|---|---|---|---|---|
| CA-1 | `probe/providers.py` (`ProviderResult.request/responses`, `raw_json`, `scrub`, `FORBIDDEN_KEYS`; captura en `_claude`/`_openai`/`_gemini` y `ask`), `probe/run_probe.py` (`RAW_NAME`, `raw_line`, append en el bucle), `probe/README.md` § Output | `probe/tests/test_raw_responses.py`: (a) `test_ca1a_one_line_per_call_with_the_row_keys`; (b) `test_ca1b_pause_turn_line_has_one_response_per_turn`, `test_claude_pause_turn_keeps_one_response_per_turn`; (c) `test_ca1c_no_headers_nor_keys_in_the_file`, `test_gemini_raw_drops_sdk_http_response_and_headers`, `test_real_sdk_objects_serialize_without_http_headers`, `test_forbidden_keys_removed_at_any_depth_case_insensitive`; error: `test_ca1_error_line_has_empty_responses_and_the_message`, `test_error_keeps_request_and_no_responses`; (d) `test_ca1d_resume_appends_and_never_rewrites`; (e) `test_ca1e_analyze_neither_reads_nor_modifies_raw`; (f) `test_ca1f_default_output_raw_file_is_gitignored`; sin recorte: `test_claude_raw_keeps_request_and_full_response`; columnas de `results.csv`: aserción en (a) | | ❌ |
| CA-2 | Comando comprobado offline (1 llamada) | `test_raw_responses.py::test_ca2_diagnostic_command_makes_exactly_one_claude_call` | | ❌ |
| CA-3 | | | | ❌ |
| CA-4 | | | | ❌ |
| CA-5 | | | | ❌ |
| CA-6 | | | | ❌ |

## Veredicto del verificador
<!-- GREEN/RED + fecha + resumen. Lo escribe SOLO sdd-verificador. -->

## Evidencia visual
<!-- Tabla CA → captura en _qa/SPEC-013/. Informe HTML opcional: _qa/SPEC-013/informe.html -->

## Salvedades / follow-ups
<!-- IDs F-SPEC-013-1, F-SPEC-013-2… con destino (spec futura o EPIC-MEJORA). -->

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
