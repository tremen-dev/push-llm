---
id: SPEC-013
tipo: spec
epica: EPIC-FIX
estado: en-revision
aprobada-por: Alberto Fojo
historial:
  - {estado: borrador, fecha: 2026-09-29, por: sdd-arquitecto}
  - {estado: aprobada, fecha: 2026-09-29, por: Alberto Fojo}
  - {estado: en-progreso, fecha: 2026-09-29, por: sdd-implementador}
  - {estado: bloqueada, fecha: 2026-09-29, por: sdd-arquitecto}
  - {estado: borrador, fecha: 2026-09-29, por: sdd-arquitecto}
  - {estado: aprobada, fecha: 2026-09-29, por: Alberto Fojo}
  - {estado: en-progreso, fecha: 2026-09-29, por: sdd-implementador}
  - {estado: en-revision, fecha: 2026-09-29, por: sdd-implementador}
---
# SPEC-013 — Respuesta cruda del proveedor y citas de Claude en el probe

> **Enmienda 2026-09-29 (c) (sdd-arquitecto): `searched_urls` en los tres proveedores.**
> En el gate de la enmienda (b), el humano (Alberto Fojo, 2026-09-29) no la aprobó y pidió
> que `searched_urls` se rellene también en OpenAI y Gemini, "para ser honestos con el
> cliente": datos comparables entre asistentes y un informe que explique igual para todos
> la diferencia entre "consultadas" y "citadas". Cambian:
> - **CA-3**: Claude se queda como en (b). Gemini pasa a tener `searched_urls` = todos los
>   `grounding_chunks` y `cited_urls` = solo los chunks referenciados por
>   `grounding_supports`. Esto **corrige el significado de `cited_urls` en Gemini**, que hoy
>   guarda todos los chunks. OpenAI obtiene `searched_urls` de
>   `web_search_call.action.sources` pidiéndolo con `include`.
> - **CA-4**: cambian las expectativas de los tests de Gemini y de OpenAI.
> - **CA-5**: la petición de OpenAI cambia, así que el dictamen de sdd-probe pasa a ser
>   obligatorio.
> - **CA-6**: una llamada por proveedor, con tope de 0,40 €.
> - **CA-7**: el dictamen de sdd-metricas se amplía a los tres proveedores.
> - También cambian Entidades, Fuera de alcance y Notas. F-SPEC-013-1 y F-SPEC-013-2 se
>   resuelven dentro de esta spec.
>
> Sigue en `borrador` a la espera de aprobación humana.

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
- **[Agente]** sdd-implementador: CA-1, CA-3, CA-4 (TDD, sin llamadas reales), en los
  adaptadores de Claude, OpenAI y Gemini.
- **[Agente]** sdd-probe: dictamen de CA-5 (advisory; obligatorio por el `include` de OpenAI).
- **[Agente]** sdd-metricas: dictamen de CA-7 (advisory).
- **[Agente]** sdd-verificador: gate.
- **Ningún agente lee, abre ni imprime `.env`** (ADR-006 §5), tampoco para diagnosticar.
- Afecta aguas abajo a SPEC-002 CA-3 (salvedad F-SPEC-002-7), a SPEC-008 CA-7 (baseline con
  probe del piloto, que **espera a esta spec** por decisión del humano del 2026-09-29) y a
  SPEC-011 (fuentes citadas; con B1, también las consultadas de Claude, CA-7).

## Criterios de aceptación
Orden de ejecución: CA-1 → CA-2 → CA-3 → CA-4/CA-5 → CA-6. Los dictámenes de CA-5
(sdd-probe) y CA-7 (sdd-metricas) pueden pedirse en paralelo con CA-3. CA-5 tiene que estar
antes de CA-6 y CA-7 antes del gate del verificador.

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

