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
| CA-1 | [Humano] comprobaciones (a)–(g) pendientes. Soporte del agente (F-SPEC-002-1): `probe/run_probe.py` carga el `.env` de la raíz (`parse_dotenv`, `load_dotenv`) sin escribir valores; `probe/README.md` (claves, comprobaciones (a)–(d)); `docs/ciclo-0/guia-claves-api.md` (Custodia) | `probe/tests/test_dotenv.py` (parser, no sobrescribe, sin `.env` igual que antes, valores ausentes de stdout/stderr/`results.csv`/`summary.md`; valores de fixture sin prefijos `sk-`/`sk-ant-`/`AIza` para no ensuciar las búsquedas (e)–(f)); `probe/tests/conftest.py` (ningún test lee el `.env` real) | | ❌ |
| CA-2 | Dictamen sdd-probe (2026-09-29) en este ledger (Notas); `probe/probe_config.json` (Claude → `claude-sonnet-5-5`, fechas y fuentes, `dictamen_date` 2026-09-29, cambio BCE 1,1378 del 2026-09-28; OpenAI y Gemini sin cambio de modelo ni precio) | `probe/tests/test_config.py` — `vigente()` (dictamen fechado más reciente entre los ledgers de SPEC-002 y SPEC-001), `test_vigente_picks_most_recent_date_and_spec_002_on_tie`, `test_spec002_ca2_*` (vigente = SPEC-002, `dictamen_date`, effort, herencia del lote Viveiro), `test_ca1_config_matches_dictamen_literally` (ahora contra el vigente); `python -m pytest probe/tests` → 173 passed (2026-09-29, con F-SPEC-002-1) | | ❌ |
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
- **F-SPEC-002-4** (2026-09-29, dictamen sdd-probe de CA-2; → humano / sdd-arquitecto):
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

- La primera línea de stderr debe decir `loaded from .env: ANTHROPIC_API_KEY, GEMINI_API_KEY, OPENAI_API_KEY (values not shown)`
  (solo las que no estén ya en la sesión); si sale `skip <proveedor>: … not set`, falta esa
  clave en el `.env`.
- En `results.csv` la columna `model` de Claude debe ser `claude-sonnet-5-5` (dictamen
  vigente); OpenAI `gpt-5.6-luna`, Gemini `gemini-3.6-flash`.
- Después, avisa: con eso el agente rellena CA-3 aquí y CA-7 (humo) en SPEC-008. La completa
  (CA-4) necesita humo aceptado, SPEC-006 en `hecho` y este dictamen con ≤ 2 días.
