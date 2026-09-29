---
id: SPEC-002
tipo: ledger
epica: EPIC-001
---
# Ledger — SPEC-002 Ejecución del probe baseline y veredicto de la hipótesis

## Resumen
- Fase: <!-- refleja el estado de la spec; la fuente de verdad es el frontmatter de la spec -->
- Rama: `ft/SPEC-002-ejecucion-del-probe-baseline-y-veredicto-de-la-hipotesis`

## Matriz de criterios de aceptación
<!-- Escritores: sdd-implementador rellena Implementado y Test; sdd-verificador rellena Verif. y Estado. Nunca al revés. -->
<!-- Estados por CA: ✅ cerrado · ⚠️ parcial/con salvedad · 🚧 en curso · ❌ sin empezar · n-a -->
<!-- Un CA está ✅ solo cuando Implementado + Test + Verif. aplicables están en verde. Una salvedad se marca ⚠️, nunca ✅. -->
| CA | Implementado (fichero) | Test (fichero/caso) | Verif. | Estado |
|---|---|---|---|---|
| CA-1 | [Humano] (g) tipo de ubicación y respaldo de `PUSHLLM_PRIVADO` (P-1) por anotar. Soporte del agente (F-SPEC-002-1): `probe/run_probe.py` carga el `.env` de la raíz sin escribir valores; `probe/README.md`; `docs/ciclo-0/guia-claves-api.md`. Comprobaciones de git (a)–(g) ejecutadas por el agente el 2026-09-29, sin abrir `.env`: ver "Evidencia CA-1 y CA-10" | `probe/tests/test_dotenv.py`; `probe/tests/conftest.py` (ningún test lee el `.env` real) | Cierre 2026-09-29 (re-ejecutado por el verificador, sin abrir `.env`): (a) `.gitignore:2:.env`; (b) 0 líneas; (c) `.env` no listado (porcelain vacío); (d) solo `.env.example`, sus 3 `*_API_KEY` vacías, `sk-`/`AIza` 0 en contenido y en `git log -p --all -- .env.example`; (e) patrones de clave en `git log -p --all` → 0 (literales: solo prosa); (f) `git grep` patrones → 0 (11 líneas literales, todas prosa); árbol de trabajo (rg sin `.env` ni `.venv`) → 0; (g) `rev-parse` → `fatal: not a git repository`, fuera del repo. Carga del `.env` revisada: `load_dotenv` no sobrescribe (`if name not in env`), solo imprime nombres; tests con fixtures `FIXTURE-…` sin forma de clave; `conftest.py` autouse redirige `DOTENV_PATH`. P-1 firmado por el humano (ver Veredicto) | ✅ |
| CA-2 | Dictamen sdd-probe (2026-09-29) en este ledger (Notas); `probe/probe_config.json` (Claude → `claude-sonnet-5-5`, fechas y fuentes, `dictamen_date` 2026-09-29, cambio BCE 1,1378 del 2026-09-28; OpenAI y Gemini sin cambio de modelo ni precio) | `probe/tests/test_config.py` — `vigente()` (dictamen fechado más reciente entre los ledgers de SPEC-002 y SPEC-001), `test_vigente_picks_most_recent_date_and_spec_002_on_tie`, `test_spec002_ca2_*` (vigente = SPEC-002, `dictamen_date`, effort, herencia del lote Viveiro), `test_ca1_config_matches_dictamen_literally` (ahora contra el vigente); `python -m pytest probe/tests` → 173 passed (2026-09-29, con F-SPEC-002-1) | Cierre 2026-09-29: `probe_config.json` = tabla del dictamen vigente (Claude `claude-sonnet-5-5`/`web_search_20260209`/`medium`, `max_tokens` 16000; OpenAI `gpt-5.6-luna`/`low`; Gemini `gemini-3.6-flash`/—); `test_config.py::vigente()` elige el más reciente (SPEC-002, 2026-09-29) y `test_ca1_config_matches_dictamen_literally` compara modelo, herramienta y effort; modelos servidos en ambos humos = dictamen; `pytest probe/tests docs/piloto-artica/tools/tests` → 317 passed; `ruff check probe` limpio | ✅ |
| CA-3 | Humo Vigo ejecutado el 2026-09-29 (orquestador, a petición del humano) con el probe de esta rama; evidencia en "Evidencia CA-3 (humo)": 12/12 `ok` (4/4 por proveedor), modelos servidos = dictamen, coste medido 0,1050 € por pregunta × ejecución. **Pendiente**: aceptación del humo por el humano; salvedad F-SPEC-002-7 (Claude sin `cited_urls`) | Revisión a ojo de `D01` por proveedor (agente); recuento desde `$PUSHLLM_PRIVADO/probe-smoke/results.csv` | Cierre 2026-09-29, recalculado desde `results.csv` privado: 12 filas, 4/4 `ok` por proveedor; modelos servidos = dictamen; Σ `cost_eur` 0,3019 / 0,0474 / 0,0705 = 0,4198 € → 0,1050 € por pregunta × ejecución (OpenAI 0,0118 €, el ledger dice 0,0119: redondeo); Claude salida máx. 1356 tokens, 4 respuestas terminan en frase completa; `D01` revisada: español y coherente. Humo aceptado por el humano con la salvedad F-SPEC-002-7 (Claude 0 de 4 `cited_urls`), trasladada a spec aparte | ⚠️ |
| CA-4 | n-a — retirado por cambio de nicho (ADR-008) | n-a | n-a (ADR-008) | n-a |
| CA-5 | n-a — retirado por cambio de nicho (ADR-008) | n-a | n-a (ADR-008) | n-a |
| CA-6 | n-a — retirado por cambio de nicho (ADR-008) | n-a | n-a (ADR-008) | n-a |
| CA-7 | n-a — retirado por cambio de nicho (ADR-008) | n-a | n-a (ADR-008) | n-a |
| CA-8 | n-a — retirado por cambio de nicho (ADR-008) | n-a | n-a (ADR-008) | n-a |
| CA-9 | n-a — retirado por cambio de nicho (ADR-008) | n-a | n-a (ADR-008) | n-a |
| CA-10 | [Verificador]. Agente, 2026-09-29: `git ls-files` sin `results.csv`, `summary.md` ni humo (solo el fixture sintético `probe/tests/fixtures/vigo_results.csv`); los humos están en `$PUSHLLM_PRIVADO` (fuera del repo); `git status --ignored` muestra `probe/out/` con datos sintéticos de tests anteriores, no de esta ejecución (F-SPEC-002-5). Ver "Evidencia CA-1 y CA-10" | — (comprobación por comandos) | Cierre 2026-09-29: `git ls-files` sin `results.csv`/`summary.md`/humos (solo fixtures sintéticos de test); `git status --ignored` → `probe/out/` solo con `piloto-artica/probe/` sintético (2026-09-29 12:58, modelo `claude-sonnet-5`, previo a esta ejecución), no datos de esta ejecución; humos en `$PUSHLLM_PRIVADO` (fuera del repo) | ✅ |

