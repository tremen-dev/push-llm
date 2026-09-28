---
id: SPEC-010
tipo: spec
epica: EPIC-002
estado: borrador
aprobada-por:
historial:
  - {estado: borrador, fecha: 2026-09-28, por: sdd-arquitecto}
---
# SPEC-010 — Instalación de la atribución del piloto

> Spec **operativa, sin código de producto**. Tremendev configura la analítica y Search
> Console de la clínica; la clínica pone la pregunta en recepción y en la reserva. Parte
> del detalle **depende de la reunión** (SPEC-009 CA-8): qué analítica tienen, qué
> software de reservas usan y quién atiende en recepción. Los CA fijan el resultado
> comprobable; el cómo se concreta en el ledger tras la reunión, y esta spec se revisará
> antes de aprobarla si la reunión cambia algo sustancial.

## Problema
D-3 y el criterio de éxito 3 de EPIC-002: la atribución se instala **el día uno, antes de
la primera acción**, o la clínica nunca verá el retorno aunque exista
(`04-mechanics-of-llm-visibility.md` §3). Tres caminos de llegada, tres señales
(AttributionEvent): clic con referencia de un asistente (`referral_tag`), búsqueda del
nombre en Google (`branded_search`) y respuesta en recepción (`reception_answer`). Una
GA4 por defecto clasifica gran parte de las visitas de IA como "directo"; si no se mira
antes de actuar, no hay "antes" contra el que comparar.

## Usuarios / roles afectados
- Humano / Tremendev: configura analítica y Search Console; recoge los datos cada semana.
  [Humano]
- Clínica: da accesos, pone la pregunta en la reserva y en recepción, entrega conteos
  semanales agregados.
- Agente (sdd-implementador): redacta procedimientos, guion de recepción y plantillas.
  [Agente]
- Consultadas: dictamen de `sdd-sanidad-regulacion` ya emitido en SPEC-009 CA-6 (se aplica
  aquí); `sdd-visibilidad-local` opcional.
- sdd-verificador. [Verificador]

## Criterios de aceptación
- **CA-1 (señal referral_tag) [Humano configura; Agente redacta el procedimiento]**: Dado
  el acceso de SPEC-009 CA-4 (b), cuando se configure la analítica de la web de la clínica
  (GA4 u otra que ya usen; si no hay ninguna, lo que se decida en la reunión y conste en el
  ledger), entonces existe una agrupación o informe guardado "Asistentes de IA" que
  clasifica como tal las visitas con origen o referencia `chatgpt.com`, `chat.openai.com`,
  `gemini.google.com`, `perplexity.ai`, `claude.ai` y `copilot.microsoft.com`, y las de
  `utm_source=chatgpt.com`; y una visita de prueba etiquetada
  (`utm_campaign=prueba-pushllm`, para poder excluirla) hecha desde un enlace en ChatGPT
  aparece clasificada así en ≤ 48 h. *Evidencia*: procedimiento en
  `docs/piloto-artica/atribucion/analitica.md`; captura privada del informe con la visita
  de prueba; fecha en el ledger.
- **CA-2 (conversiones) [Humano]**: Dado que una visita no es un paciente, cuando se
  configure la analítica, entonces la reserva online y el clic a WhatsApp (y al teléfono,
  si es enlace) quedan registrados como eventos clave y se pueden cruzar con la agrupación
  de CA-1. *Evidencia*: captura privada de un evento de prueba por tipo; fecha en el ledger.
- **CA-3 (señal branded_search) [Humano]**: Dado Search Console de la web de la clínica,
  cuando se tenga acceso, entonces se exporta al espacio privado, con fecha, la serie de
  impresiones y clics de consultas que contienen el nombre de la clínica (con y sin
  acento) de los 16 meses disponibles, y está escrito el procedimiento semanal para
  repetir la exportación. *Evidencia*: fichero fechado en
  `$PUSHLLM_PRIVADO/piloto-artica/atribucion/`; procedimiento en
  `docs/piloto-artica/atribucion/search-console.md`.
- **CA-4 (señal reception_answer) [Clínica pone; Agente redacta]**: Dado RN-09 y el
  dictamen de SPEC-009 CA-6, cuando se publiquen el guion de recepción y la opción del
  formulario, entonces: la pregunta "¿Cómo nos has conocido?" aparece en la reserva online
  y en el guion literal de recepción (teléfono, WhatsApp, presencial) con una opción
  explícita "ChatGPT, Gemini u otro asistente de inteligencia artificial" junto a las
  demás (Google, redes, recomendación, otro); y la clínica entrega cada semana solo el
  **conteo por opción**, sin nombres, teléfonos ni ningún identificador de paciente, en la
  plantilla `docs/piloto-artica/atribucion/conteo-semanal.csv` (cabecera sin filas en el
  repo). *Evidencia*: textos en el repo; captura privada del formulario publicado; la
  plantilla no tiene columnas de identificación.
- **CA-5 (antes de actuar) [Verificador]**: Dado D-3, cuando se registre la primera acción
  del piloto (SPEC-012), entonces las fechas de CA-1, CA-3 y CA-4 son **anteriores**; si
  una señal no pudo instalarse, el ledger dice cuál, por qué y la decisión del humano de
  empezar igualmente, con fecha anterior a la primera acción. *Evidencia*: comparación de
  fechas en el ledger.
- **CA-6 (rutina semanal) [Agente]**: Dado que la atribución se lee semanalmente, cuando se
  publique `docs/piloto-artica/atribucion/rutina.md` (≤ 1 página), entonces dice quién
  hace qué cada semana (la clínica envía el conteo antes del lunes; Tremendev exporta las
  tres señales y las anota en la hoja privada de AttributionEvent: fecha, señal, conteo),
  y qué hacer si un conteo trae datos de pacientes (se borra y se pide agregado, ADR-004
  §4). *Evidencia*: checklist.
- **CA-7 (accesos mínimos y sin secretos) [Verificador]**: Dado ADR-004 §5, cuando se
  cierre la spec, entonces el ledger lista cada acceso concedido (herramienta, rol, fecha)
  y su revocación prevista, y en el repo no hay IDs de medición, IDs de propiedad, tokens
  ni credenciales. *Evidencia*: tabla de accesos; búsqueda por patrón (p. ej. `G-`
  seguido de alfanuméricos, `UA-`, `GTM-`), sin coincidencias.

## Entidades y reglas afectadas
- Dominio: AttributionEvent (referral_tag, branded_search, reception_answer), Branded-search
  uplift.
- RN-07 (pacientes atribuidos = suma de eventos por señal, nunca inferidos del SoV), RN-09.
- D-3. ADR-004. Depende de SPEC-009 CA-6 y CA-9 (acuerdos, dictamen, cobro).

## Fuera de alcance
- Línea telefónica o landing dedicada al tráfico de IA (`dedicated_line`): opcional; si
  se quiere, se añade tras la reunión con su propio CA.
- Cualquier estimación en euros (necesita el ticket medio de la reunión; va en el informe
  de SPEC-012).
- Integraciones automáticas o código.

## Notas para el gate humano
- **Depende de la reunión**: herramienta de analítica, software de reservas y quién
  pregunta en recepción. Si no tienen analítica, instalarla puede exigir banner de
  cookies; lo dirá el dictamen de SPEC-009 CA-6.
- **Riesgo**: con el consentimiento de cookies, parte de las visitas no se mide. La
  pregunta en recepción es la señal más robusta en un mercado pequeño; conviene que la
  clínica la haga de verdad (se revisa en cada informe quincenal).
