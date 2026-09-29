---
id: SPEC-012
tipo: spec
epica: EPIC-002
estado: borrador
aprobada-por:
historial:
  - {estado: borrador, fecha: 2026-09-28, por: sdd-arquitecto}
---
# SPEC-012 — Ejecución, medición semanal y cierre del piloto

> **Nota 2026-09-29 (e) (sdd-arquitecto) — follow-ups del cierre de SPEC-008.** Recogidos
> F-SPEC-008-14 (forma de los comandos de medición, palancas de coste del mes de cierre y
> re-comprobación real de `sdd-probe` antes de cada medición "después"), F-SPEC-008-16 (el
> comando simple del lote, sin `--levels`, no se lanza en el piloto) en CA-3, y
> F-SPEC-008-10 (comando que lee los `results.csv` y escribe el veredicto con las funciones
> de `probe/analysis.py`) en CA-7. Concretan cómo se mide; el fondo no cambia. La spec sigue
> en `borrador`.

> **Nota 2026-09-29 (d) (sdd-arquitecto) — decisiones del humano sobre `AR` y coste.**
> ADR-009 aprobado. El humano (Alberto Fojo, 2026-09-29) eligió la **opción A** para `AR`
> (más runs, las mismas 5 preguntas; SPEC-008 CA-12) y fijó la **regla de recorte**: si el
> mes de cierre supera 20 €, lo primero que se recorta es `AG`, que pasa a medirse cada 8
> semanas. Recogido en CA-3 y en las notas; el fondo del resto no cambia. La spec sigue en
> `borrador`.

> **Nota 2026-09-29 (c) (sdd-arquitecto) — Go "crecer fuera, defender dentro" (ADR-009,
> borrador).** Tras el aviso de techo del baseline oficial (SPEC-008 CA-10), el humano
> decidió antes de la primera acción que el Go del piloto son tres condiciones sí/no:
> **crecer** en el área de influencia `AR` (H1), **defender** el núcleo `AV` (no cae de forma
> significativa frente al baseline oficial) y ≥ 1 paciente atribuido (H3), sin mezclar
> niveles en una cifra (EPIC-002, criterio 4). Ajustados CA-3 (cadencia de `AR`: la que fije
> SPEC-008 CA-11, ya no "cada 4 semanas" fijo), CA-7 (regla del cierre), CA-5 (el informe
> ya no trata `AR` como secundario), entidades y notas. La spec sigue en `borrador`.

> **Nota 2026-09-29 (b) (sdd-arquitecto) — nuevo instrumento del Go.** Por decisión del
> humano (EPIC-002, criterios 1 y 4) el probe es el instrumento de medición y del criterio
> Go; la manual es una calibración de `AV` en ChatGPT, Gemini y Google, una "antes"
> (SPEC-007) y una "después" (aquí). Ajustados CA-3, CA-5, CA-7, entidades, Fuera de alcance
> y notas; recogidos F-SPEC-007-5 (estabilidad en las dos mediciones "después"), F-SPEC-007-7
> (niveles) y F-SPEC-008-5 (cadencia). La spec sigue en `borrador`.

> **Nota 2026-09-29 (sdd-arquitecto) — cambio de nicho (ADR-008).** Ajustadas tres
> referencias (transferibilidad al resto del nicho, ADR citados, segundo cliente) sin cambiar
> el fondo; la spec sigue en `borrador`.

> Spec **operativa y deliberadamente menos detallada**: las acciones concretas salen de
> SPEC-011, que aún no existe. La cadencia del probe (SPEC-008 CA-5, aceptada por el humano)
> y la forma del Go con el probe (SPEC-008 CA-9) ya están fijadas o pedidas. Aquí se fija lo
> que no depende de SPEC-011: el registro, la puerta de publicación, la medición, los
> informes y la regla del cierre. **No debería aprobarse antes que SPEC-011**; el
> arquitecto la completará entonces.

## Problema
Criterios de éxito 4, 5 y 6 de EPIC-002. El valor del piloto es el **registro de acciones →
efecto** (`05-lean-plan.md` §2: "ese registro es el producto futuro") y un veredicto
honesto sobre H1 y H3, incluido decir "no ha funcionado" a un cliente de confianza.

## Usuarios / roles afectados
- Humano / Tremendev: ejecuta acciones, mide, informa, cierra. [Humano]
- Clínica: aporta contenidos, aprueba, avisa de cambios, entrega conteos.
- Agente (sdd-implementador): plantillas, recuentos, borradores de informe. [Agente]
- Consultadas: `sdd-sanidad-regulacion` (condiciones de SPEC-011 CA-7, por pieza),
  `sdd-metricas` (regla del cierre).
