---
id: SPEC-009
tipo: ledger
epica: EPIC-002
---
# Ledger — SPEC-009 Reunión de descubrimiento y propuesta para Clínica Ártica

## Resumen
- Fase: <!-- refleja el estado de la spec; la fuente de verdad es el frontmatter de la spec -->
- Rama: `ft/SPEC-009-reunion-y-propuesta` (desde `main`, que ya incluye `design/tremen-ds`).
  El nombre previsto era `ft/SPEC-009-reunion-de-descubrimiento-y-propuesta-para-clinica-artica`.

## Matriz de criterios de aceptación
<!-- Escritores: sdd-implementador rellena Implementado y Test; sdd-verificador rellena Verif. y Estado. Nunca al revés. -->
<!-- Estados por CA: ✅ cerrado · ⚠️ parcial/con salvedad · 🚧 en curso · ❌ sin empezar · n-a -->
<!-- Un CA está ✅ solo cuando Implementado + Test + Verif. aplicables están en verde. Una salvedad se marca ⚠️, nunca ✅. -->
| CA | Implementado (fichero) | Test (fichero/caso) | Verif. | Estado |
|---|---|---|---|---|
| CA-1 | `docs/piloto-artica/reunion/guion.md` (plantilla, 6 bloques con texto literal, 44 min); versión personalizada en privado `reunion/guion-artica.md` (44 min) | `docs/piloto-artica/tools/tests/test_meeting_kit.py`: `test_ca1_minutes_add_up_to_at_most_45`, `test_ca1_required_blocks_in_order`, `test_ca1_every_block_has_literal_text`, `test_ca1_block_contents`, `test_ca1_block_parser_on_synthetic_text`; privado: `meeting_docs.py check --solo --privado` → OK | | ❌ |
| CA-2 | `guion.md` bloque 3: P1–P16 (privado: P1–P18, sin repetir lo ya respondido en la llamada del 28/09 del otro proyecto) | `test_ca2_at_least_12_questions`, `test_ca2_coverage_checklist` (16 temas de CA-2, mapa en `meeting_docs.QUESTION_TOPICS`), `test_ca2_no_hypothetical_questions`, `test_ca2_hypothetical_detector` | | ❌ |
| CA-3 | `reunion/propuesta.md` (enmienda (e): 395 palabras la plantilla; 443 rellenada en privado; literal de Galicia en el objetivo, ChatGPT/Gemini/Claude en el callout, precio de ADR-010, pregunta en recepción no obligatoria); `meeting_docs.py` (`proposal_issues`, `GALICIA_LITERAL`, `ASSISTANTS`, `_galicia_issues`); PDF con `doc.css` (`meeting_docs.py build` + `build_pdf.mjs`): portada (título nuevo) + **1 página** de propuesta + anexos; borrador en privado `reunion/propuesta/propuesta-borrador.pdf` | `test_ca3_proposal_passes_its_checklist`, `test_ca3_proposal_fits_in_one_page`, `test_ca3_prices_equal_adr010`, `test_ca3_old_price_wording_is_flagged`, `test_ca3_no_galicia_no_percent_no_points` (Galicia una vez, literal, sección), `test_ca3_galicia_outside_the_literal_or_twice_is_flagged`, `test_ca3_galicia_literal_is_not_a_promise`, `test_ca3_names_the_assistants`, `test_ca3_reception_question_is_not_an_obligation`, `test_ca3_no_free_option_or_discount`, `test_ca3_checklist_detects_a_bad_proposal`, `test_ca3_word_count_ignores_markup_and_comments`, `test_filled_checks_apply_to_the_filled_proposal`, `test_build_document_is_self_contained_and_filled` (portada) | | ❌ |
| CA-4 | `reunion/acuerdos.md` (anexo 1: a–e de la spec + f cookies, g al terminar, del dictamen; enmienda (e): (a) email o medio con persistencia, (c) explicación llana de repositorio público, (d) conteo opcional con su consecuencia); `reunion/encargo-tratamiento.md` (anexo 2, sin cambios); `guion.md` bloque 5 (conteo opcional) | `test_ca4_agreements_cover_a_to_e_and_dictamen` (claves nuevas en `AGREEMENT_CHECKS`), `test_ca4_amendment_e_wording`, `test_ca4_traceability_to_adr004_and_dictamen` | | ❌ |
| CA-5 | `reunion/apoyo.md` (12 objeciones con respuesta literal, 6 frases para volver a hechos; "¿Cuánto cuesta?" con el modelo de ADR-010); privado `reunion/apoyo-artica.md` (14 objeciones, mismo cambio) | `test_ca5_at_least_8_objections_including_the_required_ones`, `test_ca5_every_objection_has_a_literal_answer`, `test_ca5_required_answers_say_what_the_spec_asks` (exige prepago, cuarto mes y sin permanencia), `test_ca5_at_least_4_back_to_facts_phrases` | | ❌ |
| CA-6 | Dictamen de `sdd-sanidad-regulacion` en este ledger (sección "Dictamen sdd-sanidad-regulacion (CA-6)") con tabla condición → cambio; cambios en `acuerdos.md`, `encargo-tratamiento.md`, `guion.md`, `apoyo.md` y hoja de hallazgo privada; los de SPEC-010/SPEC-011 como follow-ups | `test_ca6_processor_contract_has_article_28_content`, `test_ca6_proposal_and_agreements_reference_the_processor_contract`, `test_ca4_agreements_cover_a_to_e_and_dictamen` (claves "dictamen: …") | | ❌ |
| CA-7 | [Humano] pendiente: instrucciones en "Pasos humanos" | — | | ❌ |
| CA-8 | [Humano] pendiente | — | | ❌ |
| CA-9 | [Humano] pendiente | — | | ❌ |
| CA-10 | Todas las plantillas de `docs/piloto-artica/reunion/` (enmienda (e): `GALICIA_PROMISE_RE` sin cambios; el literal de ampliación no lo dispara) | `test_ca10_no_jargon_or_personal_data[*]` (6 ficheros), `test_ca3_galicia_literal_is_not_a_promise`, `test_ca10_detector`, `test_ca10_allows_negative_guarantees_markers_and_plan_numbers`, `test_ca10_private_person_names_absent_from_repo` (lee los nombres de `valores.json` privado; se salta sin `PUSHLLM_PRIVADO`); `meeting_docs.py check` → OK | | ❌ |