## Veredicto del verificador
<!-- GREEN/RED + fecha + resumen. Lo escribe SOLO sdd-verificador. -->

**GREEN — 2026-09-29 (sdd-verificador, cierre).** Alcance reducido por ADR-008: CA-1, CA-2 y
CA-10 ✅; CA-3 ⚠️ con salvedad aceptada por el humano; CA-4…CA-9 n-a (retirados por cambio
de nicho, ADR-008). Gates re-ejecutados: `pytest probe/tests docs/piloto-artica/tools/tests`
→ 317 passed; `ruff check probe` limpio; `valida.mjs` OK. Todo sin claves ni llamadas a
proveedores; el `.env` no se abrió.

Firmas humanas (fuente: humano Alberto Fojo vía orquestador, 2026-09-29):
- (a) **CA-3: el humano acepta el humo.**
- (b) **P-1**: espacio privado en una **carpeta sincronizada de OneDrive**; respaldo: **la
  sincronización de OneDrive**. (Solo el tipo; la ruta no se anota.) Cierra CA-1 (g).
- (c) **F-SPEC-002-7** (Claude no guarda `cited_urls`): **se arregla antes del baseline de
  Ártica**, en una spec aparte que redacta sdd-arquitecto. No bloquea SPEC-002: salvedad
  conocida y trasladada.

Observaciones (no bloquean):
- V-1: F-SPEC-002-7 afecta también al humo de Viveiro (Claude 0 de 3 `cited_urls`); la
  spec aparte debe estar cerrada antes de SPEC-008 CA-7.
- V-2: `probe/out/piloto-artica/probe/` (ignorado) contiene filas sintéticas antiguas
  (F-SPEC-002-5); no son de esta ejecución, pero SPEC-008 CA-8 exige que no haya datos en
  `probe/out/` al cerrarla: borrarlo antes.
- V-3: `ruff check docs/piloto-artica/tools` da 2 F401 (imports sin usar en
  `count_baseline.py` y `tests/test_baseline_count.py`), código de SPEC-007, no de esta spec.
- V-4: el párrafo "Caduca" del dictamen sigue citando la completa (CA-4, retirada); la regla
  en vigor es F-SPEC-002-6.
- V-5: una carpeta sincronizada replica también borrados y corrupciones; la papelera y el
  historial de versiones de OneDrive mitigan, pero no es una copia independiente.

