---
id: SPEC-011
tipo: spec
epica: EPIC-002
estado: borrador
aprobada-por:
historial:
  - {estado: borrador, fecha: 2026-09-28, por: sdd-arquitecto}
---
# SPEC-011 — Diagnóstico por palancas y plan de acciones de Clínica Ártica

> **Nota 2026-09-29 (c) (sdd-arquitecto): URLs consultadas y citadas (SPEC-013).** El probe
> guarda, en los tres proveedores, `searched_urls` (consultadas) y `cited_urls` (solo
> citadas).
> - Claude hoy consulta pero no cita.
> - En Gemini, `cited_urls` pasa a ser solo los chunks referenciados por
>   `grounding_supports`. En los `results.csv` anteriores a SPEC-013 eran todos los chunks.
> - Las URLs de Gemini siguen siendo redirecciones `vertexaisearch` (F-SPEC-001-2).
>
> Decisión del humano: en el análisis de fuentes se distingue "consultadas" de "citadas",
> igual para todos los proveedores. **Confirmado por el dictamen de sdd-metricas**
> (SPEC-013 CA-7, ledger de SPEC-013; términos en `docs/fundacion/dominio.md`):
> - El peso de citación de CA-1 (§4, RN-04), el top-10, Coverage y el orden de RN-08 se
>   calculan **solo con `cited_urls`**. Una URL solo consultada suma 0.
> - Las consultadas se muestran como **indicador aparte "consultada por"** (ChatGPT, Gemini,
>   Claude) por fuente, **sin peso**: ni RN-04, ni top-10, ni Coverage, ni RN-08. Texto al
>   cliente, igual para todos: "Consultada: el asistente la leyó al buscar. Citada: la
>   enlazó en su respuesta. Solo las citadas cuentan en el peso de fuentes." Con una nota
>   por proveedor de sus límites: los recuentos absolutos no se comparan entre proveedores,
>   y Gemini no se cruza por dominio hasta resolver sus redirecciones (F-SPEC-001-2). Dar
>   peso a las consultadas sería una definición nueva de §4 (sdd-producto y el humano).
> - **Claude aporta 0 al peso de citación mientras no cite**; su 10 % de RN-04 no se
>   redistribuye. El informe a la clínica lo dice expresamente ("Claude: 0 citas en el
>   periodo").
> - **`results.csv` anteriores a SPEC-013** (cabecera sin `searched_urls`): CA-1 usa solo el
>   baseline posterior a SPEC-013. Si se usa un fichero antiguo, se **reclasifica al
>   leerlo**, sin reescribirlo: OpenAI, `cited_urls` = citadas; Gemini, `cited_urls` =
>   consultadas y citadas desconocidas; Claude, citadas vacías y consultadas desconocidas.
>   Nunca se mezclan en un ranking filas de Gemini con los dos significados.
> El ranking de CA-1 ya es por peso de citación y no cambia. El indicador "consultada por"
> y la frase sobre Claude se incorporarán a los CA en la revisión completa de esta spec.
> Sigue en `borrador`.

> **Nota 2026-09-29 (b) (sdd-arquitecto) — nuevo instrumento.** El probe es ya el
> instrumento de medición (EPIC-002, criterios 1 y 4): su baseline oficial (SPEC-008 CA-7)
> es la fuente principal de dominios citados de ChatGPT, Gemini y Claude en los tres
> niveles; la calibración manual de SPEC-007 aporta Google AI Overviews (solo `AV`) y las
> `AM`. CA-1 ajustado en ese sentido. Pendiente de la revisión completa de esta spec:
> diagnóstico por nivel priorizando el núcleo (F-SPEC-007-7). Sigue en `borrador`.

> Spec **documental**. Traduce la foto "antes" (SPEC-007, y SPEC-008 si ya hay probe) y lo
> aprendido en la reunión (SPEC-009) en gaps y acciones priorizadas. Las prioridades
> concretas **dependen de la reunión** (qué tratamientos quieren llenar, qué contenido
> pueden aportar); los CA fijan la forma y las comprobaciones, no el contenido del plan.

## Problema
Criterio de éxito 5 de EPIC-002 y Ciclo 2 del plan lean: hay que saber **qué acción se
hizo y por qué** para poder leer después qué movió qué respuesta. El diagnóstico recorre
las cuatro palancas (`04-mechanics-of-llm-visibility.md` §2): fuentes que leen los
asistentes para estética en la zona y presencia de la clínica en ellas; páginas que
responden preguntas de paciente (hoy la clínica **no publica precios**); menciones de
terceros; legibilidad técnica (su schema es `LocalBusiness` genérico, no
`MedicalClinic`/`Physician`; su `robots.txt` no bloquea bots de IA). En medicina estética
además hay **riesgo normativo** al publicar precios, antes/después, testimonios o
promesas de resultado.

## Usuarios / roles afectados
- Agente (sdd-implementador): diagnostica y redacta el plan. [Agente]
- Consultadas: `sdd-visibilidad-local` (dictamen obligatorio, CA-6) y
  `sdd-sanidad-regulacion` (dictamen obligatorio, CA-7).
- Clínica: aprueba el plan. Humano: lo presenta. [Humano]
- sdd-verificador. [Verificador]

## Criterios de aceptación
- **CA-1 (fuentes citadas) [Agente]**: Dado el `results.csv` del baseline oficial del probe
  (SPEC-008 CA-7) y las capturas de la calibración "antes" de SPEC-007 (Google AI
  Overviews), cuando se analicen, entonces hay una lista de dominios citados
  por las respuestas del set `AV`, ordenada por peso de citación (Σ pesos de proveedor,
  RN-04; AI Overviews aparte) con su tipo (directory, clinic_site, press,
  review_aggregator, other), y el top-10 marcado. *Evidencia*: el verificador recalcula el
  top-10 desde los datos privados.
- **CA-2 (presencia en fuentes) [Agente]**: Dado CA-1 y la foto técnica de SPEC-007 CA-9,
  cuando se haga la PresenceCheck, entonces cada fuente del top-10 más Google Business
  Profile tiene estado present / incomplete / absent con URL, fecha y qué falta.
  *Evidencia*: tabla en el diagnóstico privado; el verificador abre 3 URLs al azar.
- **CA-3 (preguntas sin página) [Agente]**: Dado el set `AV`, cuando se cruce cada pregunta
  con la web de la clínica, entonces cada una queda marcada "hay página que la responde con
  datos" (URL) o "gap", indicando qué dato falta (precio, duración, quién lo hace,
  proceso, preguntas frecuentes). *Evidencia*: tabla pregunta → URL/gap.