## Registro del implementador (2026-09-30, sdd-implementador)
Solo veredictos y rutas (ADR-004 §2). Commit de la implementación: `fdef4d8`.

**Entregables en el repo** (plantillas y herramientas, sin datos de la clínica):
- `docs/piloto-artica/reunion/`: `README.md`, `guion.md`, `apoyo.md`, `propuesta.md`,
  `acuerdos.md`, `encargo-tratamiento.md`.
- `docs/piloto-artica/tools/meeting_docs.py` (comprobaciones de CA-1 a CA-5 y CA-10; relleno de
  marcadores; generador de un HTML autocontenido con `design/tremen-ds`: `colors_and_type.css`,
  `nav.css`, `eyebrows.css`, `stamp.css` y `doc.css` en línea, cuerpo `.v-papel`, portada
  `.v-tremendo`, Paged.js), `docs/piloto-artica/tools/build_pdf.mjs` (mismo enfoque que el
  `build-pdf.mjs` de otra propuesta de tremen.dev (proyecto `artica`): Playwright si lo encuentra, si no Chrome
  headless) y `docs/piloto-artica/tools/tests/test_meeting_kit.py`.
- Consejos del README de `tremen-ds` respetados: sin `white-space: nowrap` en tablas, fuentes
  cargadas antes de paginar, sin Mermaid (no hace falta en una página).

**Entregables en privado** (`$PUSHLLM_PRIVADO/piloto-artica/reunion/`): `valores.json`
(valores de los marcadores; `_pendiente` y `_personas`), `guion-artica.md`, `apoyo-artica.md`,
`hoja-hallazgo.md` (copia de la de SPEC-007 CA-10 con el ajuste de la condición C6) y
`propuesta/` (`propuesta.md`, `acuerdos.md`, `encargo-tratamiento.md`, `propuesta.html`,
`propuesta-borrador.pdf`: 6 páginas = portada, 1 de propuesta, anexos).