## Evidencia visual
<!-- Tabla CA → captura en _qa/SPEC-002/. Informe HTML opcional: _qa/SPEC-002/informe.html -->

## Notas — dictámenes de dominio
<!-- Dictámenes emitidos por los roles de dominio (lógica en .ai-context/skills/). Los aplica sdd-implementador leyendo esa lógica. -->

### Dictamen sdd-probe (2026-09-29) — re-comprobación de modelos por defecto (CA-2)
Emisor: sdd-implementador aplicando `.ai-context/skills/sdd-probe.md` (advisory). Invariantes:
D-5, RN-10, No-negociable de coste. Fuentes consultadas online el 2026-09-29 (fecha local).
**Vigente**: sustituye al de SPEC-001 (2026-09-23) para `probe/probe_config.json`;
`probe/tests/test_config.py` compara la config con el dictamen fechado más reciente.
**Caduca**: si la ejecución completa (CA-4) no se lanza como tarde el **2026-10-01**, se
repite (CA-2, ≤ 2 días).

| Proveedor | Modelo | Búsqueda web | Effort | Fuente |
|---|---|---|---|---|
| claude | `claude-sonnet-5-5` | `web_search_20260209` | `medium` | simonwillison.net/2026/Sep/28/claude-sonnet-5-5 ("now the model used for the free tier on claude.ai", 2026-09-28); anthropic.com/claude/sonnet ("Anyone can chat with Claude using Sonnet 5.5 on Claude.ai, available on web, iOS, and Android"); platform.claude.com/docs/en/models/sonnet-5-5/overview (lanzado 2026-09-28; Sonnet 5 pasa a *legacy*) |
| openai | `gpt-5.6-luna` | `web_search` | `low` | releasebot.io/updates/openai/chatgpt (notas de ChatGPT hasta 2026-09-28: GPT-6 Luna solo en Work y Codex, ninguna nota lo lleva a Chat); 9to5mac.com/2026/09/22/openai-upgrading-chatgpt-and-codex-with-two-more-gpt-6-models ("In ChatGPT, the models are available in Work and Codex, but not Chat"; Free/Go solo en la app de escritorio); macrumors.com/2026/08/06/chatgpt-free-unlimited-text-chats (GPT-5.6 Luna default de Free/Go desde 2026-08-06) |
| gemini | `gemini-3.6-flash` | `google_search` | — | gemini.google/release-notes (2026-07-21, 3.6 Flash para todos los usuarios; última nota 2026-09-10 sin cambio de modelo); layer3labs.io/guides/how-to-use-gemini-3-8-flash (act. 2026-09-06: 3.8 Flash en la app solo con AI Pro/Ultra); ai.google.dev/gemini-api/docs/models (`gemini-3.6-flash` estable, sin fecha de retirada) |

- **OpenAI — sin cambios (correcto).** GPT-6 Luna (anunciado el 2026-09-22) **no** es el
  modelo por defecto de ChatGPT Free/Go en Chat (web y móvil): para Free/Go solo está en la
  app de escritorio, y en ChatGPT los modelos GPT-6 Sol/Luna están en Work y Codex, no en
  Chat. Las notas de versión de ChatGPT del 2026-09-23 al 2026-09-28 no lo llevan a Chat. El
  default de Chat sigue siendo GPT-5.6 Luna. Se mantiene `gpt-5.6-luna`. Si antes de la
  completa GPT-6 Luna llega a Chat, se repite este dictamen (pasaría a `gpt-6-luna`,
  0,10/0,50 $ por M, developers.openai.com/api/docs/pricing).
- **Claude — CAMBIA a `claude-sonnet-5-5`.** Sonnet 5.5 salió el 2026-09-28 y es el modelo
  del plan gratuito de claude.ai; Sonnet 5 pasa a *legacy* en la tabla de modelos. Mismo
  precio (2/10 $ por M). Herramienta `web_search_20260209` sin cambios (versión vigente con
  filtrado dinámico, soportada en modelos 4.6 y posteriores). Cambios de Sonnet 5.5 que se
  han revisado contra `probe/providers.py`: `thinking: disabled`, `temperature`/`top_p` no
  por defecto y `tool_choice` forzado devuelven 400, y el adaptador no envía ninguno; el
  texto largo entre llamadas a herramientas vuelve en bloques `thinking` (el adaptador solo
  lee los bloques `text`, así que se pierden esas notas intermedias, no la respuesta final
  con citas). Riesgo a vigilar en el humo (CA-3): el pensamiento adaptativo consume parte de
  `max_tokens` (4000); una fila `empty` o cortada en Claude se escala antes de la completa.
- **Gemini — sin cambios (correcto con la salvedad RN-10 de siempre).** Default de la app
  gratuita: 3.6 Flash; 3.8 Flash solo para AI Pro/Ultra. Sin `user_location` en el
  grounding (F-SPEC-001-1).
