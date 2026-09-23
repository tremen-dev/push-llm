---
id: SPEC-001
tipo: ledger
epica: EPIC-001
---
# Ledger — SPEC-001 Ajustes del probe para el baseline

## Resumen
- Fase: <!-- refleja el estado de la spec; la fuente de verdad es el frontmatter de la spec -->
- Rama: `ft/SPEC-001-ajustes-del-probe-para-el-baseline`

## Matriz de criterios de aceptación
<!-- Escritores: sdd-implementador rellena Implementado y Test; sdd-verificador rellena Verif. y Estado. Nunca al revés. -->
<!-- Estados por CA: ✅ cerrado · ⚠️ parcial/con salvedad · 🚧 en curso · ❌ sin empezar · n-a -->
<!-- Un CA está ✅ solo cuando Implementado + Test + Verif. aplicables están en verde. Una salvedad se marca ⚠️, nunca ✅. -->
| CA | Implementado (fichero) | Test (fichero/caso) | Verif. | Estado |
|---|---|---|---|---|
| CA-1 | `probe/probe_config.json`; dictamen sdd-probe en este ledger (Notas) | `probe/tests/test_config.py` — `test_ca1_*` (lee la tabla del dictamen y compara modelo, herramienta y effort) | Dictamen sdd-probe fechado (2026-09-23) con id, herramienta, effort y fuente por proveedor; `test_config.py::test_ca1_*` parsea la tabla del ledger y compara con `probe_config.json` (no tautológico) → pass. Fuentes externas no re-verificables offline; ver F-SPEC-001-3 | ✅ |
| CA-2 | `probe/settings.py` (`load_config`, `resolve_model`), `probe/probe_config.json`, `probe/run_probe.py`, `probe/providers.py` | `test_config.py` — `test_ca2_*` (config cambiada, precedencia env, sin ids/precios literales en `probe/*.py`); `test_run_probe.py` — `test_ca2_model_used_comes_from_config_file`, `test_ca2_env_var_overrides_model_in_run` | `grep -nE "(claude|gpt|gemini)-[0-9a-z]" probe/*.py` vacío (rc=1); `test_ca2_*` (config temporal cambia el modelo usado por `main`, precedencia env, sin precios literales) → pass; precios con fecha y fuente en config | ✅ |
| CA-3 | `probe/providers.py` (`ask`, `ProviderResult`, `cost_eur`), `probe/run_probe.py` (`COLUMNS`) | `probe/tests/test_providers.py` (3 proveedores × ok/error/refusal/empty, pause_turn, coste); `test_run_probe.py` — `test_ca3_*` | `test_providers.py`: 3 proveedores × ok/error/refusal/empty + pause_turn + coste → pass; `test_ca3_*` comprueba las 16 columnas en fila real. Forma de kwargs y respuestas contrastada offline con los tipos de anthropic 1.8.0, openai 3.19.1 y google-genai 2.25.0 (output_config.effort, reasoning, WebSearchTool20260209, user_location, GroundingMetadata, usage fields) | ✅ |
| CA-4 | `probe/analysis.py` (`analyze`, `render_summary`) | `probe/tests/test_analysis.py` — `test_ca4_*` | `test_ca4_*` con fixture (error/refusal/empty fuera de num./den., conteo por proveedor×especialidad en summary) → pass; reproducido con CLI real `--analyze` | ✅ |
| CA-5 | `probe/analysis.py`; `probe/run_probe.py --analyze` | `test_analysis.py` — `test_ca5_*` (fixture con cifras a mano); `test_run_probe.py` — `test_ca5_analyze_mode_never_calls_providers` | Cifras recalculadas a mano: dental ponderado 0,375/0,90 = 41,7 %, fertility 0,375/0,65 = 57,7 %, líder dental Clínica Torres 2/4 → coinciden. `test_ca5_analyze_mode_never_calls_providers` (ADAPTERS y ask lanzan) → pass; CLI real `--analyze` sin claves: 0 imports de anthropic/openai/genai/httpx (`-X importtime`) | ✅ |
| CA-6 | `probe/matching.py` (`find_mentions`, `short_alias_hits`, `is_local_clinic`); dictamen sdd-metricas en este ledger (Notas) | `probe/tests/test_matching.py` ("IVI Vigo", "IVI" solo, "Villoria" en estética y oftalmología, marca repetida, solapes); `test_analysis.py` — `test_ca6_short_alias_bias_reported` | Dictamen sdd-metricas en ledger; `test_matching.py` (IVI solo no cuenta, "IVI Vigo", Villoria estética/oftalmología, repetición cuenta 1, solape largo gana) y líder filtrado por `spec_of` → pass. Nombres de marca únicos en brands.csv (dedupe por id seguro) | ✅ |
| CA-7 | `probe/run_probe.py` (`--resume`) | `test_run_probe.py` — `test_ca7_resume_only_calls_missing_or_failed_combinations`, `test_without_resume_refuses_to_overwrite_existing_results` | `test_ca7_resume_only_calls_missing_or_failed_combinations` (cuenta llamadas, bytes previos intactos con `startswith`) → pass. Observación: filas error/refusal previas siguen contando como "excluidas" tras un reintento con éxito (ver veredicto) | ✅ |
| CA-8 | `probe/run_probe.py` (`output_dir`, `--out`, `PUSHLLM_PRIVADO`), `.gitignore` (`probe/out/`) | `test_run_probe.py` — `test_ca8_*` (incluye `git check-ignore`) | `git check-ignore -v probe/out/results.csv` → `.gitignore:18:probe/out/`; `test_ca8_*` (--out > PUSHLLM_PRIVADO/probe > probe/out) → pass; `git ls-files probe` sin salidas; diff sin claves | ✅ |
| CA-9 | `probe/requirements.txt`, `probe/README.md` | Revisión README; `pip install -r probe/requirements.txt` en venv limpio OK (2026-09-23, Python 3.13.7); `test_run_probe.py` — `test_smoke_selection_is_twelve_calls` | README revisado: requirements fijados, humo 12 llamadas (`--only D01,E01,F01,O01 --runs 1`), completo 396, `--analyze`, `--resume`, claves en PowerShell (Read-Host) y bash (read -rs) sin ficheros. `pip install -r probe/requirements.txt` en venv limpio del verificador (Python 3.13.7) OK | ✅ |
| CA-10 | `probe/tests/` (conftest, fakes) | `python -m pytest probe/tests` → 69 passed (2026-09-23, sin claves ni red; también en venv limpio) | `python -m pytest probe/tests` → 69 passed (Python global) y 69 passed en venv limpio sin ANTHROPIC/OPENAI/GEMINI_API_KEY | ✅ |

