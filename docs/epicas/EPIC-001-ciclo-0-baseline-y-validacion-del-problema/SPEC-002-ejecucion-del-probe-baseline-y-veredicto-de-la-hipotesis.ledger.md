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
| CA-1 | | | | ❌ |
| CA-2 | Dictamen sdd-probe (2026-09-29) en este ledger (Notas); `probe/probe_config.json` (Claude → `claude-sonnet-5-5`, fechas y fuentes, `dictamen_date` 2026-09-29, cambio BCE 1,1378 del 2026-09-28; OpenAI y Gemini sin cambio de modelo ni precio) | `probe/tests/test_config.py` — `vigente()` (dictamen fechado más reciente entre los ledgers de SPEC-002 y SPEC-001), `test_vigente_picks_most_recent_date_and_spec_002_on_tie`, `test_spec002_ca2_*` (vigente = SPEC-002, `dictamen_date`, effort, herencia del lote Viveiro), `test_ca1_config_matches_dictamen_literally` (ahora contra el vigente); `python -m pytest probe/tests` → 161 passed (2026-09-29) | | ❌ |
| CA-3 | | | | ❌ |
| CA-4 | | | | ❌ |
| CA-5 | | | | ❌ |
| CA-6 | | | | ❌ |
| CA-7 | | | | ❌ |
| CA-8 | | | | ❌ |
| CA-9 | | | | ❌ |
| CA-10 | | | | ❌ |

## Veredicto del verificador
<!-- GREEN/RED + fecha + resumen. Lo escribe SOLO sdd-verificador. -->

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
| claude | `claude-sonnet-5-5` | `web_search_20260209` | `low` | simonwillison.net/2026/Sep/28/claude-sonnet-5-5 ("now the model used for the free tier on claude.ai", 2026-09-28); anthropic.com/claude/sonnet ("Anyone can chat with Claude using Sonnet 5.5 on Claude.ai, available on web, iOS, and Android"); platform.claude.com/docs/en/models/sonnet-5-5/overview (lanzado 2026-09-28; Sonnet 5 pasa a *legacy*) |
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
- **F-SPEC-002-2** (2026-09-29; → sdd-implementador de SPEC-008): SPEC-008 no duplica la
  restricción (su CA-7 remite a SPEC-002 CA-1, que ahora admite el `.env`), así que la spec
  no se enmienda. Pero las "Instrucciones para el humano (CA-7)" de su ledger solo muestran
  `Read-Host`: añadir la alternativa de cargar el `.env` de la raíz (mismo fragmento que
  F-SPEC-002-1 (a)) y citar ADR-006.
- **F-SPEC-002-3** (2026-09-29; → humano): negar a los agentes la lectura de `.env` en la
  configuración local de permisos (ADR-006, consecuencias). Fuera del alcance de los roles.

## Cómo retomar (handoff)
<!-- Estado real del trabajo para la siguiente sesión: qué está hecho, qué falta, dónde seguir. -->
- **2026-09-29 (sdd-arquitecto)**: spec en `borrador` por la enmienda de CA-1 y P-2 (claves
  en `.env` local ignorado, ADR-006 en `borrador`). Necesita re-aprobación humana de la spec
  y aprobación de ADR-006. Después: F-SPEC-002-1 y F-SPEC-002-2.
