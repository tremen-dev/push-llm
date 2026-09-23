---
id: SPEC-004
tipo: spec
epica: EPIC-001
estado: borrador
aprobada-por:
historial:
  - {estado: borrador, fecha: 2026-09-23, por: sdd-arquitecto}
---
# SPEC-004 — Kit de contacto y entrevista para un fundador no comercial

> Spec **documental**. Un agente redacta todo el kit; el humano aprueba el tono,
> hace el ensayo y envía. El kit vive en el repo en `docs/ciclo-0/kit/` **sin datos
> de ninguna persona**; contactos, registro de envíos y notas viven en el espacio
> privado (ADR-001). Material de cliente en castellano (D-8).

## Problema
El fundador **no es comercial** y lo ha dicho explícitamente (EPIC-001). Para
conseguir 10 entrevistas de problema necesita escribir en frío a clínicas y
agencias y conducir conversaciones de 20 minutos sin improvisar. El riesgo es
doble: no conseguir respuesta, o conseguir conversaciones corteses que no
distinguen curiosidad de disposición a pagar (riesgo "sesgo por enseñar datos
primero" de la épica). El kit tiene que ser usable por alguien que nunca ha hecho
una entrevista de venta: textos literales, guion para leer, frases para silencios
y objeciones, cierre explícito, y preguntas sobre **conducta pasada y gasto actual**
(estilo *The Mom Test*), no sobre intenciones futuras.

## Usuarios / roles afectados
- Humano (fundador): usa el kit, ensaya, envía, entrevista.
- Interlocutores: dirección/gerencia de clínicas; responsables de agencias de
  marketing sanitario.
- Agente: redacta. Consultadas: `sdd-sanidad-regulacion` (dictamen obligatorio,
  CA-9); `sdd-visibilidad-local` opcional para el vocabulario del bloque de dato.
- sdd-verificador: comprueba cada CA contra los ficheros del kit.

## Criterios de aceptación
- **CA-1 (lista de objetivos)**: Dado `03-local-market-vigo-pontevedra.md` §4–§5 y el
  veredicto de SPEC-002, cuando se publique `docs/ciclo-0/kit/objetivos.md`, entonces
  lista **a nivel de clínica/agencia** (nombre comercial, especialidad, ciudad, web
  pública, motivo, prioridad, tanda) al menos: 10 dental, 5 estética, 5
  fertilidad/oftalmología (sin hospitales, D-2) y 4 agencias (AMG, Hydra, Quality
  Marketing Contents y al menos una más con fuente pública citada); el orden explica su
  criterio (`03-…md` §4 ajustado por la fuerza del hallazgo del probe); toda clínica
  listada existe en `brands.csv`; no contiene nombres, emails ni teléfonos de personas.
  *Evidencia*: recuento por segmento; cruce automático con `brands.csv`; búsqueda de
  patrones de email/teléfono sin coincidencias.
- **CA-2 (mensajes de primer contacto)**: Dado el enfoque datos primero, cuando se
  publique `docs/ciclo-0/kit/mensajes.md`, entonces contiene textos literales con
  marcadores `{…}` para: email a clínica, email a agencia, LinkedIn a clínica y a
  agencia (nota de conexión ≤ 200 caracteres + mensaje tras aceptar), seguimiento 1
  (a los 4–5 días hábiles) y seguimiento 2 y último (a los 10); y cada texto: abre con
  el `{hallazgo}` de SPEC-003 CA-4 en sus dos primeras frases; dice quién escribe y de
  dónde sale el dato; dice explícitamente que no se vende nada; pide una sola cosa
  (20 minutos, con dos franjas concretas o un enlace de agenda); incluye la frase de
  baja o la información que exija el dictamen de CA-9; no menciona precio ni producto;
  emails ≤ 120 palabras. Incluye un ejemplo relleno con una clínica ficticia.
  *Evidencia*: checklist por texto; conteo de palabras y caracteres por script.
- **CA-3 (guion para leer)**: Dado un entrevistador sin experiencia, cuando se publique
  `docs/ciclo-0/kit/guion.md`, entonces tiene variante clínica y variante agencia, cada
  una con bloques de texto **literal** y minutaje que suma ≤ 20 min: apertura (quién
  soy, por qué te escribí, no vendo nada, 20 minutos, permiso para tomar notas); bloque
  de dato (enseñar el extracto y callar); preguntas en orden; cierre (CA-5). Ningún
  bloque es una instrucción sin texto ("improvisa", "presenta el producto").
  *Evidencia*: revisión estructural; suma de minutaje.
- **CA-4 (preguntas estilo Mom Test)**: Dado el guion, cuando se revisen sus preguntas,
  entonces la variante clínica tiene ≥ 8 preguntas sobre conducta pasada o gasto
  actual que cubren al menos: cómo llegó el último paciente nuevo del tratamiento
  estrella; cómo saben hoy de dónde viene un paciente (señal de atribución, H3); gasto
  mensual actual en captación por partida (agencia, anuncios, directorios); última
  acción de marketing pagada, cuánto costó y quién la decidió; valor de un paciente
  nuevo del tratamiento estrella; si algún paciente ha mencionado ChatGPT u otro
  asistente. La variante agencia tiene ≥ 8 que cubren al menos: qué venden hoy a
  clínicas y a qué precio mensual; si algún cliente ha preguntado por IA; qué han hecho
  ya; cómo incorporaron la última herramienta de terceros y quién la paga (H4). Fuera
  del cierre no hay preguntas hipotéticas o de intención futura ("¿pagarías…?",
  "¿te interesaría…?", "¿usarías…?"). *Evidencia*: checklist de cobertura; búsqueda
  de los patrones prohibidos fuera del bloque de cierre, sin coincidencias.
- **CA-5 (cierre explícito)**: Dado que el criterio Go mide disposición a pagar, cuando
  se lea el bloque de cierre, entonces contiene, literal: agradecimiento; **una única
  frase de precio** con el ancla de D-7 (199 €/mes) presentada como dato, no como
  oferta; una petición de compromiso concreto que la hoja de puntuación (CA-7) sabe
  registrar (p. ej. recibir la propuesta de piloto en el Ciclo 1 con fecha, o presentar
  a quien decide); y la petición de a quién más debería ver. *Evidencia*: revisión del
  bloque contra esta lista; trazabilidad cierre → campo de la hoja.
- **CA-6 (frases de apoyo)**: Dado un entrevistador que se bloquea, cuando se publique
  `docs/ciclo-0/kit/apoyo.md` (una página, imprimible), entonces contiene ≥ 6 frases
  para silencios o respuestas vagas que devuelven a hechos pasados ("Cuéntame la última
  vez que…", "¿Y cuánto os costó?") y respuestas literales a ≥ 8 objeciones, incluidas:
  "¿qué vendes / cuánto cuesta?", "ya tenemos agencia", "los pacientes nos vienen por
  el boca a boca", "¿cómo lo arreglo?" (sin consultoría gratis), "mándamelo por email",
  "no tengo tiempo", "¿esto es fiable si ChatGPT cambia cada vez?" y "¿de dónde has
  sacado mis datos?" (con la respuesta que fije el dictamen de CA-9). *Evidencia*:
  recuento y checklist.
- **CA-7 (plantilla de notas y hoja de puntuación, fijadas ex ante)**: Dado el riesgo de
  confundir cortesía con demanda, cuando se publiquen `plantilla-notas.md` y
  `hoja-puntuacion.md` (o `.csv`), entonces: la plantilla usa pseudónimo `Enn` y
  segmento, sin campo para nombre ni contacto; la hoja define por entrevista campos
  separados de **curiosidad** y de **señal de pago**, donde señal de pago = (A) gasto
  actual declarado ≥ 150 €/mes en al menos una partida concreta de captación o
  marketing con importe (en agencias: servicios mensuales ≥ 150 € a clínicas que
  incluyen herramientas de terceros) **y** (B) compromiso concreto aceptado en el
  cierre tras oír el precio; más campos de atribución actual (H3), interés de reventa
  (H4) y cita clave parafraseada. La hoja lleva fecha de congelación anterior a la
  primera entrevista; cualquier cambio posterior se registra con motivo y obliga a
  repuntuar todas. *Evidencia*: revisión de campos; fecha de congelación en el ledger.
- **CA-8 (procedimiento de uso)**: Dado que nada se improvisa, cuando se publique
  `docs/ciclo-0/kit/como-usar.md` (≤ 1 página), entonces describe paso a paso: dónde
  vive cada cosa (repo vs `PUSHLLM_PRIVADO`), tandas de envío, calendario de
  seguimientos (máximo 2, después se para), qué hacer al recibir un "sí", cómo tomar y
  guardar notas en ≤ 48 h, y el **punto de control**: si a los 10 días hábiles del primer
  envío hay < 5 entrevistas agendadas, se para y se revisa mensaje o canal con el
  orquestador. *Evidencia*: checklist.
- **CA-9 (dictamen normativo antes del primer envío)**: Dado el riesgo abierto sobre
  comunicaciones comerciales no solicitadas y RGPD, cuando el kit esté redactado,
  entonces consta en el ledger un dictamen de `sdd-sanidad-regulacion` (fecha,
  conclusión por punto, fuentes y condiciones) que cubre al menos: envío de emails en
  frío a clínicas y agencias; mensajes por LinkedIn; base jurídica e información a dar
  al tratar datos de contacto de profesionales; contenido del extracto de SPEC-003
  (nombrar competidores, publicidad sanitaria); toma de notas y posible grabación;
  plazo de conservación de notas nominales. Cada condición del dictamen está mapeada
  en una tabla condición → fichero/cambio del kit, y un canal que el dictamen desaconseje
  se retira del kit. El arquitecto **no** fija la normativa en esta spec. *Evidencia*:
  dictamen + tabla de trazabilidad en el ledger.
- **CA-10 (envío bloqueado)**: Dado que el kit no está listo sin dictamen, extracto ni
  ensayo, cuando se envíe el primer mensaje real, entonces su fecha (registro privado
  de envíos, reportada en el ledger) es posterior a las de CA-9, CA-11 y SPEC-003 CA-9, y
  cada objetivo de la primera tanda tiene su extracto generado. *Evidencia*: fechas en
  el ledger; recuento de extractos frente a la tanda. **Acción humana.**
- **CA-11 (ensayo)**: Dado un fundador sin experiencia de ventas, cuando el kit esté
  terminado, entonces el humano hace al menos un ensayo completo en voz alta (con un
  agente o una persona haciendo de director de clínica que pone ≥ 3 objeciones de CA-6),
  cronometrado en ≤ 22 min, y los cambios que salgan se incorporan al kit. *Evidencia*:
  fecha, duración y lista de cambios en el ledger. **Acción humana.**
- **CA-12 (sin jerga ni datos personales)**: Dado D-3 ("pacientes desde ChatGPT", no
  "visibilidad en IA") y ADR-001, cuando se revisen los textos dirigidos a clínicas y
  agencias, entonces no aparecen "AEO", "GEO", "SoV", "share of voice", "LLM",
  "visibilidad en IA" ni "posicionamiento garantizado"; y en todo `docs/ciclo-0/kit/`
  no hay emails ni teléfonos (salvo marcadores `{…}`) ni nombres de persona.
  *Evidencia*: búsqueda por script, sin coincidencias.

## Entidades y reglas afectadas
- Dominio: Clinic, Speciality, Provider (como "asistente" en texto de cliente),
  AttributionEvent (preguntas de H3, solo como conducta actual).
- D-2 (segmentos y exclusión de hospitales), D-3 (mensaje), D-7 (ancla de precio en el
  cierre), D-8 (idioma). RN-09 no aplica a interlocutores B2B: los cubre ADR-001 y el
  dictamen de CA-9.
- ADR-001. Depende de SPEC-003 (gancho y extractos) y SPEC-002 (orden de objetivos).

## Fuera de alcance
- Vender, cobrar o enviar propuestas de piloto (Ciclo 1).
- Teléfono y visita en frío (descartados en EPIC-001; se reabren solo tras el punto de
  control de CA-8).
- Entrevistas a escuelas de negocio (nicho secundario).
- Plantilla del informe completo con marca (Ciclo 1).
- Automatizar envíos (mail merge, secuencias): se envían a mano.

## Notas para el gate humano
- **Decisión a mirar con lupa (CA-5 y CA-7)**: el criterio Go de la épica ("pagarían
  > 150 €/mes") es una intención futura, justo lo que *The Mom Test* dice que no hay que
  creer. Lo operacionalizo como **gasto actual ≥ 150 €/mes + compromiso concreto tras
  oír un precio de 199 €/mes** dicho una sola vez en el cierre. Eso implica mencionar
  precio sin vender; alternativa: no decir precio y medir solo gasto actual (señal más
  débil). Cambia qué cuenta para el Go.
- Mencionar el ancla de D-7 en el Ciclo 0 no la valida: D-7 sigue "pendiente de validar
  en el Ciclo 1".
- **Dictamen normativo (CA-9)**: no he fijado normativa; sin dictamen no se envía nada.
  Si el dictamen descarta el email en frío, el kit se queda en LinkedIn/red personal y
  la tasa de respuesta es el riesgo principal.
- ¿Variante en gallego de los mensajes? D-8 lo permite; propongo castellano y decidir
  tras las primeras respuestas.
- Qué produce el agente: todos los ficheros del kit y la lista a nivel de clínica.
  Qué hace el humano: aprobar el tono, reunir contactos de personas (privado), ensayar
  (CA-11), enviar (CA-10).
- La redacción (CA-2 a CA-8, CA-12) puede empezar ya, en paralelo con SPEC-001/002;
  CA-1 necesita el veredicto de SPEC-002 y CA-10 los extractos de SPEC-003.
