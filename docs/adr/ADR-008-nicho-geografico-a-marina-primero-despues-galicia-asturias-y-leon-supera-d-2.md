---
id: ADR-008
tipo: adr
estado: borrador
historial:
  - {estado: borrador, fecha: 2026-09-29, por: sdd-arquitecto}
---
# ADR-008: Nicho geográfico: A Mariña primero, después Galicia, Asturias y León; supera D-2

- Deciders: el **humano (Alberto Fojo) decidió el cambio de nicho el 2026-09-29**;
  sdd-producto lo recogió en `docs/fundacion/vision.md`, `docs/roadmap.md` y el cierre de
  EPIC-001. Propone este ADR sdd-arquitecto (2026-09-29), que fija **qué parte de D-2 se
  supera, qué queda vigente de ADR-003 y ADR-005 y cómo se aplica al repo**. Aprueba: humano
  (pendiente). Los puntos que no vienen de la decisión del humano y que propone el
  arquitecto van marcados como *(propuesta)*.
- Specs relacionadas: SPEC-002 (alcance reducido), SPEC-003, SPEC-004 y SPEC-005
  (bloqueadas), SPEC-007 a SPEC-012 (EPIC-002, sin cambio de fondo).
- **Supera D-2** (FOUNDATION; origen DECISIONS.md D-002) en su parte geográfica y en el
  orden de especialidades. **Supera en parte ADR-003 y ADR-005**, que siguen `aprobada` y
  vigentes en lo que se enumera en §5 y §6. Registro fundacional: DECISIONS.md D-009.

## Contexto
D-2 (locked) dice: "Nicho primario = clínicas sanitarias privadas, **Vigo y Pontevedra
primero**. Dental = volumen; oftalmología y fertilidad = casos demo; estética = segundo
mercado; fisio solo vía agencias; hospitales en fase 2. Nicho secundario (año 2): educación
privada". FOUNDATION deja fuera "cualquier geografía distinta de Galicia (configurable, pero
no se vende)". Solo un ADR aceptado puede reinterpretar o superar una D-N.

El 2026-09-29 el humano cambia el nicho:
- **Vigo y Pontevedra quedan aparcados**: no se abandonan como mercado futuro, pero no hay
  trabajo activo allí.
- **Nicho nuevo**: clínicas de **sanidad privada en general**, **A Mariña primero**, después
  el resto de **Galicia**, **Asturias** y **León**.
- **EPIC-001** (Ciclo 0 en Vigo) se cierra sin completar; **EPIC-002** (piloto con Clínica
  Ártica, Viveiro) pasa a ser la validación principal.
- Motivo (vision.md): el primer cliente real está en A Mariña y en zonas con poca oferta la
  competencia por aparecer en las respuestas de la IA es menor. Coste asumido: A Mariña es un
  mercado pequeño y el volumen tiene que venir de Galicia, Asturias y León.

ADR-003 y ADR-005 (aprobados) se escribieron con D-2 en vigor: tratan el piloto como
"excepción acotada a D-2", prohíben prospectar en A Mariña, Lugo, Ferrolterra u occidente
de Asturias, dicen que "Asturias no es un mercado" y fijan una caducidad. Con el nicho nuevo
esas prohibiciones contradicen la estrategia. Otras partes (lotes separados, niveles que no
se mezclan, Go solo con `AV`) no dependen del nicho y siguen teniendo sentido.

D-2 además está **cableada** en el probe: el lote por defecto (`probe/probe_config.json`) es
Vigo/Pontevedra y SPEC-008 CA-4 exige que no cambie. El lote de Viveiro ya es configuración
(`probe/batches/viveiro.json`, ADR-003 §4).

## Decisión
1. **Geografía del nicho.** El nicho primario pasa a ser clínicas sanitarias privadas del
   noroeste: **A Mariña primero**; después el **resto de Galicia**, **Asturias** (todo el
   Principado) y la **provincia de León**. Entre estas tres no se fija orden en este ADR: lo
   decide sdd-producto en la épica de validación del nicho nuevo, con datos *(propuesta)*.
   "Primero" se lee como **orden de trabajo comercial y de medición** (dónde se buscan
   clientes, se construyen catálogos y se mide primero), no como prohibición de atender a un
   cliente de otra zona del nicho que llegue solo.
