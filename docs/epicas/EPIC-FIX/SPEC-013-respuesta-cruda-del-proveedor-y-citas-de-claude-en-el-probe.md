---
id: SPEC-013
tipo: spec
epica: EPIC-FIX
estado: en-progreso
aprobada-por: Alberto Fojo
historial:
  - {estado: borrador, fecha: 2026-09-29, por: sdd-arquitecto}
  - {estado: aprobada, fecha: 2026-09-29, por: Alberto Fojo}
  - {estado: en-progreso, fecha: 2026-09-29, por: sdd-implementador}
---
# SPEC-013 — Respuesta cruda del proveedor y citas de Claude en el probe

## Problema
Bug **F-SPEC-002-7** (ledger de SPEC-002, "Salvedades / follow-ups", registrado por
sdd-implementador el 2026-09-29). En las 7 filas de Claude de los humos del 2026-09-29
(`claude-sonnet-5-5`, `web_search_20260209`, effort `medium`; humo Vigo `D01…O01` y humo
Viveiro `AV01,AR01,AG01`):

1. `cited_urls` sale **vacío** aunque Claude hizo 1–2 búsquedas por llamada.
2. El texto de la respuesta llega **partido en fragmentos** unidos por saltos de línea.

No cambia las menciones (se leen del texto, RN-01/RN-11) ni el coste, pero vacía el
análisis de fuentes de Claude, que es la base del diagnóstico por palancas (SPEC-011,
EPIC-002) y lo que pide SPEC-002 CA-3 ("URLs en `cited_urls` si el proveedor las da").

Además, el probe **no guarda la respuesta cruda del proveedor**, solo el texto extraído
(columna `answer`). Eso impide confirmar la causa y contradice el No-negociable de
FOUNDATION "Las respuestas en bruto de los proveedores se guardan siempre".

**Qué dice la documentación oficial de Anthropic** (consultada el **2026-09-29**):
- *Web search tool*, platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool:
  con `web_search_20260209` o posterior, Claude "writes and runs code that filters the
  results first" (**dynamic filtering**); "the tool's `allowed_callers` field defaults to
  `["code_execution_20260120"]`"; "To call web search directly, without dynamic filtering,
  set `allowed_callers: ["direct"]`". En respuesta: bloques `server_tool_use` y
  `web_search_tool_result` (cada `web_search_result` con `url`, `title`,
  `encrypted_content`, `page_age`); "When a search runs through dynamic filtering, the
  response also contains the code execution tool's result blocks, and each nested
  `server_tool_use` and `web_search_tool_result` pair carries a `caller` field". Citas:
  "Citations are always enabled for web search", cada `web_search_result_location` con
  `url`, `title`, `encrypted_index`, `cited_text`. La página **no** muestra un ejemplo de
  respuesta con dynamic filtering ni dice si las citas cambian de forma en ese caso.
- *Server tools*, platform.claude.com/docs/en/agents-and-tools/tool-use/server-tools
  (§ "ZDR and allowed_callers", § "The server-side loop and pause_turn"): las versiones
  `_20260209` "default to the code execution caller only; earlier versions default to
  `["direct"]`"; `pause_turn` se continúa reenviando el turno tal cual.
