---
id: SPEC-009
tipo: spec
epica: EPIC-002
estado: en-progreso
aprobada-por: Alberto Fojo
historial:
  - {estado: borrador, fecha: 2026-09-28, por: sdd-arquitecto}
  - {estado: aprobada, fecha: 2026-09-28, por: Alberto Fojo}
  - {estado: bloqueada, fecha: 2026-09-29, por: sdd-arquitecto}
  - {estado: borrador, fecha: 2026-09-29, por: sdd-arquitecto}
  - {estado: aprobada, fecha: 2026-09-29, por: Alberto Fojo}
  - {estado: bloqueada, fecha: 2026-09-29, por: sdd-arquitecto}
  - {estado: borrador, fecha: 2026-09-29, por: sdd-arquitecto}
  - {estado: aprobada, fecha: 2026-09-29, por: Alberto Fojo}
  - {estado: en-progreso, fecha: 2026-09-29, por: sdd-implementador}
  - {estado: bloqueada, fecha: 2026-10-03, por: sdd-arquitecto}
  - {estado: borrador, fecha: 2026-10-03, por: sdd-arquitecto}
  - {estado: aprobada, fecha: 2026-10-03, por: Alberto Fojo}
  - {estado: en-progreso, fecha: 2026-10-03, por: sdd-implementador}
---
# SPEC-009 — Reunión de descubrimiento y propuesta para Clínica Ártica

> **Enmienda 2026-10-03 (e) (sdd-arquitecto) — revisión del PDF borrador por el humano.
> Requiere re-aprobación humana.** El humano (Alberto Fojo, 2026-10-03) revisó el PDF
> borrador de la propuesta (ledger, 2026-09-30) y decidió cuatro cambios que tocan CA y cinco
> que no. **Cambian CA**: (1) CA-3 y CA-10: Galicia aparece en la propuesta **solo** como
> ampliación posible del área de influencia ("…con margen para ampliarla al resto de
> Galicia"), nunca como objetivo ni con cifras (**ADR-011**, `aprobada` 2026-10-03, supera en parte ADR-009
> §3); (2) CA-3 y CA-9: el modelo de pago pasa a **450 € + IVA por los 3 primeros meses, por
> adelantado; a partir del cuarto mes 199 €/mes + IVA, sin permanencia** (**ADR-010**,
> `aprobada` 2026-10-03, supera en parte D-7; cierra F-SPEC-009-2 punto 3); (3) CA-3: desaparece la frase
> "Precios sin IVA: la factura suma el IVA vigente" (cierra F-SPEC-009-2 punto 2); (4) CA-4
> (d): la entrega del conteo semanal de "¿cómo nos has conocido?" pasa a ser **opcional**
> para la clínica, con la consecuencia dicha en CA-4 y en el ledger (condición C3 del
> dictamen; follow-up F-SPEC-009-8). Además CA-3 añade que la propuesta **nombra los
> asistentes** que se miden, y CA-4 (a) y (c) recogen los cambios 7 y 8 de abajo (medio del
> aviso; explicación llana de "repositorio público"). **Solo aplicación, sin cambio de CA**
> (lista cerrada para sdd-implementador): (5) portada: título "Atracción de clientes en
> asistentes de IA", subtítulo sin la coletilla "independientemente de…", correo de
> "Preparada por" = alberto@tremen.dev (clave `email_contacto` de `valores.json`, privado);
> (6) nombrar los asistentes (ChatGPT, Gemini y Claude: los del probe, D-5, SPEC-008); (7)
> anexo 1 (a): "avisa por escrito y con fecha" → "por email o cualquier otro medio con
> persistencia (WhatsApp, Telegram, etc.)"; (8) anexo 1 (c): explicación en lenguaje llano
> de qué es un repositorio público; (9) anexo 2: sin cambios salvo los derivados. **Aviso de
> espacio**: la propuesta rellenada está en ~440 palabras de 450; asistentes + Galicia +
> pago nuevo suman más de lo que quita "Precios sin IVA…" y la tabla de dos filas, así que el
> implementador tendrá que recortar en otro sitio para seguir en una página. CA-1, CA-2, CA-5
> (salvo la respuesta "¿Cuánto cuesta?" de `apoyo.md`, que dice el modelo nuevo), CA-6, CA-7 y
> CA-8 no cambian. La spec pasa `en-progreso` → `bloqueada` → `borrador` y espera nueva
> aprobación; con ella se aprueban ADR-010 y ADR-011 o se devuelven.

