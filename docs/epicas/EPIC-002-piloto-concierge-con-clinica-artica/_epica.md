---
id: EPIC-002
tipo: epica
estado: borrador
historial:
  - {estado: borrador, fecha: 2026-09-28, por: sdd-producto}
---
# EPIC-002 — Piloto concierge con Clínica Ártica

## Objetivo
Llevar a cabo el primer **piloto concierge de pago** con un cliente real:
**Clínica Ártica** (medicina estética; sede única en Viveiro, Lugo;
clinicaartica.es). Es un cliente cálido y de confianza que ha confirmado su
intención de invertir en posicionamiento en IA. Es lo que el plan lean llama
Ciclo 2 (`05-lean-plan.md` §2), adelantado porque la oportunidad ha llegado
antes de terminar el Ciclo 0. Todo el trabajo es manual (D-4): no hay código de
producto.

Por qué ahora: prueba a la vez las dos hipótesis centrales del negocio. **H1**:
¿se puede mover la respuesta de un LLM hacia una clínica en 8–12 semanas?
**H3**: ¿se pueden atribuir pacientes a ese canal? Si la clínica paga, también
aporta evidencia de **H2**. Un cliente de confianza permite aprender con
margen de error y con acceso real a sus datos.

Premisas del humano (2026-09-28):
- **Ejecuta Tremendev/el fundador**: diagnóstico y ejecución técnica (web,
  schema, fichas en directorios). La clínica aporta contenidos (precios, datos,
  fotos) y aprueba. Así se sabe exactamente qué acción movió qué respuesta.
- **Precio aún no hablado**: se propone después de la reunión de
  descubrimiento, anclado en D-7 (3 meses por 450 € prepago o 199 €/mes).
  **Nunca gratis.**
- **La clínica ha autorizado** que su nombre aparezca en el repositorio
  público. Cifras, capturas, datos de su analítica y cualquier dato de
  pacientes siguen fuera del repo (ADR-001).
- **El fundador no es comercial**: reunión con datos primero y material
  preparado, sin improvisar (mismo enfoque que EPIC-001).

## Criterios de éxito
1. **Baseline "antes" registrado** antes de cualquier acción, con fecha y
   evidencia: respuestas de ChatGPT, Gemini y Google (AI Overviews) a un set
   de preguntas de paciente de estética en Viveiro / A Mariña. Sin baseline
   previo no hay aprendizaje posible.
2. **Piloto pagado**: la clínica acepta y paga una propuesta anclada en D-7
   (hipótesis a validar: que la acepte a ese precio).
3. **Atribución instalada el día uno** del piloto, antes de la primera acción
   (D-3): referencias de asistentes de IA etiquetadas en su analítica,
   búsquedas de marca en Search Console, y la pregunta "¿cómo nos conociste?"
   en recepción o en la reserva, con opción de IA.
4. **Criterio Go del piloto (Ciclo 2)**, a unas 12 semanas del inicio de las
   acciones: **+15 puntos de SoV ponderado** sobre su set de prompts **y ≥ 1
   paciente atribuido** al canal IA.
   **Alcance geográfico en tres niveles** (decidido por el humano el
   2026-09-29), cada uno medido como indicador **separado**:
   - **Núcleo** (Viveiro y A Mariña): es el criterio Go (+15 pts, estable en
     las dos pasadas "después").
   - **Área de influencia** (Ferrolterra, norte de Lugo, occidente de
     Asturias): objetivo "de no aparecer a aparecer con cierta regularidad".
     No es criterio Go.
   - **Galicia**, solo para tratamientos por los que el paciente se desplaza
     (trasplante capilar DHI, blefaroplastia): objetivo "aparecer alguna vez".
     No es criterio Go y no se promete a la clínica. Ahí compiten cadenas con
     varias sedes (Novoa, Avance Capilar, Medical Hair, Hospital Capilar,
     Villoria…); dominar ese nivel es un objetivo de un año, no de un piloto
     de 12 semanas.
5. **Registro de acciones → efecto**: cada acción queda fechada y se anota
   semanalmente si movió alguna respuesta en algún asistente. Según
   `05-lean-plan.md`, este registro "es el producto futuro".
6. **Renovación**: al terminar, la clínica renueva o pasa a suscripción. Es
   hipótesis a validar y la señal más fuerte de valor.