## Veredicto del verificador
<!-- GREEN/RED + fecha + resumen. Lo escribe SOLO sdd-verificador. -->
**GREEN — 2026-09-24, sdd-verificador.** CA-1…CA-10 ✅. Verificación offline (sin claves ni red hacia proveedores): suite re-ejecutada (69 passed, también en venv limpio con requirements fijados), grep de ids vacío, `git check-ignore` OK, CLI real `--analyze` sin importar SDKs, cifras de CA-5 recalculadas a mano, kwargs de los adaptadores contrastados con los tipos de los SDK fijados. Sin cambios en FOUNDATION, reglas ni ADR. Observaciones no bloqueantes:
- V-1 (baja): tras `--resume`, las filas error/refusal/empty antiguas de una combinación luego resuelta siguen en `results.csv` y en el recuento "Excluidas" de `summary.md` (`analysis.py` no deduplica por (prompt, proveedor, run)). No afecta a numeradores ni denominadores; leer "Excluidas" como intentos fallidos, no como huecos.
- V-2 (baja): `--out` acepta una ruta dentro del repo no ignorada; la protección depende de usar `PUSHLLM_PRIVADO` o el default.
- V-3 (info): `summary.md` contiene cifras por clínica nombrada: es salida privada (ADR-001), no copiar al repo sin anonimizar (SPEC-002/003).
- V-4 (info): ruff 0.16 con reglas por defecto marca 10 avisos de estilo (I001, BLE001 intencionado, ISC004); con E/F limpio. El proyecto no configura linter.

## Evidencia visual
<!-- Tabla CA → captura en _qa/SPEC-001/. Informe HTML opcional: _qa/SPEC-001/informe.html -->
n-a: sin UI (CLI y análisis offline); evidencia por comandos en la matriz.

## Notas — dictámenes de dominio
<!-- Dictámenes emitidos por los roles de dominio (lógica en .ai-context/skills/). Los aplica sdd-implementador leyendo esa lógica. -->

### Dictamen sdd-probe (2026-09-23) — modelos y parámetros de llamada (CA-1)
Veredicto global: **correcto con una duda** (OpenAI, transitorio). Invariantes: D-5, RN-10,
No-negociable de coste. Todas las fuentes consultadas online el 2026-09-23.

