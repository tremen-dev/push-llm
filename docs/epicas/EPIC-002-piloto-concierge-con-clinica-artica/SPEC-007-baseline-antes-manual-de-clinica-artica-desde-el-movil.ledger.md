---
id: SPEC-007
tipo: ledger
epica: EPIC-002
---
# Ledger — SPEC-007 Baseline antes manual de Clínica Ártica desde el móvil

## Resumen
- Fase: <!-- refleja el estado de la spec; la fuente de verdad es el frontmatter de la spec -->
- Rama: `ft/SPEC-007-baseline-antes-manual-de-clinica-artica-desde-el-movil`

## Matriz de criterios de aceptación
<!-- Escritores: sdd-implementador rellena Implementado y Test; sdd-verificador rellena Verif. y Estado. Nunca al revés. -->
<!-- Estados por CA: ✅ cerrado · ⚠️ parcial/con salvedad · 🚧 en curso · ❌ sin empezar · n-a -->
<!-- Un CA está ✅ solo cuando Implementado + Test + Verif. aplicables están en verde. Una salvedad se marca ⚠️, nunca ✅. -->
| CA | Implementado (fichero) | Test (fichero/caso) | Verif. | Estado |
|---|---|---|---|---|
| CA-1 | `docs/piloto-artica/prompts-baseline.md` (15 `AV` + 2 `AM`); comprobador `docs/piloto-artica/tools/baseline_docs.py` (`parse_prompts_doc`, `coverage`) | `docs/piloto-artica/tools/tests/test_baseline_prompts.py` (recuento de cada condición, ids, sin "Ártica"/"Artica"/candidatas de SPEC-008 en `AV`, sin preguntas sin lugar, línea de cobertura = tabla) | | ❌ |
| CA-2 | Dictamen `sdd-metricas` 2026-09-29 y tabla condición → cambio, en este ledger (sección "Dictamen sdd-metricas (CA-2)"); fecha anterior a la pasada 1 | Checklist (a)–(f) en la sección del dictamen; cada condición mapeada a fichero y test | | ❌ |
| CA-3 | `docs/piloto-artica/protocolo-captura.md` | `docs/piloto-artica/tools/tests/test_baseline_protocol_template.py` (≤ 1100 palabras; cada campo obligatorio; apps, sesión limpia, cuenta/plan, modelo, texto literal, una por conversación, orden, captura, enlace, mismas condiciones incl. SPEC-012, tres reglas anti-contaminación) | | ❌ |
| CA-4 | `docs/piloto-artica/plantilla-captura.csv` (solo cabecera) | `test_baseline_protocol_template.py::test_template_is_header_only`, `::test_template_crosses_protocol_fields_and_ca4_extras`, `::test_protocol_documents_every_template_column` | | ❌ |
| CA-5 | [Humano] pendiente. Preparado: `$PUSHLLM_PRIVADO/piloto-artica/baseline/captura-p1-prerrellenada.csv` (49 filas en orden) y `preguntas-en-orden.txt` | — (lo cuenta el verificador en privado) | | ❌ |
| CA-6 | [Humano] pendiente. Preparado: `captura-p2-prerrellenada.csv` | — | | ❌ |
| CA-7 | Procedimiento `docs/piloto-artica/procedimiento-recuento.md` y `docs/piloto-artica/tools/count_baseline.py`. **Falta** el `recuento-antes.md` privado (necesita las pasadas 1 y 2) | `docs/piloto-artica/tools/tests/test_baseline_count.py` (SoV bruto por app y por pasada, ponderado normalizado, posición media, clínicas en su lugar con alias canónicos, Google aparte con y sin resumen, dominios, estabilidad, observaciones y `AM` aparte, filas duplicadas/vacías fallan) — fixture ficticia | | ❌ |
| CA-8 | Regla de congelación en `prompts-baseline.md` ("Estado del set"). **Falta** la fecha de congelación (= inicio de la pasada 1) y, si aplica, la decisión humana tras el recuento | — | | ❌ |
| CA-9 | `$PUSHLLM_PRIVADO/piloto-artica/baseline/foto-tecnica-2026-09-29/` (`foto-tecnica.md`, `raw/robots.txt`, `raw/sitemap_index.xml` + 8 sitemaps, HTML y JSON-LD de portada, contacto y una página por línea, `raw/SHA256SUMS.txt`). **Falta**: Google Business Profile (lo mira el humano) y los dominios citados en la pasada 1 | Comprobación manual del verificador (fechas y URLs en `foto-tecnica.md`) | | ❌ |
| CA-10 | **Pendiente** de la pasada 1. Comprobador de términos prohibidos listo: `python docs/piloto-artica/tools/baseline_docs.py "$PUSHLLM_PRIVADO/piloto-artica/baseline/hallazgo-reunion.md"` | `docs/piloto-artica/tools/tests/test_baseline_frontier.py::test_forbidden_meeting_terms` | | ❌ |
| CA-11 | [Verificador]. Apoyo: `baseline_docs.py` sin argumentos revisa `docs/piloto-artica/` (emails, teléfonos, cifras junto a marcas) | `test_baseline_frontier.py::test_repo_docs_pass_the_frontier` y `::test_frontier_detects_email_phone_and_figure_next_to_brand` | | ❌ |

