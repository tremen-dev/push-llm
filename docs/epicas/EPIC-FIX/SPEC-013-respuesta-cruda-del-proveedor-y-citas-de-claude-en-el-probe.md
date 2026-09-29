---
id: SPEC-013
tipo: spec
epica: EPIC-FIX
estado: borrador
aprobada-por: Alberto Fojo
historial:
  - {estado: borrador, fecha: 2026-09-29, por: sdd-arquitecto}
  - {estado: aprobada, fecha: 2026-09-29, por: Alberto Fojo}
  - {estado: en-progreso, fecha: 2026-09-29, por: sdd-implementador}
  - {estado: bloqueada, fecha: 2026-09-29, por: sdd-arquitecto}
  - {estado: borrador, fecha: 2026-09-29, por: sdd-arquitecto}
---
# SPEC-013 — Respuesta cruda del proveedor y citas de Claude en el probe

> **Enmienda 2026-09-29 (b) (sdd-arquitecto): caso B, opción B1.** CA-2 se ejecutó
> (evidencia en § "Evidencia de CA-2") y el resultado es el **caso B**: Claude consulta
> URLs pero no las cita. El humano (Alberto Fojo, 2026-09-29) eligió **B1**: una columna
> nueva `searched_urls` al final de `results.csv` con las URLs consultadas, sin cambiar
> cómo pregunta el probe (se mantiene el filtrado dinámico por defecto, fiel a D-5).
> Rechazó B2 (búsqueda directa) y "aceptar sin fuentes".
> Cambian: CA-1 (deja de decir que `results.csv` no cambia de columnas), **CA-3** (arreglo
> B1 sobre un fixture con la forma de CA-2), CA-4 (compatibilidad con `results.csv`
> antiguos), CA-6 (la confirmación exige `searched_urls` poblado en Claude), **CA-7 nuevo**
> (dictamen de `sdd-metricas` sobre cómo cuentan las URLs consultadas en el análisis de
> fuentes), Entidades, Fuera de alcance y Notas. CA-2 y CA-5 no cambian. CA-1 sigue
> implementado (commit `e82bbe7`) y vale tal cual. La spec vuelve a `borrador` (estaba
> `en-progreso`) y necesita **nueva aprobación humana**.

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

## Evidencia de CA-2 (forma de la respuesta, sin texto ni URLs)
Llamada ejecutada por el orquestador el **2026-09-29**, con autorización del humano:
`--providers claude --only D01 --runs 1`, 1 llamada, **coste 0,0729 €**, **1 búsqueda**.
Respuesta cruda en privado: `$PUSHLLM_PRIVADO/diagnostico/spec-013/raw_responses.jsonl`
(37,6 KB; ADR-001). El implementador copia estos datos al ledger (CA-2).
- `request.tools`: `web_search_20260209` **sin `allowed_callers`**, es decir, con el valor
  por defecto `["code_execution_20260120"]` (filtrado dinámico, según *Web search tool* y
  *Server tools*, consultadas el 2026-09-29).
- 1 turno, `stop_reason=end_turn`. 9 bloques de primer nivel en `content`, en este orden:
  1. `server_tool_use`
  2. `server_tool_use` con `caller=code_execution_20260120`
  3. `web_search_tool_result` con `caller=code_execution_20260120`
  4. `code_execution_tool_result`
  5. `server_tool_use`
  6. `code_execution_tool_result`
  7. `server_tool_use`
  8. `code_execution_tool_result`
  9. `text`
- `text`: **1 bloque, 0 con `citations`**. No hay ningún `type` de cita ni campo con URL
  en citas.
- `web_search_tool_result.content`: lista de **10 `web_search_result`**, cada uno con las
  claves `encrypted_content`, `page_age`, `title`, `type`, `url`. Los resultados de búsqueda
  están en primer nivel de `content` (con `caller`), no anidados dentro de
  `code_execution_tool_result`.
- `code_execution_tool_result`: 3, con contenido `encrypted_code_execution_result` ×1 y
  `code_execution_result` ×2.
- Esta vez el texto final llega **en un solo bloque**, sin fragmentar. La fragmentación de
  los humos anteriores pudo venir de otra ruta (varios tramos de texto entre búsquedas, o
  citas en otras respuestas). La regla de unión de CA-3 (b) se mantiene.
