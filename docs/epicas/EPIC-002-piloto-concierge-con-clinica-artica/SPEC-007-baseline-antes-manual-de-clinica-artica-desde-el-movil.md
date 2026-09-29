---
id: SPEC-007
tipo: spec
epica: EPIC-002
estado: borrador
aprobada-por: Alberto Fojo
historial:
  - {estado: borrador, fecha: 2026-09-28, por: sdd-arquitecto}
  - {estado: aprobada, fecha: 2026-09-28, por: Alberto Fojo}
  - {estado: en-progreso, fecha: 2026-09-28, por: sdd-implementador}
  - {estado: bloqueada, fecha: 2026-09-29, por: sdd-arquitecto}
  - {estado: borrador, fecha: 2026-09-29, por: sdd-arquitecto}
  - {estado: aprobada, fecha: 2026-09-29, por: Alberto Fojo}
  - {estado: en-progreso, fecha: 2026-09-29, por: sdd-implementador}
  - {estado: bloqueada, fecha: 2026-09-29, por: sdd-arquitecto}
  - {estado: borrador, fecha: 2026-09-29, por: sdd-arquitecto}
---
# SPEC-007 — Baseline antes manual de Clínica Ártica desde el móvil

> **Enmienda 2026-09-29 (b) (sdd-arquitecto) — la medición manual pasa a ser calibración.**
> Decisión del humano (Alberto Fojo, 2026-09-29), recogida por sdd-producto en EPIC-002,
> criterios 1 y 4: el **probe (API) es el instrumento de medición y del criterio Go** en
> los tres niveles (`AV`, `AR`, `AG`), con su baseline oficial en SPEC-008 CA-7. La medición
> manual desde el móvil se reduce a una **calibración**: núcleo `AV` (15 preguntas) en
> ChatGPT, Gemini y Google, más las dos `AM` en ChatGPT y Gemini (49 consultas), **una
> pasada "antes"** (aquí) y **una "después"** (SPEC-012). Sirve para (a) comprobar que las
> cifras del probe se parecen a lo que ve el paciente en la app, (b) medir Google AI
> Overviews, que el probe no cubre, y (c) sacar capturas reales para la reunión.
> Cambian: Problema, CA-2 (ampliación (k)–(n)), CA-3, CA-5, CA-6 (retirado: desaparece la
> pasada 2), CA-7 (recuento y comparación app frente a probe), CA-8 (congelación del set por
> el baseline del probe; el aviso de techo pasa a SPEC-008 CA-10), CA-9, CA-10, entidades,
> Fuera de alcance y notas. CA-1, CA-4 y CA-11 no cambian. El título se mantiene para no
> romper rutas y referencias. La spec vuelve a `borrador` (estaba `en-progreso`, sin
> ninguna pasada hecha) y necesita **nueva aprobación humana**. Lo que el implementador debe
> rehacer está en el ledger (F-SPEC-007-8).

> **Nota 2026-09-29 (sdd-arquitecto) — cambio de nicho (ADR-008). No cambia ningún CA ni
> requiere re-aprobación.** Las citas a ADR-003 y ADR-005 de esta spec siguen valiendo en lo
> que usa (lote aparte, niveles `AV`/`AR`/`AG` sin mezclar, Go solo con `AV`, nivel Galicia
> sin prometer, marcas del piloto fuera del lote de Vigo). Lo que ADR-008 deroga es el
> encuadre como "excepción a D-2" y sus prohibiciones de prospección y de "Asturias no es
> mercado"; el lote de Vigo queda aparcado, intacto, como configuración por defecto.

> Spec **documental y de medición manual**. No hay código de producto. El agente redacta
> el set de preguntas, el protocolo, la plantilla y el recuento; el humano pregunta en las
> apps del móvil y captura. Material del repo en `docs/piloto-artica/`; datos, capturas y
> recuentos en `$PUSHLLM_PRIVADO/piloto-artica/baseline/` (ADR-001, ADR-004).

> Enmienda anterior del 2026-09-29 (a) — set en tres niveles (ADR-005): el set tiene núcleo
> `AV`, área de influencia `AR` y Galicia `AG`; ya está publicado (CA-1). Tras la enmienda
> (b), `AR` y `AG` solo los mide el probe.

