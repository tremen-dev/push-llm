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
  (1) **probe, instrumento del Go**: el núcleo `AV` se ejecuta **cada semana con 1 run** y
  `AR` + `AG` **cada 4 semanas con 1 run** (cadencia de SPEC-008 CA-5, F-SPEC-008-5), con la
  configuración del lote de Viveiro sin cambios respecto al baseline; (2) **dos mediciones
  "después"** del núcleo con la forma del baseline (mismos runs), en **semanas distintas**
  según SPEC-008 CA-9 (propuesta: semanas 11 y 12 ± 1, con ≥ 7 días entre ellas), cada una
  en lugar de la ejecución semanal de su semana; (3) **calibración manual "después"**: una
  pasada con el protocolo de SPEC-007 (15 `AV` en ChatGPT, Gemini y Google + 2 `AM` en
  ChatGPT y Gemini; mismas condiciones que la "antes"), dentro de la ventana de SPEC-007
  CA-2 (k) respecto a una de las dos mediciones "después"; es la **única** medición de Google
  AI Overviews del cierre; (4) cada medición guarda sus datos en el espacio privado con
  fecha, y cualquier cambio de modelo por defecto de un proveedor se anota con fecha
  (SPEC-008 CA-9 f). *Evidencia*: fechas y ficheros de cada ejecución y de la pasada;
  semanas sin hueco en `AV`; runs por ejecución; desviaciones anotadas.
- **CA-4 (atribución semanal) [Humano]**: Dado SPEC-010 CA-6, cuando pase cada semana,
  entonces la hoja privada de AttributionEvent tiene las tres señales de esa semana (o la
  causa de su ausencia). *Evidencia*: semanas sin hueco.
- **CA-5 (informe cada 15 días) [Agente redacta; Humano envía]**: Dado que la clínica tiene
  que ver el avance, cuando pasen 15 días (± 2), entonces se envía un informe de 1–2
  páginas en castellano, sin la jerga de SPEC-009 CA-10, con qué se hizo, qué cambió en
  las respuestas, qué señales de pacientes hay y qué sigue; incluye la pregunta "¿ha
  cambiado algo por vuestra parte (web, campañas, agencia)?". Lo que cambió en las
  respuestas sale de las ejecuciones semanales del probe, informado por nivel (`AR` y `AG`
  aparte del núcleo, ADR-005 §4 y §6), y se enseñan cifras del probe solo si la calibración
  "antes" dijo que coinciden de forma razonable con la app (SPEC-007 CA-7) o el humano
  decidió seguir con la salvedad escrita. *Evidencia*: fechas de envío en el ledger;
  plantilla en `docs/piloto-artica/informe-quincenal.md`.
- **CA-6 (contaminación y tiempo) [Humano]**: Dado el riesgo de cambios en paralelo y el de
  tiempo del fundador, cuando pase cada semana, entonces se anotan los cambios de terceros
  conocidos (fecha, qué) y las horas dedicadas por el fundador. *Evidencia*: registro
  semanal.
- **CA-7 (veredicto de cierre) [Agente; consulta sdd-metricas; Humano valida]**: Dado la
  semana 12 (± 1) desde la primera acción, cuando se cierre, entonces el veredicto: H1 =
  Δ SoV ponderado del núcleo `AV` del **probe** frente al baseline oficial (SPEC-008 CA-7)
  ≥ +15 pts **en cada una de las dos mediciones "después"** (CA-3 (2); F-SPEC-007-5), o la
  regla de estabilidad y el criterio que fijen SPEC-008 CA-9 y CA-10, decididos antes de la
  primera acción; siempre probe contra probe y con la misma configuración (SPEC-007 CA-2 e):
  ninguna cifra manual entra en H1. `AR` y `AG` se informan aparte con los indicadores de
  SPEC-008 CA-9 (g) y nunca entran en H1 (ADR-005 §4). Google AI Overviews se informa como
  canal aparte, antes frente a después de la calibración manual (SPEC-007 CA-2 m), sin
  entrar en H1. El cierre recoge además el resultado de la calibración "después" (app frente
  a probe, con la regla de SPEC-007 CA-2 l); si no coinciden, se dice en el cierre como
  salvedad del veredicto. H3 = ≥ 1 AttributionEvent en cualquier señal durante el piloto
  (RN-07). Se publica en `docs/piloto-artica/cierre.md` como cumple / no cumple sin
  cifras (ADR-004 §3), con: que un piloto no es el Go del Ciclo 2 ("2 de 3 pilotos"); qué
  se considera transferible al resto del nicho (Galicia, Asturias, León) y qué no (ADR-003 §5 reinterpretado por ADR-008 §5); las horas del
  fundador. Las cifras van al informe privado de cierre a la clínica. *Evidencia*: el
  verificador recalcula desde los `results.csv` privados del baseline y de las dos
  mediciones "después", y desde el CSV de la calibración.
- **CA-8 (continuidad) [Humano]**: Dado el cierre, cuando se entregue el informe final,
  entonces se envía una propuesta de continuidad y el ledger registra la respuesta
  (renueva / suscripción / no renueva) con fecha. Si la clínica continúa, la propuesta dice
  cómo se mide: probe con la cadencia de CA-3 y calibración manual **trimestral** si la del
  cierre coincidió de forma razonable, o el ajuste previsto si no (EPIC-002, criterio 1).
  *Evidencia*: fecha y respuesta.

## Entidades y reglas afectadas
- Dominio: Action, AttributionEvent, Weighted SoV, Share of voice, Position.
- RN-02–RN-04, RN-07, RN-09. D-3, D-4, D-6. ADR-003, ADR-004, ADR-005, ADR-008.
- Depende de SPEC-007 (calibración "antes" y protocolo), SPEC-008 (baseline oficial,
  CA-7; forma del Go, CA-9; techo, CA-10) — y por tanto de SPEC-013 —, SPEC-009, SPEC-010
  y SPEC-011. ADR-005 §4 (Go solo con el núcleo).

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
  manual al cierre (49 consultas, 60–90 min); el resto lo hace el probe. (2) El Go exige
  la subida en **cada** una de las dos mediciones "después" (tu decisión P-3): más
  exigente que la media, menos expuesto al ruido. (3) Si la calibración "después" no
  coincide con el probe, el veredicto se da igual con el probe, pero con la salvedad escrita
  en el cierre.