- **CA-3 — URLs consultadas y citadas en los tres adaptadores, con TDD [Agente].**
  Dado el diagnóstico de CA-2 (caso B), la decisión B1 del humano y su ampliación a los
  tres proveedores (enmienda (c)), cuando sdd-implementador escribe primero los tests que
  fallan con el código actual y después hace el arreglo, entonces:

  **Significado común (los tres proveedores).** `ProviderResult` tiene un campo nuevo
  `searched_urls` (lista):
  - `searched_urls` son las **URLs consultadas**: las páginas que el proveedor declara
    haber recuperado con la búsqueda para esa respuesta.
  - `cited_urls` son las **URLs citadas**: las que el proveedor enlaza a un fragmento del
    texto de la respuesta.
  - Las dos listas van sin duplicados y en orden de aparición. Con `status=error` quedan
    vacías.
  - `cited_urls` nunca se rellena con URLs solo consultadas. Cuando el proveedor da las
    dos cosas, toda URL citada aparece también en `searched_urls`, y hay un test de
    inclusión por proveedor. La excepción es una cita de OpenAI a una URL que no está en
    `sources`: se conserva en `cited_urls` y no se añade a `searched_urls`; un test fija
    este caso.

  **Claude** (sin cambios respecto a la enmienda (b)). Sobre
  `probe/tests/fixtures/claude_web_search_20260209.json`, que tiene **la misma estructura**
  que la respuesta grabada en CA-2 pero **sanitizada**:
  - misma estructura: los 9 bloques de primer nivel en el orden de § "Evidencia de CA-2",
    con los mismos `type` y `caller`; 10 `web_search_result` con las mismas claves; 3
    `code_execution_tool_result` con los mismos tipos de contenido; 1 bloque `text` sin
    `citations`; `stop_reason=end_turn`;
  - sanitizado: texto sintético de una clínica ficticia; URLs en dominios reservados
    (`example.org`, `example.com`…), con al menos una repetida; `encrypted_*` e `id`
    sustituidos por marcadores; ninguna cadena copiada de la respuesta real (ADR-001).

  Casos de Claude:
  (a) `cited_urls` sale del `url` de las citas de los bloques `text`. Para el fixture queda
  **vacía**. El test existente `test_claude_ok_collects_usage_urls_and_served_model` sigue
  en verde sin cambiar su expectativa.
  (b) `searched_urls` contiene el `url` de cada `web_search_result` de todo bloque
  `web_search_tool_result` de primer nivel de `content`:
  - con `caller` o sin él;
  - en todos los turnos, incluidas las continuaciones de `pause_turn`.
  Para el fixture es exactamente la lista esperada, escrita a mano en el test. Un
  `web_search_tool_result` cuyo `content` no es una lista (error de la herramienta) no
  aporta URLs ni rompe la llamada.
  (c) **Texto completo, sin fragmentar.**
  - Los bloques `text` consecutivos se concatenan **sin separador**, como indica la doc de
    *Citations*.
  - Solo se inserta `"\n\n"` entre tramos de texto separados por un bloque que no es
    `text`, y lo mismo al continuar tras `pause_turn`. Nunca al principio ni al final.
  - Para el fixture, `r.text` es igual, carácter a carácter, al texto esperado.
  - Un segundo test, con bloques `text` partidos a mitad de frase y una búsqueda en medio,
    fija la regla.
  - `test_claude_pause_turn_accumulates_usage_and_text` se actualiza a la nueva regla.
  (d) Re-procesar **offline** la respuesta cruda real de CA-2 (en privado, con un cliente
  falso que devuelve la respuesta grabada) da:
  - `cited_urls` vacío;
  - `searched_urls` con tantas URLs como `url` distintos haya entre los 10 resultados;
  - un texto sin cortes a mitad de frase.
  El ledger anota solo los recuentos.

  **Gemini: la petición no cambia.** Lo que dice la documentación oficial (*Grounding with
  Google Search*, ai.google.dev/gemini-api/docs/generate-content/google-search,
  actualizada el 2026-09-02, consultada el 2026-09-29):
  - `groundingChunks`: "Array of objects containing the web sources (`uri` and `title`)";
  - `groundingSupports`: "Array of chunks to connect model response `text` to the sources
    in `groundingChunks`. Each chunk links a text `segment` (defined by `startIndex` and
    `endIndex`) to one or more `groundingChunkIndices`";
  - las URIs web son del tipo `https://vertexaisearch.cloud.google.com/…`;
  - las citas en línea del ejemplo oficial se construyen desde `groundingSupports`.

  Casos de Gemini:
  (e) `searched_urls` = el `web.uri` de **todos** los `grounding_chunks` con `web`, en su
  orden.
  (f) `cited_urls` = el `web.uri` de los chunks cuyo índice aparece en
  `groundingChunkIndices` de al menos un `grounding_supports`, en el orden de
  `grounding_chunks`.
  - Si no hay `grounding_supports`, `cited_urls` queda vacía y `searched_urls` no.
  - Un índice fuera de rango se ignora (test).
  - **Esto corrige lo que significa hoy `cited_urls` en Gemini**, que guarda todos los
    chunks: medía "consultadas" y lo llamaba "citadas".
  - Los fakes de Gemini (`probe/tests/fakes.py`) aprenden a llevar `grounding_supports`.
  - Hay tests con chunks citados y no citados, sin supports, y con un índice repetido en
    varios supports.
  (g) Las URIs se **guardan tal cual**, como redirecciones `vertexaisearch`; no se
  resuelven. Motivos:
  1. Resolverlas exige una petición HTTP extra por URL, fuera de la llamada al proveedor.
     El probe dejaría de hacer una sola llamada por fila, sumaría latencia y fallos de red,
     y visitaría las webs de terceros, incluida la de competidores.
  2. La doc no documenta que esas redirecciones duren. Resolverlas ahora o más tarde da el
     mismo resultado mientras funcionen, y la respuesta cruda (CA-1) conserva `uri` y
     `title` para resolverlas después.
  3. El dominio real para el análisis de fuentes lo necesita SPEC-011. Resolverlo sigue
     siendo F-SPEC-001-2 (destino SPEC-003 o SPEC-011), fuera de esta spec.
  El README lo dice: en Gemini, las dos columnas llevan redirecciones y **no se pueden
  comparar por dominio con Claude ni OpenAI hasta que se resuelvan**. Sí se pueden comparar
  los recuentos (cuántas consultadas y cuántas citadas).

  **OpenAI: la petición cambia; exige el dictamen de CA-5.** Lo que dice la documentación
  oficial (*Web search*, developers.openai.com/api/docs/guides/tools-web-search, consultada
  el 2026-09-29):
  - "To view all URLs retrieved during a web search, use the `sources` field", pidiéndolo
    con `include=["web_search_call.action.sources"]`;
  - "Unlike inline citations, which show only the most relevant references, sources
    returns the complete list of URLs the model consulted when forming its response";
  - "The number of sources is often greater than the number of citations";
  - los `sources` pueden incluir feeds propios de OpenAI (`oai-sports`, `oai-weather`,
    `oai-finance`).

  Casos de OpenAI:
  (h) `responses.create` recibe además `include=["web_search_call.action.sources"]`, y
  `request` en `raw_responses.jsonl` lo refleja. **Es el único parámetro nuevo**; lo prueba
  un test sobre los `kwargs` del cliente falso (CA-5).
  (i) `searched_urls` = el `url` de cada entrada de `action.sources` de cada item
  `web_search_call`, en orden, sin duplicados.
  - Las entradas sin `url` (los feeds `oai-*`) no entran en la columna; quedan en la
    respuesta cruda.
  - Si `action` no trae `sources`, no aporta nada y no falla.
  (j) `cited_urls` sigue saliendo de las anotaciones `url_citation`. El test existente
  `test_openai_ok` sigue en verde en lo que ya comprobaba y añade la aserción del `include`.

  **Columna y compatibilidad (los tres):**
  (k) `run_probe.COLUMNS` termina en `…, "cited_urls", "answer", "searched_urls"`: la
  columna va **al final**, con las URLs unidas por `;`. Una fila de cada proveedor, con sus
  fakes, tiene `searched_urls` poblado.
  (l) **`results.csv` antiguos** (sin la columna):
  - `--analyze` funciona y da el mismo `summary.md`. `analysis.py` no lee URLs y **no
    cambia** (lo prueba el golden de Vigo, CA-4). El mismo CSV con la columna añadida da un
    `summary.md` idéntico byte a byte (test).
  - **`--resume` se niega a continuar un `results.csv` antiguo** (decisión del humano,
    2026-09-29). Un fichero es antiguo si su cabecera no contiene `searched_urls`. En ese
    caso `run_probe.py`:
    - sale con error (código distinto de 0), **antes de llamar a ningún proveedor y antes
      de abrir para escribir** `results.csv` o `raw_responses.jsonl`;
    - muestra un mensaje claro: el fichero es anterior a SPEC-013, no tiene
      `searched_urls` y su `cited_urls` de Gemini tiene otro significado; se puede usar
      `--out` con un directorio nuevo, o `--analyze` para recontar.
    Motivo: en esos ficheros, **`cited_urls` de Gemini significa "todos los chunks"** (lo
    que ahora es `searched_urls`). Reanudar mezclaría en un mismo fichero filas de Gemini
    con dos significados.
    Test (cliente falso que cuenta las llamadas): con un `results.csv` antiguo y un
    `raw_responses.jsonl` existente, `main(["--resume", …])` termina con error y:
    - el mensaje nombra `searched_urls` y `--out`;
    - `results.csv` queda idéntico byte a byte, y `raw_responses.jsonl` también (o no se
      crea si no existía);
    - el cliente falso registra **0 llamadas**.
  - `--resume` sobre un `results.csv` que ya tiene `searched_urls` sigue funcionando como
    en CA-1 (d): añade filas y líneas, nunca reescribe.
  (m) `probe/README.md` documenta:
  - las dos columnas y su significado común;
  - qué da cada proveedor;
  - las redirecciones de Gemini;
  - el cambio de significado de `cited_urls` en Gemini, con la fecha de SPEC-013;
  - el comportamiento con ficheros antiguos.
  Y deja de decir que las columnas no cambian.