- sdd-verificador. [Verificador]

## Criterios de aceptación
- **CA-1 (registro de acciones → efecto) [Humano rellena; Agente plantilla]**: Dado el plan
  de SPEC-011, cuando se ejecute cada acción, entonces el registro
  (`docs/piloto-artica/registro-acciones.md` en el repo: id, fecha, qué, URL, palanca, sin
  cifras; y su parte privada con el efecto) tiene su fecha de publicación y, cada semana,
  una nota por acción activa "movió / no movió / no se sabe" alguna respuesta en algún
  asistente, con referencia a la evidencia privada. *Evidencia*: registro sin huecos
  semanales desde la primera acción.
- **CA-2 (puerta de publicación) [Verificador]**: Dado SPEC-011 CA-7, cuando se publique
  cualquier pieza de contenido, entonces antes de su fecha de publicación constan en el
  ledger: la comprobación de la pieza contra las condiciones del dictamen normativo y la
  aprobación escrita de la clínica. *Evidencia*: para cada acción publicada, fechas de
  comprobación y aprobación ≤ fecha de publicación.
- **CA-3 (medición) [Humano lanza y mide; Agente recuenta]**: Dado el baseline oficial del
  probe (SPEC-008 CA-7) y el dictamen de SPEC-008 CA-9, cuando avance el piloto, entonces:
  (1) **probe, instrumento del Go**: el núcleo `AV` se ejecuta **cada semana con 1 run**
  (tendencia y registro acción → efecto, no Go); `AR` se mide **con la cadencia, las
  preguntas y los runs que fije SPEC-008 CA-11** para la condición de crecimiento (el
  "cada 4 semanas con 1 run" anterior deja de valer para `AR` si CA-11 pide otra cosa; como
  mínimo, las mediciones "después" que CA-11 exija, con la forma del "antes" de SPEC-008
  CA-12); por decisión del humano (2026-09-29) `AR` usa la **opción A** de SPEC-008 CA-12:
  **las mismas 5 preguntas `AR` congeladas, con más runs** (los que fije CA-11), sin
  ampliar el set; `AG` **cada 4 semanas con 1 run** (sin objetivo), con la **regla de
  recorte**: si el coste previsto del mes de cierre (SPEC-008 CA-5 (d)) supera 20 €, lo
  **primero** que se recorta es `AG`, que pasa a **cada 8 semanas con 1 run** en todo el
  piloto (decidido antes de la primera acción y anotado en el ledger); solo si con eso
  aún no cabe se aplica la palanca que proponga `sdd-probe`, nunca bajando runs del Go; todo con la configuración del
  lote de Viveiro sin cambios respecto al baseline salvo lo que CA-11 cambie antes de la
  primera acción; (2) **mediciones "después" del Go**: las de `AR` (crecimiento) y las del
  núcleo (defensa) con la forma, las semanas y la separación que fije SPEC-008 CA-11 (para
  el núcleo, por defecto las dos de SPEC-008 CA-9 (c): semanas 11 y 12 ± 1, ≥ 7 días), cada
  una en lugar de la ejecución periódica de su nivel en esa semana; (3) **calibración manual "después"**: una
  pasada con el protocolo de SPEC-007 (15 `AV` en ChatGPT, Gemini y Google + 2 `AM` en
  ChatGPT y Gemini; mismas condiciones que la "antes"), dentro de la ventana de SPEC-007
  CA-2 (k) respecto a una de las dos mediciones "después"; es la **única** medición de Google
  AI Overviews del cierre; (4) cada medición guarda sus datos en el espacio privado con
  fecha, y cualquier cambio de modelo por defecto de un proveedor se anota con fecha
  (SPEC-008 CA-9 f); (5) **forma de los comandos** (F-SPEC-008-14 y F-SPEC-008-16; README
  del probe, "Batches"): cada medición "después" del Go se lanza con
  `--levels AV,AR --runs 3`, en las semanas 11 y 12 ± 1 con ≥ 7 días entre ellas; en la
  semana 12 sustituye también al `AR` de 1 run, y `AG`, si toca, va aparte con
  `--levels AG --runs 1`; toda ejecución de seguimiento (`AV` semanal, `AR`/`AG` de 1 run)
  lleva `--levels` y `--runs 1` explícitos, porque sin `--runs` el lote lanza `AR` con los
  3 runs del diseño; el comando simple del lote, **sin `--levels`**, no se lanza en el
  piloto (ya no es la forma del baseline oficial); (6) **mes del cierre**: al planificarlo,
  antes de la primera medición "después", se decide y anota en el ledger qué palancas de
  coste 1–4 de SPEC-008 CA-5 (enmienda (d), en su orden fijo; la 1 es el recorte de `AG`)
  se aplican, con el `c` medido entonces; nunca bajan los runs ni el número de mediciones
  del Go, y si ni con las cuatro cabe, se vuelve a `sdd-probe` y al humano; (7)
  **re-comprobación de `sdd-probe` antes de cada medición "después"**: `sdd-probe` hace una
  comprobación real del modelo por defecto y de los precios de cada app (SPEC-008 CA-9 (f)
  y CA-11 (iv)), y su dictamen fechado consta en el ledger antes del lanzamiento; la tabla
  "Modelos servidos" del `summary.md` no la sustituye, porque el probe pide un id fijo.
  *Evidencia*: fechas y ficheros de cada ejecución y de la pasada; semanas sin hueco en
  `AV`; runs por ejecución; comando exacto de cada ejecución en el ledger, con `--levels` y
  `--runs`; ejecuciones `AR` con las 5 preguntas del set congelado; cadencia de `AG` (4 u 8
  semanas) coherente con la decisión de recorte anotada en el ledger; palancas del mes de
  cierre anotadas antes de la primera medición "después"; dictamen de `sdd-probe` con fecha
  anterior a cada medición "después"; desviaciones anotadas.
