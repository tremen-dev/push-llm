---
id: SPEC-009
tipo: spec
epica: EPIC-002
estado: aprobada
aprobada-por: Alberto Fojo
historial:
  - {estado: borrador, fecha: 2026-09-28, por: sdd-arquitecto}
  - {estado: aprobada, fecha: 2026-09-28, por: Alberto Fojo}
  - {estado: bloqueada, fecha: 2026-09-29, por: sdd-arquitecto}
  - {estado: borrador, fecha: 2026-09-29, por: sdd-arquitecto}
  - {estado: aprobada, fecha: 2026-09-29, por: Alberto Fojo}
---
# SPEC-009 — Reunión de descubrimiento y propuesta para Clínica Ártica

> **Nota 2026-09-29 (c) (sdd-arquitecto) — Go "crecer fuera, defender dentro" (ADR-009,
> borrador). No cambia ningún CA ni requiere re-aprobación por sí misma; deja una decisión
> pendiente.** Esta spec no promete "+15 pts en el núcleo" en ningún sitio, así que no hay
> nada que retirar. Pero su CA-3 dice que "cómo sabremos si funciona" usa "los dos criterios
> de la épica, referidos al **núcleo**", y que el área de influencia aparece "solo como
> también lo medimos, sin objetivo". Con ADR-009 el núcleo pasa a ser condición de
> **defensa** y el crecimiento se mide en `AR`. **Follow-up F-SPEC-009-1 (→ humano, antes
> de redactar `propuesta.md`)**: decidir si la propuesta cuenta a la clínica el Go nuevo
> (p. ej. "que os recomienden también a pacientes de Ferrolterra, norte de Lugo y occidente
> de Asturias, sin perder lo que ya tenéis en A Mariña", sin garantía) o lo deja como
> criterio interno de Tremendev. Si se cuenta, CA-3 necesita enmienda y la spec,
> re-aprobación; si no, CA-3 queda como está y el Go se explica solo en el cierre
> (SPEC-012). El nivel Galicia sigue sin aparecer (ADR-005 §6, vigente).

> **Nota 2026-09-29 (sdd-arquitecto) — cambio de nicho (ADR-008). No cambia ningún CA ni
> requiere re-aprobación.** Las citas a ADR-003 y ADR-005 de esta spec siguen valiendo en lo
> que usa (lote aparte, niveles `AV`/`AR`/`AG` sin mezclar, Go solo con `AV`, nivel Galicia
> sin prometer, marcas del piloto fuera del lote de Vigo). Lo que ADR-008 deroga es el
> encuadre como "excepción a D-2" y sus prohibiciones de prospección y de "Asturias no es
> mercado"; el lote de Vigo queda aparcado, intacto, como configuración por defecto.

> **Nota 2026-09-29 (b) (sdd-arquitecto) — la manual pasa a calibración (EPIC-002,
> criterios 1 y 4). No cambia ningún CA ni requiere re-aprobación.** Donde esta spec dice
> "pasada 1 de SPEC-007", léase la **pasada "antes"** de calibración (SPEC-007 CA-5): 15
> `AV` en ChatGPT, Gemini y Google más las `AM`; la hoja de hallazgo (SPEC-007 CA-10) sale
> de ella igual que antes. El set `AR`/`AG` se congela, como tarde, con el primer baseline
> del probe (SPEC-007 CA-8), no con la pasada manual. SPEC-007 CA-7 pide además que, si la
> calibración dice que app y probe **no** coinciden, no se envíe la propuesta ni se enseñen
> cifras del probe hasta que el humano decida el ajuste; si la propuesta sale antes de que
> exista la calibración, no puede citar cifras del probe (pregunta abierta para el gate de
> SPEC-007).

> Spec **documental**. El agente redacta el kit de la reunión y la propuesta; el humano
> ensaya, se reúne, envía la propuesta y cobra. Plantillas en
> `docs/piloto-artica/reunion/` (castellano, D-8), sin datos de personas ni cifras de la
> clínica; notas, propuesta enviada, respuesta, consentimientos y factura en
> `$PUSHLLM_PRIVADO/piloto-artica/reunion/` (ADR-004).

> **Enmienda 2026-09-29 (sdd-arquitecto) — tres niveles (ADR-005).** La medición tiene
> núcleo (Viveiro y A Mariña, criterio Go), área de influencia y Galicia (solo
> tratamientos de desplazamiento). Cambian CA-2, CA-3, CA-5 y CA-10. La spec vuelve a
> `borrador` (estaba `aprobada`, sin empezar) y necesita **nueva aprobación humana**.

## Problema
La clínica es un cliente **cálido** que ya quiere invertir: no hay que conseguir la
reunión ni validar el dolor en frío, que es lo que resuelve SPEC-004 (EPIC-001). Aquí el
riesgo es otro: que una relación de confianza lleve a (a) no cobrar o cobrar por debajo de
D-7, (b) prometer lo que no se puede (`04-mechanics-of-llm-visibility.md` §4), (c) empezar
sin acuerdos que luego hacen imposible medir (cambios en paralelo, sin acceso a la
analítica, sin pregunta en recepción) y (d) un fundador no comercial improvisando. Se
reutilizan de SPEC-004 las **reglas** (texto literal para leer, preguntas sobre conducta
pasada estilo *The Mom Test*, frases de apoyo, vocabulario prohibido de su CA-12, ensayo
previo), no sus ficheros: el guion, las preguntas, el cierre y las objeciones son otros.

## Usuarios / roles afectados
- Humano (fundador): ensaya, conduce la reunión, envía la propuesta, cobra. [Humano]
- Clínica Ártica: dirección y quien decide/aprueba contenidos.
- Agente (sdd-implementador): redacta. [Agente]
- Consultada: `sdd-sanidad-regulacion` (dictamen RGPD obligatorio, CA-6).
- sdd-verificador. [Verificador]

## Criterios de aceptación
- **CA-1 (guion para leer) [Agente]**: Dado un fundador no comercial, cuando se publique
  `docs/piloto-artica/reunion/guion.md`, entonces tiene bloques de texto **literal** con
  minutaje que suma ≤ 45 min: apertura (qué vamos a hacer hoy y qué no: no se decide nada
  hoy, la propuesta llega por escrito); **dato primero** (enseñar la hoja de hallazgo de
  SPEC-007 CA-10 y callar); preguntas (CA-2); cómo funciona, en lenguaje llano (las cuatro
  palancas de `04-…md` §2 sin jerga, qué hace Tremendev y qué aporta la clínica, que el
  movimiento tarda 4–12 semanas y que **no se garantiza** aparecer ni un número de
  pacientes); acuerdos que se piden (CA-4); cierre (fecha concreta en la que llega la
  propuesta y quién la recibe). Ningún bloque es una instrucción sin texto. *Evidencia*:
  revisión estructural; suma del minutaje.
- **CA-2 (preguntas) [Agente]**: Dado lo que la épica necesita saber, cuando se revisen las
  preguntas del guion, entonces hay ≥ 12 y cubren al menos: qué tratamientos quieren
  llenar y si hay agenda libre para ellos; valor aproximado de un paciente nuevo de esos
  tratamientos; cómo llegó el último paciente nuevo de cada uno; cuántos pacientes nuevos
  tienen al mes, en tramos (para dimensionar "≥ 1 atribuido"); cómo saben hoy de dónde
  viene un paciente (qué se pregunta en recepción, qué software de reservas usan, si hay
  analítica y Search Console y quién tiene acceso); quién lleva la web y con qué gestor de
  contenidos; qué agencia, campañas o cambios de web tienen en marcha o previstos en las
  próximas 12 semanas; gasto actual en captación por partida; qué entienden por
  "posicionamiento en IA" y qué han oído o probado; si algún paciente ha mencionado ChatGPT
  u otro asistente; quién decide y quién aprueba contenidos; qué contenido podrían aportar
  (precios, fotos, datos de profesionales, preguntas frecuentes de pacientes); y, por la
  enmienda de 2026-09-29, **qué tratamientos quieren atraer de pacientes de fuera de
  A Mariña** (Ferrolterra, occidente de Asturias, resto de Galicia) y **de dónde vino el
  último paciente que se desplazó** desde fuera para un tratamiento (conducta pasada, no
  "¿os interesaría…?"). Fuera del
  bloque de expectativas no hay preguntas hipotéticas ("¿pagarías…?", "¿te
  interesaría…?"). *Evidencia*: checklist de cobertura; búsqueda de patrones prohibidos
  fuera de ese bloque, sin coincidencias.
- **CA-3 (propuesta de una página) [Agente]**: Dado D-7, cuando se publique la plantilla
  `docs/piloto-artica/reunion/propuesta.md`, entonces cabe en una página (≤ 450 palabras)
  y contiene, en lenguaje de clínica: el objetivo ("que ChatGPT, Gemini y Google os
  recomienden cuando alguien de la zona pregunta por {tratamientos}, y saber cuántos
  pacientes llegan por ahí"); qué incluye (foto de partida, medición de pacientes desde el
  día uno, diagnóstico, acciones ejecutadas por Tremendev, medición semanal, informe cada
  15 días, reunión de cierre); qué aporta la clínica (contenidos, aprobación, pregunta en
  recepción, accesos); duración de 12 semanas desde la primera acción; **precio exacto de
  D-7** en sus dos opciones (450 € por 3 meses prepago o 199 €/mes) con el tratamiento del
  IVA explícito; expectativas (movimiento en 4–12 semanas, sin garantía de aparecer ni de
  número de pacientes); "cómo sabremos si funciona", en palabras llanas, con los dos
  criterios de la épica, referidos al **núcleo** (Viveiro y A Mariña); qué pasa al terminar
  (renovar o no, sin permanencia). Por la enmienda de 2026-09-29 (ADR-005 §6): el nivel
  Galicia **no aparece** en la propuesta como objetivo, entregable ni expectativa, y el área
  de influencia, si aparece, lo hace solo como "también lo medimos y os lo contamos", sin
  objetivo. No hay
  opción gratuita ni descuento sobre D-7; cualquier desviación exige decisión del humano
  registrada en el ledger antes del envío. *Evidencia*: conteo de palabras; checklist;
  cifras de precio iguales a D-7; búsqueda de "Galicia" en `propuesta.md`, sin
  coincidencias.
- **CA-4 (acuerdos y consentimientos) [Agente]**: Dado que sin ellos no se puede medir ni
  publicar, cuando se publique `docs/piloto-artica/reunion/acuerdos.md` (anexo de la
  propuesta, para firmar o aceptar por escrito), entonces recoge: (a) la clínica avisa por
  escrito, con fecha, antes de cualquier cambio en web, fichas, directorios o campañas
  durante el piloto, propio o de su agencia; (b) consentimiento de acceso a analítica,
  Search Console, Google Business Profile y gestor de la web, con el rol mínimo y
  revocable (ADR-004 §5); (c) consentimiento para aparecer con su nombre en el repositorio
  público, explicando qué se publica y qué no (ADR-004 §1–§3) y que el historial no se
  borra si se revoca (§6); (d) que Tremendev no recibe datos de pacientes, solo conteos
  semanales agregados (RN-09); (e) que ningún contenido se publica sin aprobación escrita
  de la clínica y sin la revisión normativa de SPEC-011 CA-7; y lo que añada el dictamen de
  CA-6. *Evidencia*: checklist; trazabilidad a ADR-004 y al dictamen.
- **CA-5 (apoyo y objeciones de cliente cálido) [Agente]**: Dado un fundador que se
  bloquea, cuando se publique `docs/piloto-artica/reunion/apoyo.md` (una página), entonces
  contiene respuestas literales a ≥ 8 objeciones, incluidas: "¿me garantizas salir el
  primero?", "¿cuántos pacientes me vas a traer?", "somos amigos, ¿no me lo haces gratis?",
  "¿por qué no empezamos ya y lo hablamos luego?", "la web la lleva otra persona/agencia",
  "¿y si ChatGPT cambia?", "¿podemos poner precios / antes y después?" (remite a la
  revisión normativa, sin afirmar que se pueda), "¿esto no es SEO?" y (enmienda
  2026-09-29) "¿y saldremos cuando alguien de Coruña o Vigo busque un injerto capilar?"
  (respuesta honesta: se mide y se informa, compiten cadenas con varias sedes y no se
  promete); y ≥ 4 frases para
  volver a hechos pasados. *Evidencia*: recuento y checklist.
- **CA-6 (dictamen RGPD antes de enviar la propuesta) [Agente; consulta
  sdd-sanidad-regulacion]**: Dado que Tremendev accederá a la analítica de la clínica
  (puede contener datos personales de visitantes) y que la clínica preguntará a pacientes
  "¿cómo nos conociste?", cuando la propuesta y los acuerdos estén redactados y antes de
  enviarlos, entonces consta en el ledger un dictamen de `sdd-sanidad-regulacion` (fecha,
  conclusión por punto, fuentes, condiciones) que cubre al menos: si Tremendev actúa como
  encargado del tratamiento y qué contrato o cláusula hace falta; información a pacientes
  sobre la pregunta de procedencia y su registro; cookies/consentimiento para la analítica
  de la web; conservación de los datos agregados; y si nombrar competidores en la hoja de
  hallazgo ante la clínica plantea algún problema. Cada condición se mapea a un cambio en
  propuesta, acuerdos o SPEC-010. *Evidencia*: dictamen + tabla condición → cambio.
- **CA-7 (ensayo) [Humano]**: Dado un fundador sin experiencia comercial, cuando el kit
  esté terminado y antes de la reunión, entonces el humano hace un ensayo completo en voz
  alta (un agente o una persona hace de dirección de la clínica y plantea ≥ 3 objeciones de
  CA-5), cronometrado en ≤ 50 min, y los cambios que salgan se incorporan. *Evidencia*:
  fecha, duración y lista de cambios en el ledger.
- **CA-8 (reunión celebrada) [Humano]**: Dado CA-7 y la pasada 1 de SPEC-007 hecha, cuando
  se celebre la reunión, entonces las notas quedan en el espacio privado en ≤ 48 h y el
  ledger registra fecha, duración y qué preguntas de CA-2 quedaron respondidas (sí/no por
  pregunta, sin el contenido). *Evidencia*: registro en el ledger; fecha posterior a CA-7
  y a SPEC-007 CA-5.
- **CA-9 (propuesta enviada, aceptada y cobrada) [Humano]**: Dado la reunión, cuando se
  envíe la propuesta (≤ 5 días hábiles después) con los acuerdos de CA-4, entonces el
  ledger registra: fecha de envío; respuesta (acepta opción prepago / acepta mensual /
  negocia / rechaza) con fecha; fecha de aceptación de los acuerdos y del consentimiento de
  nombre (sin nombre de la persona que firma); fecha del primer cobro. El piloto **no
  empieza** (SPEC-010 ni primera acción) sin aceptación escrita y primer cobro.
  *Evidencia*: fechas en el ledger; documentos en el espacio privado.
- **CA-10 (sin jerga ni datos personales) [Verificador]**: Dado D-3 y ADR-004, cuando se
  revisen los textos de `docs/piloto-artica/reunion/`, entonces no aparecen "AEO", "GEO",
  "SoV", "share of voice", "LLM", "visibilidad en IA" ni "posicionamiento garantizado",
  ni una promesa de aparecer en el nivel Galicia (ADR-005 §6), y
  no hay emails, teléfonos (salvo marcadores `{…}`) ni nombres de persona. *Evidencia*:
  búsqueda por script, sin coincidencias.

## Entidades y reglas afectadas
- Dominio: Clinic, Provider (como "asistente"), AttributionEvent, Action (qué hace cada
  parte).
- D-3 (se vende pacientes, no visibilidad), D-7 (precio), D-8 (idioma), RN-07, RN-09.
- ADR-003, ADR-004, ADR-005 (§6: el nivel Galicia no se promete). Reutiliza las reglas de SPEC-004 CA-3, CA-4, CA-6, CA-11 y CA-12 sin
  copiar sus ficheros. Depende de SPEC-007 CA-5 y CA-10.

## Fuera de alcance
- Contrato mercantil formal más allá de la propuesta y los acuerdos aceptados por escrito
  (si el dictamen de CA-6 exige un contrato de encargo, se redacta como anexo aquí).
- El bot de WhatsApp del fundador (otro proyecto, fuera de la épica).
- Negociar alcance extra (redes, campañas, SEO clásico).

## Notas para el gate humano
- **Decisión a mirar**: el precio **no** se dice en la reunión; va en la propuesta escrita
  (tu decisión del 2026-09-28). Si en la reunión preguntan "¿cuánto cuesta?", el apoyo
  responde con la horquilla de D-7 y "te lo mando por escrito con todo el detalle".
  Alternativa: decirlo en el cierre como en SPEC-004 CA-5.
- **Pregunta abierta**: ¿los precios de D-7 son con o sin IVA? La propuesta tiene que
  decirlo.
- **Pregunta abierta**: la duración cuenta desde la primera acción (propuesta) o desde el
  pago. Propongo desde la primera acción, con la atribución instalada antes.
- La reunión puede prepararse ya en paralelo a SPEC-007; solo exige la pasada 1 hecha.
- **Enmienda 2026-09-29 — a mirar**: (1) la propuesta no menciona Galicia en absoluto
  (test simple y a prueba de despistes); si quieres poder decir "pacientes de toda
  Galicia para capilar" aunque sea sin compromiso, hay que relajar CA-3. (2) El área de
  influencia puede aparecer en la propuesta solo como dato que se informa, no como objetivo.
  (3) La respuesta de la clínica a "qué tratamientos queréis atraer de fuera" puede cambiar
  el set `AR`/`AG` solo si llega **antes** de la pasada 1 de SPEC-007 (después, el set está
  congelado y cualquier pregunta nueva se informa aparte).