- **CA-4 — Sin regresiones y compatibilidad [Agente].**
  Dado el cambio, cuando se ejecutan desde la raíz del repo `python -m pytest -q
  probe/tests`, `python -m pytest -q docs/piloto-artica/tools/tests` y `ruff check probe`,
  entonces todo está en verde.

  Siguen en verde **sin cambiar sus expectativas**:
  - `test_claude_ok_collects_usage_urls_and_served_model`;
  - los tests de estado, errores, rechazos y tokens de OpenAI y Gemini de
    `test_providers.py`;
  - el golden de Vigo (`test_pilot_batch.py::test_ca4_vigo_summary_identical_to_before_the_change`);
  - los tests del lote Viveiro (`test_pilot_batch.py`).

  **El golden de Vigo no se regenera.**
  - Su entrada `probe/tests/fixtures/vigo_results.csv` se queda sin `searched_urls` y con
    las `cited_urls` de Gemini con el significado antiguo, a propósito. Así prueba que
    `--analyze` lee un `results.csv` antiguo.
  - `analysis.py` no lee `cited_urls` ni `searched_urls` (comprobado el 2026-09-29), así
    que la corrección de Gemini no puede mover `summary.md`.
  - `vigo_summary_before.md` no se toca.
  - Si el golden cambiara, sería un defecto, no un motivo para regenerarlo.
  - La compatibilidad de `--resume` la prueba el test de CA-3 (l): sobre un CSV antiguo,
    sale con error, los ficheros no cambian y hay 0 llamadas.

  **Tests existentes cuya expectativa cambia**, y cada uno se cita en el ledger:
  - el de la regla de unión (CA-3 c);
  - `test_gemini_ok_sums_thoughts_and_tool_tokens`: con el fake sin supports, su
    `cited_urls` pasa de la lista de chunks a vacía, y la lista pasa a `searched_urls`;
  - `test_openai_ok`: aserción nueva del `include`;
  - si hace falta, las aserciones de columnas de `test_raw_responses.py` y
    `test_run_probe.py`, con `searched_urls` al final.