2. **Vigo y Pontevedra, aparcados.** Siguen dentro de la geografía del producto (son
   Galicia), pero **sin trabajo activo**: no se prospecta allí, no se ejecuta el lote de Vigo
   y no se amplían sus catálogos. El lote de Vigo del probe se conserva como configuración
   por defecto, sin tocar (SPEC-008 CA-4 sigue vigente), para poder retomarlo sin coste.
   **Retomarlos** es decisión del humano que sdd-producto registra en el roadmap (ya prevé
   el criterio de corte "sin vía creíble hacia unas 10 clínicas de pago, reevaluar Vigo");
   no hace falta otro ADR, porque la geografía de §1 ya los incluye *(propuesta)*.
3. **Especialidades: sanidad privada en general.** El orden de especialidades de D-2
   (dental = volumen, oftalmología y fertilidad = demo, estética = segundo mercado) **deja de
   ser vinculante**: salía del mapa de oferta de Vigo (`02-icp-and-niche.md`,
   `03-local-market-vigo-pontevedra.md`) y no se ha medido en el nicho nuevo. El orden por
   zona lo fija sdd-producto con datos. Se **mantienen** de D-2, porque no dependen de la
   geografía y el humano no los ha cambiado *(propuesta, a confirmar en el gate)*:
   hospitales en fase 2; fisioterapia solo vía agencias; nicho secundario de educación
   privada en el año 2; y la consecuencia "los catálogos de prompts, fuentes y listas de
   marcas se construyen por especialidad × ciudad" (hoy, por lote).
4. **Alcance de FOUNDATION.** "Fuera" pasa a decir: cualquier geografía distinta de
   **Galicia, Asturias y la provincia de León** (configurable, pero no se vende). D-1
   (vertical + geográfico, sin generalizar) no cambia.
5. **ADR-003: qué se deroga y qué sigue vigente.**
   - **Derogado**: el encuadre del piloto como "excepción acotada a D-2"; §2 (prohibición de
     prospectar en A Mariña o Lugo, de listas de objetivos con clínicas de Lugo, de un
     segundo cliente fuera de Vigo/Pontevedra y de mensajes de mercado de Lugo); §6
     (caducidad de la excepción). El piloto ya no es una excepción: es el primer cliente del
     nicho.
   - **Vigente**: §1 (un piloto de Clínica Ártica con catálogo y competidores propios,
     ampliado por ADR-005 §1); §3 (el lote de Viveiro es un lote aparte, con configuración y
     salida propias, y sus agregados no se mezclan con los de ningún otro lote); §4
     (multi-ciudad por configuración, con el lote de Vigo como defecto). §5 se **reinterpreta**:
     el aprendizaje sobre H1 y H3 es transferible al resto del nicho; el de mercado (fuentes
     dominantes, competidores, volumen) es **propio de Viveiro / A Mariña** y no se
     extrapola al resto de Galicia, a Asturias ni a León sin medirlo allí.
6. **ADR-005: qué se deroga y qué sigue vigente.**
   - **Derogado**: §2 en cuanto extiende las prohibiciones de ADR-003 §2 a Ferrolterra,
     occidente de Asturias y resto de Galicia; §3 ("Asturias no es un mercado"); en §5, la
     justificación "no alimentan el nicho de D-2".
   - **Vigente**: §1 (catálogo en tres niveles `AV`, `AR`, `AG`); §4 (cada nivel se cuenta e
     informa por separado; **el criterio Go se calcula solo con `AV`**; ninguna cifra `AR`
     o `AG` se suma, promedia ni pondera con el núcleo); §5 en su parte técnica (las marcas
     del piloto con sede en Vigo o Pontevedra se registran en el lote del piloto y **no
     alteran el lote de Vigo**, SPEC-008 CA-4); §6 (el nivel Galicia no se promete a la
     clínica).