## Alcance
- Dentro:
  - Baseline manual desde el móvil (gratis, ya) y, cuando haya claves
    (EPIC-001 / SPEC-002), un set de prompts propio de estética en Viveiro /
    A Mariña / Lugo medido con el probe.
  - Kit de la reunión de descubrimiento: guion para leer, preguntas sobre qué
    tratamientos quieren llenar, valor de un paciente nuevo, quién lleva la
    web, qué entienden por "posicionamiento en IA" y su disposición a medir.
    Incluye el hallazgo del baseline como apertura.
  - Propuesta económica y de alcance de una página, con expectativas
    explícitas: movimiento en 4–12 semanas y **sin garantía de aparecer**
    (`04-mechanics-of-llm-visibility.md` §4).
  - Instalación de la atribución (las tres señales).
  - Diagnóstico sobre las cuatro palancas (`04-mechanics-of-llm-visibility.md`
    §2): fuentes que citan los LLM para estética en su zona y presencia de la
    clínica en ellas; páginas que responden preguntas de paciente (hoy **no
    publica precios**); menciones de terceros; legibilidad técnica (su schema
    es `LocalBusiness` genérico; su `robots.txt` no bloquea bots de IA).
  - Ejecución de las acciones priorizadas, por Tremendev.
  - Medición semanal y registro de acciones → efecto; informe a la clínica
    cada 15 días.
  - Cierre del piloto con veredicto H1/H3 y propuesta de continuidad.
- Fuera (aparcado a propósito, no por descuido):
  - Cualquier código de producto en `src/` (Ciclo 3).
  - El bot de WhatsApp de preguntas y citas que el fundador desarrolla en otra
    conversación: es otro proyecto y no entra en este piloto.
  - Campañas de pago, redes sociales, SEO clásico no orientado a las fuentes
    que leen los LLM.
  - Garantías de posicionamiento o de número de pacientes.
  - Un segundo cliente piloto (se reevalúa al cerrar esta épica).
  - Ampliar el nicho oficial a Lugo / A Mariña: este piloto es una excepción de
    aprendizaje, no un cambio de nicho (ver Riesgos).

## Specs
<!-- El estado por spec vive en el frontmatter de cada spec; el tablero agregado se regenera con /sdd-tablero (docs/tablero.md). No mantengas listas de specs a mano aquí. -->

## Desglose orientativo en specs
> Propuesta de sdd-producto; el desglose real lo decide sdd-arquitecto.

| Orden | Spec propuesta | Entrega |
|---|---|---|
| 1 | Baseline "antes" de Clínica Ártica | Set de prompts de estética en Viveiro/A Mariña; medición manual desde el móvil ya, y con el probe cuando haya claves |
| 2 | Reunión de descubrimiento y propuesta | Guion para leer, preguntas, propuesta de una página anclada en D-7 |
| 3 | Instalación de la atribución | Las tres señales operativas antes de la primera acción |
| 4 | Diagnóstico y plan de acciones | Gaps por palanca, priorizados; qué hace Tremendev y qué aporta la clínica |
| 5 | Ejecución, medición semanal y cierre | Registro de acciones → efecto, informes cada 15 días, veredicto H1/H3 |

## Riesgos
- **Fuera del nicho D-2** (Vigo/Pontevedra primero). D-2 está bloqueada en
  FOUNDATION: sdd-arquitecto debe registrar esta excepción como ADR, o
  confirmar que "primero" no la prohíbe. El aprendizaje sobre H1/H3 es
  transferible; el de mercado (competencia, fuentes) es solo parcial.
- **Volumen bajo**: Viveiro es un mercado pequeño. Puede haber muy pocas
  búsquedas y pacientes atribuibles en 12 semanas, y "≥ 1 paciente atribuido"
  puede depender del azar. Hipótesis a validar en el baseline.
- **Relación de confianza**: cuesta cobrar el precio completo y decir "no ha
  funcionado". Mitigación: propuesta escrita anclada en D-7 y criterios de
  éxito compartidos con la clínica desde el principio.
- **Publicidad sanitaria**: en medicina estética, publicar precios, antes y
  después, o promesas de resultado puede estar regulado. Consultar a
  `sdd-sanidad-regulacion` antes de publicar contenido nuevo en su web o en
  directorios.
- **Dependencia de EPIC-001**: la medición con el probe requiere las claves de
  SPEC-002 y prompts de Viveiro que hoy no existen en `probe/prompts.csv`.
  Mitigación: el baseline manual desde el móvil no depende de nada.
- **Tiempo del fundador**: ejecutar las acciones compite con EPIC-001 y con el
  otro proyecto (bot de WhatsApp). Hipótesis: unas 2–4 h por semana durante 12
  semanas.
- **Contaminación de la medición**: si la clínica o una agencia cambian cosas
  en paralelo (web, campañas), la atribución de efectos se enturbia. Acordar
  en la reunión que cualquier cambio se comunica.