- **CA-5 — Parámetros de la llamada; dictamen de sdd-probe sobre el `include` de OpenAI
  [Agente; consulta sdd-probe].**
  Dado el arreglo, cuando se comparan los parámetros que envía cada adaptador antes y
  después (tool `type`, `allowed_callers`, `max_uses`, `user_location`, modelo, effort,
  `max_tokens`, `system`/`instructions`/`config`, `include`), entonces un test sobre los
  `kwargs` de los clientes falsos demuestra que:
  - Claude y Gemini envían **exactamente lo mismo** que antes;
  - OpenAI envía lo mismo **más** `include=["web_search_call.action.sources"]` y nada
    más.

  Además, **antes de la llamada real de CA-6 y antes del merge**, consta en el ledger de
  SPEC-013 un dictamen fechado de sdd-probe, con fuentes oficiales y fecha de consulta, que
  confirme:
  (1) que `include` solo cambia lo que la API devuelve, no lo que el modelo hace (ni la
  búsqueda ni la respuesta), y que el sondeo sigue siendo fiel a D-5 y RN-10: lo que ve un
  usuario de ChatGPT con búsqueda;
  (2) que no cambia el coste por llamada (tokens facturados y precio por búsqueda). Si
  cambia, lo cuantifica y se contrasta con la fila de OpenAI de CA-6 frente al humo de
  SPEC-002 (unos 0,012 € por llamada);
  (3) el nombre exacto del parámetro y la forma de `action.sources` vigentes, incluidos los
  feeds `oai-*` sin URL;
  (4) si las URLs de las acciones `open_page`/`find_in_page` de `web_search_call` deberían
  contar como consultadas. Si el dictamen dice que sí, se registra como follow-up; esta
  spec no las incluye.

  Si el dictamen desaconseja el `include`, la spec vuelve a `borrador` y el humano decide.
  Cualquier otro cambio de parámetros, en cualquier proveedor, sin dictamen, es RED.