| Proveedor | Modelo | Búsqueda web | Effort | Fuente |
|---|---|---|---|---|
| claude | `claude-sonnet-5` | `web_search_20260209` | `low` | anthropic.com/news/claude-sonnet-5 ("default model for Free and Pro plans", desde 2026-07-01); platform.claude.com/docs/en/about-claude/models/overview |
| openai | `gpt-5.6-luna` | `web_search` | `low` | macrumors.com/2026/08/06/chatgpt-free-unlimited-text-chats (default Free/Go desde 2026-08-06); developers.openai.com/api/docs/models/gpt-5.6-luna |
| gemini | `gemini-3.6-flash` | `google_search` | — | gemini.google/release-notes (2026-07-21, 3.6 Flash para todos los usuarios de la app); ai.google.dev/gemini-api/docs/models |

- **Claude — correcto.** El default anterior `claude-opus-5` es gama premium y violaba D-5.
  Sonnet 5 es el modelo por defecto de claude.ai Free. Herramienta `web_search_20260209`
  (versión vigente con filtrado dinámico, soportada en Sonnet 5; existe `web_search_20260318`,
  que solo añade `response_inclusion`, irrelevante aquí). `max_uses` 5, `user_location` Vigo.
- **OpenAI — dudoso (transitorio).** El 2026-09-22 OpenAI anunció GPT-6 Luna, que llega a
  Free/Go "en la app de escritorio" y "aún no en Chat", con despliegue gradual
  (techcrunch.com/2026/09/22/openai-launches-gpt-6-sol-and-luna; 9to5mac.com/2026/09/22/…).
  Hoy el default de Chat (web/móvil, lo que usa el paciente) sigue siendo GPT-5.6 Luna.
  **Re-verificar justo antes de SPEC-002**: si GPT-6 Luna ya es el default de Chat, cambiar
  `probe_config.json` a `gpt-6-luna` (0,10 $/0,50 $ por M tokens) o usar `OPENAI_MODEL`.
- **Gemini — correcto con salvedad.** Default de la app gratuita: 3.6 Flash. 3.8 Flash (GA
  2026-09-02) solo figura para AI Pro/Ultra en la app. **Salvedad RN-10**: la API de
  grounding con Google Search no documenta `user_location`; la ubicación va solo en el
  texto del prompt (todos citan Vigo/Pontevedra). Ver F-SPEC-001-1.
- **Effort (dudoso, sin fuente pública del effort de las apps)**: Claude `low` (como el
  script original) y OpenAI `reasoning.effort=low`; Gemini con el default de la API. Según
  `06-models-costs-and-usage-share.md` §1A, en preguntas locales decide la búsqueda, no la
  inteligencia del modelo, así que se prima el coste. Pregunta abierta para el humano.
- **Precios (USD, 2026-09-23)**: Claude Sonnet 5 2/10 $ por M + 10 $/1000 búsquedas;
  GPT-5.6 Luna 0,20/1,20 $ por M + 10 $/1000 llamadas de búsqueda; Gemini 3.6 Flash
  0,75/3,75 $ por M (hasta 2026-12-31) + 14 $/1000 consultas (se ignoran las 5000 gratis
  al mes: estimación conservadora). Cambio: 1 EUR = 1,1411 USD (BCE, 2026-09-23).
  Estimación ejecución completa (396 llamadas): ~20–30 €, dentro de la horquilla de EPIC-001.
- **Métricas de uso por fila**: Claude `usage.input_tokens/output_tokens` +
  `usage.server_tool_use.web_search_requests`, URLs de `citations[].url`; OpenAI
  `usage.input_tokens/output_tokens`, nº de ítems `web_search_call`, URLs de anotaciones
  `url_citation`; Gemini `usage_metadata.prompt_token_count(+tool_use_prompt_token_count)`
  y `candidates_token_count+thoughts_token_count`, búsquedas = nº de
  `grounding_metadata.web_search_queries`, URLs de `grounding_chunks[].web.uri` (son
  redirecciones `vertexaisearch.cloud.google.com`, no la URL final: F-SPEC-001-2).

### Dictamen sdd-metricas (2026-09-23) — definiciones del análisis (CA-6)
Veredicto: **correcto**, con una pregunta para el humano sobre RN-01. Invariantes: RN-01,
RN-02, RN-03, RN-04, D-6. Fuentes: `docs/fundacion/reglas.md`, `07-mvp-product-spec.md` §4,
`03-local-market-vigo-pontevedra.md` §2, `06-models-costs-and-usage-share.md` §4.

1. **Respuesta válida** = fila con `status=ok`. Las filas `error`, `refusal` y `empty` no
   entran ni en numerador ni en denominador (RN-02 habla de respuestas; un fallo no lo es)
   y se reportan aparte por proveedor × especialidad.
2. **Clínica local** = marca de `brands.csv` con `type ≠ directory` y `city ∈ {Vigo,
   Pontevedra}`, de cualquier especialidad (la hipótesis de 03 §2 pregunta si se nombra
   "una clínica de Vigo", no una de la especialidad).