- **Effort — se mantiene** `low` en Claude y OpenAI (aceptado por el humano el 2026-09-24,
  F-SPEC-001-5) y el default de la API en Gemini. **Dato nuevo para el humano**: con Sonnet
  5.5 Anthropic publica que el effort por defecto es `medium` "en Claude Code y las apps de
  Claude" y `high` en la API (unite.ai/anthropic-releases-claude-sonnet-5-5-at-unchanged-sonnet-5-pricing,
  2026-09-28), y que los niveles de effort están recalibrados respecto a Sonnet 5. Ya hay
  fuente pública del effort de la app de Claude; esta spec no cambia el effort (CA-2 (c)),
  pero se anota como pregunta abierta (F-SPEC-002-4).
- **Precios (USD, 2026-09-29)**: Claude Sonnet 5.5 2/10 $ por M + 10 $/1000 búsquedas
  (sin cambio); GPT-5.6 Luna 0,20/1,20 $ por M + 10 $/1000 llamadas de búsqueda (sin
  cambio); Gemini 3.6 Flash 0,75/3,75 $ por M hasta 2026-12-31 (1,50/7,50 $ desde
  2027-01-01) + 14 $/1000 consultas, 5000 gratis al mes compartidas entre modelos 3.x (se
  ignoran; sin cambio). **Cambio**: 1 EUR = 1,1378 USD (BCE, 2026-09-28; antes 1,1411), +0,3 %
  en euros.
- **Coste**: la estimación de la completa sigue en ~20–30 € (mismos precios USD; Anthropic
  dice que Sonnet 5.5 cuesta "hasta un 30 % menos" por tarea, no se descuenta). El dictamen de
  coste del lote Viveiro (ledger de SPEC-008, CA-5) sigue valiendo: solo cambia el tipo de
  cambio (+0,3 %), por debajo de su margen; el umbral `c ≤ 0,19 €` no se toca.
- **Lote Viveiro**: `probe/batches/viveiro.json` hereda `providers` y `currency` de
  `probe_config.json` sin copiarlos, así que usa los mismos modelos y precios
  (`test_config.py::test_spec002_ca2_viveiro_batch_inherits_vigente_models_and_prices`).