- **CA-6 — Confirmación en real, una llamada por proveedor [Humano] autoriza →
  [Orquestador] ejecuta.**
  Dado CA-3, CA-4 y el dictamen de CA-5 en verde, cuando el orquestador ejecuta, desde
  `probe\` y con el `.env` cargado por el propio probe:
  `.\.venv\Scripts\python run_probe.py --providers claude,openai,gemini --only D01 --runs 1 --out "$env:PUSHLLM_PRIVADO\diagnostico\spec-013-post"`
  es decir, **3 llamadas**, una por proveedor. Coste estimado con los humos de SPEC-002:
  Claude ≈ 0,075 €, OpenAI ≈ 0,012 €, Gemini ≈ 0,018 €, **≈ 0,11 € en total**. Tope:
  **0,40 €** en total, contando como mucho una repetición por proveedor si da
  `status=error` (6 llamadas como máximo).

  Entonces:
  - la cabecera de `results.csv` termina en `searched_urls`;
  - las tres filas tienen `status=ok`;
  - cada fila con `web_searches ≥ 1` tiene **`searched_urls` con al menos 1 URL**. En
    Gemini, `web_searches` es el número de `web_search_queries`;
  - en cada fila, toda URL de `cited_urls` está en `searched_urls`, salvo la excepción de
    OpenAI de CA-3;
  - `answer` de Claude no tiene cortes a mitad de frase;
  - hay 3 líneas en `raw_responses.jsonl`, y la de OpenAI lleva `include` en `request`.

  El ledger anota, por proveedor: fecha, coste, número de búsquedas y los recuentos de
  `searched_urls` y `cited_urls`, sin URLs ni texto. Si una fila con búsqueda sale con
  `searched_urls` vacía, CA-6 es RED para ese proveedor.

  Si el humano prefiere no gastar, CA-6 se da por cubierto con CA-3 (d) más el primer humo
  de SPEC-008 CA-7, y el verificador lo marca ⚠️ hasta ese humo.

- **CA-7 — Dictamen sobre URLs consultadas frente a citadas, en los tres proveedores
  [Agente; consulta sdd-metricas].**
  Dado que `searched_urls` y `cited_urls` pasan a significar lo mismo en los tres
  proveedores, y que `07-mvp-product-spec.md` §4 define *Source citation weight* como "Σ
  over answers citing the source of the provider weight" (RN-04) y RN-08 ordena los gaps
  por ese peso, cuando se consulta a sdd-metricas **antes del gate del verificador** (puede
  ir en paralelo con CA-3), entonces consta en el ledger de SPEC-013 un dictamen fechado,
  con conclusión por punto y fuentes, sobre:
  (1) que *Source citation weight*, *Coverage of cited sources* y RN-08 se calculan **solo
  con `cited_urls`**, y que una URL solo consultada no suma peso de citación. Consecuencias
  que el dictamen debe valorar de forma explícita:
  - mientras Claude no cite, su 10 % de RN-04 no aporta nada;
  - la corrección de Gemini reduce sus citadas respecto a los humos anteriores;
  (2) si `searched_urls` es **comparable entre proveedores** tal como la definen los CA,
  con estos límites:
  - Claude, antes del filtrado dinámico;
  - OpenAI, "the complete list of URLs the model consulted";
  - Gemini, las fuentes de grounding, como redirecciones sin resolver;
  (3) la **propuesta** para SPEC-011 y sdd-producto, sin crear aquí ninguna métrica: un
  indicador "consultada por" por fuente, con los tres proveedores (recuento o marca por
  proveedor, sin peso en el ranking de citación), junto al peso de citación, y cómo
  explicar al cliente "consultadas" frente a "citadas" igual para todos. Si recomienda un
  peso de consulta, es una definición nueva de §4 y del dominio, y la deciden sdd-producto
  y el humano fuera de esta spec;
  (4) cómo tratar los `results.csv` anteriores a SPEC-013, en los que `cited_urls` de
  Gemini son todos los chunks, si SPEC-011 los usa;
  (5) que `analysis.py` (`summary.md`: SoV, menciones y posición) no usa URLs y no cambia.

  Si el dictamen confirma (1) y (5), la spec no cambia, y el arquitecto:
  - añade "URLs consultadas" a *Probe / ProbeRun* en `docs/fundacion/dominio.md`
    (definición: URLs que el proveedor declara haber recuperado para la respuesta; no suman
    peso de citación);
  - deja en SPEC-011 una nota con (2)–(4).

  Si el dictamen pide cambiar una columna, su significado o una definición de §4 o de las
  RN, la spec vuelve a `borrador` antes del merge.

  *Evidencia*: el dictamen en el ledger y, en su caso, el diff de `dominio.md` y la nota
  en SPEC-011.

## Entidades y reglas afectadas
- FOUNDATION, No-negociables: "Las respuestas en bruto de los proveedores se guardan
  siempre; las llamadas son idempotentes y seguras ante reintentos" (CA-1).
- ADR-001 (espacio privado, respuestas en bruto solo en `PUSHLLM_PRIVADO`; `probe/out/`
  ignorado), ADR-004 §2 (respuestas en bruto del piloto, en privado), ADR-006 §5 (ningún
  agente lee el `.env`; el probe carga las claves).
- D-5 y RN-10 (modelo por defecto con búsqueda web y ubicación): Claude y Gemini no
  cambian. OpenAI añade `include`, y su fidelidad a D-5 la confirma el dictamen de CA-5.
- RN-01/RN-11: las menciones se siguen leyendo del texto; el texto sin fragmentar no
  cambia qué nombres aparecen, solo quita saltos de línea espurios.
- Dominio: *Probe / ProbeRun* ("URLs citadas"), *Source*. `07-mvp-product-spec.md` §4
  (*Source citation weight*, *Coverage of cited sources*), RN-04 y RN-08. Esta spec no
  cambia ninguna de esas definiciones:
  - añade el dato "URLs consultadas";
  - corrige `cited_urls` de Gemini para que cumpla "URLs citadas";
  - el uso en el análisis lo dictamina CA-7.
- Código:
  - `probe/providers.py`: `ProviderResult.searched_urls`, `_claude`, `_openai`
    (`include`), `_gemini` (chunks y supports), serialización cruda;
  - `probe/run_probe.py`: `COLUMNS` y rechazo de `--resume` sobre un `results.csv` sin
    `searched_urls`;
  - tests y fixtures: `probe/tests/fakes.py`,
    `probe/tests/fixtures/claude_web_search_20260209.json` (nuevo),
    `probe/tests/test_providers.py`, `probe/tests/test_run_probe.py`,
    `probe/tests/test_raw_responses.py`;
  - `probe/README.md`.
  `probe/analysis.py` **no cambia**.
- Documentación oficial citada en "Problema" y en CA-3 (Anthropic, Google y OpenAI;
  consultada el 2026-09-29).

## Fuera de alcance
- Cambiar modelo, versión del tool, `allowed_callers`, effort o `max_uses` en cualquier
  proveedor. B2 está rechazada por el humano (2026-09-29). El único cambio de petición es
  el `include` de OpenAI (CA-5).
- Rellenar `cited_urls` con URLs solo consultadas.
- **Resolver las redirecciones `vertexaisearch` de Gemini** a la URL o al dominio real
  (F-SPEC-001-2, fuera de esta spec; motivos en CA-3 g).
- Contar como consultadas las URLs de las acciones `open_page`/`find_in_page` de OpenAI
  (CA-5 punto 4: follow-up si el dictamen lo pide).
- Añadir `searched_urls` a ficheros `results.csv` existentes, o reescribir su
  `cited_urls` de Gemini, ni con `--resume` ni con un script. Los humos antiguos se quedan
  como están.
- Re-ejecutar los humos de SPEC-002 o SPEC-008.
- Cambiar `analysis.py`/`summary.md` o añadir ahí un análisis de fuentes. El análisis de
  fuentes y el posible indicador "consultada por" son de SPEC-011 y sdd-producto, con el
  dictamen de CA-7.
- Crear métricas nuevas o cambiar las definiciones de `07-mvp-product-spec.md` §4 o las
  RN.
- Retención o borrado de `raw_responses.jsonl` (lo cubre ADR-001 y su dictamen pendiente).
- Tocar los ledgers de SPEC-002 y SPEC-008 (el orquestador enlaza allí esta spec cuando
  termine el verificador que trabaja en ellos).

## Notas para el gate humano
- **Qué aprobar (enmienda (c), 2026-09-29):**
  1. `searched_urls` y `cited_urls` con el mismo significado en los tres proveedores
     (CA-3), con la columna nueva **al final** de `results.csv`.
  2. La **corrección de `cited_urls` en Gemini**: hasta ahora guardaba todos los
     `grounding_chunks` (consultadas); pasa a guardar solo los referenciados por
     `grounding_supports` (citadas).
  3. El `include` en la petición de OpenAI, condicionado al dictamen de sdd-probe (CA-5).
  4. El dictamen de sdd-metricas ampliado (CA-7).
  5. El gasto de CA-6: **3 llamadas, ≈ 0,11 €, tope 0,40 €**. Sube respecto a la
     llamada única ya autorizada (tope 0,25 €), así que hay que autorizar el tope nuevo.
  El gasto de CA-2 ya se hizo: 0,0729 €.
- **Mirar con lupa**:
  - **Humos antiguos de Gemini.** En los `results.csv` anteriores a SPEC-013, `cited_urls`
    de Gemini son "consultadas" con otro nombre. Cualquier lectura de fuentes de esos
    ficheros (SPEC-011) tiene que tenerlo en cuenta (CA-7 punto 4). `summary.md` no se ve
    afectado, porque no lee URLs, y el golden de Vigo no cambia.
  - **`--resume` sobre un fichero antiguo se niega** (decisión del humano, 2026-09-29): sale
    con error, sin tocar ficheros y sin llamar a ningún proveedor, para que nunca se
    mezclen dos significados de `cited_urls` de Gemini en el mismo fichero. `--analyze`
    sobre ficheros antiguos sigue funcionando. El baseline de SPEC-008 empieza en un
    directorio nuevo y no le afecta.
  - **Comparabilidad real.** Las tres columnas significan lo mismo, pero no miden
    exactamente lo mismo:
    - Claude declara resultados antes del filtrado dinámico;
    - OpenAI declara "todas las URLs consultadas";
    - Gemini declara sus fuentes de grounding, y solo como redirecciones: hasta resolverlas
      (F-SPEC-001-2) solo se pueden comparar recuentos, no dominios.
    CA-7 punto 2 lo pone por escrito para el informe al cliente.
  - **Con B1, Claude no aporta peso de citación** mientras no cite (§4 y RN-04). Sus
    consultadas salen como indicador aparte (propuesta de CA-7, sin métrica nueva aquí).
  - El **golden de Vigo no se regenera**: su entrada sigue en formato antiguo y prueba la
    compatibilidad.
  - **Fixture sin datos reales** (ADR-001): copia la forma, no el contenido. La prueba
    sobre la respuesta real (CA-3 d) es offline, en privado, y deja solo recuentos.
  - `raw_responses.jsonl` guarda `encrypted_content` completo: 37,6 KB en CA-2. Es dato
    privado de clase 1 (ADR-001).
- **Épica: EPIC-FIX (bucket), no EPIC-002.** El defecto vive en los adaptadores del probe
  (código de SPEC-001, EPIC-001) y afecta a los dos lotes. SPEC-008 CA-7 espera a que esta
  spec esté en `hecho`.
- **Rama**: `ft/SPEC-013-respuesta-cruda-y-citas-de-claude` (CA-1 ya en `e82bbe7`).