- **Conclusión: caso B.** Claude consulta URLs (10 resultados con `url`) y no cita
  ninguna. La documentación dice "Citations are always enabled for web search", pero no
  muestra ninguna respuesta con filtrado dinámico. Lo observado es que en ese modo no
  llegan citas. Es una sola llamada: no prueba que Claude nunca cite, solo que esta vez no
  citó. Por eso el adaptador sigue leyendo las citas si llegan (CA-3 a).

## Usuarios / roles afectados
- **[Humano]** (Alberto Fojo): aprueba esta spec; autoriza el gasto de la llamada real;
  decide en el caso B de CA-3 (decidido: B1, 2026-09-29) y re-aprueba la enmienda.
- **[Orquestador]**: lanza la(s) llamada(s) real(es) de CA-2 y CA-6 con el `.env`, que lee
  el propio probe (ADR-006 §5); lee la respuesta cruda del espacio privado para el
  diagnóstico.
- **[Agente]** sdd-implementador: CA-1, CA-3, CA-4 (TDD, sin llamadas reales).
- **[Agente]** sdd-probe: dictamen de CA-5 (advisory; solo si cambia el modo).
- **[Agente]** sdd-metricas: dictamen de CA-7 (advisory).
- **[Agente]** sdd-verificador: gate.
- **Ningún agente lee, abre ni imprime `.env`** (ADR-006 §5), tampoco para diagnosticar.
- Afecta aguas abajo a SPEC-002 CA-3 (salvedad F-SPEC-002-7), a SPEC-008 CA-7 (baseline con
  probe del piloto, que **espera a esta spec** por decisión del humano del 2026-09-29) y a
  SPEC-011 (fuentes citadas; con B1, también las consultadas de Claude, CA-7).

## Criterios de aceptación
Orden de ejecución: CA-1 → CA-2 → CA-3 → CA-4/CA-5 → CA-6. CA-7 puede ir en paralelo
con CA-3 y tiene que estar antes del gate del verificador.

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
  CA-1 no cambia las columnas de `results.csv`. La columna nueva la añade CA-3 (B1).

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