## Problema
Criterios de éxito 1 y 4 de EPIC-002. El criterio Go (+15 pts de SoV ponderado, RN-03) se
mide con el probe (SPEC-008 CA-7 y CA-9; SPEC-012 CA-7). Pero el probe pregunta por API, no
en la app que usa el paciente, y no cubre Google AI Overviews (RN-04, D-6). Antes de
enseñar cifras del probe a la clínica o de prometerle algo, hay que comprobar con una
muestra corta que **lo que ve el paciente en la app se parece a lo que mide el probe**, y
medir a mano lo único que el probe no ve (AI Overviews). La misma pasada da las capturas
reales para abrir la reunión (SPEC-009). La calibración tiene que repetirse con el mismo
protocolo en el "después" (SPEC-012), o no será comparable. Hacerlo así ahorra tiempo al
humano (49 consultas por pasada en vez de 76, y dos pasadas en vez de cuatro) y deja el
criterio Go en un instrumento automático, repetible y legal; automatizar las apps de
consumo no lo es.

## Usuarios / roles afectados
- Humano (fundador): hace las preguntas en ChatGPT, Gemini y Google desde el móvil y
  captura. [Humano]
- Agente (sdd-implementador): redacta set, protocolo, plantilla, foto técnica, recuento y
  comparación con el probe. [Agente]
- Consultadas: `sdd-metricas` (dictamen obligatorio, CA-2); `sdd-visibilidad-local`
  opcional para el set y la foto técnica.
- sdd-verificador: comprueba cada CA contra ficheros del repo y del espacio privado.
  [Verificador]
- Consumidores: SPEC-008 (mismos ids de prompt; su baseline congela el set), SPEC-009 (hoja
  de hallazgo), SPEC-011 (fuentes citadas y foto técnica), SPEC-012 (calibración
  "después" con el mismo protocolo).

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
  **Ampliación para la calibración (enmienda 2026-09-29 (b))**: antes de la pasada
  "antes" (CA-5) consta en el ledger una **segunda ampliación fechada** del dictamen de
  `sdd-metricas` que fija:
  (k) **qué se compara y con qué**: la unidad es la casilla pregunta `AV` × asistente
  presente en los dos instrumentos (ChatGPT y Gemini; Claude no está en la manual), y en
  cada casilla "sale / no sale" Clínica Ártica y su posición (RN-06); contra qué ejecución
  del probe se compara la pasada (la de `AV` más cercana en fechas, con una **ventana
  máxima** en días entre las dos) y cómo se resume una casilla del probe con varios runs
  (p. ej. "sale" si sale en la mayoría de runs, o la proporción); y cómo se tratan las
  diferencias conocidas entre instrumentos (la manual se hace desde Vilaboa y el probe
  envía la ubicación Viveiro; modelo de la app gratuita frente al modelo por defecto de la
  API, D-5/RN-10);
  (l) una definición **operativa y verificable** de "**coinciden de forma razonable**":
  umbral de acuerdo (p. ej. porcentaje mínimo de casillas con el mismo "sale / no sale" y/o
  diferencia máxima de SoV bruto por asistente entre app y probe; tolerancia de posición),
  su ruido esperable con 15 casillas por asistente, y qué se hace si no coinciden (qué se
  revisa: configuración del probe, protocolo manual o lectura; y que ninguna cifra del probe
  se enseña a la clínica ni se promete nada hasta resolverlo);
  (m) cómo se trata **Google AI Overviews**, que no tiene equivalente en el probe: canal
  aparte (RN-04), fuera del acuerdo y del criterio Go; qué cifras se dan con 15 búsquedas
  `AV` y una pasada ("x de n" o porcentaje), incluido cuándo no aparece resumen; y cómo se
  lee el antes/después de ese canal en SPEC-012;
  (n) qué queda del dictamen anterior: se declara, punto por punto, si (a)–(j) siguen
  aplicando a la manual, se sustituyen o quedan sin objeto — en particular (b) (una pasada
  "antes" y una "después" en lugar de dos y dos), (c) (si el SoV ponderado manual se sigue
  calculando y, si es así, con qué rótulo: dato de calibración, nunca cifra del Go), (e)
  (sigue: el Go es probe contra probe; ninguna cifra manual se resta de una del probe),
  (f) (el ruido del Go se re-evalúa para el probe en SPEC-008 CA-9) y (g)–(j) (los niveles
  `AR`/`AG` salen de la manual y sus indicadores se trasladan al probe en SPEC-008 CA-9).
  Cada condición nueva se mapea a un cambio en protocolo, plantilla, procedimiento o
  herramienta. El dictamen lo emite `sdd-metricas`; este CA no lo prejuzga. *Evidencia*:
  sección de la segunda ampliación con fecha anterior a la pasada "antes" y filas (k)–(n)
  en la tabla condición → cambio.
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
  ChatGPT y Gemini); y un registro de desviaciones (qué se hizo distinto y por qué).
  **Calibración (enmienda 2026-09-29 (b))**: el protocolo mide **solo** el núcleo `AV`
  (15 preguntas) en ChatGPT, Gemini y Google, más las `AM` en ChatGPT y Gemini (49
  consultas); en cada app, primero el bloque `AV` y después, en ChatGPT y Gemini, las `AM`;
  hay **una pasada "antes"** (valor de `pasada`: `antes`) y **una "después"** (`despues`,
  SPEC-012); cada pasada se hace dentro de la ventana del dictamen (CA-2 k) respecto a la
  ejecución del probe con la que se compara; y da el tiempo estimado. `AR` y `AG` no se
  preguntan a mano. Las condiciones (cuenta, plan, modo, dispositivo, municipio) son **las
  mismas en las dos pasadas**; si alguna no puede repetirse, se anota como desviación.
  *Evidencia*: checklist de campos y reglas contra el fichero; búsqueda de `AR`/`AG` en el
  orden de preguntas del protocolo, sin coincidencias.
