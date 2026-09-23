---
id: SPEC-005
tipo: spec
epica: EPIC-001
estado: borrador
aprobada-por:
historial:
  - {estado: borrador, fecha: 2026-09-23, por: sdd-arquitecto}
---
# SPEC-005 — Registro y evaluación de las entrevistas

> Spec **mixta**: las entrevistas, las notas nominales y la puntuación son **acción
> del humano** en el espacio privado; el agregado anonimizado y el cálculo del
> veredicto los puede producir un **agente**, sujeto a ADR-001 y a lo que el
> dictamen de SPEC-004 CA-9 diga sobre que un agente lea notas con datos personales.

## Problema
El criterio Go de EPIC-001 (criterio de éxito 5) necesita 10 entrevistas puntuadas
con un criterio fijado de antemano y un veredicto sin ambigüedad, publicado en un
repo público sin exponer a nadie. Hoy no hay dónde registrar, cómo agregar ni una
regla para el caso mixto (la épica y `05-lean-plan.md` §2 dicen "si no se cumple
**ninguna** de las dos, se para", pero el Go exige **ambas**).

## Usuarios / roles afectados
- Humano: entrevista, toma notas, puntúa.
- Agente: agrega, anonimiza (o el humano, según dictamen), calcula el veredicto.
- sdd-producto: recibe el veredicto para decidir el paso al Ciclo 1 y el roadmap.
- sdd-verificador: recuenta el veredicto desde la tabla pseudonimizada.

## Criterios de aceptación
- **CA-1 (10 entrevistas con reparto)**: Dado el reparto orientativo de EPIC-001,
  cuando se cierre la fase de entrevistas, entonces hay 10 entrevistas hechas con
  interlocutores con poder de decisión o influencia directa sobre el gasto de
  captación (dirección, gerencia, marketing; en agencias, dirección o cuenta), con
  reparto objetivo 4 dental, 2 estética, 2 fertilidad/oftalmología y 2 agencias; toda
  desviación del reparto se anota con motivo. *Evidencia*: tabla pseudonimizada de
  CA-4 con segmento por fila. **Acción humana.**
- **CA-2 (notas y puntuación a tiempo, en privado)**: Dada cada entrevista, cuando
  pasen 48 h, entonces existe en el espacio privado su nota completa según la plantilla
  de SPEC-004 CA-7 y su fila en la hoja de puntuación, con la versión congelada de la
  hoja. *Evidencia*: el humano reporta en el ledger, por pseudónimo, fecha de entrevista
  y fecha de nota (sin nombres). **Acción humana.**
- **CA-3 (punto de control de captación)**: Dado el procedimiento de SPEC-004 CA-8,
  cuando pasen 10 días hábiles desde el primer envío, entonces el ledger registra
  envíos, respuestas y entrevistas agendadas a esa fecha (solo recuentos por segmento)
  y, si hay < 5 agendadas, la decisión tomada (cambio de mensaje, canal o plazo) con
  fecha. *Evidencia*: registro en el ledger.
- **CA-4 (agregado anonimizado en el repo)**: Dadas las 10 fichas, cuando se publique
  `docs/ciclo-0/entrevistas-agregado.md`, entonces contiene: tabla `E01…E10` con
  segmento (dental / estética / fertilidad-oftalmología / agencia), curiosidad sí/no,
  A (gasto ≥ 150 €/mes) sí/no, B (compromiso) sí/no, señal de pago sí/no; tramos de
  gasto actual (< 150, 150–500, > 500 €/mes) sin cifras exactas; cómo miden hoy la
  procedencia de pacientes (H3); interés de reventa en agencias (H4); patrones y
  paráfrasis sin atribuir a ningún segmento con < 3 entrevistas; embudo de
  captación (envíos → respuestas → entrevistas por canal). *Evidencia*: revisión de la
  estructura.
- **CA-5 (anonimización comprobable)**: Dado ADR-001, cuando se revise el agregado,
  entonces no contiene nombres de persona, emails, teléfonos, nombres de clínicas de
  `brands.csv` o de la lista de objetivos, ni cifras de gasto exactas; y `git ls-files`
  no lista notas, registros de envío ni la tabla pseudónimo ↔ identidad. *Evidencia*:
  búsqueda por script contra `brands.csv`, `objetivos.md` y patrones de email/teléfono,
  sin coincidencias; salida de `git ls-files` en el ledger.
- **CA-6 (veredicto con regla cerrada)**: Dada la tabla de CA-4 y el veredicto de la pata
  dental/estética de SPEC-002 CA-7, cuando se emita el veredicto, entonces es uno de:
  **Go** = señal de pago en ≥ 4 de 10 **y** pata del probe `cumple`; **No-go** = < 4 de
  10 **y** pata del probe `no cumple`; **Mixto** = cualquier otro caso, que **no** se
  resuelve aquí sino que se eleva a sdd-producto y al humano con los datos. Si hay menos
  de 10 entrevistas, el veredicto es **Incompleto** con n, salvo que ya haya ≥ 4 señales de
  pago y la pata del probe cumpla. El veredicto, su regla y sus dos entradas figuran en el
  agregado y en el ledger. *Evidencia*: el verificador recuenta la tabla de CA-4, lee el
  veredicto de SPEC-002 y obtiene el mismo resultado.
- **CA-7 (hoja no retocada a posteriori)**: Dado que la hoja se congeló antes de la primera
  entrevista (SPEC-004 CA-7), cuando se emita el veredicto, entonces todas las filas usan
  la misma versión de la hoja, o, si hubo cambios, consta su motivo y la repuntuación de
  todas las entrevistas anteriores. *Evidencia*: versión y fecha de la hoja en el ledger.
- **CA-8 (entrega a producto)**: Dado un veredicto, cuando se cierre la spec, entonces el
  orquestador tiene un resumen de ≤ 10 líneas para sdd-producto con el veredicto, las
  dos entradas, las señales de pivote de `05-lean-plan.md` §5 que se observen y la
  desviación 10/≥ 4 frente a 15/≥ 6 del plan. *Evidencia*: resumen en el ledger.

## Entidades y reglas afectadas
- Dominio: Clinic, Speciality, AttributionEvent (solo como pregunta sobre conducta
  actual; no se registran eventos).
- D-2, D-4 (el veredicto abre o cierra el Ciclo 1), D-7 (ancla usada en el cierre).
- ADR-001. Depende de SPEC-004 (kit, hoja congelada) y SPEC-002 (pata probe).

## Fuera de alcance
- Decidir el paso al Ciclo 1, actualizar roadmap o épica (sdd-producto y humano).
- Vender pilotos a quien muestre señal de pago (Ciclo 1; se anota el compromiso, no se
  ejecuta).
- Análisis cualitativo profundo o codificación temática formal de las notas.
- Entrevistas a escuelas de negocio.

## Notas para el gate humano
- **Contradicción resuelta por regla, a validar**: la épica define Go como "≥ 4/10 **y**
  condición del probe" pero para la parada dice "si no se cumple **ninguna** de las dos".
  El caso con una sola pata queda sin decidir en los documentos; aquí lo marco como
  **Mixto** y lo elevo, no lo decido.
- Con 2 entrevistas en fertilidad/oftalmología en una ciudad con 3 clínicas de fertilidad,
  cualquier cita atribuida al segmento identifica a la clínica; por eso CA-4 prohíbe
  atribuir paráfrasis a segmentos con < 3 entrevistas.
- Si el dictamen de SPEC-004 CA-9 no permite que un agente lea notas con datos personales,
  el humano rellena la tabla pseudonimizada y el agente solo agrega desde ella.
- Acciones del humano: entrevistas (CA-1), notas y puntuación (CA-2), recuentos del punto
  de control (CA-3). El agente: agregado (CA-4, CA-5), veredicto (CA-6), resumen (CA-8).
- Depende de: SPEC-004 y SPEC-002. Es la última spec de la épica.