Tests: `python -m pytest -q docs/piloto-artica/tools/tests` (105 en verde el 2026-09-29) y
`python -m pytest -q probe/tests` (106, sin cambios).

## Dictamen sdd-metricas (CA-2)
- **Fecha**: 2026-09-29, antes de la pasada 1 (que no ha empezado).
- **Emisor**: sdd-implementador aplicando `.ai-context/skills/sdd-metricas.md` (rol advisory,
  sin cambiar reglas).
- **Fuentes**: `docs/fundacion/reglas.md` RN-01 a RN-06 y RN-11; `docs/fundacion/dominio.md`;
  `07-mvp-product-spec.md` §4; `06-models-costs-and-usage-share.md` §3–4; FOUNDATION D-5
  y D-6; `probe/matching.py` y `probe/analysis.py` (implementación vigente de RN-01, RN-11
  y del ponderado); SPEC-008 (alias delicados); fuentes públicas del nombre de la clínica
  consultadas el 2026-09-29 (Páxinas Galegas y el directorio de SEME la listan como
  "Ártica"; la web, como "CLÍNICA ÁRTICA"; otros directorios, como "Ártica Medicina Estética").

### (a) Alias que cuentan como mención en el conteo manual — **correcto con condiciones**
1. Clínica Ártica: cuentan "Clínica Ártica", "Ártica Medicina Estética", "Ártica" sola y el
   dominio "clinicaartica" **cuando aparece en el texto de la respuesta**. "Ártica" tiene 6
   caracteres normalizados y es forma pública del nombre: cumple RN-01 sin excepción. No
   hace falta RN-11 (no es sigla).
2. Riesgo de falso positivo: "ártica" como adjetivo (el masculino "ártico" no coincide).
   En este dominio es improbable. **Se cuenta igualmente** (RN-01 literal, coherente con
   lo que hará el probe con el mismo alias) y se marca `#artica-adjetivo` en
   `observaciones`; el recuento informa cuántas hay y se revisan a mano.
   Confirmado por el humano el 2026-09-29 (P-1).
3. Una ficha de fuente o enlace que solo muestra el dominio **no** es mención: va a
   `dominios_citados` (como en el probe, donde las URLs citadas van aparte del texto).
4. El nombre de la médica titular sin el de la clínica **no** cuenta como mención (no es
   alias de la marca en el catálogo); se anota en `observaciones` y se informa aparte.
   Marca `#medica-sin-clinica`. Confirmado por el humano el 2026-09-29 (P-2).