- **CA-4 (plantilla de registro) [Agente]**: Dado ADR-004, cuando se publique
  `docs/piloto-artica/plantilla-captura.csv`, entonces tiene cabecera y **ninguna fila de
  datos**, con los campos de CA-3 más: clínicas nombradas en orden de aparición, Clínica
  Ártica nombrada sí/no, posición (RN-06), dominios citados, enlace compartido, nombre del
  fichero de captura y observaciones. *Evidencia*: el fichero tiene exactamente una línea;
  cruce de columnas con CA-3.
- **CA-5 (pasada "antes" de calibración) [Humano]**: Dado CA-1 a CA-4, el set congelado
  (CA-8) y la segunda ampliación del dictamen (CA-2 k–n), cuando el humano haga la pasada
  "antes", entonces en `$PUSHLLM_PRIVADO/piloto-artica/baseline/AAAA-MM-DD-antes/` hay el
  CSV rellenado con una fila por pregunta `AV` × app (ChatGPT, Gemini, Google) más las `AM`
  en ChatGPT y Gemini (15 × 3 + 2 × 2 = **49 filas**) y una captura por fila; ≥ 95 % de las
  filas tienen todos los campos obligatorios, y las que no, lo explican en el registro de
  desviaciones. Es **una sola pasada**; puede repartirse en como máximo 2 días seguidos, con
  el corte entre bloques de app (nunca dentro de uno) y anotado en desviaciones. Se hace
  **antes de la primera acción** del piloto y dentro de la ventana de CA-2 (k) respecto a
  una ejecución `AV` del probe (el baseline oficial de SPEC-008 CA-7 u otra que el dictamen
  admita). *Evidencia*: el verificador cuenta filas, capturas y campos vacíos en el espacio
  privado; el ledger recoge fecha, número de filas, desviaciones y la ejecución del probe
  emparejada (fecha y carpeta), sin cifras de SoV.
- **CA-6 (pasada 2) — retirado (enmienda 2026-09-29 (b))**: la segunda pasada "antes"
  desaparece por decisión del humano. La estabilidad del criterio Go se mide con el probe
  (SPEC-008 CA-9, SPEC-012 CA-7); la calibración "después" la fija SPEC-012 CA-3. Se
  conserva el número para no renumerar los CA del ledger.
- **CA-7 (informe de calibración "antes") [Agente]**: Dado la pasada "antes" (CA-5) y la
  ejecución del probe emparejada, cuando se haga el recuento según el dictamen de CA-2,
  entonces existe `$PUSHLLM_PRIVADO/piloto-artica/baseline/calibracion-antes.md` con:
  (1) **lo que ve el paciente**, por app: respuestas válidas, SoV bruto de Clínica Ártica
  en `AV`, posición media y clínicas que aparecen en su lugar; Google AI Overviews aparte
  según CA-2 (m), con cuántas veces hubo resumen de IA; los dominios más citados; y el
  resultado de las `AM` (datos que el asistente da de la clínica y si son correctos:
  dirección, servicios, precios); (2) **la comparación app frente a probe**: una tabla por
  casilla `AV` × asistente (ChatGPT, Gemini) con "sale / no sale" y posición en la app y en
  el probe (resumen de runs según CA-2 k), el grado de acuerdo y el veredicto
  "**coinciden de forma razonable: sí / no**" según CA-2 (l), con la fecha y la carpeta de
  la ejecución del probe usada. Si el veredicto es "no", antes de enviar la propuesta de
  SPEC-009 y antes de la primera acción consta en el ledger la causa que se ha podido
  identificar y la decisión del humano (qué se ajusta, o seguir con la salvedad escrita);
  hasta entonces no se enseña a la clínica ninguna cifra del probe. Ninguna cifra de este
  informe entra en el criterio Go (CA-2 e). El procedimiento está escrito de forma que otro
  lo reproduzca a mano o con una hoja de cálculo desde el CSV manual y el `results.csv` del
  probe. *Evidencia*: el verificador recalcula desde los datos privados y coincide; si el
  veredicto es "no", decisión fechada en el ledger anterior a la propuesta y a la primera
  acción.
