---
id: SPEC-007
tipo: spec
epica: EPIC-002
estado: hecho
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
  - {estado: aprobada, fecha: 2026-09-29, por: Alberto Fojo}
  - {estado: en-progreso, fecha: 2026-09-29, por: sdd-implementador}
  - {estado: bloqueada, fecha: 2026-09-29, por: sdd-arquitecto}
  - {estado: borrador, fecha: 2026-09-29, por: sdd-arquitecto}
  - {estado: aprobada, fecha: 2026-09-29, por: Alberto Fojo}
  - {estado: en-progreso, fecha: 2026-09-29, por: sdd-implementador}
  - {estado: en-revision, fecha: 2026-09-29, por: sdd-implementador}
  - {estado: hecho, fecha: 2026-09-29, por: sdd-verificador}
---
# SPEC-007 — Baseline antes manual de Clínica Ártica desde el móvil

> **Enmienda 2026-09-29 (c) (sdd-arquitecto) — la calibración se reorienta al Go de ADR-009,
> con el mismo esfuerzo (49 consultas).** El Go del piloto ya no es "+15 pts en el núcleo":
> ADR-009 (aprobado por el humano el 2026-09-29; está en la PR #5, aún no en esta rama) lo
> define como **(C) crecer en `AR`**, **(D) defender `AV`** y **(A) ≥ 1 paciente**. El
> baseline oficial (SPEC-008 CA-7) dejó el núcleo por encima del umbral de techo y `AR` con
> presencia minoritaria y resultados repartidos (veredictos; cifras solo en privado, ADR-004
> §2). Decisión del humano (Alberto Fojo, 2026-09-29): la calibración pasa a medir **`AR01`–`AR05`
> en ChatGPT, Gemini y Google (15)**, **`AV01`–`AV15` en ChatGPT y Gemini (30)** y **`AM01`–`AM02`
> en ChatGPT y Gemini (4)**. **Desaparece `AV` en Google**; `AG` sigue sin calibración manual;
> **no se añade ninguna pregunta** (set congelado; las preguntas del noroeste son de una
> épica futura de validación del nicho). Así la calibración comprueba el probe donde se
> decide (C), da Google AI Overviews fuera de la comarca y sigue respaldando la frase
> comercial de SPEC-009 y la condición (D).
> Cambian: Problema, CA-2 (tercera ampliación (o)–(s)), CA-3 (bloque de calibración), CA-5,
> CA-7 (comparación **por nivel**), CA-8 (nota), CA-10 (cifras del probe por nivel),
> entidades, Fuera de alcance y notas. CA-1, CA-4, CA-6 (retirado), CA-9 y CA-11 no cambian.
> La spec pasa `en-progreso` → `bloqueada` → `borrador` (la pasada "antes" no ha empezado) y
> necesita **nueva aprobación humana**. Lo que el implementador debe rehacer está en el
> ledger (F-SPEC-007-11). Donde el texto de la enmienda (b) contradiga esta, manda esta.

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

**Enmienda (c)**: con ADR-009 el Go ya no se decide en el núcleo sino en tres condiciones:
(C) crecer en `AR`, (D) defender `AV` y (A) ≥ 1 paciente. La pregunta de la calibración pasa
a ser doble y **por nivel**: ¿lo que ve el paciente en `AR` se parece a lo que mide el probe
en `AR`, donde se decide (C) y donde los resultados están repartidos (lo más difícil de
medir)?, y ¿lo que ve en `AV` se parece a lo que mide el probe en `AV`, que respalda la
frase "ya sois la clínica que la IA recomienda en A Mariña" (SPEC-009) y la defensa (D)?
Google AI Overviews se mide ahora **fuera de la comarca** (`AR`) y deja de medirse en el
núcleo. Mismo esfuerzo: 49 consultas por pasada.

## Usuarios / roles afectados
- Humano (fundador): hace las preguntas en ChatGPT, Gemini y Google desde el móvil y
  captura (enmienda (c): `AV` y `AM` solo en ChatGPT y Gemini; `AR` en las tres). [Humano]
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
  **Tercera ampliación: calibración por nivel (enmienda 2026-09-29 (c), ADR-009)**: antes
  de la pasada "antes" (CA-5) consta en el ledger una **tercera ampliación fechada** del
  dictamen de `sdd-metricas` que fija:
  (o) **`AR`: qué se compara y con qué**. Unidad: la casilla pregunta `AR` × asistente
  presente en los dos instrumentos (ChatGPT ↔ `openai`, Gemini ↔ `gemini`): **5 casillas
  por asistente**, 10 en total. Contra qué ejecución `AR` del probe se compara (la del
  "antes" de (C) con el diseño del Go, SPEC-008 CA-12, 3 runs; o las filas `AR` de 1 run del
  baseline oficial, SPEC-008 CA-7), con su ventana máxima en días, y cómo se resume la
  casilla del probe con esos runs. Si las reglas de (k) (lado app, lado probe, resumen de
  runs, diferencias conocidas) se aplican tal cual a `AR` o se matizan; en particular, el
  peso de la diferencia de ubicación (la manual desde Vilaboa, el probe con Viveiro, y las
  preguntas `AR` formuladas desde Ferrolterra, Lugo o Asturias). Y cómo se leen en `AR` las
  clínicas de fuera de la comarca que aparecen en lugar de la clínica (cadenas con varias
  sedes: una marca o una por sede en `alias-canonicos.csv`; se reactiva, solo para la
  lectura manual de `AR`, lo que decía (i)).
  (p) **"Coinciden de forma razonable" en `AR`**: una definición **operativa y verificable**
  con 5 casillas por asistente, que **redefine** la de (l) para este nivel: casillas
  comparables mínimas, umbral de acuerdo "sale / no sale", si se usa o no la diferencia de
  SoV bruto (y con qué tope), si el veredicto es por asistente o sobre las 10 casillas `AR`
  juntas (nunca juntas con `AV`), el tratamiento de la posición, y el ruido esperable con 5
  casillas cuando los resultados están repartidos. Si con 5 casillas ningún umbral permite
  distinguir un acuerdo real de uno por azar, el dictamen lo dice y fija qué puede afirmar
  el veredicto (p. ej. solo "sin discrepancia gruesa") y con qué rótulo; **sin** proponer
  preguntas nuevas (el set está congelado, decisión del humano). Qué implica un "no" en
  `AR`: qué se revisa (orden de (l.4)) y qué no se hace hasta que el humano decida (no se
  enseña a la clínica ninguna cifra `AR` del probe; se revisa la frase del objetivo de
  SPEC-009 antes de enviar la propuesta). Ninguna cifra manual entra en (C) (CA-2 e).
  (q) **`AV` con 2 asistentes**: confirma o ajusta (k) y (l) para el núcleo ahora que `AV`
  solo se pregunta en ChatGPT y Gemini (15 casillas por asistente, 30 en total; sin filas
  Google): la ejecución emparejada sigue siendo el baseline oficial (SPEC-008 CA-7) con su
  ventana; los umbrales de (l.2) siguen o se ajustan; y qué implica un "no" en `AV` (se
  revisa la frase "ya sois la clínica que la IA recomienda en A Mariña" de SPEC-009 antes de
  enviar; no se enseña a la clínica ninguna cifra `AV` del probe). Ninguna cifra manual entra
  en (D).
  (r) **Google AI Overviews en `AR`**: canal aparte (RN-04, D-6), fuera del acuerdo, de los
  dos veredictos y del Go ((C) incluida). Qué se da con **5 búsquedas** y una pasada
  (recuentos "x de 5", sin porcentajes, o menos aún), incluido cuándo no aparece resumen;
  cómo pesa la ubicación Vilaboa en unas búsquedas que nombran Ferrolterra, Lugo o Asturias;
  y cómo se lee el antes/después en SPEC-012 con 5 búsquedas (la regla de "cambio claro" de
  (m.4), ≥ 5 búsquedas de 15, no cabe: el dictamen la sustituye o dice que el antes/después
  de este canal solo se describe).
  (s) **Qué queda del dictamen anterior**: punto por punto, si (k)–(n) siguen, se matizan o
  se sustituyen — en particular (k.1) (solo `AV`), (l) (queda solo para `AV` o se ajusta),
  (m) (queda **sin objeto en `AV`**: ya no hay búsquedas `AV` en Google; su lectura pasa a
  `AR` según (r)) y (n) en lo que tocaba a (g)–(j) (`AR` vuelve a la manual solo como
  calibración; sus indicadores del Go siguen en el probe, SPEC-008 CA-11). **Ninguna regla
  suma, promedia ni pondera casillas, acuerdos o SoV de `AR` y `AV` en una cifra o en un
  veredicto común** (ADR-005 §4, ADR-009 §2).
  Cada condición nueva se mapea a un cambio en protocolo, plantilla, procedimiento o
  herramienta, igual que las anteriores. El dictamen lo emite `sdd-metricas`; este CA no lo
  prejuzga. *Evidencia*: sección de la tercera ampliación con fecha anterior a la pasada
  "antes" y filas (o)–(s) en la tabla condición → cambio.
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
  **Calibración por nivel (enmienda 2026-09-29 (c); sustituye en lo que choque al párrafo
  anterior)**: el protocolo mide `AR01`–`AR05` en ChatGPT, Gemini y Google, `AV01`–`AV15` en
  ChatGPT y Gemini y `AM01`–`AM02` en ChatGPT y Gemini: **49 consultas**. **Orden fijo por
  app y bloque**, igual en las dos pasadas (**`AR` primero**, decisión del humano en el gate
  del 2026-09-29: lo que decide el Go se pregunta con la atención fresca): (1) **ChatGPT**:
  bloque `AR` (5), bloque `AV` (15), bloque `AM` (2) = 22; (2) **Gemini**: `AR` (5), `AV`
  (15), `AM` (2) = 22; (3)
  **Google**: solo `AR` (5). Dentro de cada bloque, en el orden del set. En Google **no** se
  pregunta ninguna `AV` ni `AM`; `AG` no se pregunta en ninguna app. Cada pasada se hace
  dentro de las ventanas del dictamen respecto a **las dos** ejecuciones del probe con que se
  compara (la de `AV` según CA-2 (q) y la de `AR` según CA-2 (o)). Si la pasada se reparte
  en dos días, el corte cae entre apps (nunca dentro de un bloque ni entre bloques de una
  misma app). Tiempo estimado: el mismo que en la enmienda (b) (60–90 min de consultas más
  20–25 min de CSV y capturas). *Evidencia*: el orden de preguntas del protocolo es
  exactamente el de arriba (49 entradas); búsqueda de `AG` y de `AV`/`AM` en el bloque de
  Google, sin coincidencias.
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
  **Enmienda 2026-09-29 (c)**: el CSV tiene una fila por pregunta × app según el orden de
  CA-3: 15 `AV` × (ChatGPT, Gemini) + 5 `AR` × (ChatGPT, Gemini, Google) + 2 `AM` ×
  (ChatGPT, Gemini) = 30 + 15 + 4 = **49 filas**, sin ninguna fila `AV` o `AM` de Google ni
  ninguna `AG`. La pasada queda dentro de la ventana de CA-2 (q) respecto a la ejecución `AV`
  del probe (baseline oficial, SPEC-008 CA-7) **y** de la ventana de CA-2 (o) respecto a la
  ejecución `AR` que fije el dictamen (p. ej. el "antes" de (C), SPEC-008 CA-12). El ledger
  recoge **las dos** ejecuciones emparejadas (fecha y carpeta de cada una). *Evidencia*: el
  verificador cuenta filas por nivel y app (30 / 15 / 4) y comprueba las dos distancias.
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
  **Por nivel (enmienda 2026-09-29 (c); sustituye en lo que choque al párrafo anterior)**:
  el informe tiene una sección **por nivel**, sin mezclarlos (ADR-005 §4, ADR-009 §2):
  (1) **lo que ve el paciente**: por app y **por nivel** (`AV` en ChatGPT y Gemini; `AR` en
  ChatGPT y Gemini): respuestas válidas, SoV bruto de la clínica, posición y clínicas que
  aparecen en su lugar; Google AI Overviews **solo en `AR`**, aparte, según CA-2 (r); los
  dominios más citados (por nivel); y el resultado de las `AM` como hasta ahora;
  (2) **la comparación app frente a probe, una tabla por nivel**:
  - **Tabla `AV`**: casilla `AV` × asistente (ChatGPT, Gemini; 15 × 2) con "sale / no sale"
    y posición en la app y en el probe, acuerdo por asistente y veredicto "**coinciden de
    forma razonable en `AV`: sí / no**" según CA-2 (q), con fecha y carpeta de la ejecución
    `AV` del probe;
  - **Tabla `AR`**: casilla `AR` × asistente (ChatGPT, Gemini; 5 × 2), igual, con el
    veredicto "**coinciden de forma razonable en `AR`: sí / no**" (o el rótulo que fije
    CA-2 (p)) según CA-2 (p), con fecha y carpeta de la ejecución `AR` del probe.
  No hay acuerdo, SoV ni veredicto que sume o combine los dos niveles, ni un veredicto
  "global". **Efecto sobre SPEC-009**: la frase comercial "ya sois la clínica que la IA
  recomienda en A Mariña" se apoya en el veredicto de **`AV`**; la frase del objetivo
  ("aparecer también en el área de influencia…") y cualquier dato de partida en `AR` se
  apoyan en el de **`AR`**. Si el veredicto de un nivel es "no", antes de enviar la
  propuesta y antes de la primera acción consta en el ledger la causa identificada y la
  decisión del humano **para ese nivel** (qué se ajusta, qué frase de SPEC-009 se revisa, o
  seguir con la salvedad escrita); hasta entonces no se enseña a la clínica ninguna cifra
  del probe **de ese nivel**. Un "no" en `AR` no cambia cómo se calcula (C), que es probe
  contra probe (CA-2 e), pero el humano decide con él si sigue con (C) tal cual o con la
  salvedad escrita. *Evidencia*: dos tablas separadas con su veredicto y su ejecución del
  probe; test de que el informe no contiene ninguna cifra ni veredicto que combine `AV` y
  `AR`; si un veredicto es "no", decisión fechada del humano para ese nivel en el ledger,
  anterior a la propuesta y a la primera acción.
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
  **Nota enmienda (c)**: la congelación ya consta (baseline oficial, SPEC-008 CA-7,
  2026-09-29T15:30:43Z). La reorientación de la calibración **no añade ni cambia ninguna
  pregunta**; la reapertura "solo para añadir" que admite ADR-009 §4 no se usa (SPEC-008
  CA-11 eligió la opción A, sin preguntas nuevas).
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
  **Enmienda (c)**: "coinciden de forma razonable" se lee **por nivel**: la hoja usa cifras
  del probe de un nivel solo si CA-7 dice que coinciden en ese nivel. Las 3 respuestas del
  núcleo salen de ChatGPT o Gemini (ya no hay `AV` en Google).
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
- Enmienda (c): **ADR-009** (Go = (C) crecer en `AR`, (D) defender `AV`, (A) ≥ 1 paciente;
  niveles nunca en una misma cifra, §2; aprobado, en la PR #5); SPEC-008 CA-11 (dictamen del
  Go con `AR`) y CA-12 ("antes" de `AR`, 3 runs); SPEC-009 CA-3 (frase comercial y
  objetivo, enmienda (d), en la PR #5).

## Fuera de alcance
- La medición con el probe y el criterio Go: baseline oficial en SPEC-008 CA-7; forma,
  estabilidad y ruido en SPEC-008 CA-9; techo en SPEC-008 CA-10; veredicto en SPEC-012 CA-7.
- ~~`AR` y `AG` en la medición manual: los mide el probe. Consecuencia aceptada: Google AI
  Overviews **no se mide** en `AR` ni en `AG` (el probe no lo cubre).~~ Sustituido por la
  enmienda (c): `AR` vuelve a la manual como **calibración** (no como medición del Go).
- `AG` en la medición manual (ni calibración ni AI Overviews); `AV` y `AM` en Google.
  Consecuencia aceptada (enmienda (c)): Google AI Overviews **deja de medirse en el núcleo**
  (antes y después) y no se mide en `AG`.
- Preguntas nuevas en el set (enmienda (c)): está congelado. Las del noroeste (Asturias,
  León) son de una épica futura de validación del nicho, no de este piloto.
- Usar cifras manuales de `AR` en la condición (C) o de `AV` en la (D) (ADR-009; CA-2 e).
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
- **Enmienda 2026-09-29 (c) — qué cambia para ti**: las mismas **49 consultas**, en otro
  reparto y en este orden: ChatGPT 22 (5 `AR` → 15 `AV` → 2 `AM`), Gemini 22 (igual), Google
  5 (solo `AR`).
  Mismo tiempo. El informe da **dos veredictos separados** ("coinciden en `AV`" y
  "coinciden en `AR`"), nunca uno combinado.
- **Decisiones a mirar con lupa (enmienda (c))**:
  1. **Con 5 casillas por asistente, el veredicto de `AR` es débil.** Es el precio de no
     añadir preguntas. El dictamen (CA-2 p) puede concluir que solo se puede afirmar "sin
     discrepancia gruesa". Si eso no te basta para apoyar la frase del objetivo, la única
     palanca sin tocar el set es más pasadas manuales `AR`, que no están en esta enmienda.
  2. **Se pierde Google AI Overviews en el núcleo**, también en el "después" de SPEC-012:
     no habrá antes/después de AI Overviews en A Mariña. Afecta al diagnóstico de SPEC-011
     (capturas de AI Overviews del núcleo) y al cierre de SPEC-012.
  3. **Dos ejecuciones del probe emparejadas**: `AV` con el baseline oficial (SPEC-008 CA-7)
     y `AR` con la que diga el dictamen (previsiblemente el "antes" de (C), SPEC-008 CA-12,
     3 runs). Las dos son del 2026-09-29: si la ventana sigue siendo de 7 días, la pasada
     tiene que hacerse **como tarde el 2026-10-06** y antes de la primera acción.
  4. **Un "no" en un nivel bloquea solo lo que se apoya en ese nivel**: "no" en `AV` → se
     revisa la frase "ya sois la clínica que la IA recomienda en A Mariña"; "no" en `AR` →
     se revisa la frase del objetivo, y tú decides si (C) sigue tal cual o con salvedad.
  5. **ADR-009 y la enmienda (d) de SPEC-009 aún no están en esta rama** (PR #5). Esta
     enmienda los cita; conviene fusionar la PR #5 antes que la #6.
  6. **Decidido en el gate (humano, Alberto Fojo, 2026-09-29)**: (i) orden **`AR` primero**
     en cada app (CA-3); (ii) si el veredicto de `AR` sale débil ("sin discrepancia
     gruesa", CA-2 p), **basta para contar el objetivo en la propuesta de SPEC-009, sin
     garantía**: el objetivo se cuenta como objetivo, no como dato; (iii) qué ejecución `AR`
     del probe se empareja (CA-12 o filas `AR` de CA-7) lo decide el dictamen (CA-2 o).
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
     añadir 4–9 búsquedas de Google a la manual (sin tocar el Go). *(Superado por la
     enmienda (c): AI Overviews se mide en `AR` y deja de medirse en `AV`.)*
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