5. Competidores: una clínica cuenta como nombrada cuando aparece su nombre o un alias
   distintivo de ≥ 4 caracteres referido a ella. Palabras comunes sueltas ("Luxury",
   "Ribera") solo cuentan si el contexto dice que es la clínica (en manual lo decide el
   lector; en el probe, SPEC-008 CA-2). Las variantes se unifican con
   `alias-canonicos.csv` en privado. Siglas < 4 caracteres: no cuentan (no hay ninguna
   en `exact_aliases` para este piloto; RN-11).
6. Posición (RN-06): puesto entre clínicas y médicos nombrados, **sin** directorios ni
   plataformas (Doctoralia, Top Doctors, Multiestetica, Páxinas Galegas…), igual que
   `probe/analysis.py`, que separa `type = directory`.

### (b) Número de pasadas y separación — **correcto**
Dos pasadas "antes", separadas **entre 3 y 10 días**, a hora parecida (± 2 h), ambas
antes de la primera acción. Menos de 3 días mide casi la misma respuesta dos veces; más de
10 alarga el "antes". El "antes" es la unión de las dos pasadas; el "después" (SPEC-012)
repite el mismo esquema: dos pasadas con la misma separación.

### (c) SoV bruto por app y ponderado — **correcto con condiciones**
- SoV bruto (RN-02) por app = respuestas válidas con la clínica ÷ respuestas válidas de
  las preguntas `AV`, sumando las dos pasadas; también se da por pasada.
- Respuesta válida = la app contestó a la pregunta, aunque se niegue a recomendar (eso es
  lo que ve el paciente y cuenta en el denominador). Inválida = fallo técnico, respuesta
  cortada o pregunta mal pegada: se excluye y se cuenta aparte.
- Ponderado (RN-03/RN-04) = (SoV ChatGPT × 0,55 + SoV Gemini × 0,25) ÷ 0,80, normalizado a
  las apps con respuestas válidas (como `probe/analysis.py`).
- **Cuentas**: solo las gratuitas (D-5: modelo por defecto de la app que usa la mayoría;
  `06-…md` §3: ~94 % de usuarios de ChatGPT no pagan). Filas de cuentas de pago: solo
  observación, nunca en el cálculo.
- **Claude**: **observación, no entra en el ponderado.** Motivos: la spec fija el ponderado
  "con solo ChatGPT y Gemini" (CA-2 c) y su Fuera de alcance exige repetir Claude en todas
  las pasadas para usarlo; con peso 10 % sobre 90 su efecto es pequeño y alarga cada pasada
  15 consultas. Recomendación: no incluirlo en la pasada 1; si el humano lo incluye, debe
  hacerlo en las cuatro pasadas y se informa aparte.

### (d) Google AI Overviews — **correcto**
Canal aparte, sin ponderar (RN-04, D-6). Por búsqueda válida se anota `resumen_ia`
(`si`/`no`). Se informan dos cifras: clínica en el resumen ÷ búsquedas válidas (lo que ve
el paciente: si no hay resumen, no la ve por esta vía) y clínica en el resumen ÷ búsquedas
con resumen. Sin resumen, la fila es válida, con `clinicas_nombradas` vacío. El paquete
local de mapas y los resultados normales no cuentan (no son IA); se pueden anotar en
`observaciones`. "Modo IA" no se usa.

### (e) Mismo instrumento — **correcto**
El criterio Go (+15 pts) solo se compara manual contra manual con este protocolo y
condiciones (cuentas gratuitas, modos, móvil, municipio, mismo set congelado), o probe
contra probe. Nunca se mezclan cifras manuales y del probe en una misma diferencia. Si las
claves llegan después de la primera acción, el Go se mide solo a mano (SPEC-008 CA-7).

### (f) Margen de ruido frente a +15 pts — **dudoso** (no cambia ninguna regla; ver P-3)
Con 15 preguntas × 2 pasadas = 30 respuestas por app, pesos normalizados 0,6875/0,3125, el
error típico del ponderado y el margen del 95 % de una **diferencia** antes/después son
aproximadamente (binomial; entre paréntesis, si las dos pasadas de una pregunta salen
siempre iguales y la muestra efectiva es 15):