- **CA-3 — Arreglo del adaptador de Claude, opción B1, con TDD sobre un fixture derivado
  [Agente].**
  Dado el diagnóstico de CA-2 (caso B) y la decisión B1 del humano, cuando
  sdd-implementador crea `probe/tests/fixtures/claude_web_search_20260209.json` con **la
  misma estructura** que la respuesta grabada (los 9 bloques de primer nivel en el orden de
  § "Evidencia de CA-2", con los mismos `type` y `caller`; 10 `web_search_result` con las
  mismas claves; 3 `code_execution_tool_result` con los mismos tipos de contenido; 1 bloque
  `text` sin `citations`; `stop_reason=end_turn`), pero **sanitizado** (texto sintético de
  una clínica ficticia; URLs de ejemplo en dominios reservados, `example.org`, `example.com`
  y parecidos, con al menos una URL repetida para probar la deduplicación; `encrypted_*` e
  `id` sustituidos por marcadores; ninguna cadena copiada de la respuesta real; ADR-001), y
  escribe primero los tests que fallan con el código actual, entonces, tras el arreglo:
  (a) **`cited_urls` sigue significando "URLs citadas"**: para el fixture queda **vacía**;
  el adaptador sigue leyendo el `url` de las citas de los bloques `text` cuando las hay
  (el test existente `test_claude_ok_collects_usage_urls_and_served_model` sigue en verde
  sin cambiar su expectativa), y **nunca** mete en `cited_urls` URLs de resultados de
  búsqueda;
  (b) **URLs consultadas**: `ProviderResult` tiene un campo nuevo `searched_urls` (lista).
  En Claude contiene el `url` de cada `web_search_result` de **todo** bloque
  `web_search_tool_result` de primer nivel de `content`, con `caller` o sin él (llamada
  directa o `code_execution_*`), de **todos** los turnos (incluidas las continuaciones de
  `pause_turn`), sin duplicados y en orden de aparición. Para el fixture es exactamente la
  lista de URLs de ejemplo esperada, escrita a mano en el test. Un
  `web_search_tool_result` cuyo `content` no es una lista (error de la herramienta, p. ej.
  `web_search_tool_result_error`) no aporta URLs ni rompe la llamada (test propio). Con
  `status=error`, `searched_urls` queda vacía;
  (c) **texto completo, sin fragmentar**: los bloques `text` consecutivos se concatenan
  **sin separador** (como indica la doc de *Citations*); solo se inserta `"\n\n"` entre
  tramos de texto separados por un bloque que no es `text` (búsqueda, resultado, código),
  y lo mismo al continuar tras `pause_turn`; nunca al principio ni al final. Para el
  fixture, `r.text` es igual, carácter a carácter, al texto sintético esperado escrito a
  mano en el test. Un segundo test, con varios bloques `text` partidos a mitad de frase y
  un bloque de búsqueda en medio (forma de la doc de *Citations*), fija la regla de unión.
  El test existente `test_claude_pause_turn_accumulates_usage_and_text` se actualiza a la
  nueva regla (cambio de expectativa explícito, citado en el ledger);
  (d) **columna `searched_urls` en `results.csv`**: `run_probe.COLUMNS` termina en
  `…, "cited_urls", "answer", "searched_urls"` (la columna nueva va **al final**, después de
  `answer`, para no mover ninguna columna existente), con las URLs unidas por `;`, como
  `cited_urls`. Contenido por proveedor:
  - **Claude**: la lista de (b).
  - **OpenAI**: **vacía**. La API Responses solo devuelve las fuentes consultadas de un
    `web_search_call` si se pide expresamente
    (`include=["web_search_call.action.sources"]`), y eso cambia los parámetros de la
    llamada, cosa que esta spec no hace (CA-5). Rellenarla queda como follow-up
    (F-SPEC-013 en el ledger, con dictamen de sdd-probe).
  - **Gemini**: **vacía**. `grounding_metadata.grounding_chunks` ya alimenta `cited_urls`,
    y esta spec no cambia lo que significa (Fuera de alcance). La API no da otra lista
    separada de páginas consultadas.
  - Vacía en OpenAI y Gemini significa "no medido", no "ninguna". Lo dice el README.
  Tests (clientes falsos, sin red): una fila de Claude con el fixture tiene `searched_urls`
  poblado y `cited_urls` vacío; las filas de OpenAI y Gemini con sus fakes actuales tienen
  `searched_urls` vacío;
  (e) **compatibilidad con `results.csv` antiguos** (sin la columna):
  - `--analyze` sobre un `results.csv` antiguo funciona y da el mismo `summary.md` que
    antes. `analysis.py` no lee `searched_urls` ni `cited_urls` y **no cambia** (lo prueba
    el golden de Vigo de CA-4). Además, el mismo `results.csv` con la columna nueva
    añadida da un `summary.md` idéntico byte a byte (test);
  - `--resume` sobre un `results.csv` antiguo **no reescribe la cabecera ni las filas
    existentes**. Las filas nuevas se escriben con las columnas de la cabecera que ya tiene
    el fichero, así que en ese fichero no se escribe `searched_urls`. En stderr sale un
    aviso: `results.csv` sin `searched_urls` (anterior a SPEC-013), no se añade la columna
    al reanudar, y las URLs consultadas están en `raw_responses.jsonl`. Test: las filas
    antiguas quedan idénticas byte a byte, cada fila nueva tiene tantos campos como la
    cabecera, y el aviso aparece;
  - `--resume` sobre un `results.csv` que ya tiene la columna escribe `searched_urls`
    normalmente;
  (f) re-procesar **offline** la respuesta cruda real de CA-2 (en el espacio privado, sin
  llamar al proveedor, con un cliente falso que devuelve la respuesta grabada) con el
  adaptador nuevo da `cited_urls` vacío, `searched_urls` con tantas URLs únicas como
  `url` distintos haya entre los 10 resultados, y un texto sin cortes a mitad de frase. El
  ledger anota solo los recuentos y la comprobación, no las URLs ni el texto;
  (g) `probe/README.md` documenta `searched_urls` (qué contiene por proveedor, que vacía
  en OpenAI/Gemini significa "no medido", la diferencia con `cited_urls` y el
  comportamiento con `--resume` sobre ficheros antiguos) y deja de decir que las columnas
  de `results.csv` no cambian.
  No se cambia la configuración del tool (CA-5).