- *Citations*, platform.claude.com/docs/en/build-with-claude/citations (§ "Response
  structure"): "When citations are enabled, responses include multiple text blocks with
  citations" — la respuesta es la concatenación de varios bloques `text`, partidos a mitad
  de frase (`"According to the document, "`, `"the grass is green"`, `" and "`…).

Consecuencia: el síntoma 2 está **explicado por la documentación**: `probe/providers.py`
une los bloques `text` con `"\n"`, y con citas activas un párrafo llega en muchos bloques.
Que el texto llegue partido indica además que **sí hay bloques con citas**; por qué su `url`
no se lee (forma distinta de la cita con dynamic filtering, citas solo en bloques anidados,
o ninguna cita) **no está confirmado**: lo confirma CA-2 con una respuesta grabada.

## Usuarios / roles afectados
- **[Humano]** (Alberto Fojo): aprueba esta spec; autoriza el gasto de la llamada real;
  decide en el caso B de CA-3.
- **[Orquestador]**: lanza la(s) llamada(s) real(es) de CA-2 y CA-6 con el `.env`, que lee
  el propio probe (ADR-006 §5); lee la respuesta cruda del espacio privado para el
  diagnóstico.
- **[Agente]** sdd-implementador: CA-1, CA-3, CA-4 (TDD, sin llamadas reales).
- **[Agente]** sdd-probe: dictamen de CA-5 (advisory).
- **[Agente]** sdd-verificador: gate.
- **Ningún agente lee, abre ni imprime `.env`** (ADR-006 §5), tampoco para diagnosticar.
- Afecta aguas abajo a SPEC-002 CA-3 (salvedad F-SPEC-002-7), a SPEC-008 CA-7 (baseline con
  probe del piloto, que **espera a esta spec** por decisión del humano del 2026-09-29) y a
  SPEC-011 (fuentes citadas).

## Criterios de aceptación
Orden de ejecución: CA-1 → CA-2 → CA-3 → CA-4/CA-5 → CA-6.

- **CA-1 — Respuesta cruda guardada en privado [Agente].**
  Dado un run del probe con cualquiera de los tres proveedores (incluido `--resume`),
  cuando el adaptador recibe la respuesta del SDK,
  entonces `run_probe.py` añade una línea por llamada a `raw_responses.jsonl` **en el mismo
  directorio que `results.csv`** (por defecto `$PUSHLLM_PRIVADO/<output_subdir>`; ADR-001,
  ADR-004 §2), con: `timestamp_utc`, `prompt_id`, `provider`, `run` y `model` idénticos a
  los de su fila de `results.csv`; `status`; `request` (parámetros enviados: modelo, `tools`,
  `system`, `max_tokens`, effort y el texto de la pregunta; nunca el cliente ni sus
  credenciales); y `responses`: la lista de **todas** las respuestas del SDK de esa llamada
  (una por turno, incluidas las de `pause_turn`) serializadas a JSON completo, sin recortar
  (se conservan `encrypted_content` y `encrypted_index`). Una llamada con `status=error`
  deja su línea con `responses` vacía y el mensaje de error.
  Tests (con clientes falsos, sin red) que demuestran:
  (a) una línea por llamada y claves de enlace iguales a las de la fila;
  (b) con `pause_turn`, `responses` tiene tantas entradas como turnos;
  (c) **sin cabeceras ni claves**: a ninguna profundidad aparece una clave llamada
  `headers`, `sdk_http_response`, `api_key`, `authorization` ni `x-api-key` (el objeto de
  Gemini trae `sdk_http_response` con cabeceras: se excluye), y el valor de una clave falsa
  inyectada en el entorno del test no aparece en el fichero;
  (d) `--resume` añade líneas y nunca reescribe ni borra las existentes;
  (e) `--analyze` no lee ni modifica `raw_responses.jsonl`;
  (f) con la salida por defecto dentro del repo (`probe/out/…`), el fichero queda ignorado
  por git (`git check-ignore`).
  `probe/README.md` documenta el fichero, su contenido y que es dato privado (ADR-001).
  `results.csv` **no cambia de columnas**.

- **CA-2 — Diagnóstico con evidencia grabada [Humano] autoriza → [Orquestador] ejecuta →
  [Orquestador/Agente] anota.**
  Dado CA-1 implementado y en verde, y la autorización del humano para gastar ≤ 0,25 €,
  cuando el orquestador ejecuta **una sola llamada** real, desde `probe\`, con el `.env`
  cargado por el propio probe:
  `.\.venv\Scripts\python run_probe.py --providers claude --only D01 --runs 1 --out "$env:PUSHLLM_PRIVADO\diagnostico\spec-013"`
  (misma pregunta que falló en el humo Vigo; lote Vigo por defecto, sin tocar la salida del
  piloto), entonces queda en ese directorio privado un `raw_responses.jsonl` con la
  respuesta cruda, y el ledger de SPEC-013 recoge, **sin copiar texto de la respuesta, URLs
  ni nombres de clínica**: fecha y hora, modelo servido, coste de la fila, número de
  búsquedas, y la **forma** de la respuesta: lista ordenada de tipos de bloque de primer
  nivel (con `caller` si lo hay), número de bloques `text`, cuántos traen `citations`, los
  `type` de cita observados y en qué campo viene la URL, y si hay `web_search_tool_result`
  anidados con URLs. El diagnóstico concluye **caso A** (hay citas con URL legible en algún
  sitio de la respuesta) o **caso B** (no hay citas con URL; solo resultados de búsqueda), y
  cita la documentación oficial de este documento con su fecha de consulta.
  Si la llamada devuelve `status=error`, se anota el error y se repite **una** vez como
  máximo; el total de CA-2 no pasa de 2 llamadas.

- **CA-3 — Arreglo del adaptador de Claude con TDD sobre un fixture derivado [Agente].**
  Dado el diagnóstico de CA-2, cuando sdd-implementador crea
  `probe/tests/fixtures/claude_web_search_20260209.json` con **la misma estructura** que la
  respuesta grabada (mismos tipos de bloque, orden, anidamiento, campos `caller`,
  posición y `type` de las citas y número de bloques `text` en que se parte un párrafo),
  pero **sanitizado**: texto sustituido por texto sintético de una clínica ficticia, URLs
  sustituidas por dominios de ejemplo (`example.org`…), `encrypted_*` e `id` sustituidos
  por marcadores, sin ninguna cadena copiada de la respuesta real (ADR-001: la respuesta en
  bruto vive solo en privado); y escribe primero los tests que fallan con el código actual,
  entonces, tras el arreglo:
  (a) **caso A**: `cited_urls` contiene las URLs de todas las citas de la respuesta, sin
  duplicados, en orden de aparición (sigue siendo "URLs citadas", no "URLs consultadas");
  (b) **texto completo, sin fragmentar**: los bloques `text` consecutivos se concatenan
  **sin separador** (como indica la doc de *Citations*); solo se inserta `"\n\n"` entre
  tramos de texto separados por un bloque que no es `text` (búsqueda, resultado, código),
  y lo mismo al continuar tras `pause_turn`. Para el fixture, `r.text` es igual,
  carácter a carácter, al texto sintético esperado escrito a mano en el test;
  (c) el test existente `test_claude_pause_turn_accumulates_usage_and_text` se actualiza a
  la nueva regla de unión (cambio de expectativa explícito, citado en el ledger);
  (d) re-procesar **offline** la respuesta cruda real de CA-2 (en el espacio privado, sin
  llamar al proveedor) con el adaptador nuevo da `cited_urls` no vacío en el caso A y un
  texto sin cortes a mitad de frase; el ledger anota solo el recuento de URLs y la
  comprobación, no las URLs ni el texto.
  **Caso B**: el implementador **para** tras CA-1 y el fixture, no cambia la configuración
  ni rellena `cited_urls` con URLs de resultados de búsqueda, y la spec vuelve a
  `borrador` para que el humano elija, con dictamen de sdd-probe (CA-5), entre
  (B1) columna nueva de URLs consultadas (cambia el esquema de `results.csv` y lo que mide
  SPEC-011) o (B2) `allowed_callers: ["direct"]` / otra versión del tool (cambia lo que se
  sondea). El arreglo del texto (b) sí se entrega en ambos casos.

- **CA-4 — Sin regresiones [Agente].**
  Dado el cambio, cuando se ejecuta `python -m pytest -q probe/tests` y
  `python -m pytest -q docs/piloto-artica/tools/tests` y `ruff check probe` desde la raíz
  del repo, entonces todo está en verde; en particular siguen en verde, sin cambiar sus
  expectativas: los tests de OpenAI y Gemini de `test_providers.py`, el golden de Vigo
  (`test_pilot_batch.py::test_ca4_vigo_summary_identical_to_before_the_change`) y los tests
  del lote Viveiro (`test_pilot_batch.py`). El único test existente cuya expectativa cambia
  es el de CA-3 (c).

- **CA-5 — Modo de búsqueda: sin cambio, o con dictamen [Agente sdd-probe].**
  Dado el arreglo, cuando se comparan los parámetros que el adaptador de Claude envía antes
  y después (tool `type`, `allowed_callers`, `max_uses`, `user_location`, modelo, effort,
  `max_tokens`), entonces o bien son idénticos (lo demuestra un test sobre los `kwargs`
  del cliente falso, y no hace falta dictamen), o bien **cualquier** diferencia lleva un
  dictamen fechado de sdd-probe en el ledger de SPEC-013 (invariantes D-5 y RN-10: qué
  cambia de lo que ve el usuario de claude.ai, fuentes, fecha) y la aprobación del humano
  **antes** del merge. Un cambio de modo sin dictamen es RED.

- **CA-6 — Confirmación en real [Humano] autoriza → [Orquestador] ejecuta.**
  Dado CA-3 caso A en verde, cuando el orquestador repite la llamada de CA-2 con el código
  arreglado y `--out "$env:PUSHLLM_PRIVADO\diagnostico\spec-013-post"` (1 llamada,
  ≤ 0,25 €), entonces la fila de Claude tiene `status=ok`, `cited_urls` no vacío y
  `answer` sin cortes a mitad de frase, y su línea de `raw_responses.jsonl` existe. El
  ledger anota fecha, coste y recuento de URLs (sin URLs ni texto). Si el humano prefiere
  ahorrarse la llamada, CA-6 se da por cubierto con CA-3 (d) más el primer humo de SPEC-008
  CA-7, y el verificador lo marca ⚠️ hasta ese humo.

## Entidades y reglas afectadas
- FOUNDATION, No-negociables: "Las respuestas en bruto de los proveedores se guardan
  siempre; las llamadas son idempotentes y seguras ante reintentos" (CA-1).
- ADR-001 (espacio privado, respuestas en bruto solo en `PUSHLLM_PRIVADO`; `probe/out/`
  ignorado), ADR-004 §2 (respuestas en bruto del piloto, en privado), ADR-006 §5 (ningún
  agente lee el `.env`; el probe carga las claves).
- D-5 y RN-10 (modelo por defecto con búsqueda web y ubicación): no se tocan salvo por CA-5.
- RN-01/RN-11: las menciones se siguen leyendo del texto; el texto sin fragmentar no
  cambia qué nombres aparecen, solo quita saltos de línea espurios.
- Código: `probe/providers.py` (`_claude`; serialización cruda en los tres adaptadores),
  `probe/run_probe.py` (escritura de `raw_responses.jsonl`), `probe/tests/fakes.py`,
  `probe/tests/test_providers.py`, `probe/tests/test_run_probe.py`, `probe/README.md`.
- Documentación oficial citada en "Problema" (consultada el 2026-09-29).

## Fuera de alcance
- Cambiar modelo, versión del tool, `allowed_callers`, effort o `max_uses` (solo vía CA-5,
  caso B y aprobación humana).
- Columna nueva en `results.csv` (caso B1: requiere enmienda de esta spec).
- Re-ejecutar los humos de SPEC-002 o SPEC-008, o reescribir sus `results.csv`: los humos
  antiguos se quedan como están; no hay respuesta cruda que re-procesar.
- Análisis de fuentes (qué dominios cita Claude): es de SPEC-011.
- Retención o borrado de `raw_responses.jsonl` (lo cubre ADR-001 y su dictamen pendiente).
- Tocar los ledgers de SPEC-002 y SPEC-008 (el orquestador enlaza allí esta spec cuando
  termine el verificador que trabaja en ellos).

## Notas para el gate humano
- **Épica: EPIC-FIX (nueva, bucket), no EPIC-002.** El defecto vive en el adaptador de
  Claude del probe (código de SPEC-001, EPIC-001), afecta a los dos lotes (Vigo y Viveiro)
  y el guardado de respuestas crudas es una deuda contra un No-negociable de FOUNDATION,
  no una tarea del piloto. EPIC-001 está bloqueada/cerrada por ADR-008 y EPIC-002 es un
  piloto concierge manual (D-4) cuyos criterios no incluyen herramientas. Lo que sí liga a
  EPIC-002 es la dependencia: SPEC-008 CA-7 espera a esta spec.
- **Qué aprobar**: (1) la spec; (2) el gasto de CA-2: **1 llamada** a Claude, estimada en
  **≈ 0,07–0,08 €** (en los humos, Claude costó ≈ 0,076 € por llamada en Vigo y ≈ 0,069 € en
  Viveiro; una búsqueda son 0,01 $), tope 0,25 € y como mucho 2 llamadas si la primera
  da error; (3) CA-6 opcional, otra llamada del mismo coste (o sustituirla por el primer
  humo de SPEC-008 CA-7).
- **Mirar con lupa**:
  - La **regla de unión del texto** (CA-3 b): concatenación sin separador dentro de un
    tramo y `"\n\n"` entre tramos separados por búsquedas. El preámbulo "voy a buscar…"
    se conserva en `answer` (no se filtra texto: filtrar sería decidir qué es respuesta).
  - **`cited_urls` sigue significando "citadas"**. Si CA-2 da caso B, no se rellenará con
    URLs consultadas sin tu decisión: te tocará elegir B1 (columna nueva) o B2 (sondeo
    directo sin dynamic filtering, que se aleja de cómo busca claude.ai si este usa
    filtrado; necesita dictamen de sdd-probe).
  - **Fixture sin datos reales**: por ADR-001 la respuesta en bruto no entra al repo; el
    fixture copia la forma, no el contenido. La prueba sobre el contenido real (CA-3 d) se
    hace offline en el espacio privado y solo deja recuentos en el ledger.
  - `raw_responses.jsonl` guarda `encrypted_content` completo: pesa (estimado decenas de KB
    por llamada; unos MB por baseline completo), pero es lo que hace la auditoría
    reproducible. Es dato privado de clase 1 (ADR-001).
- **Rama**: `ft/SPEC-013-…`, apilada sobre la rama activa de SPEC-002 (aún sin merge).