| SoV "antes" | Error típico del ponderado | Margen 95 % de la diferencia |
|---|---|---|
| 5 % | 3 pts (4) | ± 8 pts (± 12) |
| 10 % | 4 pts (6) | ± 12 pts (± 16) |
| 20 % | 5,5 pts (8) | ± 15 pts (± 22) |
| 35 % | 6,6 pts (9) | ± 18 pts (± 26) |
| 50 % | 7 pts (10) | ± 19 pts (± 27) |

Lectura: si la clínica parte de casi 0, +15 pts es distinguible del ruido; si parte de
20–50 %, +15 pts está dentro del ruido. Condición: el recuento informa siempre la
estabilidad por pregunta (cuántas `AV` × app pasan de "0 de 2" antes a "2 de 2" después) y
la diferencia entre la pasada 1 y la 2 (ruido medido). El humano decidió el 2026-09-29 (P-3)
que el criterio Go exige estabilidad: la subida debe verse en las dos pasadas "después"
(follow-up F-SPEC-007-5 para SPEC-012).

### Tabla condición → cambio
| Condición | Cambio | Dónde |
|---|---|---|
| a1–a3 alias de Ártica, dominio no es mención | Reglas de mención al leer capturas | `procedimiento-recuento.md` §0.3; columna `artica_nombrada` |
| a2 adjetivo | Marca `#artica-adjetivo` y recuento de marcas | `procedimiento-recuento.md` §0.3; `count_baseline.py` (`adjective_flags`); test `test_adjective_flag_is_reported` |
| a4 nombre de la médica | Se anota en observaciones; no cuenta | `procedimiento-recuento.md` §0.3 (implícito: solo nombre/alias de la clínica); P-2 |
| a5 competidores y variantes | `alias-canonicos.csv` privado | `procedimiento-recuento.md` §0.4; `count_baseline.py --aliases`; test `test_clinics_in_its_place_are_canonicalised` |
| a6 posición sin directorios | Definición de `posicion_artica` | `protocolo-captura.md` (campos); `procedimiento-recuento.md` §0.3 |
| b 2 pasadas, 3–10 días, ± 2 h | Plazo y hora de la pasada 2 | `protocolo-captura.md` "Pasada 2 y siguientes"; CA-6 |
| c válida/excluida | Columna `respuesta_valida` | `plantilla-captura.csv`; `protocolo-captura.md`; test `test_raw_sov_per_app` |
| c solo cuentas gratuitas | `plan_cuenta`; filtro de filas principales | `protocolo-captura.md` "Antes de empezar" 3; `count_baseline.py` (`MAIN_PLANS`); test `test_observation_and_brand_rows_apart` |
| c ponderado normalizado ChatGPT+Gemini | Fórmula | `procedimiento-recuento.md` §3; tests `test_weighted_*` |
| c Claude como observación | Solo observación, repetir en todas o nada | `protocolo-captura.md` "Pasada 2 y siguientes"; `count_baseline.py` (`WEIGHTS` sin Claude) |
| d AI Overviews aparte | Columna `resumen_ia`; dos cifras | `plantilla-captura.csv`; `procedimiento-recuento.md` §4; tests `test_google_*` |
| e mismo instrumento | Condiciones iguales en todas las pasadas; set congelado | `protocolo-captura.md` "Antes de empezar" 2; `prompts-baseline.md` "Estado del set" |
| f ruido | Estabilidad por pregunta y SoV por pasada en el recuento | `procedimiento-recuento.md` §2 y §6; tests `test_sov_per_pass`, `test_stability_per_question` |

