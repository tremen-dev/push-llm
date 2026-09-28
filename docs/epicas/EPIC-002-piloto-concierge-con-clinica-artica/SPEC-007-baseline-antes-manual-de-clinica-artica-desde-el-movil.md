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
---
# SPEC-007 — Baseline antes manual de Clínica Ártica desde el móvil

> Spec **documental y de medición manual**. No hay código. El agente redacta el set de
> preguntas, el protocolo, la plantilla y el recuento; el humano pregunta en las apps
> del móvil y captura. Ejecutable **ya, sin claves de API**. Material del repo en
> `docs/piloto-artica/`; datos, capturas y recuentos en
> `$PUSHLLM_PRIVADO/piloto-artica/baseline/` (ADR-001, ADR-004).

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
  hay el CSV rellenado con una fila por pregunta `AV` × app (ChatGPT, Gemini, Google) más
  las `AM` en ChatGPT y Gemini, y una captura por fila; ≥ 95 % de las filas tienen todos
  los campos obligatorios, y las que no, lo explican en el registro de desviaciones. La
  pasada puede repartirse en como máximo 2 días seguidos. *Evidencia*: el verificador
  cuenta filas, capturas y campos vacíos en el espacio privado; el ledger recoge fecha,
  número de filas y desviaciones (sin cifras de SoV).
- **CA-6 (pasada 2) [Humano]**: Dado la variabilidad de las respuestas, cuando se haga la
  pasada 2, entonces se hace con las mismas condiciones que la 1, en la separación que fije
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
  hoja de cálculo desde el CSV. *Evidencia*: el verificador recalcula desde el CSV privado
  y coincide.
- **CA-8 (margen para el criterio Go) [Agente avisa; Humano decide]**: Dado que la clínica
  podría ya aparecer mucho en las preguntas de Viveiro, cuando el recuento de CA-7 deje al
  SoV ponderado a menos de 15 pts de su techo (≥ 85 %) en el set completo, entonces antes de
  la primera acción el humano decide y deja registrado en el ledger si se mantiene el
  criterio, se mide sobre un subconjunto (p. ej. preguntas de Lugo o capilar) o se cambia
  el umbral; nunca después de ver el efecto. En todo caso, el set `AV` queda **congelado**
  con fecha antes de la primera acción; las preguntas que se añadan después se informan
  aparte y no cuentan para el criterio Go. *Evidencia*: fecha de congelación y, si aplica,
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
  CA-12). *Evidencia*: checklist; búsqueda de los términos prohibidos, sin coincidencias.
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
- ADR-001, ADR-003 (lote de Viveiro separado de Vigo), ADR-004.

## Fuera de alcance
- Medición con el probe (SPEC-008) y la ejecución completa del probe de EPIC-001
  (SPEC-002).
- Claude y Perplexity en la medición manual: opcionales; si se incluyen, deben repetirse en
  todas las pasadas posteriores o no se usan en el ponderado.
- Diagnóstico de gaps y plan de acciones (SPEC-011): aquí solo la foto.
- Enseñar nada a la clínica (SPEC-009).

## Notas para el gate humano
- **Qué puede hacer el humano esta semana, sin claves**: en cuanto el agente publique
  CA-1, CA-3 y CA-4 y conste el dictamen de CA-2 (horas de trabajo de agente), hacer la
  pasada 1 desde el móvil (unas 40–50 consultas, estimación 60–90 min) y, entre 2 y 10
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