> **Enmienda 2026-09-29 (d) (sdd-arquitecto) — la propuesta cuenta el objetivo nuevo
> (ADR-009, aprobado). Cierra F-SPEC-009-1. Requiere re-aprobación humana.** El humano
> (Alberto Fojo, 2026-09-29) decidió que la propuesta **sí** cuenta a la clínica el Go
> "crecer fuera, defender dentro", **sin garantía y sin cifras**: "ya sois la clínica que la
> IA recomienda en A Mariña; el objetivo es aparecer también en el área de influencia
> (Ferrolterra, norte e interior de Lugo, occidente de Asturias) sin perder la comarca".
> Cambian CA-3 (objetivo y "cómo sabremos si funciona"), y por dependencia CA-1 (el bloque
> "cómo funciona" del guion dice el mismo objetivo), CA-5 (una objeción más) y CA-10 (sin
> promesa de aparecer en el área de influencia). Expectativas sin cambio (4–12 semanas, sin
> garantía). El nivel Galicia sigue **sin mencionarse** (ADR-005 §6 y ADR-009 §3). La spec
> pasa `aprobada` → `bloqueada` → `borrador` y espera nueva aprobación.

> **Nota 2026-09-29 (c) (sdd-arquitecto) — Go "crecer fuera, defender dentro" (ADR-009,
> borrador). No cambia ningún CA ni requiere re-aprobación por sí misma; deja una decisión
> pendiente.** *(Resuelta por la enmienda (d): F-SPEC-009-1 cerrado.)* Esta spec no promete "+15 pts en el núcleo" en ningún sitio, así que no hay
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
  pacientes; por la enmienda (d), dice el mismo objetivo que la propuesta de CA-3, sin
  garantía y sin cifras); acuerdos que se piden (CA-4); cierre (fecha concreta en la que llega la
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
- **CA-3 (propuesta de una página) [Agente]**: Dado D-7 superado en parte por ADR-010,
  cuando se publique la plantilla
  `docs/piloto-artica/reunion/propuesta.md`, entonces cabe en una página (≤ 450 palabras)
  y contiene, en lenguaje de clínica: **punto de partida y objetivo** (enmienda (d),
  ADR-009), con este sentido y sin cifras: "ya sois la clínica que la IA recomienda en
  A Mariña; el objetivo es aparecer también en el área de influencia (Ferrolterra, norte e
  interior de Lugo, occidente de Asturias) sin perder la comarca, cuando alguien pregunta
  por {tratamientos}, y saber cuántos pacientes llegan por ahí"; por la enmienda (e)
  (ADR-011), las tres zonas van seguidas, en la misma frase, de la ampliación posible con
  este literal: **"con margen para ampliarla al resto de Galicia"**; el objetivo va
  acompañado, en la misma sección o inmediatamente después, de que **no se garantiza**;
  **qué asistentes** se miden, por su nombre (enmienda (e)): ChatGPT, Gemini y Claude, los
  tres del probe (D-5; lote de SPEC-008), sin nombrar ninguno que no se mida; qué
  incluye (foto de partida, medición de pacientes desde el
  día uno, diagnóstico, acciones ejecutadas por Tremendev, medición semanal, informe cada
  15 días, reunión de cierre); qué aporta la clínica (contenidos, aprobación, pregunta en
  recepción —por la enmienda (e) coherente con CA-4 (d): la entrega del conteo es opcional y
  la propuesta no la presenta como obligación—, accesos); duración de 12 semanas desde la
  primera acción; **precio exacto de ADR-010** (enmienda (e)), que el cliente lee así, con el
  IVA explícito junto a cada importe: **450 € + IVA por los 3 primeros meses, pagados por
  adelantado; a partir del cuarto mes, 199 €/mes + IVA, y se puede dejar en cualquier
  momento (sin permanencia)**; no existe opción mensual durante los 3 primeros meses ni la
  frase "Precios sin IVA: la factura suma el IVA vigente"; expectativas (movimiento en 4–12
  semanas, sin garantía de aparecer ni de
  número de pacientes, también en el área de influencia); "cómo sabremos si funciona", en
  palabras llanas y sin umbrales numéricos, con las tres condiciones de ADR-009 (que os
  recomienden más en el área de influencia que al empezar; que en A Mariña no se pierda lo
  que ya tenéis; y que llegue al menos un paciente por esta vía); qué pasa al terminar
  (renovar o no, sin permanencia). Por la enmienda de 2026-09-29 (ADR-005 §6, ADR-009 §3) y
  la enmienda (e) (ADR-011): el nivel Galicia **no aparece** en la propuesta como objetivo,
  entregable, condición ni expectativa; la **única** aparición permitida de la palabra
  "Galicia" es el literal de ampliación de arriba, una vez, en la sección del objetivo.
  La enmienda (d) sustituye la regla anterior "el área de influencia, si aparece, solo como
  dato que se informa, sin objetivo": ahora es el objetivo, sin garantía. La propuesta no
  incluye ninguna cifra de visibilidad de la clínica (ADR-004); el punto de partida es un
  veredicto en palabras. No hay
  opción gratuita ni descuento sobre el precio de ADR-010; cualquier desviación exige
  decisión del humano
  registrada en el ledger antes del envío (la de ADR-010 ya lo está, 2026-10-03). *Evidencia*: conteo de palabras; checklist
  (objetivo con las tres zonas del área de influencia y "sin perder la comarca"; literal de
  ampliación a Galicia en la misma frase; "no se
  garantiza" junto al objetivo; ChatGPT, Gemini y Claude nombrados; las tres condiciones de
  "cómo sabremos"; 4–12 semanas; "pagados por adelantado", "a partir del cuarto mes" y
  "en cualquier momento" junto al precio);
  cifras de precio iguales a ADR-010 (solo 450 y 199, con "+ IVA" cada una) y sin "Pago
  mensual, 3 meses" ni "Precios sin IVA"; búsqueda de "Galicia" en `propuesta.md`:
  **exactamente una** coincidencia, dentro del literal de ampliación y en la sección "Punto
  de partida y objetivo"; búsqueda de `%` y de "puntos" en `propuesta.md`, sin coincidencias
  fuera del precio y el IVA.
- **CA-4 (acuerdos y consentimientos) [Agente]**: Dado que sin ellos no se puede medir ni
  publicar, cuando se publique `docs/piloto-artica/reunion/acuerdos.md` (anexo de la
  propuesta, para firmar o aceptar por escrito), entonces recoge: (a) la clínica avisa
  antes de cualquier cambio en web, fichas, directorios o campañas
  durante el piloto, propio o de su agencia, **por email o cualquier otro medio con
  persistencia (WhatsApp, Telegram, etc.)** (enmienda (e); sustituye a "por escrito, con
  fecha": el medio persistente deja la fecha); (b) consentimiento de acceso a analítica,
  Search Console, Google Business Profile y gestor de la web, con el rol mínimo y
  revocable (ADR-004 §5); (c) consentimiento para aparecer con su nombre en el repositorio
  público, explicando **primero, en lenguaje llano y para no técnicos, qué es un repositorio
  público** (enmienda (e): un sitio en internet donde cualquiera puede leer los ficheros y su
  historial de versiones), qué se publica y qué no (ADR-004 §1–§3) y que el historial no se
  borra si se revoca (§6); (d) que Tremendev no recibe datos de pacientes, solo conteos
  semanales agregados (RN-09); por la enmienda (e), **la entrega del conteo semanal de
  "¿cómo nos has conocido?" es opcional para la clínica**: el acuerdo lo dice así y dice la
  consecuencia, sin inventar alternativa: si la clínica no entrega el conteo, la condición
  "que llegue al menos un paciente por esta vía" de "cómo sabremos si funciona" **no se puede
  medir por esa vía** (lo que se mida por otras vías lo fijan SPEC-010 y SPEC-012; follow-up
  F-SPEC-009-8); si lo entrega, sigue siendo solo el conteo semanal por opción, sin día ni
  tratamiento, con las condiciones C3 del dictamen de CA-6; (e) que ningún contenido se
  publica sin aprobación escrita
  de la clínica y sin la revisión normativa de SPEC-011 CA-7; y lo que añada el dictamen de
  CA-6. *Evidencia*: checklist (incluye "opcional" y la consecuencia en (d), el medio
  persistente en (a) y la explicación llana en (c)); trazabilidad a ADR-004 y al dictamen.
- **CA-5 (apoyo y objeciones de cliente cálido) [Agente]**: Dado un fundador que se
  bloquea, cuando se publique `docs/piloto-artica/reunion/apoyo.md` (una página), entonces
  contiene respuestas literales a ≥ 8 objeciones, incluidas: "¿me garantizas salir el
  primero?", "¿cuántos pacientes me vas a traer?", "somos amigos, ¿no me lo haces gratis?",
  "¿por qué no empezamos ya y lo hablamos luego?", "la web la lleva otra persona/agencia",
  "¿y si ChatGPT cambia?", "¿podemos poner precios / antes y después?" (remite a la
  revisión normativa, sin afirmar que se pueda), "¿esto no es SEO?" y (enmienda
  2026-09-29) "¿y saldremos cuando alguien de Coruña o Vigo busque un injerto capilar?"
  (respuesta honesta: se mide y se informa, compiten cadenas con varias sedes y no se
  promete); por la enmienda (d), "¿y si por buscar pacientes fuera perdemos lo que ya
  tenemos en A Mariña?" (respuesta: la comarca se sigue midiendo cada semana y no perderla
  es parte de cómo sabremos si funciona; sin garantía); y ≥ 4 frases para
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
  ledger registra: fecha de envío; respuesta (acepta / negocia / rechaza; enmienda (e),
  ADR-010: ya no hay opción mensual de entrada) con fecha; fecha de aceptación de los
  acuerdos y del consentimiento de
  nombre (sin nombre de la persona que firma); si la clínica acepta entregar el conteo
  semanal de recepción (sí/no, CA-4 (d)); fecha del primer cobro (los 3 primeros meses por
  adelantado). El piloto **no
  empieza** (SPEC-010 ni primera acción) sin aceptación escrita y primer cobro.
  *Evidencia*: fechas en el ledger; documentos en el espacio privado.
- **CA-10 (sin jerga ni datos personales) [Verificador]**: Dado D-3 y ADR-004, cuando se
  revisen los textos de `docs/piloto-artica/reunion/`, entonces no aparecen "AEO", "GEO",
  "SoV", "share of voice", "LLM", "visibilidad en IA" ni "posicionamiento garantizado",
  ni una promesa de aparecer en el nivel Galicia (ADR-005 §6; por la enmienda (e) y
  ADR-011, el literal de ampliación de CA-3 no es promesa y es la única mención de Galicia
  admitida en `propuesta.md`; en `guion.md` y `apoyo.md` Galicia solo aparece como hoy, en
  una pregunta de conducta pasada y en una objeción respondida con "no te lo prometo"), ni
  (enmienda (d)) una
  promesa o garantía de aparecer en el área de influencia o de mantener la comarca, ni
  cifras de visibilidad de la clínica (ADR-004), y
  no hay emails, teléfonos (salvo marcadores `{…}`) ni nombres de persona. *Evidencia*:
  búsqueda por script, sin coincidencias (el detector de promesas sobre Galicia no se relaja:
  si el literal de ampliación lo disparase, se cambia la redacción del literal con decisión
  del humano, no el detector); revisión de que toda mención de "garantiz…" o
  "aseguramos" en los textos es negativa ("no se garantiza").

## Entidades y reglas afectadas
- Dominio: Clinic, Provider (como "asistente"), AttributionEvent, Action (qué hace cada
  parte).
- D-3 (se vende pacientes, no visibilidad), D-5 (asistentes del probe), D-7 (precio;
  superado en parte por ADR-010, enmienda (e)), D-8 (idioma), RN-07, RN-09.
- ADR-003, ADR-004, ADR-005 (§6: el nivel Galicia no se promete), ADR-009 (Go "crecer en
  `AR`, defender `AV`, ≥ 1 paciente"; la propuesta lo cuenta sin garantía, enmienda (d)),
  ADR-010 (modelo de pago, enmienda (e)), ADR-011 (Galicia solo como ampliación posible,
  enmienda (e)). Reutiliza las reglas de SPEC-004 CA-3, CA-4, CA-6, CA-11 y CA-12 sin
  copiar sus ficheros. Depende de SPEC-007 CA-5 y CA-10.

## Fuera de alcance
- Contrato mercantil formal más allá de la propuesta y los acuerdos aceptados por escrito
  (si el dictamen de CA-6 exige un contrato de encargo, se redacta como anexo aquí).
- El bot de WhatsApp del fundador (otro proyecto, fuera de la épica).
- Negociar alcance extra (redes, campañas, SEO clásico).

## Notas para el gate humano
- **Decisión a mirar**: el precio **no** se dice en la reunión; va en la propuesta escrita
  (tu decisión del 2026-09-28). Si en la reunión preguntan "¿cuánto cuesta?", el apoyo
  responde con el modelo de ADR-010 (enmienda (e); antes, la horquilla de D-7) y "te lo
  mando por escrito con todo el detalle".
  Alternativa: decirlo en el cierre como en SPEC-004 CA-5.
- **Pregunta abierta**: ¿los precios de D-7 son con o sin IVA? La propuesta tiene que
  decirlo.
- **Pregunta abierta**: la duración cuenta desde la primera acción (propuesta) o desde el
  pago. Propongo desde la primera acción, con la atribución instalada antes.
- La reunión puede prepararse ya en paralelo a SPEC-007; solo exige la pasada 1 hecha.
- **Enmienda 2026-09-29 — a mirar**: (1) la propuesta no menciona Galicia en absoluto
  (test simple y a prueba de despistes); si quieres poder decir "pacientes de toda
  Galicia para capilar" aunque sea sin compromiso, hay que relajar CA-3. (2) ~~El área de
  influencia puede aparecer en la propuesta solo como dato que se informa, no como
  objetivo.~~ Sustituido por la enmienda (d): es el objetivo, sin garantía.
  (3) La respuesta de la clínica a "qué tratamientos queréis atraer de fuera" puede cambiar
  el set `AR`/`AG` solo si llega **antes** de la pasada 1 de SPEC-007 (después, el set está
  congelado y cualquier pregunta nueva se informa aparte).
- **Enmienda (d), 2026-09-29 — a mirar para re-aprobar**: (1) "ya sois la clínica que la
  IA recomienda en A Mariña" es una afirmación sobre la clínica: se apoya en el baseline
  oficial (aviso de techo, SPEC-008 CA-10) y, si se enseña como dato del probe, en la regla
  de SPEC-007 CA-7 (calibración). Si la calibración dijera que app y probe no coinciden, la
  frase se revisa antes de enviar. (2) "Cómo sabremos si funciona" nombra las tres
  condiciones de ADR-009 en llano y sin umbrales: los umbrales de `sdd-metricas` (SPEC-008
  CA-11) son criterio interno y no se cuentan. (3) Nueva objeción en CA-5 ("¿perdemos
  A Mariña?"). (4) ~~Galicia sigue fuera de la propuesta con el mismo test de búsqueda.~~
  Sustituido por la enmienda (e): una sola mención literal, como ampliación posible.
- **Enmienda (e), 2026-10-03 — a mirar para re-aprobar** (con ADR-010 y ADR-011, ambos
  `aprobada` el 2026-10-03 por Alberto Fojo junto con esta spec):
  (1) **Alcance de ADR-010**: tal como está escrito, el modelo nuevo (450 € prepago los 3
  primeros meses; después 199 €/mes sin permanencia) sustituye a la fórmula de D-7 como
  **ancla de pilotos**, no solo para Clínica Ártica. Si lo quieres acotado a EPIC-002, dilo y
  se recorta §4 antes de aprobarlo. (2) **Literal de Galicia** (ADR-011 §1 y CA-3): "con
  margen para ampliarla al resto de Galicia", una vez, pegado a las tres zonas. Si prefieres
  otra redacción, tiene que seguir siendo una frase fija (es lo que hace el test
  comprobable) y no disparar el detector de promesas de CA-10. (3) **Conteo opcional (CA-4
  (d))**: la consecuencia que se escribe es solo "sin conteo, la condición 'al menos un
  paciente' no se puede medir por esa vía". No se ha inventado una vía alternativa; queda
  F-SPEC-009-8 para SPEC-010/SPEC-012. Mira también si la pregunta en recepción sigue en
  "qué aportáis vosotros" de la propuesta (CA-3 la deja como aportación no obligatoria,
  coherente con (d)) o prefieres quitarla de esa lista. (4) **Asistentes nombrados** (CA-3):
  ChatGPT, Gemini y Claude, los del probe. Google (AI Overviews / Modo IA) solo se mira a
  mano en `AR` (SPEC-007) y no se nombra para no prometer un canal que el probe no mide; si
  quieres nombrarlo, hay que decir "a mano, sin compromiso". (5) **Medio del aviso (CA-4
  (a))**: "por escrito, con fecha" pasa a "email o cualquier otro medio con persistencia
  (WhatsApp, Telegram…)"; la fecha la da el medio. (6) **Espacio**: la propuesta rellenada
  está en ~440 palabras de 450; el implementador tendrá que recortar en otro sitio.