## Instrucciones para el humano — pasada 1 (CA-5)
Tiempo: 60–90 min de consultas (49) + 15–20 min para pasar capturas y rellenar el CSV.
Mejor **antes de la reunión** de SPEC-009. Todas las pasadas desde Vilaboa (P-4 revisada).
1. Imprime `docs/piloto-artica/protocolo-captura.md` y ábrete
   `$PUSHLLM_PRIVADO/piloto-artica/baseline/preguntas-en-orden.txt` (preguntas listas para
   copiar, en orden: 17 en ChatGPT, 17 en Gemini, 15 en Google).
2. Prepara las cuentas **gratuitas**: ChatGPT con memoria desactivada; Gemini con la
   actividad desactivada. No uses las de pago (si quieres mirarlas, solo como observación y
   anotado).
3. Crea `$PUSHLLM_PRIVADO/piloto-artica/baseline/AAAA-MM-DD-p1/` (fecha del primer día), y
   dentro: copia `captura-p1-prerrellenada.csv` como `captura-p1.csv`, un
   `desviaciones.txt` vacío y una carpeta `capturas/`.
4. Anota la cabecera de sesión: municipio (Vilaboa), ubicación del móvil sí/no (el mismo
   ajuste en todas las pasadas), alias de cuenta y modelo que muestra cada app. Nada de
   VPN ni de GPS simulado.
5. Haz las consultas siguiendo el protocolo (chat temporal nuevo por pregunta, texto
   literal, captura completa; Google en incógnito). No pulses enlaces a la web de la clínica
   ni busques su nombre en Google.
6. Al terminar el bloque de Google, en Google Maps (incógnito) busca **"medicina estética
   Viveiro"** (no el nombre de la clínica) y haz captura: si sale la ficha de la clínica,
   con cuántas reseñas, fotos, horario y web. Guárdala como `capturas/gbp.png` (CA-9).
7. Pasa las capturas a `capturas/` y rellena en `captura-p1.csv` las columnas tuyas
   (condiciones, hora, `respuesta_valida`, `resumen_ia`, `fichero_captura`, enlace,
   observaciones). Las de lectura (`clinicas_nombradas`, `artica_nombrada`,
   `posicion_artica`, `dominios_citados`) las rellena el agente; si prefieres, el agente
   también puede sacar la hora y el fichero de las capturas.
8. Avisa al orquestador con la fecha de inicio (congela el set, CA-8), el nº de filas y las
   desviaciones. Con eso el agente hace la hoja de hallazgo (CA-10) y completa la foto
   técnica (CA-9).
9. Pasada 2: entre 3 y 10 días después, misma hora (± 2 h), mismas condiciones, con
   `captura-p2-prerrellenada.csv`, en `AAAA-MM-DD-p2/`, y **antes de la primera acción**.

## Preguntas abiertas
Todas respondidas el 2026-09-29 — **decidido por el humano (Alberto Fojo)**:
- **P-1** ("ártica" como adjetivo): **cuenta** (RN-01 literal) y se marca
  `#artica-adjetivo` para revisarla a mano. Sin cambio de regla. Reflejado en
  `protocolo-captura.md` (marcas en `observaciones`), `procedimiento-recuento.md` §0.3 y
  `count_baseline.py` (`adjective_flags`).
- **P-2** (nombre de la médica titular sin "Clínica Ártica"): **no cuenta** como mención;
  se marca `#medica-sin-clinica` y se informa aparte como observación. Reflejado en
  `protocolo-captura.md`, `procedimiento-recuento.md` §0.3 y `count_baseline.py`
  (`doctor_only_flags`); test `test_doctor_without_clinic_flag_is_reported_apart`.
- **P-3** (ruido frente a +15 pts): el criterio Go **exige estabilidad**: la subida tiene que
  verse en **las dos** pasadas "después". Afecta a SPEC-012 (borrador, del arquitecto): ver
  F-SPEC-007-5. El recuento "antes" ya da SoV por pasada y estabilidad por pregunta.