7. **Datos del piloto y prospección** *(propuesta; sustituye a las prohibiciones derogadas
   con una regla más estrecha)*. Prospectar en A Mariña y en el resto del nicho está
   permitido, pero **dentro de la épica de validación del nicho nuevo** y con sus propias
   mediciones. Las respuestas medidas **para** Clínica Ártica (lote de Viveiro y pasadas
   manuales de SPEC-007) no se usan como lista de objetivos ni como "hallazgo" de apertura
   con competidoras suyas mientras dure el piloto: son datos del servicio a un cliente
   (ADR-004), no un estudio de mercado. Si se quiere contactar competidoras directas de
   Ártica en A Mariña, lo decide el humano (es una cuestión comercial y de confianza con el
   cliente, no técnica).
8. **Normativa fuera de Galicia.** Antes de publicar material de cliente o de contactar en
   frío a clínicas de Asturias o León, `sdd-sanidad-regulacion` emite dictamen sobre la
   normativa de publicidad sanitaria de esas comunidades (su dominio hoy es "España y
   Galicia"). Medir preguntas que nombran esas zonas no lo necesita.

## Consecuencias
### Positivas
- La estrategia escrita coincide con la decisión del humano: FOUNDATION deja de contradecir
  a vision.md y al roadmap, y EPIC-002 deja de depender de una excepción con caducidad.
- Lo técnico que protegía la medición (lotes separados, niveles sin mezclar, Go solo con
  `AV`, lote de Vigo intacto) sigue siendo comprobable por el verificador con los mismos
  tests de SPEC-008.
- El trabajo del probe no se pierde: el lote de Vigo queda aparcado como configuración y el
  de Viveiro sigue igual.

### Negativas / follow-ups
- Mercado pequeño en A Mariña: el volumen depende de Galicia, Asturias y León, donde no hay
  ningún dato. La épica de validación del nicho nuevo (sdd-producto) tiene que medirlo
  antes de prometer métricas norte.
- Los documentos fundacionales en inglés (`README.md` "Ground rules for agents" 2, `02-…`, `03-…`)
  siguen describiendo Vigo/Pontevedra. No se reescriben: son la historia del porqué;
  DECISIONS.md D-009 remite a este ADR. Follow-up para sdd-producto: una línea en
  `README.md` que remita a D-009, para que ningún agente lea el nicho viejo como vigente.
- EPIC-001 queda cerrada sin veredicto de la hipótesis de Vigo: SPEC-002 se reduce a lo ya
  hecho (claves, modelos, humo) y SPEC-003, SPEC-004 y SPEC-005 quedan `bloqueada`, con lo
  rescatable anotado en cada una.
- `sdd-sanidad-regulacion` necesita ampliar su dominio a Asturias y Castilla y León (§8).
- El lote de Vigo por defecto en `probe_config.json` sigue siendo Vigo: cuando el nicho
  nuevo tenga su propio lote de validación, se decidirá (otra spec) si el defecto cambia.

## Alternativas consideradas
- **Seguir con el piloto como excepción (ADR-003) y no tocar D-2**: rechazada. El humano ha
  cambiado el nicho; mantener D-2 dejaría FOUNDATION, vision.md y roadmap contradiciéndose y
  prohibiría justo la prospección que ahora toca.
- **Superseder ADR-003 y ADR-005 enteros y reescribir sus partes técnicas aquí**: rechazada.
  Las partes técnicas están aprobadas, implementadas y probadas (SPEC-008); reescribirlas
  obligaría a revalidarlas sin que cambien. Se derogan solo las partes que dependen del
  nicho, con el mismo patrón de "amplía / supera en parte" que ADR-004 y ADR-007.
- **Abandonar Vigo y Pontevedra (fuera de alcance)**: rechazada; el humano los aparca, no
  los descarta, y el roadmap prevé volver si el nicho nuevo no da volumen.
- **Fijar ya el orden Galicia → Asturias → León**: rechazada; el humano no ha dado orden
  entre ellas y no hay datos. Lo decide sdd-producto con la épica de validación.
- **Mantener el orden de especialidades de D-2**: rechazada; venía del mapa de oferta de
  Vigo y el humano ha dicho "sanidad privada en general".

<!-- REGLA: un ADR aceptado es INMUTABLE. Para cambiar la decisión, escribe otro ADR que lo supersede (estado del viejo -> bloqueada + nota "superseded por ADR-NNN"). -->