3. **Alias < 4 caracteres**: se aplica RN-01 tal cual — "IVI" o "MIA" solos NO cuentan;
   "IVI Vigo" (nombre de marca, 8 caracteres) sí. Para medir el sesgo sin cambiar la regla,
   el resumen informa aparte de cuántas respuestas válidas contienen un alias corto como
   palabra suelta sin que se haya contado la marca. **Pregunta para el humano** (cambio de
   RN-01, no lo decide este dictamen): ¿excepción para alias cortos inequívocos (IVI)?
4. **Solapes y alias compartidos**: el matching es por palabras completas sobre texto
   normalizado; si una ocurrencia está contenida en otra más larga ("Clínica Villoria"
   dentro de "Clínica Villoria L'Essence") solo cuenta la larga. Un alias compartido por
   varias marcas ("Villoria", "Povisa", "Vitaldent") se asigna a las candidatas de la
   especialidad del prompt; si quedan varias, a las de la ciudad del prompt; si aún quedan
   varias (o ninguna encaja), a todas las candidatas.
5. **Deduplicación**: una respuesta cuenta como mucho una vez por marca.
6. **Ponderación (RN-03/RN-04)**: por especialidad, Σ(% proveedor × peso) ÷ Σ pesos de los
   proveedores con ≥ 1 respuesta válida en esa especialidad. Pesos iniciales RN-04 en
   `probe_config.json` (OpenAI 0,55, Gemini 0,25, Claude 0,10; Perplexity no se sondea).
7. **Marca líder** de una especialidad: solo entre marcas de esa especialidad; frecuencia =
   nº de respuestas válidas de prompts de esa especialidad (todos los proveedores) que la
   nombran; % sobre esas respuestas válidas. Empates: se listan todas. En `hospital` no hay
   marcas de esa especialidad en `brands.csv`: líder vacío.
8. **Directorios**: por especialidad, nº y % de respuestas válidas que nombran cada
   directorio (deduplicado por respuesta).

## Salvedades / follow-ups
<!-- IDs F-SPEC-001-1, F-SPEC-001-2… con destino (spec futura o EPIC-MEJORA). -->
- **F-SPEC-001-1** (RN-10, Gemini sin ubicación): el grounding con Google Search de la API de Gemini no documenta `user_location`; la ubicación va solo en el texto del prompt. Destino: humano / SPEC-002 (contraste manual en app real).
- **F-SPEC-001-2** (URLs de Gemini): `grounding_chunks[].web.uri` son redirecciones `vertexaisearch.cloud.google.com`; resolver a la URL final hace falta para SPEC-003 / Ciclo 1. Destino: SPEC-003.
- **F-SPEC-001-3** (modelo OpenAI transitorio): GPT-6 Luna anunciado el 2026-09-22 para Free/Go, aún no en Chat. Re-verificar el default justo antes de SPEC-002 y, si cambió, actualizar `probe_config.json` (o `OPENAI_MODEL`). Destino: SPEC-002.
- **F-SPEC-001-4** (RN-01, pregunta al humano): "IVI"/"MIA" solos no cuentan; el resumen informa el sesgo aparte. ¿Excepción a RN-01 para alias cortos inequívocos? Cambio de regla: lo decide el humano.
- **F-SPEC-001-5** (effort): no hay fuente pública del effort de las apps de consumo; se usa `low` en Claude y OpenAI por coste. Pregunta al humano.
- **F-SPEC-001-6** (alias ambiguos por texto): "Clínica Villoria" (nombre de marca de oftalmología) en una respuesta de estética cuenta para oftalmología, no para L'Essence; "De Castro" puede dar falsos positivos (apellido común). Revisión manual de SPEC-002 CA-6.
- **F-SPEC-001-7** (comportamiento añadido): sin `--resume`, el probe se niega a sobrescribir un `results.csv` existente (protege el No-negociable de guardar respuestas en bruto). No lo pedía la spec.

## Cómo retomar (handoff)
<!-- Estado real del trabajo para la siguiente sesión: qué está hecho, qué falta, dónde seguir. -->
- 2026-09-23, sdd-implementador: CA-1…CA-10 implementados con tests en la rama `ft/SPEC-001-ajustes-del-probe-para-el-baseline` (sin push). Pendiente: verificación (sdd-verificador).
- Verificar: `python -m pytest probe/tests` desde la raíz; `grep -nE "(claude|gpt|gemini)-[0-9a-z]" probe/*.py` vacío; `git check-ignore -v probe/out/results.csv`; `pip install -r probe/requirements.txt` en venv limpio.
- No se ha llamado a ninguna API real. Antes de SPEC-002: re-verificar modelos por defecto (F-SPEC-001-3).