- **P-4** (municipio) — **REVISADA el 2026-09-29, decidido por el humano (Alberto
  Fojo)**: todas las pasadas, antes y después, se hacen desde **Vilaboa (Pontevedra)**, con
  el mismo ajuste de ubicación del móvil, sin VPN ni GPS simulado. Es el método del piloto,
  no una desviación. Motivo: todas las preguntas nombran el lugar y lo que importa es medir
  antes y después desde el mismo sitio y con el mismo método. Limitación escrita en el
  protocolo (pesa sobre todo en Google, sus resúmenes de IA y Maps). Opcional: bloque
  Google/Maps desde Viveiro como observación de sensibilidad a la ubicación, fuera del
  cómputo. Reflejado en `protocolo-captura.md`, `procedimiento-recuento.md` §1 y
  `count_baseline.py` (`MAIN_MUNICIPIO`, `location_sensitivity`); tests
  `test_protocol_fixed_municipality_vilaboa`,
  `test_rows_from_another_municipality_are_location_sensitivity_observations`.
  - Historial: ~~2026-09-29: desde Viveiro o A Mariña, las dos pasadas desde el mismo
    sitio~~ (sustituida por la revisión anterior).

## Veredicto del verificador
<!-- GREEN/RED + fecha + resumen. Lo escribe SOLO sdd-verificador. -->

## Evidencia visual
<!-- Tabla CA → captura en _qa/SPEC-007/. Informe HTML opcional: _qa/SPEC-007/informe.html -->

## Salvedades / follow-ups
- **F-SPEC-007-1** (→ SPEC-011): posible inconsistencia NAP y ficha ajena: en fuentes
  públicas aparecen otra dirección y otro teléfono para la clínica, y en Doctoralia una
  "Clínica Ártica" con una ginecóloga. Detalle en `foto-tecnica.md` §4 (privado).
- **F-SPEC-007-2** (→ SPEC-008 CA-2): alias de Clínica Ártica para `brands.csv`: este
  dictamen avala "Ártica" sola (RN-01) y el dominio; SPEC-008 puede reutilizarlo.
- **F-SPEC-007-3** (→ sdd-documentalista): las matrices de los ledgers de SPEC-007 a
  SPEC-012 se generaron con `\n` literales en una sola línea; aquí se ha corregido el
  formato de la de SPEC-007 (sin tocar Verif./Estado); las demás siguen igual.
- **F-SPEC-007-4**: las herramientas de comprobación y recuento viven en
  `docs/piloto-artica/tools/` (no son producto ni probe; nada en `src/`). Se ejecutan con
  `python -m pytest -q docs/piloto-artica/tools/tests` y reutilizan `probe/matching.norm`.
- **F-SPEC-007-5** (→ sdd-arquitecto, SPEC-012): por decisión del humano del 2026-09-29
  (P-3), el criterio Go de +15 pts de SoV ponderado exige que la subida se vea en **cada
  una de las dos** pasadas "después" (no solo en su media). SPEC-012 debe recogerlo antes
  de la primera acción; no se ha editado SPEC-012.

## Cómo retomar (handoff)
- Hecho (2026-09-29): CA-1, CA-3, CA-4 publicados; dictamen CA-2 en este ledger;
  procedimiento y herramienta de CA-7; foto técnica CA-9 salvo GBP y dominios de la
  pasada 1; CSV prerrellenados y preguntas en orden en privado.
- Falta, en este orden: pasada 1 (humano) → fecha de congelación (CA-8) y hoja de hallazgo
  `hallazgo-reunion.md` (CA-10, agente) + dominios de la pasada 1 y GBP en la foto técnica
  (CA-9) → pasada 2 (humano) → rellenar columnas de lectura y `recuento-antes.md` (CA-7,
  agente) → aviso de CA-8 si el ponderado ≥ 85 % → decisión humana si aplica.
- La spec queda **en-progreso**; pasa a `en-revision` cuando estén las dos pasadas, el
  recuento y la hoja de hallazgo.
