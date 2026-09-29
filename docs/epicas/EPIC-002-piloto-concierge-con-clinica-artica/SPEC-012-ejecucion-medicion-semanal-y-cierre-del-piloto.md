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

> **Nota 2026-09-29 (sdd-arquitecto) — cambio de nicho (ADR-008).** Ajustadas tres
> referencias (transferibilidad al resto del nicho, ADR citados, segundo cliente) sin cambiar
> el fondo; la spec sigue en `borrador`.

> Spec **operativa y deliberadamente menos detallada**: las acciones concretas salen de
> SPEC-011 y la cadencia del probe de SPEC-008 CA-5, que aún no existen. Aquí se fija lo
> que no depende de ellas: el registro, la puerta de publicación, la medición, los
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
- **CA-3 (medición) [Humano mide; Agente recuenta]**: Dado SPEC-007 y SPEC-008, cuando
  avance el piloto, entonces: el set `AV` congelado se mide **a mano con el protocolo de
  SPEC-007** al menos en las semanas 4, 8 y 12 (± 1) desde la primera acción, y con el
  probe en la cadencia de SPEC-008 CA-5 si hay claves; Google AI Overviews, siempre a mano.
  Cada medición guarda sus datos en el espacio privado con fecha. *Evidencia*: fechas y
  ficheros; desviaciones de protocolo anotadas.
- **CA-4 (atribución semanal) [Humano]**: Dado SPEC-010 CA-6, cuando pase cada semana,
  entonces la hoja privada de AttributionEvent tiene las tres señales de esa semana (o la
  causa de su ausencia). *Evidencia*: semanas sin hueco.
- **CA-5 (informe cada 15 días) [Agente redacta; Humano envía]**: Dado que la clínica tiene
  que ver el avance, cuando pasen 15 días (± 2), entonces se envía un informe de 1–2
  páginas en castellano, sin la jerga de SPEC-009 CA-10, con qué se hizo, qué cambió en
  las respuestas, qué señales de pacientes hay y qué sigue; incluye la pregunta "¿ha
  cambiado algo por vuestra parte (web, campañas, agencia)?". *Evidencia*: fechas de envío
  en el ledger; plantilla en `docs/piloto-artica/informe-quincenal.md`.
- **CA-6 (contaminación y tiempo) [Humano]**: Dado el riesgo de cambios en paralelo y el de
  tiempo del fundador, cuando pase cada semana, entonces se anotan los cambios de terceros
  conocidos (fecha, qué) y las horas dedicadas por el fundador. *Evidencia*: registro
  semanal.
- **CA-7 (veredicto de cierre) [Agente; consulta sdd-metricas; Humano valida]**: Dado la
  semana 12 (± 1) desde la primera acción, cuando se cierre, entonces el veredicto: H1 =
  Δ SoV ponderado sobre el set congelado ≥ +15 pts (o el criterio decidido en SPEC-007
  CA-8), **con el mismo instrumento** que el baseline (manual contra manual; probe contra
  probe si hubo baseline de probe); H3 = ≥ 1 AttributionEvent en cualquier señal durante el
  piloto (RN-07). Se publica en `docs/piloto-artica/cierre.md` como cumple / no cumple sin
  cifras (ADR-004 §3), con: que un piloto no es el Go del Ciclo 2 ("2 de 3 pilotos"); qué
  se considera transferible al resto del nicho (Galicia, Asturias, León) y qué no (ADR-003 §5 reinterpretado por ADR-008 §5); las horas del
  fundador. Las cifras van al informe privado de cierre a la clínica. *Evidencia*: el
  verificador recalcula desde los datos privados.
- **CA-8 (continuidad) [Humano]**: Dado el cierre, cuando se entregue el informe final,
  entonces se envía una propuesta de continuidad y el ledger registra la respuesta
  (renueva / suscripción / no renueva) con fecha. *Evidencia*: fecha y respuesta.

## Entidades y reglas afectadas
- Dominio: Action, AttributionEvent, Weighted SoV, Share of voice, Position.
- RN-02–RN-04, RN-07, RN-09. D-3, D-4, D-6. ADR-003, ADR-004, ADR-005, ADR-008.
- Depende de SPEC-007, SPEC-008 (opcional), SPEC-009, SPEC-010 y SPEC-011.

## Fuera de alcance
- Automatizar la medición semanal o el informe (Ciclo 3).
- Un segundo cliente piloto: no entra en esta épica; la prospección del nicho nuevo va en su propia épica (ADR-008; ~~ADR-003 §2~~, derogado).

## Notas para el gate humano
- **Pendiente de detalle** hasta SPEC-011 y SPEC-008 CA-5: lista de acciones, cadencia del
  probe y si la medición manual cada 4 semanas es suficiente o hace falta más.
- **Mirar con lupa**: medir a mano 3 veces más el set completo son ~3 × 45 consultas; es
  el coste de no tener claves.
