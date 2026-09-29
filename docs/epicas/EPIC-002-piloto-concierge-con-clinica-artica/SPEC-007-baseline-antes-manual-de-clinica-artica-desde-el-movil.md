---
id: SPEC-007
tipo: spec
epica: EPIC-002
estado: en-progreso
aprobada-por: Alberto Fojo
historial:
  - {estado: borrador, fecha: 2026-09-28, por: sdd-arquitecto}
  - {estado: aprobada, fecha: 2026-09-28, por: Alberto Fojo}
  - {estado: en-progreso, fecha: 2026-09-28, por: sdd-implementador}
  - {estado: bloqueada, fecha: 2026-09-29, por: sdd-arquitecto}
  - {estado: borrador, fecha: 2026-09-29, por: sdd-arquitecto}
  - {estado: aprobada, fecha: 2026-09-29, por: Alberto Fojo}
  - {estado: en-progreso, fecha: 2026-09-29, por: sdd-implementador}
---
# SPEC-007 — Baseline antes manual de Clínica Ártica desde el móvil

> **Nota 2026-09-29 (sdd-arquitecto) — cambio de nicho (ADR-008). No cambia ningún CA ni
> requiere re-aprobación.** Las citas a ADR-003 y ADR-005 de esta spec siguen valiendo en lo
> que usa (lote aparte, niveles `AV`/`AR`/`AG` sin mezclar, Go solo con `AV`, nivel Galicia
> sin prometer, marcas del piloto fuera del lote de Vigo). Lo que ADR-008 deroga es el
> encuadre como "excepción a D-2" y sus prohibiciones de prospección y de "Asturias no es
> mercado"; el lote de Vigo queda aparcado, intacto, como configuración por defecto.

> Spec **documental y de medición manual**. No hay código. El agente redacta el set de
> preguntas, el protocolo, la plantilla y el recuento; el humano pregunta en las apps
> del móvil y captura. Ejecutable **ya, sin claves de API**. Material del repo en
> `docs/piloto-artica/`; datos, capturas y recuentos en
> `$PUSHLLM_PRIVADO/piloto-artica/baseline/` (ADR-001, ADR-004).

> **Enmienda 2026-09-29 (sdd-arquitecto) — set en tres niveles geográficos.** Por decisión
> del humano (Alberto Fojo, 2026-09-29; EPIC-002 criterio 4; ADR-005), el set se amplía con
> dos niveles medidos como indicadores **separados** que no son criterio Go: área de
> influencia (`AR`) y Galicia (`AG`). El núcleo (`AV01`–`AV15`, sin cambios) sigue siendo
> el único que cuenta para el Go. Cambian CA-1, CA-2, CA-5, CA-6, CA-7, CA-8, CA-10, las
> entidades, Fuera de alcance y las notas. La spec vuelve a `borrador` (estaba
> `en-progreso`, con la pasada 1 sin empezar y el set sin congelar) y necesita **nueva
> aprobación humana**. Lo que el implementador debe rehacer está en el ledger
> (F-SPEC-007-6).

## Problema
Criterio de éxito 1 de EPIC-002: sin un "antes" fechado no hay forma de saber si una
acción movió una respuesta, y el criterio Go del piloto (+15 pts de SoV ponderado, RN-03)
no tiene punto de partida. El probe (EPIC-001) sigue bloqueado por las claves (SPEC-002) y
no cubre Google AI Overviews; además hoy está fijado a Vigo (ADR-003). Lo único que se
puede medir hoy es lo que ve un paciente en su móvil. Esa medición manual tiene que ser
**repetible con el mismo protocolo** a las 4–12 semanas, o el "después" no será comparable.

## Usuarios / roles afectados
- Humano (fundador): hace las preguntas en ChatGPT, Gemini y Google desde el móvil y
  captura. [Humano]
- Agente (sdd-implementador): redacta set, protocolo, plantilla, foto técnica y recuento.
  [Agente]
- Consultadas: `sdd-metricas` (dictamen obligatorio, CA-2); `sdd-visibilidad-local`
  opcional para el set y la foto técnica.
- sdd-verificador: comprueba cada CA contra ficheros del repo y del espacio privado.
  [Verificador]