**Frontera (ADR-004)**: en el repo, plantillas con marcadores `{…}`, herramientas y este ledger.
En privado, todo lo rellenado. El único enunciado sobre la clínica en la plantilla es el que fija
la propia spec ("ya sois la clínica que la IA recomienda en A Mariña"): es un veredicto sin cifra,
ya público en EPIC-002 y ADR-009, y ADR-004 §3 permite veredictos sin cifras. El matiz ("no en
todas las respuestas…") y los tratamientos van en marcadores rellenados en privado. Los
generadores se niegan a escribir dentro del repo.

**Apoyo del punto de partida**: veredicto `AV` de calibración "coinciden de forma razonable: sí"
(SPEC-007 CA-7, justo y sensible a la ubicación): la frase comercial queda apoyada con la cautela
del matiz. La propuesta no contiene ninguna cifra del probe (SPEC-007 CA-7) ni de la pasada
manual.

**Fuentes consultadas del otro proyecto de tremen.dev con la clínica** (solo lectura; nada de su
contenido entra en el repo): `D:\src\tremen-dev\artica\docs\interno\analisis_clinica_artica.md`,
`…\interno\preguntas_llamada_artica.md`, `…\interno\supuestos_y_datos_por_verificar.md`,
`…\cliente\cumplimiento_normativo.md`, `…\interno\plan_validacion_y_kpis.md`,
`…\decisiones\0003`, `0004`, `0006`, `0007`, `0009`, `…\cliente\resumen_ejecutivo.md` y
`…\cliente\propuesta\index.html` + `build-pdf.mjs`. Uso: no repetir en la reunión lo ya
respondido, mismo tono, sinergia de medición (en privado).

**Desviaciones de D-7**: ninguna. 450 € + IVA (3 meses, prepago) o 199 €/mes + IVA (3 meses);
sin opción gratuita ni descuento; sin paquete ni precio combinado con otros servicios.

## Registro del implementador (2026-10-03, enmienda (e), sdd-implementador)
Solo veredictos y rutas (ADR-004 §2). Aplica la lista cerrada de la enmienda (e) con ADR-010 y
ADR-011 aprobados.

- **Repo**: `docs/piloto-artica/reunion/propuesta.md` (título de portada "Atracción de clientes
  en asistentes de IA", subtítulo sin la coletilla de independencia; literal de ampliación a
  Galicia en el objetivo; ChatGPT, Gemini y Claude en el callout "No se garantiza"; pregunta en
  recepción como aportación no obligatoria; precio de ADR-010 en texto, sin tabla ni "Precios sin
  IVA"), `acuerdos.md` ((a), (c), (d)), `apoyo.md` ("¿Cuánto cuesta?"), `guion.md` (bloque 5,
  punto cuatro: conteo opcional y su consecuencia), `README.md` ("precio de ADR-010"),
  `docs/piloto-artica/tools/meeting_docs.py` (`proposal_issues`, `AGREEMENT_CHECKS`) y
  `docs/piloto-artica/tools/tests/test_meeting_kit.py`. `encargo-tratamiento.md` sin cambios: su
  §4 no menciona el conteo y §6 sigue valiendo si la clínica lo entrega.
- **Privado**: `valores.json` (`email_contacto` nuevo), `apoyo-artica.md` ("¿Cuánto cuesta?"),
  `guion-artica.md` (punto cuatro del bloque 5 y correo del cierre, coherente con
  `email_contacto`), `propuesta/` regenerada (`propuesta.md`, `acuerdos.md`,
  `encargo-tratamiento.md`, `propuesta.html`, `propuesta-borrador.pdf`).
- **Veredictos**: pytest de `docs/piloto-artica/tools/tests` verde (351, con `PUSHLLM_PRIVADO`
  definido, sin saltos); `ruff` limpio; `meeting_docs.py check` OK; `check --solo --privado` de
  las copias privadas OK. Propuesta rellenada ≤ 450 palabras y PDF revisado a ojo: 6 páginas,
  portada con título y correo nuevos, propuesta en **una** página con hueco libre, fuentes
  cargadas, anexo 1 con los textos nuevos. El literal de Galicia **no** dispara
  `GALICIA_PROMISE_RE` (detector sin cambios).
- **Desviación de redacción (sin cambio de fondo)**: en el acuerdo (a) el medio va al final de la
  frase ("avisa antes de cualquier cambio en …, lo haga la clínica o su agencia, por email o
  cualquier otro medio con persistencia (WhatsApp, Telegram, etc.)") para conservar la clave
  `antes de cualquier cambio` que la lista cerrada pedía mantener; la redacción propuesta la
  partía en dos.
- **Ajuste de texto pedido por el humano (2026-10-03, sin cambio de CA)**: en "Qué incluye" de
  `propuesta.md`, el primer punto ("Foto de partida") pasa a "Informe de situación actual,
  entregado antes de empezar: …". `guion.md`, `apoyo.md` y sus copias privadas no lo citan como
  entregable: sin cambios. Ningún check ni test buscaba el término. Propuesta rellenada sigue
  ≤ 450 palabras; PDF regenerado y revisado a ojo: propuesta en una página. pytest, `ruff` y
  ambos `check` en verde.
- **Ajuste de texto pedido por el humano (2026-10-03, sin cambio de CA): la clínica ve cada
  texto antes de publicarlo**. `propuesta.md`, punto de acciones de "Qué incluye": añade "Veis
  cada texto antes de publicarlo y podéis cambiarlo.". Para caber en ≤ 450 palabras se recorta:
  "las tres cosas" → "tres cosas"; "El piloto empieza" → "Empieza"; "Accesos con el permiso
  mínimo" → "Accesos con permiso mínimo"; "Al terminar": "no hay permanencia" → "sin
  permanencia" y "Con esta propuesta van dos anexos" → "Van dos anexos". `acuerdos.md` (e):
  añade "La clínica recibe cada texto antes de publicarlo y puede proponer cambios o mejoras."
  (`AGREEMENT_CHECKS` (e) sigue pasando). `apoyo.md` sin objeción de ese tipo: sin cambios.
  Ningún check vigila las frases nuevas (sin test nuevo). Propuesta rellenada ≤ 450 palabras;
  PDF regenerado y revisado a ojo: propuesta en una página. pytest, `ruff` y ambos `check` en
  verde.

## Decisión del humano sobre el precio (2026-10-03, enmienda (e)) — registro exigido por CA-3
Registra sdd-arquitecto. El humano (Alberto Fojo), al revisar `propuesta-borrador.pdf` el
2026-10-03 y **antes del envío**, modifica D-7 para esta propuesta: desaparece la opción
"199 €/mes" de entrada; el cliente lee **450 € + IVA por los 3 primeros meses, pagados por
adelantado; a partir del cuarto mes, 199 €/mes + IVA, y se puede dejar en cualquier momento
(sin permanencia)**. Formalizado en **ADR-010** (borrador; supera en parte D-7) y recogido en
SPEC-009 CA-3 y CA-9 (enmienda (e)). Sin opción gratuita ni descuento. Cierra F-SPEC-009-2
puntos 2 y 3. El registro del implementador de 2026-09-30 ("Desviaciones de D-7: ninguna")
describía la propuesta anterior y queda como historia.

Mismo día y misma revisión, el humano decidió además: Galicia en la propuesta solo como
ampliación posible (**ADR-011**, borrador; SPEC-009 CA-3 y CA-10); conteo semanal de recepción
**opcional** para la clínica (CA-4 (d); condición C3 del dictamen de abajo se lee ahora "si la
clínica entrega el conteo"; consecuencia en F-SPEC-009-8); y los cambios de texto 5–9 de la
enmienda (e) (portada, asistentes nombrados, medio del aviso, explicación de "repositorio
público"). Todo pendiente de re-aprobación de la spec.

## Dictamen sdd-sanidad-regulacion (CA-6)
- **Fecha**: 2026-09-30. Emitido por el rol `sdd-sanidad-regulacion` a petición de
  sdd-implementador, sobre la propuesta y los acuerdos ya redactados y **antes del envío**.
- **Alcance**: RGPD (encargo, información a pacientes, conservación), cookies (LSSI),
  publicidad sanitaria en lo que dice la propuesta y lo que el piloto publicará, y nombrar
  competidores ante la clínica. Resumen técnico, no asesoramiento jurídico: la clínica debería
  pasarlo por su asesor de protección de datos.
- **Fuentes oficiales** (consultadas el 2026-09-30):
  - RGPD (Reglamento (UE) 2016/679), texto en BOE `DOUE-L-2016-80807`: art. 4.15 (datos de salud),
    art. 6.1.f, art. 13, art. 28 (contrato de encargo por escrito, también electrónico, 28.3 y
    28.9), art. 32, art. 33, considerando 26 (datos anónimos).
  - AEPD, FAQ "¿Cuál sería el contenido del contrato de encargo de tratamiento?" y *Directrices
    para la elaboración de contratos entre responsables y encargados del tratamiento*
    (aepd.es/guias/guia-directrices-contratos.pdf).
  - LSSI (Ley 34/2002), art. 22.2, texto consolidado en BOE `BOE-A-2002-13758` (última
    actualización 23/01/2025).
  - AEPD, *Guía sobre el uso de las cookies* (actualizada en mayo de 2024), §2.1.2 c) cookies de
    análisis o medición y §4.1; AEPD, *Uso de cookies para herramientas de medición de audiencia*
    (v. enero de 2024), apartados II y III.
  - RD 1907/1996, publicidad con pretendida finalidad sanitaria, BOE `BOE-A-1996-18085`: art. 4.4
    (seguridades de alivio o curación), 4.7 (testimonios de profesionales o pacientes), 4.16, y
    art. 6 (la publicidad de centros sanitarios se ajusta a su autorización).
  - Decreto 12/2009 de Galicia (autorización de centros sanitarios), DOG 29/01/2009: art. 3.e y
    26.2 (número de registro sanitario en la publicidad y comunicaciones externas).
  - RDL 1/2015, Ley de garantías del medicamento, BOE `BOE-A-2015-8343` (actualización
    31/07/2026): art. 80.1 (solo los medicamentos no sujetos a prescripción pueden anunciarse al
    público).
  - Ley 3/1991 de Competencia Desleal, BOE `BOE-A-1991-628` (actualización 27/12/2025): art. 2
    (actos en el mercado con fines concurrenciales), 9 (denigración) y 10 (comparación pública).
  - TJUE, Gran Sala, 4-10-2024, asunto C-21/23 (*Lindenapotheke*): interpretación amplia de "datos
    relativos a la salud" (datos de un pedido que permiten inferir el estado de salud).
- **Conclusión general**: **nada bloquea el envío** de la propuesta y los acuerdos. Sí bloquean
  otros pasos: ningún acceso a herramientas de la clínica sin el contrato de encargo firmado (C1) y
  ninguna etiqueta de analítica que funcione sin consentimiento (C4). La propuesta, tal como está,
  no promete resultados y no nombra medicamentos.

### Conclusión por punto
- **C1. Encargado del tratamiento — correcto con condiciones.** La analítica guarda
  identificadores en línea y datos de navegación de visitantes, que son datos personales aunque
  estén seudonimizados (considerando 26); la ficha de Google, reseñas con nombre de su autor.
  tremen.dev los consulta y configura **por cuenta de la clínica** y para su fin: es **encargado
  del tratamiento** (art. 28) y la clínica, responsable. Hace falta un contrato por escrito
  (vale el electrónico, art. 28.9) con el contenido del art. 28.3 **antes de cualquier acceso**.
  Search Console y los conteos semanales son datos agregados. → Anexo 2
  `encargo-tratamiento.md`; acuerdos (b) "Antes de dar acceso…".
- **C2. Gestor de la web — correcto con condiciones.** El gestor de contenidos puede guardar
  formularios, reservas o pedidos de pacientes (posibles datos de salud, art. 9; C-21/23). El
  acceso de tremen.dev debe excluirlos: permiso que no los muestre o, si no existe, la tarea la
  hace la clínica. → acuerdos (b); anexo 2 §4 "Excluido".
- **C3. Pregunta "¿cómo nos has conocido?" — correcto con condiciones.** Si recepción la apunta
  **solo en una hoja de conteo sin identificar a nadie**, no hay tratamiento de datos personales.
  Si se guarda en la ficha o la reserva del paciente, es un dato personal del paciente de una
  clínica médica, que por contexto puede revelar información de salud (C-21/23): la clínica, como
  responsable, lo incluye en su información de privacidad (art. 13; base razonable: interés
  legítimo, art. 6.1.f), la respuesta es voluntaria y hay opción "prefiero no decirlo". tremen.dev
  solo recibe **conteos semanales por opción, sin día ni tratamiento** (con pocos pacientes, un
  conteo por día o tratamiento podría reidentificar a alguien). → acuerdos (d); follow-up
  F-SPEC-009-3 (SPEC-010 CA-4).
- **C4. Cookies de la analítica — correcto con condiciones.** Una analítica de terceros que
  reutiliza los datos (el caso de las herramientas habituales del mercado) **no está exenta** de
  consentimiento (LSSI 22.2; guía de medición de audiencia de la AEPD, apdo. II): solo mide a quien
  acepta. El editor de la web (la clínica) responde de su aviso de cookies, y los terceros que
  intervienen comparten la responsabilidad de que el usuario esté informado (guía de cookies,
  §4.1). tremen.dev no instala ni cambia nada que se active antes del consentimiento, y los informes
  dicen que la cifra se queda corta. Alternativa a estudiar: la AEPD admite sin consentimiento una
  medición de audiencia propia, anónima y agregada, que incluye el **referente por página,
  agregado diariamente**, con las garantías del apdo. III. → acuerdos (f); follow-up F-SPEC-009-4
  (SPEC-010 CA-1).
- **C5. Conservación — correcto.** Los conteos agregados que no permiten identificar a nadie no
  son datos personales (considerando 26); se guardan en el espacio privado (ADR-004 §2) el tiempo
  que haga falta para el caso. Al terminar el encargo, tremen.dev suprime cualquier dato personal y
  pierde los accesos (art. 28.3.g). → acuerdos (g); anexo 2 §6.
- **C6. Nombrar competidores en la hoja de hallazgo — correcto con condiciones.** Enseñar en
  privado a la clínica lo que contestan los asistentes, copiado tal cual y con app y fecha, no es
  una comparación pública (Ley 3/1991, art. 10) y, si es exacto y pertinente, tampoco denigración
  (art. 9). Condiciones: citas literales, sin valorar a las otras clínicas, sin entregar la hoja
  como fichero para difundir, sin datos identificativos de profesionales ajenos que no aporten
  nada, y nunca en el repo junto a una cifra (ADR-004 §3). → guion bloque 2 (nota "no añadas
  opiniones"); hoja privada ajustada (se quitó el dato de una profesional ajena).
- **C7. Publicidad sanitaria en la propuesta y en lo que se publique — correcto con condiciones.**
  La propuesta es una oferta entre empresas, no publicidad sanitaria al público; aun así no promete
  resultados (coherente con el art. 4.4 del RD 1907/1996) ni nombra medicamentos. Lo que el piloto
  publique en la web, fichas o directorios **sí** es publicidad del centro: se ajusta a su
  autorización sanitaria (RD 1907/1996 art. 6), lleva el número de registro sanitario donde toque
  (Decreto 12/2009, art. 3.e y 26.2), sin testimonios de pacientes o profesionales como reclamo
  (art. 4.7), sin anunciar al público medicamentos de prescripción (RDL 1/2015, art. 80.1) y con
  precios o antes y después solo si la revisión lo admite. → acuerdos (e); apoyo ("¿podemos poner
  precios / antes y después?"); follow-up F-SPEC-009-5 (SPEC-011 CA-7).
- **C8. Nombre de la clínica en el repo — correcto.** Es una persona jurídica: su nombre no es
  dato personal; las personas de la clínica no se nombran (ADR-004 §7). La revocación y que el
  historial no se borra se explican antes de publicar (ADR-004 §6). → acuerdos (c).
- **C9. Si otro servicio de tremen.dev a la clínica hiciera la pregunta de procedencia — dudoso,
  a resolver antes de usarlo.** Si la pregunta la hiciera un asistente de mensajería de otro
  servicio (fuera de este repo), ese tratamiento cae en el contrato de encargo de **ese** servicio
  y en su información al paciente; a este piloto solo llegan conteos semanales agregados, sin
  acceso a conversaciones. Además, si recepción y el asistente preguntan al mismo paciente, los
  conteos se duplican: hay que fijar quién pregunta en cada canal. → follow-up F-SPEC-009-3
  (SPEC-010 CA-4). No afecta al envío.
- **C10. Normativa fuera de Galicia — pendiente, no bloquea.** El objetivo incluye pacientes del
  occidente de Asturias. Un centro gallego anuncia con arreglo a su autorización en Galicia, pero
  si alguna acción crea contenido dirigido expresamente a Asturias, ADR-008 §7 pide dictamen sobre
  la normativa del Principado antes de publicarlo. → follow-up F-SPEC-009-5 (SPEC-011).

### Tabla condición → cambio
| Condición | Cambio | Dónde |
|---|---|---|
| C1 contrato de encargo antes de cualquier acceso | Anexo 2 con el contenido del art. 28.3; acuerdos (b) lo exige antes de dar acceso; la propuesta anuncia los dos anexos | `encargo-tratamiento.md`, `acuerdos.md` (b), `propuesta.md` "Al terminar" |
| C2 sin acceso a formularios, reservas o pedidos | Permiso que los oculte o tarea para la clínica; excluidos del encargo | `acuerdos.md` (b), `encargo-tratamiento.md` §4 |
| C3 pregunta de procedencia voluntaria, informada y agregada | "Prefiero no decirlo"; información de privacidad si se guarda con el paciente; conteo semanal sin día ni tratamiento. **Enmienda (e), 2026-10-03**: la entrega del conteo es **opcional** para la clínica; C3 aplica solo si lo entrega; sin conteo, la condición (A) "≥ 1 paciente" no se mide por esta vía (F-SPEC-009-8) | `acuerdos.md` (d); F-SPEC-009-3 → SPEC-010 CA-4; F-SPEC-009-8 |
| C4 cookies | La analítica solo mide con consentimiento; nada antes del consentimiento; límite dicho en los informes | `acuerdos.md` (f); F-SPEC-009-4 → SPEC-010 CA-1 |
| C5 conservación | Supresión y fin de accesos al terminar; agregados en privado | `acuerdos.md` (g), `encargo-tratamiento.md` §6 |
| C6 competidores en la hoja | Citas literales, sin valorar, sin difundir, sin datos de profesionales ajenos | `guion.md` bloque 2; hoja privada `reunion/hoja-hallazgo.md` |
| C7 publicidad sanitaria | Revisión antes de publicar: autorización, registro sanitario, sin testimonios, sin medicamentos con receta, precios y antes/después solo si se admite | `acuerdos.md` (e), `apoyo.md`; F-SPEC-009-5 → SPEC-011 CA-7 |
| C8 nombre en el repo | Qué se publica y qué no, revocación, historial | `acuerdos.md` (c) |
| C9 pregunta hecha por otro servicio | Contrato e información de ese servicio; solo agregados; un único canal por paciente | F-SPEC-009-3 → SPEC-010 CA-4 |
| C10 normativa de Asturias | Dictamen antes de publicar contenido dirigido a Asturias | F-SPEC-009-5 → SPEC-011 |

## Pasos humanos (CA-7, CA-8, CA-9) — instrucciones
Antes de nada, confirma en `$PUSHLLM_PRIVADO/piloto-artica/reunion/valores.json` lo que está en
`_pendiente` (razón social y NIF de la clínica, NIF de tremen.dev, tratamientos tras la reunión,
fecha de envío) y vacía la lista.

**CA-7 — Ensayo (antes de la reunión)**
1. Imprime `hoja-hallazgo.md`, `guion-artica.md` y `apoyo-artica.md` (privado).
2. Ensayo completo **en voz alta**, cronometrado, leyendo el guion literal. Alguien (una persona o
   un agente) hace de dirección de la clínica y plantea **al menos 3 objeciones** de `apoyo.md`
   (propuestas: "somos amigos, ¿no me lo haces gratis?", "¿y si perdemos A Mariña?", "¿esto va
   junto con lo otro que nos propusiste?").
3. Objetivo ≤ 50 min. Anota lo que se atasca y cámbialo en las plantillas (repo) o en las copias
   privadas; vuelve a pasar `meeting_docs.py check`.
4. Registra aquí: fecha, duración, objeciones planteadas y lista de cambios.

**CA-8 — Reunión**
1. Tras el ensayo (y con SPEC-007 CA-5 ya hecha: lo está desde el 2026-09-29/30).
2. Notas en `$PUSHLLM_PRIVADO/piloto-artica/reunion/notas-AAAA-MM-DD.md` en ≤ 48 h, sin datos de
   pacientes.
3. Registra aquí: fecha, duración y, por pregunta P1–P16 de `guion.md` (más P17–P18 de la versión
   privada), **sí/no respondida**, sin el contenido.
4. Si la respuesta a P15 cambia los tratamientos de fuera, actualiza `tratamientos` en
   `valores.json` (el set `AR`/`AG` ya está congelado: una pregunta nueva se informa aparte).

**CA-9 — Envío, aceptación y cobro**
1. En ≤ 5 días hábiles tras la reunión: `meeting_docs.py build` **sin** `--borrador` y
   `build_pdf.mjs` (ver `docs/piloto-artica/reunion/README.md`). Revisa que la propuesta queda en
   una página.
2. Envía el PDF (propuesta + anexo 1 acuerdos + anexo 2 encargo) a la dirección de la clínica. Si
   hay algún cambio de precio o condiciones frente a D-7, **antes** regístralo aquí como decisión
   tuya; si no, no se toca.
3. Registra aquí: fecha de envío; respuesta (acepta / negocia / rechaza; enmienda (e): ya no hay
   opción mensual de entrada) y su fecha; fecha de aceptación de los acuerdos, del consentimiento
   de nombre (sí/no) y de si entregarán el conteo semanal de recepción (sí/no, CA-4 (d)), **sin
   nombre** de quien firma; fecha del contrato de encargo firmado; fecha del primer cobro (los 3
   primeros meses por adelantado, ADR-010).
   Documentos (propuesta enviada, respuesta, acuerdos y encargo firmados, factura) en
   `$PUSHLLM_PRIVADO/piloto-artica/reunion/`.
4. Regla: sin aceptación escrita y primer cobro, **no empieza** SPEC-010 ni ninguna acción; sin
   el encargo firmado, ningún acceso a herramientas de la clínica (C1).

## Veredicto del verificador
<!-- GREEN/RED + fecha + resumen. Lo escribe SOLO sdd-verificador. -->

## Evidencia visual
<!-- Tabla CA → captura en _qa/SPEC-009/. Informe HTML opcional: _qa/SPEC-009/informe.html -->
El PDF de la propuesta rellenada es privado (ADR-004): no hay capturas en `_qa/`. Para revisar el
maquetado sin datos del cliente, basta generar el HTML con valores ficticios (los de
`test_meeting_kit.VALUES`) en una carpeta temporal fuera del repo.

## Salvedades / follow-ups
<!-- IDs F-SPEC-009-1, F-SPEC-009-2… con destino (spec futura o EPIC-MEJORA). -->
- **F-SPEC-009-1** (sdd-arquitecto, 2026-09-29) — ¿la propuesta cuenta el Go de ADR-009?
  **Cerrado 2026-09-29**: el humano (Alberto Fojo) decidió que sí, sin garantía y sin
  cifras; recogido en la enmienda (d) de la spec (CA-1, CA-3, CA-5, CA-10). Spec en
  `borrador`, pendiente de re-aprobación.
- **F-SPEC-009-2** (→ humano, antes del envío): datos que la spec no fija y el agente no
  inventa: (1) razón social y NIF de la clínica y NIF de quien factura por tremen.dev (anexo 2);
  (2) ~~tipo de IVA: la propuesta dice "+ IVA; la factura suma el IVA vigente", sin cifrar el
  tipo~~ **cerrado 2026-10-03 (enmienda (e))**: se quita la frase "Precios sin IVA: la factura
  suma el IVA vigente"; queda "+ IVA" junto a cada importe, sin cifrar el tipo;
  (3) ~~en la opción mensual, si se puede dejar antes de los 3 meses~~ **cerrado 2026-10-03
  (ADR-010)**: no hay opción mensual de entrada; los 3 primeros meses se pagan por adelantado y
  después es mensual sin permanencia; (4) si el contrato de encargo de este
  piloto y el de otro servicio de tremen.dev a la clínica, si lo contrata, se firman juntos.
  Quedan abiertos (1) y (4).
- **F-SPEC-009-3** (→ sdd-arquitecto, SPEC-010 CA-4): del dictamen C3 y C9: opción "prefiero no
  decirlo"; conteo semanal por opción **sin día ni tratamiento**; información de privacidad de la
  clínica si la respuesta se guarda con el paciente; y, si otro servicio de mensajería de la
  clínica hace la pregunta, un único canal por paciente para no contar dos veces.
- **F-SPEC-009-4** (→ sdd-arquitecto, SPEC-010 CA-1): del dictamen C4: la agrupación "Asistentes de
  IA" solo cuenta visitas con consentimiento; la visita de prueba de CA-1 debe aceptar cookies; los
  informes dicen que la cifra se queda corta; valorar la medición de audiencia exenta de la AEPD
  (referente por página, agregado diario) como señal complementaria.
- **F-SPEC-009-5** (→ SPEC-011 CA-7): la revisión normativa de cada contenido aplica el dictamen C7
  (autorización sanitaria, número de registro, sin testimonios, sin medicamentos de prescripción,
  precios y antes/después solo si se admiten) y C10 (dictamen de Asturias si el contenido se dirige
  allí, ADR-008 §7).
- **F-SPEC-009-6** (→ sdd-verificador): "cabe en una página" se implementa como una página de
  propuesta más una portada `.v-tremendo` (petición del humano: mismo estilo que la otra propuesta
  de tremen.dev a la clínica) y dos anexos. Si se lee "una página" como el documento entero, `build_document`
  necesita un modo sin portada.
- **F-SPEC-009-7** (→ sdd-documentalista): la matriz de este ledger tenía `\n` literales (como
  F-SPEC-007-3); corregido el formato sin cambiar Verif./Estado.
- **F-SPEC-009-8** (sdd-arquitecto, 2026-10-03 → sdd-arquitecto, SPEC-010 CA-4 y SPEC-012
  CA-3/CA-7): con la enmienda (e) la clínica puede **no** entregar el conteo semanal de "¿cómo
  nos has conocido?" (CA-4 (d)). Sin él, la condición (A) del Go (ADR-009 §1, "≥ 1 paciente
  atribuido", RN-07) no se puede medir por la pregunta de recepción. Esta spec **no** fija una
  vía alternativa (no se inventa): SPEC-010 debe decir qué señales de atribución quedan sin el
  conteo (las que ya prevé: referencias etiquetadas en la analítica, búsquedas de marca en
  Search Console) y SPEC-012 cómo se evalúa (A) en ese caso, o si se declara "no medible".
  Decisión del humano si hace falta. La respuesta de la clínica (entrega sí/no) se registra en
  CA-9.

## Cómo retomar (handoff)
- **Hecho (agente)**: CA-1 a CA-6 y CA-10 implementados con tests (`test_meeting_kit.py`, 63 casos
  de SPEC-009 en la suite de `docs/piloto-artica/tools/tests`), `ruff` limpio, dictamen CA-6 en
  este ledger, copias personalizadas y PDF borrador en privado.
- **Falta (humano)**: vaciar `_pendiente` de `valores.json` (F-SPEC-009-2), CA-7 ensayo, CA-8
  reunión, CA-9 envío en ≤ 5 días hábiles, aceptación, encargo firmado y primer cobro.
- **Estado de la spec**: `en-progreso` a propósito: los CA humanos no están hechos. Cuando lo
  estén, sdd-implementador pasa la spec a `en-revision` y sdd-verificador verifica.
- **Comprobar**: `python -m pytest -q docs/piloto-artica/tools/tests` (con `PUSHLLM_PRIVADO`
  definido, también comprueba que ningún nombre privado está en el repo) y
  `python docs/piloto-artica/tools/meeting_docs.py check`.
