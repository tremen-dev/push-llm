---
id: EPIC-001
tipo: epica
estado: borrador
historial:
  - {estado: borrador, fecha: 2026-09-23, por: sdd-producto}
---
# EPIC-001 — Ciclo 0 — Baseline y validación del problema

## Objetivo
Obtener la primera evidencia real de que el problema existe y duele, antes de
construir nada (Ciclo 0 de `05-lean-plan.md`, D-4): **(a)** un baseline medido
de qué clínicas nombran ChatGPT, Gemini y Claude para preguntas de pacientes en
Vigo/Pontevedra, y **(b)** 10 entrevistas de problema con clínicas y agencias.

Premisa del humano, que condiciona todo el diseño: **el fundador no es
comercial**. Por eso el enfoque es *datos primero*: la puerta se abre con un
hallazgo medido sobre la clínica del interlocutor ("he medido qué clínicas
recomienda ChatGPT en Vigo; esto es lo que sale de la vuestra"), el primer
contacto es **escrito** (email/LinkedIn con texto preparado), y la conversación
es la de un técnico que enseña un dato y pregunta, no la de un vendedor. Nada
se improvisa: todo el material se entrega listo para usar.

Por qué ahora: H1–H2 (`05-lean-plan.md` §1) son las hipótesis más baratas de
comprobar y las que pueden matar la idea; sin este ciclo, cualquier código es
especulación.

## Criterios de éxito
1. **Baseline ejecutado**: el probe corre sobre los 44 prompts × 3 runs × 3
   proveedores (OpenAI, Anthropic, Gemini), coste real registrado y dentro de
   15–30 € (estimación a validar), con resultados por especialidad y proveedor.
2. **Hipótesis del probe contestada** con dato, no opinión: en dental y
   estética, ¿menos de la mitad de las respuestas nombran una clínica local?;
   en fertilidad y oftalmología, ¿aparece siempre la misma clínica?
   (`03-local-market-vigo-pontevedra.md` §2).
3. **Kit de entrevistas para un no-comercial** listo antes del primer contacto:
   el humano puede usarlo sin haber hecho nunca una entrevista de venta.
4. **10 entrevistas hechas**: 4 dental, 2 estética, 2 fertilidad/oftalmología,
   2 agencias de marketing sanitario (reparto orientativo).
5. **Criterio Go de la épica**: ≥ 4 de 10 dicen que pagarían > 150 €/mes
   **y** se cumple la condición del probe en dental y estética. Si no se cumple
   ninguna de las dos, se para (no se pasa al Ciclo 1).

> Desviación consciente respecto a `05-lean-plan.md`: 10 entrevistas y ≥ 4
> (no 15 y ≥ 6). Misma proporción (~40 %), menos evidencia a cambio de un
> esfuerzo realista para un fundador no comercial. Decidido por el humano el
> 2026-09-23.

## Alcance
- Dentro:
  - Ejecución del probe baseline y lectura de resultados frente a la hipótesis.
  - Extracto por clínica objetivo a partir del probe (el "hallazgo" que abre
    la puerta): una captura o media página con qué dice cada asistente de su
    clínica y de sus competidores.
  - Mensajes de primer contacto escritos (email y LinkedIn), con variantes
    para clínica y para agencia, y seguimiento si no contestan.
  - Guion de entrevista de 20 min pensado para leerse: apertura, preguntas en
    orden, frases para salir de silencios, cierre. Preguntas sobre conducta
    pasada y gasto actual, no sobre intenciones futuras.
  - Plantilla de notas y hoja de puntuación común para las 10 entrevistas,
    con la que se evalúa el criterio Go.
  - Lista de objetivos priorizada (base: `03-local-market-vigo-pontevedra.md` §4).
- Fuera (aparcado a propósito, no por descuido):
  - Vender o cobrar: los pilotos de pago son el Ciclo 1.
  - El informe de visibilidad completo y con marca (Ciclo 1). Aquí solo el
    extracto mínimo que sirve para abrir la conversación.
  - Adaptador de Google AI Overviews y de Perplexity para el probe.
  - Cualquier código de producto en `src/`.
  - Contacto por teléfono o visita presencial en frío (descartados por la
    premisa del humano; se pueden reabrir si el escrito no da respuesta).
  - Las entrevistas a escuelas de negocio de `02-icp-and-niche.md` (nicho
    secundario, año 2).
  - Guardar notas de entrevista con datos personales en el repositorio, que
    es **público**: las notas nominales viven fuera del repo; al repo solo
    llegan agregados anonimizados.

## Specs
<!-- El estado por spec vive en el frontmatter de cada spec; el tablero agregado se regenera con /sdd-tablero (docs/tablero.md). No mantengas listas de specs a mano aquí. -->

## Riesgos
- **Sesgo por enseñar datos primero**: el hallazgo puede provocar interés
  cortés ("qué interesante") que no significa disposición a pagar.
  Mitigación: el guion pregunta por gasto y conducta actuales, y la hoja de
  puntuación separa curiosidad de disposición a pagar.
- **Tasa de respuesta baja al contacto escrito**: hipótesis a validar. Si
  tras ~2 semanas hay < 5 entrevistas agendadas, se revisa el mensaje o se
  reabre el canal (red personal, agencias como puente).
- **Comunicaciones comerciales no solicitadas**: escribir en frío a clínicas
  puede estar sujeto a la normativa española de comunicaciones comerciales
  electrónicas y al RGPD. Consultar a `sdd-sanidad-regulacion` antes de enviar
  el primer mensaje; no se da por resuelto aquí.
- **Resultados del probe con datos de terceros en un repo público**: las
  respuestas de los asistentes nombran clínicas reales. Las salidas en bruto
  ya están en `.gitignore`; decidir qué agregados se publican.
- **Coste o comportamiento del probe distinto al estimado**: las cifras de
  `06-models-costs-and-usage-share.md` son de septiembre de 2026 y el script
  nunca se ha ejecutado. Hacer primero una ejecución de humo.
- **API ≠ app de consumo**: el probe aproxima lo que ve el paciente, no lo
  replica (`06-models-costs-and-usage-share.md` §1A). Contrastar a mano unas
  pocas preguntas en la app real desde un móvil en Vigo.

## Desglose orientativo en specs
> Propuesta de sdd-producto; el desglose real lo decide sdd-arquitecto.

| Orden | Spec propuesta | Entrega |
|---|---|---|
| 1 | Ejecución del probe baseline | Humo + ejecución completa, coste real, resultados frente a la hipótesis |
| 2 | Extracto de hallazgos por clínica | Media página por clínica objetivo, generada desde los resultados |
| 3 | Kit de entrevistas para no-comerciales | Mensajes, guion, plantilla de notas, hoja de puntuación, lista de objetivos |
| 4 | Registro y evaluación de las entrevistas | Agregado anonimizado y veredicto Go/No-go |