- Consumidores: SPEC-008 (mismos ids de prompt), SPEC-009 (hoja de hallazgo), SPEC-011
  (fuentes citadas y foto técnica), SPEC-012 (repetición del protocolo al cierre).

## Criterios de aceptación
- **CA-1 (set de preguntas de paciente) [Agente]**: Dado que la clínica trabaja estética
  facial, corporal, capilar (incl. trasplante DHI) y cirugía menor facial en Viveiro,
  cuando se publique `docs/piloto-artica/prompts-baseline.md`, entonces contiene entre
  **12 y 16 preguntas de medición** con id `AV01…AVnn`, cada una con línea de tratamiento,
  intent (vocabulario de `dominio.md`: discovery, price, comparison, urgent, trust,
  specific), ámbito geográfico e idioma, y cumple: ≥ 1 pregunta por cada una de las cuatro
  líneas de tratamiento; ≥ 1 de cada intent discovery, price, comparison, trust y specific;
  ≥ 4 que nombran Viveiro, ≥ 2 que nombran A Mariña, Burela, Foz o Ribadeo, ≥ 2 que nombran
  Lugo (ciudad o provincia); ≥ 2 en gallego; ninguna nombra a Clínica Ártica ni a un
  competidor; ninguna depende de la ubicación sin nombrar un lugar ("cerca de mí" sin
  topónimo). Aparte, bajo el título "Preguntas de marca (no cuentan para el SoV)", 1–2
  preguntas `AM01…` sobre la propia clínica ("¿Qué sabes de Clínica Ártica de Viveiro?")
  para comprobar qué dice de ella cada asistente. *Evidencia*: recuento por script de cada
  condición; búsqueda de "Ártica", "Artica" y de las marcas candidatas de SPEC-008 en las
  preguntas `AV`, sin coincidencias.
  **Niveles (enmienda 2026-09-29, ADR-005)**. El documento tiene tres secciones de medición
  separadas, cada una con su línea de cobertura:
  - **Núcleo — `AV`** (cuenta para el criterio Go): las condiciones de arriba. Las
    preguntas `AV01`–`AV15` publicadas el 2026-09-29 **se mantienen con el mismo id y el
    mismo texto** (no se renumeran ni se reescriben).
  - **Área de influencia — `AR01…ARnn`** (indicador aparte, no cuenta para el Go): entre
    **4 y 5** preguntas; ≥ 1 nombra un municipio de Ferrolterra, ≥ 1 un municipio del norte
    de Lugo **fuera de A Mariña** y ≥ 1 un municipio del occidente de Asturias; ninguna
    nombra Viveiro ni un municipio de A Mariña (Ribadeo es A Mariña: es núcleo, no
    influencia); ≥ 3 están formuladas desde el lugar del paciente con apertura a
    desplazarse ("vivo en…", "cerca de…", "por la zona de…"), no como "solo en X"; ≥ 2
    líneas de tratamiento y ≥ 2 intents distintos; ≥ 1 en gallego y la(s) de Asturias en
    castellano.
  - **Galicia — `AG01…AGnn`** (indicador aparte, no cuenta para el Go): entre **3 y 4**
    preguntas; solo líneas `capilar` (trasplante DHI) y `cirugia_facial` (blefaroplastia),
    ≥ 1 de cada; ámbito "Galicia" sin nombrar ciudad ni comarca; ≥ 1 de intent `price` o
    `comparison`; ≥ 1 en gallego. Cada tratamiento del nivel lo ofrece la clínica según su
    web: el ledger cita URL y fecha de consulta por tratamiento.
  - Comunes: ids únicos en todo el documento; ninguna `AR`/`AG` nombra a Clínica Ártica ni
    a un competidor ni depende de "cerca de mí" sin topónimo; ninguna repite el texto de
    otra pregunta del set; número total de preguntas de medición (`AV`+`AR`+`AG`) ≤ 24.
    Las `AM` no cambian.
  *Evidencia adicional*: el comprobador cuenta cada condición **por nivel**; test de que
  `AV01`–`AV15` son idénticas (id y texto) a la versión publicada el 2026-09-29; búsqueda
  de "Ártica", "Artica" y de las marcas candidatas de SPEC-008 también en `AR` y `AG`, sin
  coincidencias; URL y fecha de los tratamientos `AG` en el ledger.