- **CA-8 (congelación del set) [Agente registra; Humano fija]**: Dado que el set es común a
  los dos instrumentos, cuando empiece la primera ejecución del baseline oficial del probe
  (SPEC-008 CA-7) — o antes, si el humano fija una fecha en el ledger —, entonces el set
  completo (`AV`, `AR`, `AG`) queda **congelado** con esa fecha: no cambia ni una coma; una
  pregunta que se añada después lleva id nuevo, se informa aparte y no cuenta para el
  criterio Go; `AR` y `AG` nunca pasan a contar para el Go. La pasada "antes" (CA-5) no
  empieza sin fecha de congelación: si el baseline del probe aún no se ha lanzado, el humano
  fija la congelación en el ledger antes de empezarla. El **aviso de techo** (SoV ponderado
  del núcleo ≥ 85 %) ya no se calcula con la medición manual: pasa a SPEC-008 CA-10, con el
  baseline del probe. *Evidencia*: fecha de congelación en el ledger, anterior o igual al
  inicio de la pasada "antes" y del baseline del probe, y anterior a la primera acción.
- **CA-9 (foto técnica "antes") [Agente]**: Dado la palanca 4 y la palanca 1
  (`04-mechanics-of-llm-visibility.md` §2), cuando se tome la foto antes de la primera
  acción, entonces en `$PUSHLLM_PRIVADO/piloto-artica/baseline/foto-tecnica-AAAA-MM-DD/`
  hay, con fecha: copia de `robots.txt`; el JSON-LD de la portada y de al menos una página
  por línea de tratamiento; el `sitemap` si existe; y una tabla de presencia
  (present / incomplete / absent, con URL) de Clínica Ártica en Google Business Profile,
  Doctoralia, Multiestetica, Top Doctors y Páxinas Galegas, y en los dominios citados en la
  pasada "antes" y, si ya existe, en el baseline oficial del probe (SPEC-008 CA-7).
  *Evidencia*: el verificador abre los ficheros y comprueba fechas y URLs.