**Adenda 2026-09-29 — effort de Claude `medium` (decisión humana).** El humano (Alberto
Fojo) resolvió F-SPEC-002-4 el 2026-09-29: el effort de Claude pasa a **`medium`**, como en
la app (D-5: medir lo que ve el paciente). Fuente: unite.ai/anthropic-releases-claude-sonnet-5-5-at-unchanged-sonnet-5-pricing
(2026-09-28: "Defaults are Medium in Claude Code and the Claude apps and High on the Claude
Platform, which is also the API default"). OpenAI sigue en `low` y Gemini con el default de
la API. La tabla de arriba ya refleja `medium` en Claude. Esto supera F-SPEC-001-5 para
Claude. El punto "Effort — se mantiene" de más arriba queda sustituido por esta adenda.
- **`max_tokens` de Claude: 4000 → 16000** (configuración, `probe_config.json`). Fuente:
  platform.claude.com/docs/en/build-with-claude/effort, "Recommended effort levels for
  Claude Sonnet 5.5": "Set `max_tokens` with room for thinking and the reply. Thinking counts
  toward `max_tokens` even when the thinking content isn't returned", y
  platform.claude.com/docs/en/build-with-claude/thinking: el pensamiento se factura como
  tokens de salida. 4000 estaba pensado para `low`; con `medium` el pensamiento adaptativo
  puede comerse el hueco de la respuesta (filas `empty` o cortadas). Techo: el SDK fijado
  (anthropic 1.8.0) rechaza sin streaming un `max_tokens` > 21 333 (10 min estimados), y el
  adaptador no hace streaming; 16000 queda por debajo. `max_tokens` es un tope por petición,
  no un gasto: solo se paga lo que se genera. Tests:
  `test_config.py::test_spec002_ca2_effort_medium_claude_low_openai_api_default_gemini`,
  `::test_spec002_ca2_claude_max_tokens_leaves_room_for_adaptive_thinking`,
  `test_providers.py::test_claude_ok_collects_usage_urls_and_served_model` (el adaptador pasa
  `max_tokens` de la config).
- **Efecto estimado en el coste por llamada de Claude** (supuestos del dictamen CA-5 de
  SPEC-008; no hay cifra pública de tokens de pensamiento por nivel, se estima): el
  pensamiento a `medium` añade salida, estimada en +1k tokens (típico) y +3k (alto) sobre
  0,8k y 1,5k: +0,010 $ y +0,030 $ por llamada (10 $/M de salida). Claude pasa de 0,078 $ a
  ~0,088 $ (típico) y de 0,145 $ a ~0,175 $ (alto). Por pregunta × ejecución con los tres
  proveedores: 0,141 $ → ~0,151 $ (**≈ 0,133 €**) típico y 0,257 $ → ~0,287 $
  (**≈ 0,252 €**) alto (1 EUR = 1,1378 USD). Peor caso acotado por el tope: 40k de entrada +
  16k de salida + 5 búsquedas = 0,29 $ por petición de Claude. Completa del lote Vigo (132
  preguntas × ejecución): ~17,5 € típico / ~33 € alto; el alto roza el tope de 30 € de CA-3,
  que **el humo decide** con la extrapolación medida (Σ `cost_eur` ÷ 4 × 132).
- **Umbral `c ≤ 0,19 €` de SPEC-008: sigue valiendo** como regla, porque se aplica al coste
  **medido** en el humo, que ya incluirá el pensamiento a `medium`. El típico estimado
  (0,133 €) sigue por debajo; el alto (0,252 €) sigue por encima, igual que antes. Lo único
  que cambia es la probabilidad: es algo más fácil caer en la rama de 2 runs en `AV`.

## Evidencia CA-3 (humo)
Ejecutados el 2026-09-29 por el orquestador a petición del humano, con el probe de esta rama
(Claude `claude-sonnet-5-5`, effort `medium`, `max_tokens` 16000). Cifras recalculadas por
el agente desde los `results.csv` privados (sin nombres de clínica junto a cifras).

**Humo Vigo (CA-3)**: `run_probe.py --only D01,E01,F01,O01 --runs 1 --out "$PUSHLLM_PRIVADO\probe-smoke"`.

| Proveedor | Filas | `ok` | Modelo servido | Σ `cost_eur` | € por pregunta × ejecución | Salida máx. (tokens) | Búsquedas | Filas con `cited_urls` |
|---|---|---|---|---|---|---|---|---|
| claude | 4 | 4 | `claude-sonnet-5-5` | 0,3019 € | 0,0755 € | 1356 | 5 | **0 de 4** |
| openai | 4 | 4 | `gpt-5.6-luna` | 0,0474 € | 0,0119 € | 902 | 4 | 4 de 4 |
| gemini | 4 | 4 | `gemini-3.6-flash` | 0,0705 € | 0,0176 € | 1827 | 4 | 3 de 4 |
| **Total** | 12 | 12 | = dictamen de CA-2 | **0,4198 €** | **0,1050 €** | | | |

- ≥ 3 de 4 `ok` por proveedor: sí (4/4). Modelo servido igual al dictamen: sí, los tres.
- Claude sin filas `empty` ni cortadas: la salida máxima es de 1356 tokens, muy por debajo
  del tope de 16000, y las cuatro respuestas terminan en frase completa.
- Revisión a ojo de `D01` (implantes en Vigo), una respuesta por proveedor: las tres en
  español, coherentes con la pregunta, nombran clínicas de Vigo y dan criterios de
  elección. OpenAI cita URLs (directorios y webs de clínicas); Gemini da redirecciones
  `vertexaisearch` (F-SPEC-001-2); **Claude no deja ninguna URL en `cited_urls`** aunque
  busca, y su texto llega partido en fragmentos (F-SPEC-002-7). Gemini `O01`: sin búsqueda
  registrada ni URLs (contestó sin grounding; la columna queda vacía, como está previsto).
- Coste medido: **0,1050 € por pregunta × ejecución** con los tres proveedores (Claude el
  72 %), por debajo de la estimación típica de la adenda (0,133 €).

**Humo Viveiro (SPEC-008 CA-7; aquí solo informativo)**: `--config batches/viveiro.json
--only AV01,AR01,AG01 --runs 1 --out "$PUSHLLM_PRIVADO\piloto-artica\probe-smoke"`: 9/9 `ok`
(3/3 por proveedor), mismos modelos servidos, Σ 0,3425 € → **c = 0,1142 €** (Claude 0,2083 €,
Gemini 0,0904 €, OpenAI 0,0437 €); salida máxima de Claude 1513 tokens; Claude de nuevo sin
`cited_urls` (0 de 3). Con `c ≤ 0,19 €`, la regla de SPEC-008 permite `AV` con 3 runs.

**Aceptación del humo: pendiente de firma humana** (la lleva el orquestador), con el punto
F-SPEC-002-7 por decidir.

## Evidencia CA-1 y CA-10
Comandos ejecutados por sdd-implementador el 2026-09-29 desde la raíz del repo, **sin abrir
`.env`** (solo órdenes de git sobre su ruta):
- (a) `git check-ignore -v .env` → `.gitignore:2:.env	.env`.
- (b) `git log --all --oneline -- .env` → vacío (0 líneas).
- (c) `git status --porcelain` → no lista `.env`.
- (d) `git ls-files` con `.env` en el nombre → solo `.env.example`. En `.env.example`,
  `OPENAI_API_KEY=`, `ANTHROPIC_API_KEY=` y `GEMINI_API_KEY=` están vacías; `sk-`/`AIza`: 0
  coincidencias en su contenido y 0 en `git log -p --all -- .env.example`.
- (e) `git log -p --all` con patrones de clave (`sk-ant-` + 8, `sk-` + 16 o `AIza` + 20
  caracteres de clave) → 0. La búsqueda literal de `sk-`/`sk-ant-`/`AIza` da 16 líneas, todas
  prosa que nombra los prefijos (ADR-006, ADR-007, guía de claves, esta spec y su ledger).
- (f) `git grep` con los mismos patrones de clave → 0; la búsqueda literal solo da esa prosa.
- (g) `git -C "$PUSHLLM_PRIVADO" rev-parse --show-toplevel` → `fatal: not a git
  repository`: no es este repo (raíz `D:/src/tremen-dev/push-llm`). Tipo de ubicación y
  respaldo (P-1): **[Humano]**, pendiente de anotar.
- CA-10: `git ls-files` sin `results.csv`, `summary.md` ni ficheros de humo (solo
  `probe/tests/fixtures/vigo_results.csv`, fixture sintético de tests). `git status
  --ignored` → `.env`, cachés y `probe/out/`; `probe/out/` solo contiene
  `piloto-artica/probe/{results.csv,summary.md}` sintéticos del 2026-09-29 12:58 (tests
  anteriores, F-SPEC-002-5), no los humos, que están en `$PUSHLLM_PRIVADO`.

## Salvedades / follow-ups
<!-- IDs F-SPEC-002-1, F-SPEC-002-2… con destino (spec futura o EPIC-MEJORA). -->
- **F-SPEC-002-1** (2026-09-29, enmienda de CA-1 / ADR-006; → sdd-implementador, tras la
  re-aprobación): (a) actualizar `probe/README.md` ("Keys and output directory"), que hoy
  dice "never in a file inside the repo", para documentar el `.env` en la raíz del árbol de
  trabajo local, ignorado por git, como alternativa a `Read-Host`, con las comprobaciones de
  CA-1 (a)–(d) y el fragmento de carga en PowerShell que se ejecuta desde `probe/`
  (`Get-Content ..\.env | ForEach-Object { if ($_ -match '^\s*([A-Z_]+)\s*=\s*(.+?)\s*$') { Set-Item "env:$($Matches[1])" $Matches[2] } }`);
  (b) actualizar `docs/ciclo-0/guia-claves-api.md`, sección "Custodia de las claves", que
  hoy dice "no se escriben en ningún sitio": `.env` local ignorado + nota segura en el gestor
  de contraseñas para el traslado; nunca email, mensajería ni nube sin cifrar; revocar si se
  filtra (ADR-006 §4–§6); (c) valorar si `run_probe.py` carga `.env` por sí mismo (parser
  mínimo `NOMBRE=valor`, sin dependencias nuevas, sin sobrescribir variables ya definidas en
  el entorno, sin registrar valores en logs ni en `summary.md`, con test offline). Si se
  hace, se documenta en (a) y el fragmento de PowerShell pasa a ser opcional.
  **Hecho 2026-09-29 (sdd-implementador)**: (c) sí: `probe/run_probe.py` (`parse_dotenv`,
  `load_dotenv`, `DOTENV_PATH` = `<raíz>/.env`) carga el `.env` de la raíz al arrancar, sin
  dependencias nuevas; admite comentarios `#`, líneas vacías, `export` y comillas; un valor
  vacío no se carga; nunca sobrescribe una variable ya presente en el entorno; solo informa
  de los **nombres** cargados por stderr, nunca de los valores; sin `.env`, igual que antes.
  Solo lo lee una ejecución real (`main` sin `env` inyectado); los tests usan `.env`
  temporales y `conftest.py` redirige `DOTENV_PATH` en todos los tests
  (`probe/tests/test_dotenv.py`). Con ello el fragmento de PowerShell ya no hace falta y no
  se documenta. (a) `probe/README.md`: sección de claves reescrita (`.env` en la raíz,
  ADR-006/ADR-007, comprobaciones de CA-1 (a)–(d), traslado por nota segura, revocar;
  `Read-Host` queda como alternativa sin fichero) y comandos con `.\.venv\Scripts\python`
  desde `probe\`. (b) `docs/ciclo-0/guia-claves-api.md`, "Custodia de las claves",
  reescrita igual.
- **F-SPEC-002-2** (2026-09-29; → sdd-implementador de SPEC-008): SPEC-008 no duplica la
  restricción (su CA-7 remite a SPEC-002 CA-1, que ahora admite el `.env`), así que la spec
  no se enmienda. Pero las "Instrucciones para el humano (CA-7)" de su ledger solo muestran
  `Read-Host`: añadir la alternativa de cargar el `.env` de la raíz (mismo fragmento que
  F-SPEC-002-1 (a)) y citar ADR-006.
  **Hecho 2026-09-29 (sdd-implementador)**: las instrucciones (CA-7) del ledger de SPEC-008
  ya no usan `Read-Host`: claves en el `.env` de la raíz, que `run_probe.py` carga solo
  (F-SPEC-002-1 (c)); cita ADR-006 y ADR-007. Sin cambios de código en SPEC-008.
- **F-SPEC-002-3** (2026-09-29; → humano): negar a los agentes la lectura de `.env` en la
  configuración local de permisos (ADR-006, consecuencias). Fuera del alcance de los roles.
- **F-SPEC-002-4** — **RESUELTO 2026-09-29 por el humano: Claude `medium`** (ver adenda del
  dictamen; `max_tokens` 4000 → 16000). Texto original (2026-09-29, dictamen sdd-probe de CA-2; → humano / sdd-arquitecto):
  con Sonnet 5.5 Anthropic publica que el effort por defecto de las apps de Claude es
  `medium` (API: `high`) y que los niveles están recalibrados. El effort `low` aceptado el
  2026-09-24 (F-SPEC-001-5) se eligió "sin fuente pública del effort de las apps", y esa
  premisa ya no se cumple para Claude. Esta spec lo mantiene (CA-2 (c)); decidir si se
  sube a `medium` en Claude (más coste por llamada) o se deja y se anota en las
  limitaciones de CA-8.
- **F-SPEC-002-5** (2026-09-29; → verificador / humano): existe `probe/out/piloto-artica/probe/results.csv`
  (ignorado por git) con filas sintéticas del 2026-09-29 ("Te recomiendo Clínica Ártica",
  tokens 100/10), no de una ejecución real. No es de esta spec; revisarlo en CA-10
  (`git status --ignored`) y borrarlo si nadie lo necesita.
- **F-SPEC-002-6** (2026-09-29, alcance reducido por ADR-008; → orquestador para SPEC-008
  CA-7 y SPEC-012): CA-2 ya no caduca con la completa de Vigo, pero el dictamen de modelos
  (2026-09-29) sigue caducando para cualquier **ejecución real**: se re-comprueba (sdd-probe)
  si el baseline del lote de Viveiro (SPEC-008 CA-7) se lanza después del **2026-10-01**
  (misma regla de ≤ 2 días), y en la medición semanal (SPEC-012) al menos una vez al mes o
  cuando sdd-probe sepa de un cambio de modelo por defecto en una app (p. ej. GPT-6 Luna en
  Chat). SPEC-008 está aprobada y no se enmienda aquí: se lleva como instrucción de
  ejecución; si se quiere vinculante, enmienda de SPEC-008 CA-7 o CA de SPEC-012.
- **F-SPEC-002-7** (2026-09-29, humos; → humano / orquestador; posible arreglo en el
  adaptador de Claude): en las 7 filas de Claude de los dos humos, `cited_urls` sale vacío
  aunque hay búsquedas (1–2 por llamada), y el texto de la respuesta llega partido en
  fragmentos unidos por saltos de línea. Hipótesis sin confirmar (no se guarda la respuesta
  cruda): con `web_search_20260209` la búsqueda va por *dynamic filtering* (code execution)
  y las citas no llegan como `web_search_result_location` con `url`, que es lo único que lee
  `probe/providers.py`; además el adaptador une los bloques `text` con `\n`. No cambia las
  menciones (se leen del texto) ni el coste, pero CA-3 pide "URLs en `cited_urls` si el
  proveedor las da", y el piloto usará las fuentes. Opciones: (i) aceptar el humo con esta
  salvedad y abrir un arreglo (leer las URLs de los bloques de resultados de búsqueda y unir
  los fragmentos sin `\n`), con test sobre una respuesta grabada; (ii) fijar
  `allowed_callers: ["direct"]` o volver a `web_search_20250305` (decisión de sdd-probe:
  cambia lo que se sondea). No se ha tocado código.
  **Decisión humana 2026-09-29** (humano Alberto Fojo vía orquestador; registrada por
  sdd-verificador): se arregla **antes del baseline de Ártica** en una spec aparte
  (sdd-arquitecto). No bloquea SPEC-002: salvedad conocida y trasladada; CA-3 ⚠️.

## Cómo retomar (handoff)
<!-- Estado real del trabajo para la siguiente sesión: qué está hecho, qué falta, dónde seguir. -->
- **2026-09-29 (sdd-arquitecto)**: spec en `borrador` por la enmienda de CA-1 y P-2 (claves
  en `.env` local ignorado, ADR-006 en `borrador`). Necesita re-aprobación humana de la spec
  y aprobación de ADR-006. Después: F-SPEC-002-1 y F-SPEC-002-2.
- **2026-09-29 (sdd-implementador)**: spec en `en-progreso`. Hecho: CA-2 (dictamen vigente
  en Notas; Claude pasa a `claude-sonnet-5-5`; OpenAI y Gemini sin cambios) y
  F-SPEC-002-1/-2 (carga del `.env` por `run_probe.py`, README, guía de claves, ledger de
  SPEC-008). Siguiente: [Humano] CA-1 (comprobaciones) y los dos humos (ver
  "Instrucciones para el humano"); después el agente revisa el humo (CA-3). **CA-2 caduca**
  si la completa no se lanza como tarde el 2026-10-01. La spec se queda en `en-progreso`
  hasta que existan CA-3…CA-9.
- **2026-09-29 (sdd-arquitecto) — alcance reducido (ADR-008)**: el humano cambia el nicho
  (A Mariña primero; Vigo y Pontevedra aparcados) y cierra EPIC-001. La spec pasa
  `en-progreso` → `bloqueada` → `borrador` y se queda con CA-1, CA-2 (effort `medium` de
  Claude incorporado), CA-3 (coste medido por pregunta × ejecución, sin extrapolar a la
  completa) y CA-10; CA-4…CA-9 retirados (se marcan `n-a`, "retirado por cambio de nicho
  (ADR-008)"). Necesita **re-aprobación humana** (y ADR-008). Después: sdd-implementador
  pasa a `en-progreso` y rellena CA-3 con el humo de Vigo ya ejecutado el 2026-09-29;
  humano: comprobaciones de CA-1; verificador: CA-1, CA-2, CA-3, CA-10.

- **2026-09-29 (sdd-implementador)**: tras la re-aprobación con alcance reducido, spec en
  `en-progreso` y después `en-revision`. CA-3 rellenado con los humos reales (12/12 y 9/9
  `ok`, modelos = dictamen, 0,1050 € y 0,1142 € por pregunta × ejecución); aceptación del
  humo **pendiente de firma humana**, con la salvedad F-SPEC-002-7. CA-1: comprobaciones de
  git (a)–(g) hechas por el agente; falta que el humano anote P-1. CA-10: evidencia
  preliminar. CA-4…CA-9 `n-a` en mis columnas (el Estado es del verificador). Siguiente:
  sdd-verificador (CA-1, CA-2, CA-3, CA-10).

## Instrucciones para el humano (humos, CA-3)
Claves en el `.env` de la raíz del repo (copia de `.env.example` con los valores
rellenos); `PUSHLLM_PRIVADO` como variable de usuario. `run_probe.py` carga el `.env` solo:
sin `Read-Host` ni fragmentos de PowerShell. Desde `probe\` en PowerShell:

```powershell
if (-not $env:PUSHLLM_PRIVADO) { throw "PUSHLLM_PRIVADO no está definida" }
.\.venv\Scripts\python -m pytest -q tests

# Humo Vigo (CA-3): 4 preguntas x 1 run x 3 proveedores = 12 llamadas
.\.venv\Scripts\python run_probe.py --only D01,E01,F01,O01 --runs 1 --out "$env:PUSHLLM_PRIVADO\probe-smoke"

# Humo Viveiro (SPEC-008 CA-7): 3 preguntas x 1 run x 3 proveedores = 9 llamadas
.\.venv\Scripts\python run_probe.py --config batches/viveiro.json --only AV01,AR01,AG01 --runs 1 --out "$env:PUSHLLM_PRIVADO\piloto-artica\probe-smoke"
```

- Claude va con effort `medium` y `max_tokens` 16000 (adenda del dictamen): en el humo,
  mira también que ninguna fila de Claude salga `empty` o cortada.
- La primera línea de stderr debe decir `loaded from .env: ANTHROPIC_API_KEY, GEMINI_API_KEY, OPENAI_API_KEY (values not shown)`
  (solo las que no estén ya en la sesión); si sale `skip <proveedor>: … not set`, falta esa
  clave en el `.env`.
- En `results.csv` la columna `model` de Claude debe ser `claude-sonnet-5-5` (dictamen
  vigente); OpenAI `gpt-5.6-luna`, Gemini `gemini-3.6-flash`.
- Después, avisa: con eso el agente rellena CA-3 aquí y CA-7 (humo) en SPEC-008. La completa
  (CA-4) necesita humo aceptado, SPEC-006 en `hecho` y este dictamen con ≤ 2 días.