- **CA-2 (dictamen de métricas antes de la primera pasada) [Agente; consulta
  sdd-metricas]**: Dado RN-01 a RN-06 y que una medición manual no es el probe, cuando el
  protocolo (CA-3) esté redactado y antes de la pasada 1, entonces consta en el ledger un
  dictamen de `sdd-metricas` (fecha, conclusión por punto, condiciones) que fija al menos:
  (a) alias que cuentan como mención de Clínica Ártica y de cada competidor en conteo manual
  (en particular si "Ártica" sola cuenta, RN-01); (b) número de pasadas y separación entre
  ellas; (c) cálculo del SoV bruto por app (RN-02) y ponderado con solo ChatGPT y Gemini
  (RN-03/RN-04 normalizado a lo sondeado); (d) tratamiento de Google AI Overviews como canal
  aparte (RN-04), incluido qué pasa cuando no aparece resumen de IA; (e) que la comparación
  antes/después del criterio Go solo es válida **con el mismo instrumento** (manual contra
  manual; probe contra probe) y (f) el margen de ruido esperable con este tamaño de
  muestra frente al umbral de +15 pts. Cada condición del dictamen se mapea a un cambio en
  protocolo, plantilla o recuento. *Evidencia*: dictamen + tabla condición → cambio en el
  ledger, con fecha anterior a la pasada 1.
  **Ampliación por niveles (enmienda 2026-09-29)**: el dictamen de `sdd-metricas` del
  2026-09-29 cubre solo el núcleo (sus puntos (c) y (f) se refieren a "las preguntas
  `AV`"). Antes de la pasada 1 consta en el ledger una **ampliación fechada** del dictamen
  que fija además: (g) qué indicador se calcula para `AR` y para `AG` (recuento "x de n
  respuestas" y/o porcentaje, por app y por pasada; si hay ponderado o no) y una definición
  **operativa y verificable** de "aparecer con cierta regularidad" (`AR`) y "aparecer
  alguna vez" (`AG`), que se usará igual en el "después" de SPEC-012; (h) que el SoV
  ponderado del criterio Go, la estabilidad de P-3 y el aviso de techo de CA-8 usan **solo**
  `AV`, y que ninguna cifra `AR`/`AG` se suma, promedia ni pondera con el núcleo (ADR-005
  §4); (i) cómo se tratan en la lectura las clínicas de fuera de la comarca (cadenas con
  varias sedes: una marca o una por sede en `alias-canonicos.csv`) y si la posición (RN-06)
  se informa en `AR`/`AG`; (j) si el margen de ruido con 3–5 preguntas por nivel permite
  dar porcentajes o solo recuentos. Los puntos (a), (b), (d) y (e) del dictamen existente
  se declaran aplicables a todos los niveles o se matizan. Cada condición nueva se mapea a
  un cambio en protocolo, plantilla, procedimiento de recuento o herramienta, igual que las
  anteriores. El dictamen lo emite `sdd-metricas`; este CA no lo prejuzga. *Evidencia*:
  sección de ampliación con fecha anterior a la pasada 1 y filas nuevas (g)–(j) en la
  tabla condición → cambio.
- **CA-3 (protocolo de captura para leer) [Agente]**: Dado un humano que mide desde el
  móvil, cuando se publique `docs/piloto-artica/protocolo-captura.md` (≤ 2 páginas,
  imprimible, instrucciones literales paso a paso), entonces fija, para cada app (ChatGPT,
  Gemini, Google con resumen de IA): cómo abrir una sesión limpia (p. ej. chat temporal /
  sin memoria, actividad y personalización desactivadas, pestaña de incógnito en Google),
  con qué cuenta y plan (o sin sesión) y cómo anotar el modelo que muestra la app; que se
  pregunta con el texto literal del set, una pregunta por conversación nueva, en el orden
  del set; qué se captura (captura de la respuesta completa, con desplazamiento si hace
  falta; enlace compartido si la app lo permite); y los campos obligatorios por fila:
  fecha y hora local, pasada, id de pregunta, app, modo (normal / temporal / incógnito),
  sesión iniciada sí/no, plan de la cuenta, modelo mostrado, municipio desde el que se
  pregunta, ubicación del dispositivo activada sí/no, idioma. Incluye además tres reglas
  **anti-contaminación de la atribución**: no pulsar enlaces a la web de la clínica desde
  las respuestas; no buscar el nombre de la clínica en Google (las preguntas `AM` solo en
  ChatGPT y Gemini); y un registro de desviaciones (qué se hizo distinto y por qué). Las
  condiciones (cuenta, plan, modo, dispositivo, municipio) son **las mismas en todas las
  pasadas, incluidas las de SPEC-012**; si alguna no puede repetirse, se anota como
  desviación. *Evidencia*: checklist de campos y reglas contra el fichero.
- **CA-4 (plantilla de registro) [Agente]**: Dado ADR-004, cuando se publique
  `docs/piloto-artica/plantilla-captura.csv`, entonces tiene cabecera y **ninguna fila de
  datos**, con los campos de CA-3 más: clínicas nombradas en orden de aparición, Clínica
  Ártica nombrada sí/no, posición (RN-06), dominios citados, enlace compartido, nombre del
  fichero de captura y observaciones. *Evidencia*: el fichero tiene exactamente una línea;
  cruce de columnas con CA-3.
- **CA-5 (pasada 1) [Humano]**: Dado CA-1 a CA-4 y el dictamen de CA-2, cuando el humano
  haga la pasada 1, entonces en `$PUSHLLM_PRIVADO/piloto-artica/baseline/AAAA-MM-DD-p1/`
  hay el CSV rellenado con una fila por pregunta `AV`, `AR` y `AG` × app (ChatGPT, Gemini,
  Google) más las `AM` en ChatGPT y Gemini, y una captura por fila (con el set propuesto:
  24 × 3 + 2 × 2 = 76 filas); ≥ 95 % de las filas tienen todos los campos obligatorios, y
  las que no, lo explican en el registro de desviaciones. Es **una sola pasada** con el set
  completo de los tres niveles (no una pasada por nivel). Dentro de cada app se pregunta
  primero el bloque `AV`; el orden de los bloques `AR`, `AG` y `AM` lo fija el protocolo y
  es el mismo en todas las pasadas. La pasada puede repartirse en como máximo 2 días
  seguidos; si se reparte, el corte cae entre bloques (nunca dentro de un bloque app ×
  nivel), se anota en desviaciones y la pasada 2 se reparte igual. *Evidencia*: el verificador
  cuenta filas, capturas y campos vacíos en el espacio privado; el ledger recoge fecha,
  número de filas y desviaciones (sin cifras de SoV).
- **CA-6 (pasada 2) [Humano]**: Dado la variabilidad de las respuestas, cuando se haga la
  pasada 2, entonces se hace con las mismas condiciones y **el mismo set de los tres
  niveles, en el mismo orden** que la 1, en la separación que fije
  el dictamen de CA-2 (propuesta: entre 2 y 10 días después), y **antes de la primera
  acción** del piloto. *Evidencia*: fechas de las pasadas frente a la fecha de la primera
  acción del registro de SPEC-012; condiciones iguales o desviación anotada.
- **CA-7 (recuento "antes") [Agente]**: Dado las pasadas 1 y 2, cuando se haga el
  recuento según el dictamen de CA-2, entonces existe
  `$PUSHLLM_PRIVADO/piloto-artica/baseline/recuento-antes.md` con, por app: respuestas
  válidas, SoV bruto de Clínica Ártica, posición media y clínicas que aparecen en su lugar;
  el SoV ponderado ChatGPT+Gemini; Google AI Overviews aparte (con cuántas veces hubo
  resumen de IA); los dominios más citados; y el resultado de las preguntas `AM` (datos que
  el asistente da de la clínica y si son correctos: dirección, servicios, precios). El
  procedimiento de recuento está escrito de forma que otro lo reproduzca a mano o con una
  hoja de cálculo desde el CSV. Todo lo anterior se refiere al **núcleo** (`AV`). Además
  (enmienda 2026-09-29), el recuento tiene **una sección por nivel** (`AR`, `AG`) con los
  indicadores y definiciones de la ampliación del dictamen (CA-2 g–j), las clínicas que
  aparecen en su lugar y los dominios citados de ese nivel; ninguna cifra de `AR`/`AG` entra
  en el SoV bruto o ponderado del núcleo ni en su estabilidad. *Evidencia*: el verificador
  recalcula desde el CSV privado y coincide, por nivel; el ponderado del núcleo es el mismo
  si se borran del CSV todas las filas `AR` y `AG`.
- **CA-8 (margen para el criterio Go) [Agente avisa; Humano decide]**: Dado que la clínica
  podría ya aparecer mucho en las preguntas de Viveiro, cuando el recuento de CA-7 deje al
  SoV ponderado a menos de 15 pts de su techo (≥ 85 %) en el set completo, entonces antes de
  la primera acción el humano decide y deja registrado en el ledger si se mantiene el
  criterio, se mide sobre un subconjunto (p. ej. preguntas de Lugo o capilar) o se cambia
  el umbral; nunca después de ver el efecto. En todo caso, el set `AV` queda **congelado**
  con fecha antes de la primera acción; las preguntas que se añadan después se informan
  aparte y no cuentan para el criterio Go. El aviso de techo se calcula solo con `AV`. Las
  secciones `AR` y `AG` se congelan en la misma fecha que `AV` (inicio de la pasada 1) y con
  la misma regla (una pregunta nueva lleva id nuevo y se informa aparte); nunca pasan a
  contar para el criterio Go. *Evidencia*: fecha de congelación y, si aplica,
  decisión fechada en el ledger, ambas anteriores a la primera acción.
- **CA-9 (foto técnica "antes") [Agente]**: Dado la palanca 4 y la palanca 1
  (`04-mechanics-of-llm-visibility.md` §2), cuando se tome la foto antes de la primera
  acción, entonces en `$PUSHLLM_PRIVADO/piloto-artica/baseline/foto-tecnica-AAAA-MM-DD/`
  hay, con fecha: copia de `robots.txt`; el JSON-LD de la portada y de al menos una página
  por línea de tratamiento; el `sitemap` si existe; y una tabla de presencia
  (present / incomplete / absent, con URL) de Clínica Ártica en Google Business Profile,
  Doctoralia, Multiestetica, Top Doctors y Páxinas Galegas, y en los dominios citados en la
  pasada 1. *Evidencia*: el verificador abre los ficheros y comprueba fechas y URLs.
- **CA-10 (hoja de hallazgo para la reunión) [Agente]**: Dado que la reunión de SPEC-009
  abre con el dato, cuando esté hecha la pasada 1, entonces existe
  `$PUSHLLM_PRIVADO/piloto-artica/baseline/hallazgo-reunion.md` (una página, castellano,
  para enseñar en el móvil o en papel) con: 3 respuestas reales representativas (captura o
  cita literal, con app y fecha); quién aparece cuando no aparece la clínica; qué páginas
  citan los asistentes; qué dice un asistente de la clínica cuando se le pregunta por ella
  (`AM`); y una frase honesta de límites ("es una foto de un día; las respuestas varían;
  esto no es una promesa"). Sin "LLM", "SoV", "share of voice", "AEO", "GEO",
  "visibilidad en IA" ni "posicionamiento garantizado" (mismo criterio que SPEC-004
  CA-12). Las 3 respuestas representativas salen del núcleo (`AV`); si la hoja menciona
  `AR` o `AG`, lo hace como dato "fuera de la comarca", sin objetivo ni promesa, y no
  presenta el nivel Galicia como algo que se vaya a conseguir (ADR-005 §6).
  *Evidencia*: checklist; búsqueda de los términos prohibidos, sin coincidencias.
- **CA-11 (nada en bruto en el repo) [Verificador]**: Dado ADR-001 y ADR-004, cuando se
  cierre la spec, entonces `git ls-files` no lista capturas, CSV con datos, recuentos ni la
  hoja de hallazgo, y `docs/piloto-artica/` no contiene cifras junto a nombres de clínicas
  de `brands.csv` ni emails, teléfonos o nombres de persona. *Evidencia*: salida de
  `git ls-files` y de la búsqueda por patrón en el ledger.

## Entidades y reglas afectadas
- Dominio: Prompt, Prompt catalogue, Provider, Mention, Position, Share of voice, Weighted
  SoV, Source, PresenceCheck.
- RN-01 (con la precisión de alias de CA-2), RN-02, RN-03, RN-04 (AI Overviews aparte),
  RN-06, RN-09.
- D-3 (la foto "antes" existe antes de actuar), D-5/RN-10 (se mide en la app de consumo:
  aquí literalmente), D-6.
- ADR-001, ADR-003 (lote de Viveiro separado de Vigo), ADR-004, ADR-005 (tres niveles;
  Go solo con el núcleo; niveles nunca mezclados).

## Fuera de alcance
- Medición con el probe (SPEC-008) y la ejecución completa del probe de EPIC-001
  (SPEC-002).
- Claude y Perplexity en la medición manual: opcionales; si se incluyen, deben repetirse en
  todas las pasadas posteriores o no se usan en el ponderado.
- Diagnóstico de gaps y plan de acciones (SPEC-011): aquí solo la foto.
- Enseñar nada a la clínica (SPEC-009).
- Usar `AR` o `AG` para el criterio Go, ni solas ni mezcladas con `AV` (ADR-005 §4).
- Tratamientos del nivel Galicia distintos de trasplante capilar DHI y blefaroplastia;
  preguntas de Galicia que nombren una ciudad concreta (serían otro nivel).
- Preguntas de otras comunidades distintas del occidente de Asturias; cualquier uso de las
  respuestas `AR`/`AG` como lista de objetivos o estudio del mercado de Vigo (ADR-005 §5).
- Pasadas separadas por nivel: los tres niveles van en la misma pasada.

## Notas para el gate humano
- **Qué puede hacer el humano esta semana, sin claves**: en cuanto el agente publique
  CA-1, CA-3 y CA-4 y conste el dictamen de CA-2 (horas de trabajo de agente), hacer la
  pasada 1 desde el móvil (~~unas 40–50 consultas, 60–90 min~~; tras la enmienda del
  2026-09-29, unas 76 consultas y 95–140 min, ver abajo) y, entre 2 y 10
  días después, la pasada 2. La pasada 1 debería ir **antes de la reunión** de SPEC-009.
- **Decisiones a mirar con lupa**: (1) comparar solo manual con manual y probe con probe
  (CA-2 e): si las claves llegan después de la primera acción, el criterio Go se mide solo
  a mano. (2) CA-8: si la clínica ya aparece casi siempre en Viveiro, el +15 es inalcanzable
  y hay que decidir el criterio **antes** de actuar. (3) Reglas anti-contaminación: en un
  mercado pequeño, clics y búsquedas de marca propios pueden verse en la atribución.
- **Pregunta abierta**: desde qué municipio y con qué cuenta medirá el humano. Si no está
  en A Mariña, el resumen de IA de Google puede variar por ubicación; por eso todas las
  preguntas nombran un lugar. Si el humano paga ChatGPT Plus, el modelo no es el de la
  mayoría de pacientes (D-5): preferible una cuenta gratuita o sin sesión, y anotarlo.
- **Propuesta orientativa de set** (el implementador la cierra contra CA-1; no es parte
  del contrato):
  AV01 ¿Cuál es la mejor clínica de medicina estética en Viveiro? · AV02 Recomiéndame una
  clínica de medicina estética en A Mariña lucense. · AV03 Mejores clínicas de medicina
  estética en Lugo. · AV04 ¿Dónde ponerme bótox en Viveiro con un médico de confianza? ·
  AV05 ¿Cuánto cuesta el ácido hialurónico en labios en Viveiro y dónde me lo hago? · AV06
  ¿Dónde hacerme un trasplante capilar en la provincia de Lugo? · AV07 ¿Cuánto cuesta un
  injerto capilar DHI en Galicia y qué clínica me recomiendas cerca de Viveiro? · AV08
  Tratamiento para grasa localizada o flacidez en Viveiro, ¿qué clínica? · AV09 ¿Qué
  clínica estética de la zona de Viveiro tiene médicos y buenas opiniones? · AV10 ¿Merece
  la pena ir a Lugo o a A Coruña para medicina estética o hay buenas clínicas en A Mariña? ·
  AV11 Quitar un lunar o una verruga de la cara en Viveiro, ¿dónde me lo hacen? · AV12
  Tratamiento de manchas en la cara con láser en Burela o Foz. · AV13 Cal é a mellor clínica
  de medicina estética en Viveiro? · AV14 Onde me podo facer un transplante capilar preto
  de Viveiro? · AM01 ¿Qué sabes de Clínica Ártica de Viveiro? ¿Es de fiar?
- No aprobar SPEC-008 no bloquea esta spec; son independientes.

### Enmienda 2026-09-29 — tres niveles (para el gate)
- **Tiempo de cada pasada**: de 49 a **76 consultas** con el set propuesto (24 de medición
  × 3 apps + 2 `AM` × 2). Estimación: **95–140 min** de consultas + 25–30 min de CSV y
  capturas; se puede repartir en 2 días seguidos (corte entre bloques). Las dos pasadas
  "antes" y las dos "después" de SPEC-012 tienen ya este tamaño.
- **Ids**: se mantiene `AV01`–`AV15` como núcleo sin tocar (SPEC-008 CA-1, los tests y los
  CSV ya los usan, y el Go se define sobre ellos); `AR` (área de influencia, "regional") y
  `AG` (Galicia) siguen el patrón `A` + letra + 2 dígitos del piloto, de modo que el nivel
  se lee en el propio id y el recuento no puede mezclarlos por accidente. `AI` se descartó
  (se confunde con "IA/AI").
- **Decisiones a mirar con lupa**: (1) el núcleo es el set vigente tal cual, aunque
  `AV03`, `AV09`–`AV12` nombran también Lugo, A Coruña o Galicia: se respeta la decisión
  del humano de que el núcleo es "el set actual"; si prefiere un núcleo solo Viveiro/
  A Mariña, este es el último momento (el set no está congelado). (2) "Norte de Lugo fuera
  de A Mariña" = Terra Chá (Vilalba) en la propuesta; A Mariña ya es el norte de Lugo.
  (3) Ribadeo es A Mariña (Lugo), no Asturias: sigue siendo núcleo; el occidente de
  Asturias se mide con Navia, Tapia de Casariego, Vegadeo o Castropol. (4) Los tratamientos
  `AG` exigen que la clínica los ofrezca según su web (URL y fecha en el ledger).
- **Propuesta orientativa de `AR` y `AG`** (el implementador la cierra contra CA-1; no es
  parte del contrato):
  AR01 Vivo en Ortigueira. ¿Qué clínica de medicina estética con médicos me recomiendas por
  la zona? · AR02 Onde me podo poñer bótox cun médico de confianza preto de Ferrol? ·
  AR03 Vivo en Vilalba. ¿Dónde me hago un tratamiento de ácido hialurónico en el norte de
  Lugo? · AR04 Vivo en Tapia de Casariego (Asturias). ¿Qué clínica de medicina estética me
  recomiendas cerca, aunque tenga que desplazarme un poco? · AR05 ¿Cuánto cuesta un injerto
  capilar DHI cerca de Navia o Vegadeo y qué clínica me recomiendas?
  AG01 ¿Cuál es la mejor clínica de Galicia para hacerme un injerto capilar con técnica
  DHI? · AG02 ¿Cuánto cuesta un trasplante capilar en Galicia y dónde me recomiendas
  hacerlo? · AG03 ¿Dónde me recomiendas operarme los párpados (blefaroplastia) en Galicia?
  · AG04 Cal é a mellor clínica de Galicia para facer unha blefaroplastia?
- **Contexto de competencia** (búsqueda pública del orquestador, 2026-09-29; no forma parte
  del set): en Galicia el capilar lo disputan cadenas y clínicas con sedes en Vigo,
  Santiago, A Coruña, Pontevedra, Ourense y Vilagarcía; la blefaroplastia, cirujanos de
  A Coruña y Vigo y una cadena en Lugo; los directorios se organizan por ciudad. Por eso el
  objetivo de `AG` es "aparecer alguna vez" y no se promete.