- **CA-4 — Sin regresiones y compatibilidad [Agente].**
  Dado el cambio, cuando se ejecuta `python -m pytest -q probe/tests` y
  `python -m pytest -q docs/piloto-artica/tools/tests` y `ruff check probe` desde la raíz
  del repo, entonces todo está en verde; en particular siguen en verde, sin cambiar sus
  expectativas: los tests de OpenAI y Gemini de `test_providers.py` (su `cited_urls` no
  cambia), `test_claude_ok_collects_usage_urls_and_served_model`, el golden de Vigo
  (`test_pilot_batch.py::test_ca4_vigo_summary_identical_to_before_the_change`) y los tests
  del lote Viveiro (`test_pilot_batch.py`). **El golden de Vigo no se regenera**: su
  entrada `probe/tests/fixtures/vigo_results.csv` se queda **sin** la columna
  `searched_urls`, a propósito, y así el golden prueba también que `--analyze` lee un
  `results.csv` antiguo (CA-3 e). `vigo_summary_before.md` no se toca. Si el golden
  cambiara, sería un defecto del cambio, no un motivo para regenerarlo. Los únicos tests
  existentes cuya expectativa cambia son el de la regla de unión de CA-3 (c) y, si hace
  falta, las aserciones de columnas de `test_raw_responses.py` y `test_run_probe.py`, que
  pasan a incluir `searched_urls` al final. Cada uno se cita en el ledger.

- **CA-5 — Modo de búsqueda: sin cambio, o con dictamen [Agente sdd-probe].**
  Dado el arreglo, cuando se comparan los parámetros que el adaptador de Claude envía antes
  y después (tool `type`, `allowed_callers`, `max_uses`, `user_location`, modelo, effort,
  `max_tokens`), entonces o bien son idénticos (lo demuestra un test sobre los `kwargs`
  del cliente falso, y no hace falta dictamen), o bien **cualquier** diferencia lleva un
  dictamen fechado de sdd-probe en el ledger de SPEC-013 (invariantes D-5 y RN-10: qué
  cambia de lo que ve el usuario de claude.ai, fuentes, fecha) y la aprobación del humano
  **antes** del merge. Un cambio de modo sin dictamen es RED.

- **CA-6 — Confirmación en real [Humano] autoriza → [Orquestador] ejecuta.**
  Dado CA-3 (B1) y CA-4 en verde, cuando el orquestador repite la llamada de CA-2 con el
  código arreglado y `--out "$env:PUSHLLM_PRIVADO\diagnostico\spec-013-post"` (1 llamada,
  ≤ 0,25 €, estimada en ≈ 0,07 €), entonces la fila de Claude tiene `status=ok`, la
  cabecera de `results.csv` termina en `searched_urls`, **`searched_urls` está poblado**
  (≥ 1 URL si `web_searches ≥ 1`), `cited_urls` contiene solo URLs de citas (vacío si la
  respuesta no trae citas), `answer` no tiene cortes a mitad de frase, y la línea de
  `raw_responses.jsonl` existe. El ledger anota fecha, coste, número de búsquedas y los
  recuentos de `searched_urls` y `cited_urls` (sin URLs ni texto). Si la llamada da
  `status=error`, se repite una vez como máximo. Si el humano prefiere ahorrarse la
  llamada, CA-6 se da por cubierto con CA-3 (f) más el primer humo de SPEC-008 CA-7, y el
  verificador lo marca ⚠️ hasta ese humo.