- **CA-4 (atribución semanal) [Humano]**: Dado SPEC-010 CA-6, cuando pase cada semana,
  entonces la hoja privada de AttributionEvent tiene las tres señales de esa semana (o la
  causa de su ausencia). *Evidencia*: semanas sin hueco.
- **CA-5 (informe cada 15 días) [Agente redacta; Humano envía]**: Dado que la clínica tiene
  que ver el avance, cuando pasen 15 días (± 2), entonces se envía un informe de 1–2
  páginas en castellano, sin la jerga de SPEC-009 CA-10, con qué se hizo, qué cambió en
  las respuestas, qué señales de pacientes hay y qué sigue; incluye la pregunta "¿ha
  cambiado algo por vuestra parte (web, campañas, agencia)?". Lo que cambió en las
  respuestas sale de las ejecuciones semanales del probe, informado por nivel (`AV`, `AR` y
  `AG` cada uno aparte, ADR-005 §4 y ADR-009 §2; `AG` sin objetivo, ADR-005 §6), y se enseñan cifras del probe solo si la calibración
  "antes" dijo que coinciden de forma razonable con la app (SPEC-007 CA-7) o el humano
  decidió seguir con la salvedad escrita. *Evidencia*: fechas de envío en el ledger;
  plantilla en `docs/piloto-artica/informe-quincenal.md`.
- **CA-6 (contaminación y tiempo) [Humano]**: Dado el riesgo de cambios en paralelo y el de
  tiempo del fundador, cuando pase cada semana, entonces se anotan los cambios de terceros
  conocidos (fecha, qué) y las horas dedicadas por el fundador. *Evidencia*: registro
  semanal.
- **CA-7 (veredicto de cierre) [Agente; consulta sdd-metricas; Humano valida]**: Dado la
  semana 12 (± 1) desde la primera acción, cuando se cierre, entonces el veredicto (ADR-009;
  EPIC-002, criterio 4) da tres sí/no por separado y el Go = los tres en sí:
  **(C) crecer** = la cifra de `AR` del **probe** frente a su "antes" (SPEC-008 CA-12) cumple
  el umbral y la regla de estabilidad de SPEC-008 CA-11 (ii); es **H1**;
  **(D) defender** = el SoV ponderado del núcleo `AV` del probe no cae por debajo del umbral
  de SPEC-008 CA-11 (iii) frente al baseline oficial (SPEC-008 CA-7), en las mediciones que
  fije ese dictamen;
  **(A) atribución** = H3 (abajo).
  Reglas fijadas antes de la primera acción; siempre probe contra probe y con la misma
  configuración (SPEC-007 CA-2 e): ninguna cifra manual entra en (C) ni en (D). Ninguna cifra
  combina niveles (ADR-009 §2); `AG` se informa aparte con los indicadores de SPEC-008 CA-9
  (g) y nunca entra en el Go (ADR-005 §6). Google AI Overviews se informa como
  canal aparte, antes frente a después de la calibración manual (SPEC-007 CA-2 m), sin
  entrar en H1. El cierre recoge además el resultado de la calibración "después" (app frente
  a probe, con la regla de SPEC-007 CA-2 l); si no coinciden, se dice en el cierre como
  salvedad del veredicto. H3 = ≥ 1 AttributionEvent en cualquier señal durante el piloto
  (RN-07). Se publica en `docs/piloto-artica/cierre.md` como cumple / no cumple sin
  cifras (ADR-004 §3), con: que un piloto no es el Go del Ciclo 2 ("2 de 3 pilotos"); qué
  se considera transferible al resto del nicho (Galicia, Asturias, León) y qué no (ADR-003 §5 reinterpretado por ADR-008 §5); las horas del
  fundador. Las cifras van al informe privado de cierre a la clínica. **Comando del
  veredicto [Agente implementa; Humano lanza]** (F-SPEC-008-10): un comando lee los
  `results.csv` privados del baseline oficial, del "antes" de `AR` y de las mediciones
  "después", pasa cada uno por `analysis.analyze` y calcula (C) y (D) **solo** con las
  funciones ya existentes de `probe/analysis.py` (`growth_verdict`, `defense_verdict`,
  `render_go_verdict`), sin reimplementar la regla ni sus umbrales (los de
  `probe/batches/viveiro.json`); añade (A) desde la hoja privada de AttributionEvent
  (CA-4); y escribe el veredicto (C)/(D)/(A) en el espacio privado, nunca en el repo
  (ADR-004 §2). *Evidencia*: el verificador recalcula desde los `results.csv` privados del
  baseline, del "antes" de `AR` y de las mediciones "después", y desde el CSV de la
  calibración; un test con `results.csv` sintéticos comprueba que el comando da el mismo
  (C) y (D) que llamar a esas funciones directamente y que no escribe nada dentro del repo.