- **CA-4 (terceros y técnica) [Agente]**: Dado las palancas 3 y 4, cuando se complete el
  diagnóstico, entonces lista: candidatos concretos de menciones de terceros (prensa
  local, asociaciones, listas) con viabilidad; estado del schema frente a lo recomendado
  por el dictamen de CA-6; consistencia NAP (nombre, dirección, teléfono) en web, Google
  Business Profile y cada fuente de CA-2, con cada discrepancia; y `robots.txt`.
  *Evidencia*: listas con URL y fecha.
- **CA-5 (gaps → acciones) [Agente]**: Dado CA-1 a CA-4 y lo respondido en la reunión
  (SPEC-009 CA-8), cuando se publique `docs/piloto-artica/plan-acciones.md`, entonces cada
  acción (Action) tiene: id `ACC-nn`, gap de origen, palanca, responsable (Tremendev /
  clínica), qué aporta la clínica, esfuerzo, impacto esperado, orden según RN-08, si
  **requiere revisión normativa** (sí/no) y si requiere aprobación de la clínica; y el plan
  cabe en las 2–4 h/semana del fundador durante 12 semanas o dice qué se deja fuera. El
  documento del repo nombra a la clínica pero **no** contiene cifras de SoV ni nombres de
  competidores (ADR-004 §3). *Evidencia*: checklist por acción; búsqueda de nombres de
  competidores de `brands.csv`, sin coincidencias.
- **CA-6 (dictamen de visibilidad local) [Agente; consulta sdd-visibilidad-local]**: Dado
  el diagnóstico, cuando esté redactado, entonces consta en el ledger un dictamen (fecha,
  conclusión por punto, fuentes) sobre: tipo de schema adecuado para la clínica y sus
  profesionales; fuentes prioritarias para estética en la zona; orden de las acciones.
  *Evidencia*: dictamen + cambios aplicados.
- **CA-7 (dictamen de publicidad sanitaria antes de publicar nada) [Agente; consulta
  sdd-sanidad-regulacion]**: Dado el riesgo normativo de la publicidad sanitaria en
  medicina estética, cuando el plan esté redactado y **antes de publicar cualquier
  contenido nuevo** (web, fichas, directorios, Google Business Profile, prensa), entonces
  consta en el ledger un dictamen (fecha, conclusión por punto, normativa estatal y
  gallega citada, condiciones) que cubre al menos: publicar precios (incluidos "desde",
  promociones y financiación); fotos de antes y después; testimonios y reseñas (incluidas
  las incentivadas); promesas o expresiones de resultado ("el mejor", "sin dolor",
  "garantizado"); identificación de los profesionales y su colegiación; datos de
  autorización del centro sanitario que deban figurar; y comparaciones con otras clínicas.
  Cada acción con "requiere revisión normativa = sí" tiene sus condiciones mapeadas, y una
  acción que el dictamen desaconseje se retira del plan. El arquitecto **no** fija la
  normativa en esta spec. *Evidencia*: dictamen + tabla condición → acción.
- **CA-8 (plan aprobado por la clínica) [Humano]**: Dado CA-5 a CA-7, cuando se presente el
  plan a la clínica, entonces el ledger registra la fecha de aprobación y los cambios que
  pidió; ninguna acción se ejecuta antes de esa fecha. *Evidencia*: fecha frente a la
  primera acción del registro de SPEC-012.

## Entidades y reglas afectadas
- Dominio: Source, Source citation weight, PresenceCheck, Coverage of cited sources, Gap,
  Action, NAP.
- RN-04, RN-08. ADR-004. Depende de SPEC-007 (CA-7, CA-9), SPEC-009 (CA-8, CA-9) y,
  opcionalmente, SPEC-008 CA-7.

## Fuera de alcance
- Ejecutar las acciones (SPEC-012).
- Redactar los contenidos finales (se redactan en SPEC-012, pieza a pieza, con la
  revisión de CA-7).
- SEO clásico no orientado a las fuentes que leen los asistentes, campañas y redes.

## Notas para el gate humano
- **Depende de la reunión**: qué tratamientos priorizar y qué contenidos puede aportar la
  clínica deciden el plan; esta spec solo garantiza que el plan es trazable y revisado.
- **Mirar con lupa**: publicar precios es la acción de mayor impacto previsible (palanca 2)
  y la de mayor riesgo normativo; sin dictamen favorable no entra.