- **CA-7 — Dictamen sobre URLs consultadas frente a citadas [Agente; consulta
  sdd-metricas].**
  Dado que con B1 Claude aporta URLs **consultadas** y no **citadas**, y que
  `07-mvp-product-spec.md` §4 define *Source citation weight* como "Σ over answers citing
  the source of the provider weight" (RN-04) y RN-08 ordena los gaps por ese peso, cuando
  se consulta a sdd-metricas **antes del gate del verificador** (puede ir en paralelo con
  CA-3), entonces consta en el ledger de SPEC-013 un dictamen fechado, con conclusión por
  punto y fuentes, sobre:
  (1) que *Source citation weight*, *Coverage of cited sources* y RN-08 se calculan **solo
  con `cited_urls`**, y que una URL solo consultada no suma peso de citación. Consecuencia
  que el dictamen debe valorar de forma explícita: mientras Claude no cite, su peso de
  RN-04 (10 %) no aporta nada al peso de citación;
  (2) la propuesta de tratamiento para SPEC-011: las URLs consultadas de Claude se
  muestran como **indicador aparte** (p. ej. una marca o recuento "consultada por Claude"
  por fuente, junto al peso de citación), **sin** un peso propio ponderado dentro del
  ranking. O bien, si el dictamen lo recomienda, un "peso de consulta" separado, que sería
  una definición nueva de §4 y del dominio y se decide fuera de esta spec (sdd-producto y
  el humano);
  (3) si `searched_urls` vacía en OpenAI y Gemini ("no medido") sesga alguna comparación
  entre proveedores que haga el análisis;
  (4) que `analysis.py` (`summary.md`: SoV, menciones y posición) no usa URLs y no cambia.
  Si el dictamen confirma (1), (3) y (4), la spec no cambia y el arquitecto añade
  "URLs consultadas" a *Probe / ProbeRun* en `docs/fundacion/dominio.md` (definición: URLs
  de resultados de búsqueda que el proveedor expone, no citadas; no suman peso de
  citación) y deja una nota en SPEC-011 con el tratamiento (2). Si el dictamen pide cambiar
  la columna, su significado o una definición de §4 o de las RN, la spec vuelve a
  `borrador` antes del merge. *Evidencia*: dictamen en el ledger y, en su caso, el diff de
  `dominio.md` y la nota en SPEC-011.

## Entidades y reglas afectadas
- FOUNDATION, No-negociables: "Las respuestas en bruto de los proveedores se guardan
  siempre; las llamadas son idempotentes y seguras ante reintentos" (CA-1).
- ADR-001 (espacio privado, respuestas en bruto solo en `PUSHLLM_PRIVADO`; `probe/out/`
  ignorado), ADR-004 §2 (respuestas en bruto del piloto, en privado), ADR-006 §5 (ningún
  agente lee el `.env`; el probe carga las claves).
- D-5 y RN-10 (modelo por defecto con búsqueda web y ubicación): no se tocan. B1 mantiene
  el filtrado dinámico por defecto (CA-5).
- RN-01/RN-11: las menciones se siguen leyendo del texto; el texto sin fragmentar no
  cambia qué nombres aparecen, solo quita saltos de línea espurios.
- Dominio: *Probe / ProbeRun* ("URLs citadas"), *Source*. `07-mvp-product-spec.md` §4
  (*Source citation weight*, *Coverage of cited sources*), RN-04 y RN-08. Esta spec no
  cambia ninguna de esas definiciones. Solo añade el dato "URLs consultadas", y el
  tratamiento que se le dé en el análisis lo dictamina CA-7.
- Código: `probe/providers.py` (`ProviderResult.searched_urls`; `_claude`; serialización
  cruda en los tres adaptadores), `probe/run_probe.py` (`COLUMNS`, escritura con cabecera
  antigua en `--resume`, `raw_responses.jsonl`), `probe/tests/fakes.py`,
  `probe/tests/fixtures/claude_web_search_20260209.json` (nuevo),
  `probe/tests/test_providers.py`, `probe/tests/test_run_probe.py`,
  `probe/tests/test_raw_responses.py`, `probe/README.md`. `probe/analysis.py` **no
  cambia**.
- Documentación oficial citada en "Problema" (consultada el 2026-09-29).

## Fuera de alcance
- Cambiar modelo, versión del tool, `allowed_callers`, effort o `max_uses`. B2 está
  rechazada por el humano (2026-09-29). Cualquier cambio de modo pasa por CA-5.
- Rellenar `cited_urls` con URLs consultadas, o rellenar `searched_urls` con citas.
- `searched_urls` de OpenAI (necesita `include=["web_search_call.action.sources"]`: cambia
  la petición) y cambiar qué significa `cited_urls` en Gemini (`grounding_chunks` frente a
  `grounding_supports`). Quedan como follow-ups en el ledger, con dictamen de sdd-probe y
  de sdd-metricas.
- Añadir `searched_urls` a ficheros `results.csv` existentes (ni con `--resume` ni con un
  script): los humos antiguos se quedan como están.