- **CA-10 (hoja de hallazgo para la reunión) [Agente]**: Dado que la reunión de SPEC-009
  abre con el dato, cuando esté hecha la pasada "antes", entonces existe
  `$PUSHLLM_PRIVADO/piloto-artica/baseline/hallazgo-reunion.md` (una página, castellano,
  para enseñar en el móvil o en papel) con: 3 respuestas reales representativas del núcleo
  `AV` (captura o cita literal, con app y fecha); quién aparece cuando no aparece la
  clínica; qué páginas citan los asistentes; qué dice un asistente de la clínica cuando se
  le pregunta por ella (`AM`); y una frase honesta de límites ("es una foto de un día; las
  respuestas varían; esto no es una promesa"). Sin "LLM", "SoV", "share of voice", "AEO",
  "GEO", "visibilidad en IA" ni "posicionamiento garantizado" (mismo criterio que SPEC-004
  CA-12). La hoja no usa cifras del probe salvo que CA-7 diga que coinciden de forma
  razonable, y no presenta el nivel Galicia como algo que se vaya a conseguir (ADR-005 §6).
  *Evidencia*: checklist; búsqueda de los términos prohibidos, sin coincidencias.
- **CA-11 (nada en bruto en el repo) [Verificador]**: Dado ADR-001 y ADR-004, cuando se
  cierre la spec, entonces `git ls-files` no lista capturas, CSV con datos, recuentos, el
  informe de calibración ni la hoja de hallazgo, y `docs/piloto-artica/` no contiene cifras
  junto a nombres de clínicas de `brands.csv` ni emails, teléfonos o nombres de persona.
  *Evidencia*: salida de `git ls-files` y de la búsqueda por patrón en el ledger.

## Entidades y reglas afectadas
- Dominio: Prompt, Prompt catalogue, Provider, Mention, Position, Share of voice, Weighted
  SoV, Source, PresenceCheck.
- RN-01 (con la precisión de alias de CA-2), RN-02, RN-03, RN-04 (AI Overviews aparte),
  RN-06, RN-09, RN-10 (el probe usa el modelo por defecto: es la diferencia que la
  calibración mide).
- D-3 (la foto "antes" existe antes de actuar), D-5 (el probe es el instrumento del
  producto; la manual lo contrasta con la app de consumo), D-6.
- ADR-001, ADR-003 (lote de Viveiro separado de Vigo), ADR-004, ADR-005 (tres niveles;
  Go solo con el núcleo; niveles nunca mezclados, en ningún instrumento).
- SPEC-008 CA-7, CA-9 y CA-10 (baseline oficial, dictamen del Go con el probe, techo).

## Fuera de alcance
- La medición con el probe y el criterio Go: baseline oficial en SPEC-008 CA-7; forma,
  estabilidad y ruido en SPEC-008 CA-9; techo en SPEC-008 CA-10; veredicto en SPEC-012 CA-7.
- `AR` y `AG` en la medición manual: los mide el probe. Consecuencia aceptada: Google AI
  Overviews **no se mide** en `AR` ni en `AG` (el probe no lo cubre).
- La pasada 2 "antes" (retirada, CA-6) y cualquier pasada manual extra antes de la
  primera acción.
- Usar cifras manuales en el criterio Go, solas o combinadas con las del probe (CA-2 e;
  ADR-005 §4).
- Claude y Perplexity en la medición manual: opcionales y solo observación; no entran en
  la comparación con el probe ni en ninguna cifra.
- Diagnóstico de gaps y plan de acciones (SPEC-011): aquí solo la foto.
- Enseñar nada a la clínica (SPEC-009).
- La calibración "después" y la comprobación trimestral posterior al piloto (SPEC-012).

## Notas para el gate humano
- **Enmienda 2026-09-29 (b) — qué cambia para ti**: una pasada "antes" de **49 consultas**
  (15 `AV` × ChatGPT, Gemini y Google + 2 `AM` × ChatGPT y Gemini): unos **60–90 min** de
  consultas más 20–25 min de CSV y capturas; y otra igual al cierre (SPEC-012). Antes eran
  76 consultas × 4 pasadas.
- **AM01 y AM02 se mantienen** en la manual: son 4 consultas, el probe no las hace
  (SPEC-008 CA-1) y dan a la reunión lo que dice cada asistente de la clínica (CA-10) y al
  diagnóstico los datos erróneos (NAP, servicios). En el "después" muestran si esos datos
  se corrigieron.
- **Decisiones a mirar con lupa**:
  1. **Orden**: el set se congela, como tarde, con el primer baseline del probe (CA-8). La
     pasada "antes" necesita el set congelado y una ejecución `AV` del probe dentro de la
     ventana del dictamen (CA-2 k). Si quieres hacer la pasada antes de que exista el
     baseline oficial (que espera a SPEC-013), fija tú la congelación en el ledger y lanza
     una ejecución `AV` del probe cercana en fechas, si el dictamen lo admite.
  2. **Google AI Overviews en `AR`/`AG` deja de medirse.** Es la consecuencia directa de
     quitar esos niveles de la manual. Si te importa para el capilar en Galicia, habría que
     añadir 4–9 búsquedas de Google a la manual (sin tocar el Go).
  3. **Ubicación distinta por instrumento**: la manual se hace desde Vilaboa (P-4) y el
     probe envía la ubicación Viveiro. Todas las preguntas nombran el lugar, pero es una
     diferencia que la calibración absorberá; el dictamen (CA-2 k) dice cómo se trata.
  4. **Si app y probe no coinciden** (CA-7): no se enseña ninguna cifra del probe ni se
     envía la propuesta hasta decidir qué se ajusta. Eso puede retrasar la propuesta.
- **Lo que no cambia**: el set publicado (CA-1), la plantilla (CA-4), las reglas de
  mención (P-1, P-2), la ubicación de medición desde Vilaboa (P-4) y la frontera de datos
  (CA-11).
- **Preguntas abiertas heredadas**: P-5 (Mondoñedo) y P-6 (Sarria/A Fonsagrada frente a
  ADR-005 §1) siguen abiertas en el ledger; con esta enmienda, P-5 ya solo afecta al probe
  y hay que resolverla antes de la congelación (CA-8).