- **CA-8 (continuidad) [Humano]**: Dado el cierre, cuando se entregue el informe final,
  entonces se envía una propuesta de continuidad y el ledger registra la respuesta
  (renueva / suscripción / no renueva) con fecha. Si la clínica continúa, la propuesta dice
  cómo se mide: probe con la cadencia de CA-3 y calibración manual **trimestral** si la del
  cierre coincidió de forma razonable, o el ajuste previsto si no (EPIC-002, criterio 1).
  *Evidencia*: fecha y respuesta.

## Entidades y reglas afectadas
- Dominio: Action, AttributionEvent, Weighted SoV, Share of voice, Position.
- RN-02–RN-04, RN-07, RN-09. D-3, D-4, D-6. ADR-003, ADR-004, ADR-005, ADR-008, ADR-009.
- Depende de SPEC-007 (calibración "antes" y protocolo), SPEC-008 (baseline oficial,
  CA-7; forma del Go, CA-9; techo y decisión, CA-10; Go con `AR`, CA-11; "antes" de `AR`,
  CA-12) — y por tanto de SPEC-013 —, SPEC-009, SPEC-010 y SPEC-011. ADR-009 (Go = crecer
  en `AR` + defender `AV` + atribución; supera en parte ADR-005 §4).

## Fuera de alcance
- Automatizar el informe o la medición en las apps de consumo (Ciclo 3; automatizar las
  apps no es legal ni repetible). La ejecución del probe ya es automática; lanzarla con un
  programador de tareas queda fuera.
- Pasadas manuales intermedias (semanas 4 y 8): desaparecen; la manual es solo la
  calibración "antes" (SPEC-007) y "después" (CA-3 (3)).
- Un segundo cliente piloto: no entra en esta épica; la prospección del nicho nuevo va en su propia épica (ADR-008; ~~ADR-003 §2~~, derogado).

## Notas para el gate humano
- **Pendiente de detalle** hasta SPEC-011: lista de acciones. La cadencia del probe ya
  está (SPEC-008 CA-5) y la forma del Go la fija el dictamen de SPEC-008 CA-9.
- **Mirar con lupa**: (1) tu tiempo de medición en todo el piloto queda en **una** pasada
  manual al cierre (49 consultas, 60–90 min); el resto lo hace el probe. (2) ~~El Go exige
  la subida en **cada** una de las dos mediciones "después" (tu decisión P-3)~~ —
  **sustituido (nota (c), ADR-009)**: la subida se exige en `AR` y el núcleo solo se
  defiende; si la regla de P-3 ("en cada una, no en la media") se mantiene para `AR` lo
  fija SPEC-008 CA-11 (ii). (4) La cadencia de `AR` deja de ser "cada 4 semanas" fija:
  será la que pida el Go (SPEC-008 CA-11), probablemente mediciones de varios runs al
  final; el coste del mes de cierre lo recalcula SPEC-008 CA-5. **Decidido (nota (d))**:
  opción A (mismas 5 preguntas `AR`, más runs) y, si el mes de cierre supera 20 €, `AG`
  pasa a cada 8 semanas antes que tocar nada más. (3) Si la calibración "después" no
  coincide con el probe, el veredicto se da igual con el probe, pero con la salvedad escrita
  en el cierre.