- Re-ejecutar los humos de SPEC-002 o SPEC-008.
- Cambiar `analysis.py`/`summary.md`, o añadir ahí un análisis de fuentes. El análisis de
  fuentes (qué dominios cita o consulta cada proveedor, peso de citación, top-10) es de
  SPEC-011, con el dictamen de CA-7.
- Cambiar las definiciones de `07-mvp-product-spec.md` §4 o las RN. Si CA-7 lo pide, lo
  deciden sdd-producto y el humano fuera de esta spec.
- Retención o borrado de `raw_responses.jsonl` (lo cubre ADR-001 y su dictamen pendiente).
- Tocar los ledgers de SPEC-002 y SPEC-008 (el orquestador enlaza allí esta spec cuando
  termine el verificador que trabaja en ellos).

## Notas para el gate humano
- **Re-aprobación (enmienda (b), 2026-09-29).** Qué aprobar: (1) B1 tal como la concreta
  CA-3: columna `searched_urls` **al final** de `results.csv`, poblada solo en Claude,
  vacía en OpenAI y Gemini ("no medido"); (2) el comportamiento de `--resume` sobre
  ficheros antiguos: **no** añade la columna, conserva la cabecera, avisa por stderr, y las
  URLs quedan en `raw_responses.jsonl`; (3) CA-7, el dictamen de sdd-metricas; (4) el
  gasto de CA-6 (1 llamada, ≈ 0,07 €, tope 0,25 €) o su sustitución por el primer humo de
  SPEC-008 CA-7. El gasto de CA-2 ya se hizo: 0,0729 €.
- **Mirar con lupa**:
  - **Con B1, Claude no aporta peso de citación.** Según §4 y RN-04, el peso de citación
    solo cuenta respuestas que *citan*. Mientras Claude no cite, su 10 % no suma nada al
    ranking de fuentes de SPEC-011, y sus URLs consultadas salen como indicador aparte.
    Es lo que pediste ("consultadas, no citadas"). CA-7 lo hace confirmar por sdd-metricas
    antes del merge. Un "peso de consulta" sería una métrica nueva y no entra aquí.
  - **OpenAI y Gemini con `searched_urls` vacía.** OpenAI podría dar sus fuentes
    consultadas, pero para eso hay que cambiar la petición (`include=…`), cosa que esta
    spec no hace. Gemini ya usa sus `grounding_chunks` como `cited_urls`, y es posible que
    esa lista mezcle fuentes consultadas y citadas. Las dos cosas quedan como follow-ups.
    La columna, por tanto, **no sirve para comparar proveedores**.
  - **`--resume` sobre un fichero antiguo pierde la columna en el CSV** (no el dato, que
    está en `raw_responses.jsonl`). La alternativa, reescribir la cabecera, rompe la regla
    de CA-1 (d) de no reescribir nunca lo existente. Para el baseline de SPEC-008 CA-7, que
    empieza en un directorio nuevo, no afecta.
  - El **golden de Vigo no se regenera**: su entrada se queda en el formato antiguo y sirve
    de prueba de compatibilidad. Si cambia, es un fallo.
  - La **regla de unión del texto** (CA-3 c) se mantiene aunque en CA-2 el texto llegó en
    un solo bloque: la fragmentación de los humos es real y la regla sale de la doc de
    *Citations*.
  - **Fixture sin datos reales**: por ADR-001 la respuesta en bruto no entra al repo; el
    fixture copia la forma, no el contenido. La prueba sobre el contenido real (CA-3 f) se
    hace offline en el espacio privado y solo deja recuentos en el ledger.
  - `raw_responses.jsonl` guarda `encrypted_content` completo: 37,6 KB en la llamada de
    CA-2 (unos MB por baseline completo). Es lo que hace la auditoría reproducible. Es dato
    privado de clase 1 (ADR-001).
- **Épica: EPIC-FIX (bucket), no EPIC-002.** El defecto vive en el adaptador de Claude del
  probe (código de SPEC-001, EPIC-001) y afecta a los dos lotes. Lo que liga esta spec a
  EPIC-002 es que SPEC-008 CA-7 espera a que esté en `hecho`.
- **Rama**: `ft/SPEC-013-respuesta-cruda-y-citas-de-claude` (CA-1 ya en `e82bbe7`).
