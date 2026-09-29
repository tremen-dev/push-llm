---
id: SPEC-007
tipo: ledger
epica: EPIC-002
---
# Ledger — SPEC-007 Baseline antes manual de Clínica Ártica desde el móvil

## Resumen
- Fase: <!-- refleja el estado de la spec; la fuente de verdad es el frontmatter de la spec -->
- Rama: `ft/SPEC-007-calibracion` (desde `ft/SPEC-013-respuesta-cruda-y-citas-de-claude`; antes, `ft/SPEC-007-baseline-antes-manual-de-clinica-artica-desde-el-movil`)

## Matriz de criterios de aceptación
<!-- Escritores: sdd-implementador rellena Implementado y Test; sdd-verificador rellena Verif. y Estado. Nunca al revés. -->
<!-- Estados por CA: ✅ cerrado · ⚠️ parcial/con salvedad · 🚧 en curso · ❌ sin empezar · n-a -->
<!-- Un CA está ✅ solo cuando Implementado + Test + Verif. aplicables están en verde. Una salvedad se marca ⚠️, nunca ✅. -->
| CA | Implementado (fichero) | Test (fichero/caso) | Verif. | Estado |
|---|---|---|---|---|
| CA-1 | `docs/piloto-artica/prompts-baseline.md`: núcleo `AV01`–`AV15` (sin cambios), `AR01`–`AR05`, `AG01`–`AG04`, `AM01`–`AM02` (ninguna pregunta cambia en la enmienda (b); solo la entradilla: la manual mide `AV` + `AM`, el probe `AV`, `AR` y `AG`); comprobador `docs/piloto-artica/tools/baseline_docs.py` (`parse_prompts_doc`, `coverage`, `coverage_regional`, `render_coverage_galicia`); copia congelada `tools/tests/av-2026-09-29.tsv`; tratamientos `AG` con URL y fecha en "Tratamientos del nivel AG" | `docs/piloto-artica/tools/tests/test_baseline_prompts.py` (condiciones por nivel, ids únicos y por prefijo, `AV` idénticas a la versión publicada, sin textos repetidos, ≤ 24, sin "Ártica"/"Artica"/candidatas de SPEC-008 en `AV`, `AR` ni `AG`, sin preguntas sin lugar, líneas de cobertura = tablas, Mondoñedo es A Mariña; entradilla: `test_intro_and_state_reflect_the_calibration`) | | ❌ |
| CA-2 | Dictamen `sdd-metricas` 2026-09-29 (a)–(f), ampliación por niveles (g)–(j) y **segunda ampliación (k)–(n) del 2026-09-29 (calibración)**, con tabla condición → cambio (filas k1–n), en este ledger; todas antes de la pasada "antes" | Checklist (a)–(n) en la sección del dictamen; cada condición mapeada a fichero y test (tabla condición → cambio); umbrales fijados en `test_baseline_count.py::test_thresholds_of_the_dictamen` y `test_baseline_procedure.py` | | ❌ |
| CA-3 | `docs/piloto-artica/protocolo-captura.md` (calibración: 49 consultas, ChatGPT y Gemini con `AV` y después `AM`, Google solo `AV`; `pasada` = `antes`/`despues`; baseline oficial del probe primero y ventana de 7 días; corte entre apps; 60–90 + 20–25 min; mismas condiciones en las dos pasadas; Vilaboa) | `docs/piloto-artica/tools/tests/test_baseline_protocol_template.py` (≤ 1100 palabras; campos obligatorios; apps, sesión limpia, cuenta/plan, modelo, texto literal, una por conversación, orden, captura, enlace, mismas condiciones incl. SPEC-012, reglas anti-contaminación, Vilaboa; `test_protocol_calibration_covers`, `test_protocol_calibration_asks_no_ar_or_ag`, `test_protocol_calibration_has_no_second_before_pass`; orden de las 49: `test_calibration_order_has_49_queries`, `test_calibration_order_blocks`) | | ❌ |
| CA-4 | `docs/piloto-artica/plantilla-captura.csv` (solo cabecera; sin cambios: el dictamen (k)–(n) no pide columna nueva, la ejecución emparejada va en el ledger y en `--probe`) | `test_baseline_protocol_template.py::test_template_is_header_only`, `::test_template_crosses_protocol_fields_and_ca4_extras`, `::test_protocol_documents_every_template_column` | | ❌ |
| CA-5 | [Humano] pendiente (después del baseline oficial del probe, dentro de 7 días). Preparado: `$PUSHLLM_PRIVADO/piloto-artica/baseline/captura-antes-prerrellenada.csv` y `captura-despues-prerrellenada.csv` (49 filas cada uno, en el orden del protocolo) y `preguntas-en-orden.txt` (49, por app y bloque), generados con `baseline_docs.py --prefill`; los de 76 filas renombrados `*-obsoleto` | `test_baseline_protocol_template.py::test_prefill_rows_follow_the_template`, `::test_prefill_rejects_unknown_pass`, `::test_questions_in_order_text`, `::test_prefill_cli_writes_the_three_private_files`; filas, capturas y campos los cuenta el verificador en privado | | ❌ |
| CA-6 | Retirado (enmienda 2026-09-29 (b)): no hay pasada 2. `captura-p2-prerrellenada.csv` renombrado `captura-p2-prerrellenada-obsoleto.csv` | — | | ❌ |
| CA-7 | Procedimiento `docs/piloto-artica/procedimiento-recuento.md` (una pasada; §3 AI Overviews en recuentos; §6 comparación app frente a probe, veredicto y qué hacer si no) y `docs/piloto-artica/tools/count_baseline.py` (`count`, `read_probe` —rechaza `results.csv` sin `searched_urls`—, `summarize_probe`, `compare_with_probe`, `render_calibration`, CLI `--probe`). **Falta** `calibracion-antes.md` privado (necesita el baseline del probe y la pasada "antes") | `docs/piloto-artica/tools/tests/test_baseline_count.py` (pasada: SoV bruto, sin ponderado, posición, en su lugar, Google en recuentos, dominios, observaciones, marcas, pasadas mezcladas, `AR`/`AG` ignoradas; probe: lectura, mayoría/empate/mediana, errores/otros niveles/Claude fuera; comparación: acuerdo, SoV, veredicto y umbrales, ventana, posición informativa, modelos; informe y CLI) y `test_baseline_procedure.py` — fixtures ficticias | | ❌ |
| CA-8 | Regla de congelación en `prompts-baseline.md` ("Estado del set": como tarde al empezar el baseline oficial del probe, o fecha del humano; la pasada "antes" no empieza sin ella). Aviso de techo: ya no es de la manual (SPEC-008 CA-10); `count_baseline.py` no calcula ponderado. **Falta** la fecha de congelación | `test_baseline_prompts.py::test_intro_and_state_reflect_the_calibration`, `::test_freeze_no_longer_tied_to_pass_1`; `test_baseline_count.py::test_no_manual_weighted_figure` | | ❌ |
| CA-9 | `$PUSHLLM_PRIVADO/piloto-artica/baseline/foto-tecnica-2026-09-29/` (`foto-tecnica.md`, `raw/robots.txt`, `raw/sitemap_index.xml` + 8 sitemaps, HTML y JSON-LD de portada, contacto y una página por línea, `raw/SHA256SUMS.txt`). **Falta**: Google Business Profile (lo mira el humano) y los dominios citados en la pasada "antes" y en el baseline del probe | Comprobación manual del verificador (fechas y URLs en `foto-tecnica.md`) | | ❌ |
| CA-10 | **Pendiente** de la pasada "antes" (respuestas representativas del núcleo; cifras del probe solo si CA-7 dice que coinciden). Comprobador de términos prohibidos listo: `python docs/piloto-artica/tools/baseline_docs.py "$PUSHLLM_PRIVADO/piloto-artica/baseline/hallazgo-reunion.md"` | `docs/piloto-artica/tools/tests/test_baseline_frontier.py::test_forbidden_meeting_terms` | | ❌ |
| CA-11 | [Verificador]. Apoyo: `baseline_docs.py` sin argumentos revisa `docs/piloto-artica/` (emails, teléfonos, cifras junto a marcas); `--prefill` y `count_baseline.py --out` escriben solo en la ruta privada que se les da | `test_baseline_frontier.py::test_repo_docs_pass_the_frontier` y `::test_frontier_detects_email_phone_and_figure_next_to_brand` | | ❌ |

Tests (2026-09-29, tras la enmienda (b)): `python -m pytest -q docs/piloto-artica/tools/tests` (200 en verde) y
`python -m pytest -q probe/tests` (213 en verde, 1 saltado sin `PUSHLLM_PRIVADO`; sin cambios en `probe/`), con el
entorno `probe/.venv` (el Python del sistema no tiene el SDK `anthropic` y falla `test_raw_responses.py::test_real_sdk_objects_serialize_without_http_headers`, ajeno a esta spec). `ruff check probe docs/piloto-artica/tools`: OK.

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

### Ampliación por niveles (g)–(j) — 2026-09-29, antes de la pasada 1
- **Emisor**: sdd-implementador aplicando `.ai-context/skills/sdd-metricas.md`. **Fuentes**:
  las del dictamen anterior más ADR-005 (§4 indicadores separados, §6 no se promete) y la
  enmienda de SPEC-007 (CA-1, CA-2, CA-7, CA-8). Ningún punto cambia una regla de negocio:
  `AR`/`AG` no son SoV (RN-02/RN-03 siguen aplicándose solo al núcleo, que es el set de la
  clínica para el Go).
- **(g) Indicadores de `AR` y `AG` — correcto con condiciones.** Por nivel, app (ChatGPT,
  Gemini, Google con resumen de IA) y pasada: **"x de n"** respuestas válidas con la
  clínica; en Google, además, cuántas búsquedas tuvieron resumen. Sin ponderado.
  Definiciones operativas, iguales en el "después" de SPEC-012 (periodo = las dos pasadas
  "antes" o las dos "después"):
  - `AR` "aparece con cierta regularidad" ⇔ al menos **2 casillas** pregunta × app en las
    que la clínica aparece en **las dos** pasadas del periodo.
  - `AG` "aparece alguna vez" ⇔ al menos **1** respuesta válida del periodo, en cualquier
    app, con la clínica.
  Las dos se deciden con sí/no desde el CSV y se reproducen a mano.
- **(h) Separación del núcleo — correcto.** El ponderado del criterio Go, la estabilidad de
  P-3 y el aviso de techo de CA-8 usan **solo** `AV`. Ninguna cifra `AR`/`AG` se suma,
  promedia ni pondera con el núcleo (ADR-005 §4). Verificable: el ponderado del núcleo es el
  mismo si se borran las filas `AR` y `AG`.
- **(i) Clínicas de fuera de la comarca y posición — correcto con condiciones.** Una cadena
  con varias sedes cuenta como **una marca** (nombre canónico en `alias-canonicos.csv`); la
  sede, si la respuesta la dice, va a `observaciones`. Motivo: RN-01 casa por nombre y las
  respuestas no siempre dan la sede. La posición (RN-06) se informa en `AR`/`AG` como
  **lista de puestos**, sin media (con tan pocas respuestas, la media engaña).
- **(j) Ruido — correcto.** Con 4–5 preguntas por nivel y 2 pasadas hay 8–10 respuestas por
  app: una sola respuesta mueve 10–12 puntos y el margen del 95 % supera ± 30 puntos. Solo
  **recuentos** ("x de n"), nunca porcentajes.
- **(a), (b), (d), (e) en los niveles**: (a) alias y reglas de mención, iguales; (b) los
  niveles van en las mismas dos pasadas y con la misma separación, sin pasadas propias;
  (d) Google con resumen de IA se cuenta dentro de cada nivel como una app más, sin
  ponderar; si no hay resumen, la búsqueda es válida y sin clínica; (e) mismo instrumento
  también en los niveles. (c) y (f) siguen siendo solo del núcleo.

### Segunda ampliación (k)–(n) — calibración, 2026-09-29, antes de la pasada "antes"
- **Emisor**: sdd-implementador aplicando `.ai-context/skills/sdd-metricas.md` (advisory,
  sin cambiar reglas). **Fecha**: 2026-09-29; la pasada "antes" no ha empezado y el
  baseline oficial del probe (SPEC-008 CA-7) tampoco. **Fuentes**: las de los dictámenes
  anteriores; SPEC-007 enmienda (b) (CA-2 k–n, CA-3, CA-5, CA-7, CA-8); SPEC-008 CA-7 y CA-9;
  SPEC-013 y `docs/fundacion/dominio.md` (URLs citadas frente a consultadas);
  `probe/run_probe.py` (`COLUMNS`), `probe/analysis.py` (SoV bruto sobre todas las
  respuestas válidas de los runs) y `probe/batches/viveiro.json` (ubicación Viveiro,
  `client_brand`); ADR-005 §4. Decisiones del humano del 2026-09-29 que se aplican tal cual:
  49 consultas; AI Overviews solo en el núcleo; **orden: primero el baseline oficial del
  probe y después la pasada "antes"**, emparejada con esa ejecución; P-5 cerrada; pasadas
  desde Vilaboa.
- **Ninguna regla de negocio cambia.** RN-01 (alias), RN-02 (SoV bruto sobre respuestas
  válidas), RN-04 (AI Overviews aparte) y RN-06 (posición sin directorios) se aplican igual;
  lo nuevo son reglas de lectura de la calibración, que no entran en ninguna cifra del Go.

#### (k) Qué se compara y con qué — **correcto con condiciones**
1. **Unidad**: la casilla pregunta `AV` × asistente presente en los dos instrumentos:
   ChatGPT (app `chatgpt` ↔ proveedor `openai`) y Gemini (`gemini` ↔ `gemini`). 15 × 2 = 30
   casillas. Claude (solo en el probe) y Google (solo en la manual) no tienen pareja.
2. **Lado app**: la fila de la pasada que cuenta (cuenta gratuita, Vilaboa, respuesta
   válida): "sale" si `artica_nombrada` = `si`, y `posicion_artica`.
3. **Lado probe**: las filas de `results.csv` con `prompt_id` `AV…`, ese proveedor y
   `status` = `ok`. Se usa la columna `brands_mentioned` tal como la escribió el probe (lo
   reproduce cualquiera con una hoja de cálculo): la clínica "sale" en un run si
   `Clínica Ártica` está en la lista; su posición es su puesto en esa lista (que ya excluye
   directorios, RN-06).
4. **Resumen de runs por casilla**: `k de n` runs válidos con la clínica. "Sale" si
   k/n > 1/2; "no sale" si k/n < 1/2; **"empate"** si k/n = 1/2 (posible con 2 runs). La
   posición del probe es la **mediana** de sus puestos en los runs donde sale.
5. **Qué ejecución del probe**: la del baseline oficial de SPEC-008 CA-7 (decisión del
   humano: primero el baseline, después la pasada "antes"). En el "después" (SPEC-012), la
   medición "después" del probe más cercana en fechas. **Ventana máxima: 7 días** entre la
   ejecución `AV` del probe (fechas de sus filas `AV`) y la pasada manual (fechas de sus
   filas); si los dos intervalos se solapan, la distancia es 0. Motivo: una semana es la
   cadencia de medición del piloto (SPEC-012) y deja margen para repartir la pasada en 2
   días; más allá, un cambio de modelo o del índice de búsqueda se confunde con una
   diferencia de instrumento. Si la pasada cae fuera de la ventana, la comparación se hace
   igual pero el veredicto es "no" (hay que lanzar una ejecución `AV` del probe dentro de la
   ventana, que no sustituye al baseline oficial).
6. **Diferencias conocidas, sin corregir**: (i) la manual se hace desde **Vilaboa** y el
   probe envía la ubicación **Viveiro**. Todas las `AV` nombran el lugar, así que en ChatGPT
   y Gemini el efecto esperable es pequeño; no se corrige ni se estima aparte: la
   calibración mide "instrumento + ubicación" juntos, que es justo lo que importa (lo que ve
   un paciente que pregunta nombrando el sitio frente a lo que mide el probe). Si el
   veredicto es "no", la ubicación es una de las causas a revisar (l.4). (ii) Modelo de la
   app gratuita frente al modelo por defecto de la API (D-5, RN-10): se anota
   `modelo_mostrado` y la columna `model` del probe; que no coincidan no invalida la
   comparación (es la diferencia que la calibración mide), pero se escribe en el informe.
   (iii) El probe solo reconoce las marcas de su catálogo y la manual anota todas las
   clínicas nombradas: la posición del probe puede salir mejor. Por eso la posición no
   entra en el veredicto (l.2).

#### (l) "Coinciden de forma razonable" — **correcto con condiciones**
1. **Acuerdo por asistente** = casillas comparables con el mismo resultado ÷ casillas
   comparables. Comparable = fila válida en la app y ≥ 1 run válido en el probe. Mismo
   resultado = "sale/sale" o "no sale/no sale"; un **empate** del probe cuenta como
   acuerdo (con p = 1/2 cualquier respuesta de la app es compatible).
2. **Veredicto "coinciden de forma razonable: sí"** si y solo si se cumplen **todas**:
   (a) la pasada está dentro de la ventana de 7 días (k.5); (b) en ChatGPT **y** en Gemini
   hay **≥ 12 casillas comparables** (de 15); (c) en cada uno el **acuerdo es ≥ 70 %**
   (con 15 comparables, ≥ 11); y (d) en cada uno la **diferencia de SoV bruto** entre app
   (menciones ÷ respuestas válidas `AV` de la pasada) y probe (runs con la clínica ÷ runs
   válidos `AV`, como `probe/analysis.py`) es **≤ 20 pts** en valor absoluto. Si falla
   una, "no". La **posición** se informa (casillas donde sale en los dos; "parecida" si la
   diferencia es ≤ 2 puestos), pero no decide.
3. **Ruido esperable con 15 casillas**: si los dos instrumentos midieran lo mismo, la app
   (una respuesta) difiere de la mayoría de runs solo por azar; con casillas casi siempre
   "sale" o casi siempre "no sale" el acuerdo esperable es ≥ 85 %, y con casillas
   repartidas, en torno al 75 %. El error típico de un acuerdo del 80 % con 15 casillas es
   ≈ 10 pts: el umbral del 70 % queda ≈ 1 error típico por debajo, y 11 de 15 no se
   alcanza por suerte si los instrumentos no se parecen. Para el SoV bruto, el error típico
   de la diferencia app (15 respuestas) − probe (≈ 45 runs) llega a ≈ 15 pts con un SoV del
   50 % y ≈ 12 pts con uno del 20 %: 20 pts es ≈ 1,3–1,7 errores típicos. Son umbrales de
   **alarma**, no una prueba estadística: con esta muestra no se puede afirmar igualdad,
   solo detectar una diferencia gruesa.
4. **Si no coinciden**: se revisa, en este orden, y se anota en el ledger qué se ha
   encontrado: (1) **lectura**: releer las capturas y los `answer` del probe de las casillas
   en desacuerdo (alias o variante no reconocida, adjetivo, médica sin clínica); (2)
   **protocolo manual**: desviaciones, cuenta, modo, modelo mostrado, fechas; (3)
   **configuración del probe**: modelo por defecto (RN-10), búsqueda web activa, ubicación
   Viveiro; (4) **ubicación Vilaboa/Viveiro** como causa posible, sin corregirla. Hasta que
   el ledger tenga la causa y la **decisión del humano** (qué se ajusta, o seguir con la
   salvedad escrita), **no se enseña a la clínica ninguna cifra del probe** ni se envía la
   propuesta de SPEC-009 (CA-7). Si el humano decide repetir la pasada, la nueva se empareja
   con una ejecución `AV` del probe dentro de la ventana y el informe da **las dos**, sin
   elegir la que más convenga.

#### (m) Google AI Overviews — **correcto con condiciones**
1. Canal aparte (RN-04, D-6): **fuera del acuerdo, del veredicto y del criterio Go**. Solo
   en el núcleo `AV` (decisión del humano: `AR`/`AG` no se miden en Google).
2. Con 15 búsquedas y una pasada se dan **recuentos "x de n"**, sin porcentajes: búsquedas
   válidas; cuántas tuvieron resumen de IA; en cuántas sale la clínica **dentro** del
   resumen, sobre las válidas y sobre las que tuvieron resumen. Una búsqueda mueve 6,7
   pts: un porcentaje daría una precisión que no hay.
3. **Sin resumen**: la búsqueda es válida, cuenta en el denominador de "sobre las
   válidas" y sin la clínica (lo que ve el paciente: por esta vía no la ve). El paquete de
   mapas y los resultados normales no cuentan; pueden ir en `observaciones`.
4. **Antes/después (SPEC-012)**: se informa "x de n antes → y de n después", junto con
   cuántas búsquedas tuvieron resumen en cada pasada (Google puede mostrar más o menos
   resúmenes por su cuenta). Solo se describe como **cambio claro** si la diferencia es de
   **≥ 5 búsquedas** con la clínica sobre las mismas 15 (margen del 95 % de una diferencia
   de dos proporciones con n = 15 ≈ ± 33 pts ≈ 5 búsquedas); si no, "dentro de lo que varía
   de un día a otro". Sin objetivo ni promesa. La ubicación Vilaboa pesa más aquí que en
   ChatGPT y Gemini: se escribe como limitación.

#### (n) Qué queda del dictamen anterior
| Punto | Estado | Detalle |
|---|---|---|
| (a) alias y reglas de mención | **Sigue** | Igual en la lectura de la manual. P-1 y P-2 siguen. |
| (b) dos pasadas, 3–10 días, ± 2 h | **Sustituido** | Una pasada "antes" y una "después" (SPEC-012), cada una emparejada con una ejecución `AV` del probe dentro de la ventana de 7 días (k.5). La separación 3–10 días queda sin objeto. |
| (c) SoV bruto, válida/excluida, cuentas gratuitas, Claude observación | **Sigue** | SoV bruto por app de la pasada ("lo que ve el paciente" y término de (l.2 d)). |
| (c) SoV ponderado manual | **Sin objeto** | **No se calcula.** Evita que una cifra manual se lea como Go. El ponderado solo existe en el probe (SPEC-008 CA-9 b). |
| (d) AI Overviews aparte | **Sustituido por (m)** | Mismo canal aparte; ahora recuentos "x de n" sin porcentajes y regla de lectura del antes/después. |
| (e) mismo instrumento | **Sigue, reforzado** | El Go es probe contra probe (SPEC-008 CA-7/CA-9). Ninguna cifra manual se resta, suma ni promedia con una del probe; la manual antes/después es descriptiva. |
| (f) ruido frente a +15 pts | **Sin objeto en la manual** | El ruido del Go se re-evalúa con el probe en SPEC-008 CA-9 (e). El ruido de la calibración está en (l.3). |
| (g)–(j) niveles `AR`/`AG` | **Sin objeto en la manual** | `AR` y `AG` ya no se preguntan a mano; sus definiciones se trasladan al probe en SPEC-008 CA-9 (g). |
| "b/d en niveles" | **Sin objeto** | Ya no hay bloques `AR`/`AG` en la pasada. |

### Tercera ampliación (o)–(s) — calibración por nivel, 2026-09-29, antes de la pasada "antes"
- **Emisor**: sdd-implementador aplicando `.ai-context/skills/sdd-metricas.md` (advisory, sin
  cambiar reglas), como las ampliaciones anteriores. **Fecha**: 2026-09-29; la pasada "antes"
  no ha empezado. **Fuentes**: las de los dictámenes anteriores; SPEC-007 enmienda (c) (CA-2
  o–s, CA-3, CA-5, CA-7, CA-10) y sus decisiones del gate (AR primero; un veredicto `AR`
  débil basta para contar el objetivo sin garantía; la ejecución `AR` la fija este
  dictamen); ADR-009 §2 y §5 (niveles nunca en una cifra común); SPEC-008 CA-7 (baseline
  oficial: `AV` con 3 runs, `AR` con 1 run) y CA-11/CA-12 (dictamen del Go con `AR`: las filas
  `AR` de 1 run del baseline no sirven como base de (C); el "antes" de `AR` tiene 3 runs,
  ejecutado el 2026-09-29, `…\piloto-artica\probe-AR-antes\`); ADR-004 §2.
- **Ninguna regla de negocio cambia.** RN-01, RN-02, RN-04 y RN-06 se aplican igual. Lo nuevo
  son reglas de lectura de la calibración por nivel; ninguna entra en (C), en (D) ni en otra
  cifra del Go. Aquí solo hay reglas y umbrales: ningún dato de visibilidad de la clínica
  (ADR-004 §2).

#### (o) `AR`: qué se compara y con qué — **correcto con condiciones**
1. **Unidad**: la casilla pregunta `AR` × asistente presente en los dos instrumentos
   (ChatGPT ↔ `openai`, Gemini ↔ `gemini`): 5 casillas por asistente, 10 en total. Claude
   (solo probe) y Google (solo manual) no tienen pareja.
2. **Ejecución emparejada: el "antes" de `AR` de SPEC-008 CA-12** (3 runs, mismo diseño que
   (C)), **no** las filas `AR` del baseline oficial (CA-7). Motivos: (i) con 1 run una casilla
   no se puede resumir por mayoría ni distinguir una casilla estable de una repartida, que
   es justo lo que hace falta en un nivel con resultados repartidos; (ii) SPEC-008 CA-11 ya
   descartó esas filas como base de (C): calibrar contra ellas sería calibrar un instrumento
   que el Go no usa. En el "después" (SPEC-012), la medición `AR` "después" del probe más
   cercana en fechas, con sus 3 runs. **Ventana máxima: 7 días**, igual que (k.5), medida con
   las fechas de las filas `AR` del probe y las de las filas `AR` de la pasada (0 si se
   solapan). La ventana `AR` y la `AV` (q) se comprueban **por separado**. Fuera de la
   ventana: la comparación se hace, pero el veredicto `AR` es "no"; si hace falta otra
   ejecución `AR` (`--levels AR --runs 3`, directorio nuevo, con autorización del humano),
   no sustituye al "antes" de CA-12 como base de (C).
3. **Lado app y lado probe**: como (k.2) y (k.3), con `AR` en lugar de `AV`. El
   `results.csv` de `AR` se lee aparte del de `AV`; de cada fichero solo cuentan las filas de
   su nivel.
4. **Resumen de runs** (matiza k.4): "k de n" runs válidos con la clínica. La casilla del
   probe es **comparable** solo con **≥ 2 runs válidos** (con 1 no hay resumen posible). Es
   **unánime** si k = 0 o k = n (la clínica sale en todos los runs o en ninguno) y
   **repartida** en cualquier otro caso (con 3 runs, 1 de 3 o 2 de 3; con 2 runs, el empate).
   Se sigue dando la mayoría ("sale", "no sale", "empate") y la posición mediana, pero lo que
   decide en (p) es unánime/repartida.
5. **Diferencias conocidas** (matiza k.6): (i) **ubicación**: las preguntas `AR` se formulan
   desde Ferrolterra, Vilalba, Sarria/A Fonsagrada o Tapia de Casariego; la manual se hace
   desde **Vilaboa** y el probe envía **Viveiro**, y ninguno de los dos está en el lugar del
   paciente. Aquí pesa más que en `AV`: la ubicación Viveiro del probe está al lado de la
   clínica y puede empujarla hacia arriba en una pregunta que pide desplazarse, y Vilaboa la
   aleja. No se corrige (sería inventar un efecto); la calibración mide "instrumento +
   ubicación" juntos, se escribe como limitación en el informe y es la primera causa
   candidata en un "no" tras la lectura. (ii) Modelo de la app frente al de la API y (iii)
   catálogo cerrado del probe: como (k.6).
6. **Clínicas de fuera de la comarca** (se reactiva (i), solo para la lectura manual de
   `AR`): una cadena con varias sedes cuenta como **una marca** (nombre canónico en
   `alias-canonicos.csv`); la sede, si la respuesta la dice, va a `observaciones`. La
   posición de la clínica en `AR` se informa como **lista de puestos**, sin media.

#### (p) "Coinciden de forma razonable" en `AR` — **dudoso con 5 casillas: el veredicto se rebaja a "sin discrepancia gruesa"**
1. **Qué se puede afirmar**: con 5 casillas por asistente **ningún umbral de acuerdo
   distingue un acuerdo real de uno por azar**. Si la clínica sale poco en `AR`, los dos
   instrumentos dirán "no sale" en casi todas las casillas y el acuerdo será alto aunque no
   midan lo mismo; si sale repartida, dos instrumentos idénticos discrepan a menudo (una
   casilla con 1 de 3 o 2 de 3 runs discrepa de la app por puro azar una vez de cada tres, y
   una con p ≈ 1/2, la mitad de las veces). Una casilla mueve 20 pts del acuerdo. Por eso
   **en `AR` no se afirma "coinciden de forma razonable"**: el veredicto se rotula
   "**sin discrepancia gruesa en `AR`: sí / no**" y el informe dice que es un veredicto débil
   (solo descarta una contradicción clara), sin preguntas nuevas (set congelado).
2. **Discrepancia gruesa**: una casilla comparable (app válida y probe con ≥ 2 runs válidos)
   **unánime** en el probe en la que la app dice lo contrario (probe en todos los runs y app
   "no sale", o probe en ninguno y app "sale"). Una casilla **repartida** es **compatible**
   con cualquier respuesta de la app (generaliza el empate de (l.1): la app, con una sola
   respuesta, puede salir de cualquiera de los dos lados).
3. **Veredicto "sin discrepancia gruesa en `AR`: sí"** si y solo si se cumplen **todas**:
   (a) la pasada está dentro de la ventana de 7 días respecto a la ejecución `AR` (o.2); y en
   ChatGPT **y** en Gemini (b) hay **≥ 4 casillas comparables** (de 5); (c) hay **≥ 3
   casillas decisivas** (comparables y unánimes en el probe): con menos no hay nada que
   contrastar y el "sí" sería vacío; y (d) hay **como mucho 1 discrepancia gruesa**. Si falla
   una, "no". El veredicto es **por asistente y después de nivel** (los dos asistentes
   tienen que pasar), sobre las 10 casillas `AR`, **nunca** junto con `AV`.
4. **Ruido**: si los dos instrumentos midieran lo mismo, una casilla unánime en 3 runs
   corresponde a una probabilidad real alta o baja, y que la app salga del otro lado es poco
   probable (del orden de 1 de cada 10 o menos); **dos** contradicciones en 5 casillas por
   azar es raro. Con 1 permitida, el "no" señala una diferencia gruesa de verdad, no mala
   suerte. Es un umbral de **alarma**, no una prueba.
5. **SoV bruto en `AR`: no se usa en el veredicto.** Con 5 respuestas de la app una sola
   mueve 20 pts y el error típico de la diferencia app − probe supera ± 25 pts con resultados
   repartidos: un tope sería ruido. Se informan los dos lados como **recuentos** ("x de 5" en
   la app, "k de n" runs en el probe), **sin porcentajes** (como (j)).
6. **Posición**: informativa, como lista de puestos por casilla en los dos lados; no decide.
7. **Si es "no"**: se revisa en el orden de (l.4) (lectura → protocolo manual →
   configuración del probe → ubicación, que aquí pesa más, o.5) y se anota en el ledger la
   causa y la **decisión del humano para `AR`**. Hasta entonces **no se enseña a la clínica
   ninguna cifra `AR` del probe** y **se revisa la frase del objetivo de SPEC-009** antes de
   enviar la propuesta. Un "no" no cambia cómo se calcula (C) (probe contra probe, CA-2 e):
   el humano decide si (C) sigue tal cual o con la salvedad escrita. Un "sí" débil basta para
   contar el objetivo en la propuesta **como objetivo, no como dato ni garantía** (decisión
   del humano en el gate). Ninguna cifra manual entra en (C).

#### (q) `AV` con 2 asistentes — **correcto: (k) y (l) siguen, sin cambiar umbrales**
1. Casilla pregunta `AV` × asistente (ChatGPT, Gemini): 15 por asistente, 30 en total. La
   ausencia de filas Google no toca el acuerdo: Google nunca estuvo en él ((k.1), (m.1)).
2. **Ejecución emparejada**: el baseline oficial (SPEC-008 CA-7, `AV` con 3 runs,
   `…\piloto-artica\probe\`), con la ventana de 7 días de (k.5) medida con sus filas `AV`. En
   el "después", la medición "después" del probe más cercana.
3. **Umbrales de (l.2), sin cambios**: ≥ 12 casillas comparables, acuerdo ≥ 70 % y diferencia
   de SoV bruto ≤ 20 pts en cada asistente; posición informativa (± 2 puestos). Con 15
   casillas el ruido de (l.3) sigue igual. Veredicto rotulado "**coinciden de forma razonable
   en `AV`: sí / no**".
4. **Si es "no"**: orden de revisión de (l.4); **no se enseña a la clínica ninguna cifra `AV`
   del probe** y **se revisa la frase "ya sois la clínica que la IA recomienda en A Mariña"**
   de SPEC-009 antes de enviar. Ninguna cifra manual entra en (D).

#### (r) Google AI Overviews en `AR` — **correcto con condiciones**
1. Canal aparte (RN-04, D-6): **fuera del acuerdo, de los dos veredictos y del Go** ((C)
   incluida). Solo búsquedas `AR` (5 por pasada); en `AV` ya no hay búsquedas Google.
2. Con 5 búsquedas y una pasada se dan **recuentos "x de 5"**, sin porcentajes: búsquedas
   válidas; cuántas tuvieron resumen de IA; en cuántas sale la clínica **dentro** del
   resumen, sobre las válidas y sobre las que tuvieron resumen. **Sin resumen**: búsqueda
   válida, en el denominador de "sobre las válidas" y sin la clínica. El paquete de mapas y
   los resultados normales no cuentan (van a `observaciones`).
3. **Ubicación**: Google pesa mucho la ubicación del dispositivo. Una búsqueda que nombra
   Ferrol, Vilalba, Sarria o Tapia hecha desde Vilaboa mide "alguien de Pontevedra que busca
   en esa zona", no al paciente de allí. No se corrige; se escribe como limitación y se
   repite igual en el "después" (misma ubicación, P-4).
4. **Antes/después (SPEC-012)**: la regla de "cambio claro" de (m.4) (≥ 5 búsquedas de 15)
   **no cabe** y se **sustituye**: con 5 búsquedas el margen del 95 % de una diferencia de dos
   proporciones es de unos ± 60 pts, más que casi cualquier cambio posible. El antes/después
   de este canal **solo se describe**: "x de 5 antes → y de 5 después", con las búsquedas con
   resumen de cada pasada; nunca se llama "cambio claro", ni mejora ni empeoramiento, ni se
   pone objetivo ni promesa.

#### (s) Qué queda del dictamen anterior
| Punto | Estado | Detalle |
|---|---|---|
| (k.1) unidad | **Sigue en `AV`** | 15 × 2. `AR` tiene su unidad propia (o.1). |
| (k.2)–(k.3) lado app y lado probe | **Siguen**; en `AR` **matizados** | En `AR`, su propio `results.csv` y solo sus filas (o.3). |
| (k.4) resumen de runs | **Sigue en `AV`**; en `AR` **matizado** | En `AR`, ≥ 2 runs válidos y unánime/repartida (o.4). |
| (k.5) ejecución y ventana | **Sigue en `AV`** (q.2); en `AR` **sustituido** por (o.2) | Dos ejecuciones emparejadas, dos ventanas de 7 días, comprobadas por separado. |
| (k.6) diferencias conocidas | **Sigue**; en `AR` **matizado** | La ubicación pesa más en `AR` (o.5). |
| (l) "coinciden de forma razonable" | **Queda solo para `AV`** (q.3), sin cambios de umbral | En `AR` lo sustituye (p): "sin discrepancia gruesa". |
| (m) AI Overviews | **Sin objeto en `AV`** (no hay búsquedas `AV` en Google) | Su lectura pasa a `AR` según (r); (m.4) sustituido por (r.4). |
| (n)(b) una pasada | **Sigue** | Una pasada "antes" y una "después", cada una con 49 consultas y dos ejecuciones emparejadas. |
| (n)(c) sin ponderado manual | **Sigue, en los dos niveles** | Tampoco hay ponderado manual en `AR`. |
| (n)(e) mismo instrumento | **Sigue** | (C) y (D) son probe contra probe; ninguna cifra manual entra en ellas. |
| (n)(f) ruido del Go | **Sin objeto en la manual** | Sin cambios. |
| (n)(g) indicadores de `AR` | **Sin objeto en la manual** | Los indicadores de `AR` del Go son los del probe (SPEC-008 CA-11). |
| (n)(i) cadenas y posición | **Reactivado solo para la lectura manual de `AR`** (o.6) | Cadena = una marca; puestos en lista, sin media. |
| (n)(j) solo recuentos | **Reactivado para `AR`** | Todo lo de `AR` (app, probe, Google) en recuentos, sin porcentajes. |
| `AG` | **Sigue fuera de la manual** | Ni calibración ni AI Overviews. |
- **Regla transversal**: **ninguna regla suma, promedia ni pondera casillas, acuerdos,
  recuentos ni SoV de `AR` y `AV` en una cifra o en un veredicto común**; no hay veredicto
  "global" (ADR-005 §4, ADR-009 §2). El informe tiene una sección por nivel.
- **Plantilla**: no hace falta columna nueva: el nivel sale del prefijo de `id_pregunta` y las
  dos ejecuciones emparejadas van en el ledger y en la línea de órdenes (`--probe-av`,
  `--probe-ar`).

### Tabla condición → cambio
| Condición | Cambio | Dónde |
|---|---|---|
| a1–a3 alias de Ártica, dominio no es mención | Reglas de mención al leer capturas | `procedimiento-recuento.md` §0.3; columna `artica_nombrada` |
| a2 adjetivo | Marca `#artica-adjetivo` y recuento de marcas | `procedimiento-recuento.md` §0.3; `count_baseline.py` (`adjective_flags`); test `test_adjective_flag_is_reported` |
| a4 nombre de la médica | Se anota en observaciones; no cuenta | `procedimiento-recuento.md` §0.3 (implícito: solo nombre/alias de la clínica); P-2 |
| a5 competidores y variantes | `alias-canonicos.csv` privado | `procedimiento-recuento.md` §0.4; `count_baseline.py --aliases`; test `test_clinics_in_its_place_are_canonicalised` |
| a6 posición sin directorios | Definición de `posicion_artica` | `protocolo-captura.md` (campos); `procedimiento-recuento.md` §0.3 |
| ~~b 2 pasadas, 3–10 días, ± 2 h~~ **sustituida por (n)(b)** | Plazo y hora de la pasada 2 | `protocolo-captura.md` "Pasada 2 y siguientes"; CA-6 |
| c válida/excluida | Columna `respuesta_valida` | `plantilla-captura.csv`; `protocolo-captura.md`; test `test_raw_sov_per_app` |
| c solo cuentas gratuitas | `plan_cuenta`; filtro de filas principales | `protocolo-captura.md` "Antes de empezar" 3; `count_baseline.py` (`MAIN_PLANS`); test `test_observation_and_brand_rows_apart` |
| ~~c ponderado normalizado ChatGPT+Gemini~~ **sin objeto (n)(c)**: tests `test_weighted_*` retirados | Fórmula | `procedimiento-recuento.md` §3; tests `test_weighted_*` |
| c Claude como observación | Solo observación, en las dos pasadas o en ninguna | `protocolo-captura.md` "Opcional"; `count_baseline.py` (`PAIRED` sin Claude); test `test_observation_and_brand_rows_apart` |
| d AI Overviews aparte (**sustituida por (m)**) | Columna `resumen_ia`; dos cifras | `plantilla-captura.csv`; `procedimiento-recuento.md` §4; tests `test_google_*` |
| e mismo instrumento | Condiciones iguales en todas las pasadas; set congelado | `protocolo-captura.md` "Antes de empezar" 2; `prompts-baseline.md` "Estado del set" |
| ~~f ruido~~ **sin objeto en la manual (n)(f)**: `test_sov_per_pass` y `test_stability_per_question` retirados | Estabilidad por pregunta y SoV por pasada en el recuento | `procedimiento-recuento.md` §2 y §6; tests `test_sov_per_pass`, `test_stability_per_question` |
| ~~g indicadores `AR`/`AG`~~ **sin objeto (n)(g–j)**, histórico | "x de n" por nivel × app × pasada; regularidad (≥ 2 casillas estables) y alguna vez (≥ 1) | `procedimiento-recuento.md` §7; `count_baseline.py` (`count_level`, `AR_MIN_STABLE_CELLS`); tests `test_level_counts_per_app_and_pass`, `test_regularity_*`, `test_galicia_indicator_is_at_least_once` |
| h núcleo aparte (sigue en el probe; en la manual solo hay `AV`) | Go, estabilidad y techo solo con `AV` | `procedimiento-recuento.md` §1; `count_baseline.py` (el núcleo filtra `AV`); test `test_core_unchanged_when_level_rows_removed` |
| ~~i cadenas y posición~~ **sin objeto (n)** en la manual | Cadena = una marca en `alias-canonicos.csv`; puestos en lista | `procedimiento-recuento.md` §7; tests `test_chains_are_one_brand_in_levels`, `test_level_positions_are_listed_not_averaged` |
| ~~j solo recuentos~~ **sin objeto (n)** en la manual | Secciones de nivel sin porcentajes | `count_baseline.py` (`render`); test `test_render_levels_as_counts_without_percentages` |
| ~~b/d en niveles~~ **sin objeto (n)** | Una sola pasada con los tres niveles; Google dentro de cada nivel | `protocolo-captura.md` ("Antes de empezar" 4, "Cómo preguntar" 1); test `test_protocol_three_levels_block_order` |
| k1–k4 casilla, lado app, lado probe, resumen de runs (**solo `AV`** desde (s); en `AR`, (o)) | `summarize_probe` (mayoría k/n, empate, mediana de puestos) y `compare_with_probe` | `procedimiento-recuento.md` §6; `count_baseline.py`; tests `test_probe_cell_*`, `test_probe_position_*`, `test_agreement_*` |
| k5 ejecución emparejada y ventana de 7 días (**`AV`**, (q.2); en `AR`, (o.2)) | Baseline del probe primero; ventana comprobada por la herramienta | `protocolo-captura.md` "Antes de empezar" 1; `procedimiento-recuento.md` §6.1; `count_baseline.py` (`MAX_WINDOW_DAYS`); tests `test_window_*`; "Instrucciones para el humano" |
| k5 `results.csv` posterior a SPEC-013 | La herramienta rechaza un `results.csv` sin `searched_urls` | `count_baseline.py` (`read_probe`); test `test_read_probe_refuses_results_without_searched_urls` |
| k6 Vilaboa/Viveiro, modelo, catálogo | Limitaciones escritas; modelos en el informe | `protocolo-captura.md` "Antes de empezar" 2; `procedimiento-recuento.md` §6.4; render (`test_render_calibration_*`) |
| l1–l2 acuerdo y veredicto (**queda solo para `AV`**, (q.3)) | Umbrales 12 comparables, 70 %, 20 pts; posición informativa (≤ 2) | `procedimiento-recuento.md` §6.2–6.3; `count_baseline.py` (`MIN_COMPARABLE`, `MIN_AGREEMENT`, `MAX_SOV_GAP`, `POSITION_TOLERANCE`); tests `test_verdict_*` |
| l4 si no coinciden | Orden de revisión; sin cifras del probe a la clínica ni propuesta hasta decisión | `procedimiento-recuento.md` §6.5; texto del informe (`test_render_calibration_says_what_to_do_if_no`) |
| ~~m AI Overviews~~ **sin objeto en `AV` (s)**; sustituida por (r); `AIO_CLEAR_CHANGE` y los tests `test_google_*` sobre `AV` retirados | Recuentos "x de n" sin porcentajes; lectura antes/después (≥ 5 búsquedas) | `procedimiento-recuento.md` §3; `count_baseline.py` (`AIO_CLEAR_CHANGE`); tests `test_google_*`, `test_render_google_as_counts_without_percentages` |
| n (b) una pasada | Protocolo de 49 consultas, `pasada` = `antes`/`despues`; herramienta de una pasada | `protocolo-captura.md`; `count_baseline.py` (`_check`); tests `test_protocol_calibration_*`, `test_mixed_passes_fail_loudly` |
| n (c) sin ponderado manual | La herramienta no calcula ponderado | `count_baseline.py`; test `test_no_manual_weighted_figure` |
| n (f), (g)–(j), "b/d en niveles" | **Sin objeto en la manual** (filas `f`, `g`, `i`, `j` y "b/d en niveles" de arriba quedan históricas; `b` sustituida; `h` sigue en el probe) | Retirados `count_level`, estabilidad p1/p2 y sus tests; `test_level_rows_are_ignored` |
| o1–o3 casilla `AR` × asistente; ejecución `AR` = "antes" de SPEC-008 CA-12 (3 runs), ventana de 7 días propia; `results.csv` por nivel | `compare_ar` con su propio `results.csv`; `--probe-av` y `--probe-ar`; ventanas por nivel | `procedimiento-recuento.md` §6-AR.1; `protocolo-captura.md` "Antes de empezar" 1; `count_baseline.py` (`compare_ar`, `AR_MAX_WINDOW_DAYS`, `main`); tests `test_ar_*window*`, `test_cli_writes_two_tables_and_two_verdicts` |
| o4 ≥ 2 runs válidos; unánime / repartida | `summarize_probe(level="AR")` con `unanimous`; casilla con 1 run no comparable | `count_baseline.py` (`AR_MIN_VALID_RUNS`); tests `test_ar_probe_cell_*`, `test_ar_one_run_rows_are_not_comparable` |
| o5 ubicación Vilaboa/Viveiro frente a preguntas de fuera | Limitación escrita; primera causa candidata tras la lectura | `protocolo-captura.md` "Antes de empezar" 3; `procedimiento-recuento.md` §6-AR.5; render (`test_render_ar_writes_its_limits`) |
| o6 (reactiva i) cadenas y puestos en lista | Cadena = una marca; posiciones `AR` en lista, sin media | `procedimiento-recuento.md` §2; `count_baseline.py` (`count`, nivel `AR`); tests `test_ar_positions_are_listed_not_averaged`, `test_ar_chains_are_one_brand` |
| p1–p3 "sin discrepancia gruesa en `AR`": ≥ 4 comparables, ≥ 3 decisivas, ≤ 1 discrepancia gruesa por asistente; repartida = compatible; veredicto por asistente y de nivel | `compare_ar` y su veredicto | `procedimiento-recuento.md` §6-AR.2–6-AR.4; `count_baseline.py` (`AR_MIN_COMPARABLE`, `AR_MIN_DECISIVE`, `AR_MAX_GROSS`); tests `test_ar_verdict_*`, `test_thresholds_of_the_dictamen` |
| p5–p6 sin SoV ni porcentajes en `AR`; posición informativa | Recuentos "x de 5" y "k de n"; puestos en lista | `count_baseline.py` (`render_calibration`); tests `test_render_ar_sections_without_percentages`, `test_ar_verdict_ignores_sov` |
| p7 si es "no" en `AR` | Orden de revisión; sin cifras `AR` del probe a la clínica; revisar la frase del objetivo de SPEC-009; (C) no cambia | `procedimiento-recuento.md` §6-AR.6 y §7; render (`test_render_says_what_each_no_blocks`) |
| q `AV` con 2 asistentes | Mismos umbrales de (l.2); veredicto "coinciden de forma razonable en `AV`"; "no" revisa la frase "ya sois la clínica que la IA recomienda en A Mariña" | `procedimiento-recuento.md` §6-AV; `count_baseline.py` (`compare_av`); tests `test_verdict_*`, `test_render_says_what_each_no_blocks` |
| r AI Overviews solo `AR`: "x de 5", sin porcentajes; antes/después solo descrito | Google solo en `AR`; filas Google `AV`/`AM` rechazadas | `protocolo-captura.md`; `procedimiento-recuento.md` §3; `count_baseline.py` (`_check`, `count`); tests `test_google_overviews_only_in_ar`, `test_render_google_as_counts_without_percentages`, `test_google_av_or_am_rows_are_rejected` |
| s ningún número ni veredicto que combine niveles | Informe con una sección por nivel y dos veredictos | `count_baseline.py` (`render_calibration`); tests `test_render_never_combines_levels`, `test_levels_are_counted_apart` |
| CA-3/CA-5 (c) reparto de 49 filas | Orden `AR` → `AV` → `AM` en ChatGPT y Gemini, Google solo `AR`; `_check` exige el reparto y rechaza `AG` | `baseline_docs.py` (`CALIBRATION_BLOCKS`, `EXPECTED_LAYOUT`); `count_baseline.py` (`_check`); tests `test_calibration_order_blocks`, `test_incomplete_or_extra_layout_fails_loudly`, `test_ag_rows_are_rejected` |

### Tratamientos del nivel AG (CA-1)
Comprobado en clinicaartica.es el **2026-09-29** (HTTP 200; título y H1 de cada página):
- Trasplante capilar DHI:
  https://clinicaartica.es/tratamientos-capilares/microinjerto-capilar-con-tecnica-dhi/
  ("Microinjerto capilar con técnica DHI") y
  https://clinicaartica.es/tratamientos-capilares/trasplante-capilar/ ("Trasplante capilar").
- Blefaroplastia:
  https://clinicaartica.es/unidad-de-cirugia-estetica-facial/blefaroplastia-superior-rejuvenecimiento-mirada/
  ("Blefaroplastia superior"). La clínica ofrece la **superior**: por eso `AG03`/`AG04`
  preguntan por los párpados superiores. No hizo falta sustituir el tratamiento.

## Instrucciones para el humano — pasada "antes" de calibración (CA-5)
> **Obsoletas desde la enmienda 2026-09-29 (c) de SPEC-007 (sdd-arquitecto).** No empezar la
> pasada con estas instrucciones: el reparto de las 49 consultas cambia (ChatGPT y Gemini:
> `AR` → `AV` → `AM`; Google: solo `AR`) y hay dos ejecuciones del probe emparejadas. Tras la
> re-aprobación, el implementador las reescribe (F-SPEC-007-11). Se conservan como historial.

Vigentes desde el 2026-09-29 (enmienda (b), F-SPEC-007-8). 49 consultas: 60–90 min de
preguntas + 20–25 min de CSV y capturas. Todo desde **Vilaboa**.
0. **Orden** (tu decisión del 2026-09-29): **primero el baseline oficial del probe**
   (SPEC-008 CA-7). Al lanzarlo se congela el set (CA-8): anota aquí la fecha de
   congelación si no la has fijado antes. Apunta también la fecha y la carpeta de esa
   ejecución: es la que se empareja con esta pasada.
1. Haz la pasada **como mucho 7 días después** de esa ejecución del probe (ventana del
   dictamen (k)); si se te pasa, habrá que lanzar otra ejecución `AV` del probe dentro de la
   ventana (no sustituye al baseline). Hazla también **antes de la primera acción** del
   piloto.
2. Imprime `docs/piloto-artica/protocolo-captura.md` y abre
   `$PUSHLLM_PRIVADO/piloto-artica/baseline/preguntas-en-orden.txt` (17 en ChatGPT: AV01–AV15,
   AM01, AM02; 17 en Gemini, igual; 15 en Google: AV01–AV15).
3. Cuentas **gratuitas**: ChatGPT con memoria desactivada; Gemini con la actividad
   desactivada. Nada de VPN ni GPS simulado; el mismo ajuste de ubicación del móvil que
   usarás en el "después".
4. Crea `$PUSHLLM_PRIVADO/piloto-artica/baseline/AAAA-MM-DD-antes/` (fecha del primer día) y
   dentro: copia `captura-antes-prerrellenada.csv` como `captura-antes.csv`, un
   `desviaciones.txt` vacío y una carpeta `capturas/`.
5. Haz las consultas según el protocolo (chat temporal nuevo por pregunta, texto literal,
   captura completa; Google en incógnito). No pulses enlaces a la web de la clínica ni
   busques su nombre en Google. Si lo repartes en 2 días, corta entre apps.
6. Al terminar Google, en Google Maps (incógnito) busca **"medicina estética Viveiro"** y
   captura si sale la ficha de la clínica (reseñas, fotos, horario, web):
   `capturas/gbp.png` (CA-9).
7. Rellena en `captura-antes.csv` tus columnas (condiciones, hora, `respuesta_valida`,
   `resumen_ia`, `fichero_captura`, enlace, observaciones). Las de lectura las rellena el
   agente.
8. Avisa al orquestador con la fecha, el nº de filas, las desviaciones y la carpeta del
   probe emparejada. El agente hace `calibracion-antes.md` (CA-7, con el veredicto
   "coinciden de forma razonable"), la hoja de hallazgo (CA-10) y completa la foto técnica
   (CA-9).
9. El "después" (SPEC-012) se hace igual, con `captura-despues-prerrellenada.csv`, en
   `AAAA-MM-DD-despues/`, dentro de los 7 días de la medición "después" del probe.

## Instrucciones para el humano — pasada 1 (CA-5)
> **OBSOLETO desde la enmienda 2026-09-29 (b) (sdd-arquitecto).** No hagas esta pasada de
> 76 consultas. La spec ha vuelto a `borrador`: tras la re-aprobación, el implementador
> reescribe estas instrucciones para la pasada "antes" de calibración (49 consultas, solo
> `AV` + `AM`), según F-SPEC-007-8. Se conserva el texto como historial.

Tiempo: 95–140 min de consultas (76, una sola pasada con los tres niveles) + 25–30 min para
pasar capturas y rellenar el CSV. Se puede repartir en 2 días seguidos, cortando solo entre
bloques (y anotándolo).
Mejor **antes de la reunión** de SPEC-009. Todas las pasadas desde Vilaboa (P-4 revisada).
1. Imprime `docs/piloto-artica/protocolo-captura.md` y ábrete
   `$PUSHLLM_PRIVADO/piloto-artica/baseline/preguntas-en-orden.txt` (preguntas listas para
   copiar, en orden y por bloques: 26 en ChatGPT y 26 en Gemini (AV, AR, AG, AM), 24 en
   Google (AV, AR, AG)).
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
- **P-5** (2026-09-29, enmienda; → humano): **Mondoñedo no cabe** sin romper CA-1. Es
  A Mariña Central, así que no puede ir en `AR` ("ninguna nombra un municipio de A Mariña");
  `AG` no admite ciudades; y meterlo en el núcleo exigiría una `AV16`, que cambia el núcleo
  "tal cual" decidido por el humano y, con 5 `AR` y 4 `AG`, pasaría de 24 preguntas. Opción,
  si el humano la quiere: `AV16` con Mondoñedo y quitar una `AR` o una `AG` (total 24),
  antes de la pasada 1. Hoy queda fuera.
  **CERRADA el 2026-09-29 — decidido por el humano (Alberto Fojo), transmitido por el
  orquestador: sin cambios en el set.** Mondoñedo no entra; ninguna pregunta cambia.
- **P-6** (2026-09-29, enmienda; → arquitecto/humano): ADR-005 §1 enumera el área de
  influencia como Ferrolterra, norte de Lugo fuera de A Mariña y occidente de Asturias.
  **Sarria y A Fonsagrada** (interior de Lugo, al sur y al este) no están en esa lista,
  aunque sí dentro de "Lugo" de ADR-003 §1. `AR04` las incluye por decisión del humano y el
  set lo describe tal cual ("interior de Lugo"). Si se quiere que ADR-005 lo recoja
  literalmente, lo decide el arquitecto (no he editado el ADR).

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
  **Recogido el 2026-09-29 (b) (sdd-arquitecto)** con el nuevo instrumento: las dos
  mediciones "después" son del **probe**, en semanas distintas (SPEC-012 CA-3 (2) y CA-7);
  forma, separación y ruido los fija el dictamen de SPEC-008 CA-9.
- **F-SPEC-007-6**: **hecho el 2026-09-29 por sdd-implementador** tras la re-aprobación
  humana (commits 355ae66, e29044a y el de este ledger). Lista original:
- ~~F-SPEC-007-6~~ (→ sdd-implementador, **tras la re-aprobación humana** de la enmienda
  del 2026-09-29; sdd-arquitecto). La spec volvió a `borrador` por el set en tres niveles
  (ADR-005). **No tocar nada de esta lista antes de la re-aprobación.** Después, en este
  orden:
  1. **Tratamientos `AG`**: citar en este ledger URL y fecha de la web de la clínica que
     muestra trasplante capilar DHI y blefaroplastia (CA-1).
  2. **Set** `docs/piloto-artica/prompts-baseline.md`: añadir secciones `AR` (4–5) y `AG`
     (3–4) con su línea de cobertura; `AV01`–`AV15` y `AM` sin cambios; ampliar "Estado
     del set" (congelación de los tres niveles, CA-8) y la entradilla (ya no es solo
     Viveiro/A Mariña/Lugo).
  3. **Dictamen**: pedir a `sdd-metricas` la ampliación (g)–(j) de CA-2 y añadirla a la
     sección del dictamen y a la tabla condición → cambio, con fecha anterior a la pasada 1.
  4. **Protocolo** `protocolo-captura.md`: orden de bloques por app (`AV` primero), una sola
     pasada con los tres niveles, regla de corte entre bloques si se reparte en 2 días,
     tiempo estimado; sigue ≤ 2 páginas (≤ 1100 palabras según su test).
  5. **Plantilla** `plantilla-captura.csv`: solo si la ampliación del dictamen pide una
     columna (p. ej. `nivel`); si el nivel se deriva del prefijo del id, no cambia.
  6. **Procedimiento y herramienta de recuento** (`procedimiento-recuento.md`,
     `tools/count_baseline.py`): sección por nivel; núcleo solo con `AV`; indicadores de
     `AR`/`AG` según el dictamen ampliado.
  7. **Comprobador** `tools/baseline_docs.py` (`parse_prompts_doc`, `coverage`): parsear las
     tres secciones y contar condiciones por nivel.
  8. **Tests** (`tools/tests/`): `test_baseline_prompts.py` (condiciones `AR`/`AG`, ids
     únicos, `AV01`–`AV15` idénticas a la versión del 2026-09-29, sin marcas en `AR`/`AG`);
     `test_baseline_protocol_template.py` (orden y corte de bloques);
     `test_baseline_count.py` (recuento por nivel; el ponderado del núcleo no cambia al
     quitar las filas `AR`/`AG`); `test_baseline_frontier.py` si cambia la frontera.
  9. **Privado** (`$PUSHLLM_PRIVADO/piloto-artica/baseline/`): regenerar
     `captura-p1-prerrellenada.csv` y `captura-p2-prerrellenada.csv` (76 filas con el set
     propuesto, en el orden del protocolo) y `preguntas-en-orden.txt`.
  10. **Este ledger**: actualizar la matriz de CA-1, CA-2, CA-5, CA-7 y CA-8 y las
      "Instrucciones para el humano — pasada 1" (nº de consultas y tiempo: 76 y 95–140 min
      con el set propuesto).
- **F-SPEC-007-7** (→ sdd-arquitecto, SPEC-011 y SPEC-012, borradores): recoger los tres
  niveles de ADR-005: SPEC-012 mide los tres en las pasadas "después", informa `AR`/`AG`
  aparte y deja el Go solo en `AV` (junto con F-SPEC-007-5); SPEC-011 diagnostica fuentes y
  preguntas sin página por nivel, priorizando el núcleo.
  **2026-09-29 (b)**: SPEC-012 recogido (niveles con el probe, CA-3 y CA-7). SPEC-011:
  CA-1 ya toma las fuentes del baseline del probe; **sigue pendiente** el diagnóstico por
  nivel en su revisión completa.
- **F-SPEC-007-8** (→ sdd-implementador, **tras la re-aprobación humana** de la enmienda
  2026-09-29 (b); sdd-arquitecto). La manual pasa a calibración. **No tocar nada de esta
  lista antes de la re-aprobación.** Después, en este orden:
  1. **Dictamen**: pedir a `sdd-metricas` la segunda ampliación (k)–(n) de CA-2 y añadirla
     a "Dictamen sdd-metricas (CA-2)" y a la tabla condición → cambio, con fecha anterior a
     la pasada "antes". Marcar en la tabla qué filas antiguas quedan sin objeto (sobre todo
     b, f, g, j y "b/d en niveles").
  2. **Set** `docs/piloto-artica/prompts-baseline.md`: sin tocar ninguna pregunta. Cambiar
     la entradilla (la manual mide solo `AV` + `AM`; el probe mide `AV`, `AR` y `AG`) y
     "Estado del set" (congelación como tarde al inicio del baseline oficial del probe, o
     fecha fijada por el humano; CA-8).
  3. **Protocolo** `protocolo-captura.md`: 49 consultas (AV en ChatGPT, Gemini y Google;
     AM en ChatGPT y Gemini), orden AV → AM; `pasada` = `antes` / `despues`; quitar bloques
     `AR`/`AG` y "Pasada 2 y siguientes" (sustituir por la calibración "después" de SPEC-012
     con las mismas condiciones); ventana respecto a la ejecución del probe (CA-2 k); tiempo
     60–90 min + 20–25 min; ≤ 2 páginas.
  4. **Plantilla** `plantilla-captura.csv`: sin cambios salvo que el dictamen pida una
     columna (p. ej. la ejecución del probe emparejada).
  5. **Procedimiento** `procedimiento-recuento.md`: una sola pasada (sin unión p1+p2 ni
     estabilidad entre pasadas manuales); §7 de niveles fuera de la manual; sección nueva de
     **comparación app frente a probe** (casilla `AV` × ChatGPT/Gemini, resumen de runs,
     acuerdo y veredicto de CA-2 k–l) reproducible a mano desde el CSV y el `results.csv`;
     AI Overviews según CA-2 (m); el techo ya no se calcula aquí (SPEC-008 CA-10).
  6. **Herramienta** `tools/count_baseline.py`: recuento de una pasada; función de
     comparación con el `results.csv` del probe; render de `calibracion-antes.md`; quitar o
     dejar sin uso `count_level` y la estabilidad p1/p2 para la manual.
  7. **Comprobador** `tools/baseline_docs.py`: la cobertura de CA-1 no cambia; ajustar lo
     que compruebe el protocolo.
  8. **Tests** (`tools/tests/`): `test_baseline_protocol_template.py` (49 consultas, sin
     bloques `AR`/`AG`, valores `antes`/`despues`; retirar `test_protocol_three_levels_block_order`
     o adaptarlo); `test_baseline_count.py` (comparación app/probe con fixture ficticia de
     CSV manual + `results.csv`; veredicto con el umbral del dictamen; AIO aparte; los tests
     de estabilidad p1/p2 y de niveles en la manual se retiran o adaptan);
     `test_baseline_prompts.py` sin cambios salvo la entradilla.
  9. **Privado** (`$PUSHLLM_PRIVADO/piloto-artica/baseline/`): sustituir
     `captura-p1-prerrellenada.csv` y `captura-p2-prerrellenada.csv` por
     `captura-antes-prerrellenada.csv` (49 filas, en el orden del protocolo) y regenerar
     `preguntas-en-orden.txt` (solo `AV` y `AM`).
  10. **Este ledger**: matriz de CA-3, CA-5, CA-6 (n-a: retirado), CA-7 y CA-8; reescribir
      las "Instrucciones para el humano" para la pasada "antes" (incluido el paso de
      congelación y la ejecución del probe emparejada).
  No se toca `probe/` desde aquí: lo del probe va en F-SPEC-008-9.
  **Hecho el 2026-09-29 por sdd-implementador** en la rama `ft/SPEC-007-calibracion`
  (puntos 1–10; `probe/` sin tocar). Punto 9 ampliado a petición del orquestador: también
  `captura-despues-prerrellenada.csv` (49 filas), y los ficheros de 76 filas **renombrados**
  con sufijo `-obsoleto` (no borrados). Ruff F401 corregido en `count_baseline.py` y
  `tests/test_baseline_count.py`.
- **F-SPEC-007-9** (→ sdd-arquitecto / orquestador, SPEC-012): la calibración "después"
  usa la misma ventana de 7 días respecto a una medición "después" del probe (dictamen
  (k.5)) y la lectura de AI Overviews de (m.4) (≥ 5 búsquedas = cambio claro). SPEC-012
  CA-3 debería citarlo; no se ha editado SPEC-012.
- **F-SPEC-007-10** (→ sdd-implementador de SPEC-008, informativo): la comparación usa la
  columna `brands_mentioned` del `results.csv` tal como la escribe el probe y el
  `client_brand` "Clínica Ártica" de `probe/batches/viveiro.json`. Si SPEC-008 cambia ese
  nombre o el formato de la columna, hay que pasar `--client` o ajustar
  `count_baseline.py`.

- **F-SPEC-007-11** (→ sdd-implementador, **tras la re-aprobación humana** de la enmienda
  2026-09-29 (c); sdd-arquitecto). La calibración pasa a ser **por nivel**: 49 consultas =
  15 `AV` × (ChatGPT, Gemini) + 5 `AR` × (ChatGPT, Gemini, Google) + 2 `AM` × (ChatGPT,
  Gemini). **No tocar nada de esta lista antes de la re-aprobación.** Después, en este orden:
  1. **Dictamen**: pedir a `sdd-metricas` la tercera ampliación (o)–(s) de CA-2 y añadirla a
     "Dictamen sdd-metricas (CA-2)" con fecha anterior a la pasada "antes"; filas (o)–(s) en
     la tabla condición → cambio, marcando qué filas de (k)–(n) quedan sin objeto o
     ajustadas (sobre todo k1, l, m y la fila "n (g)–(j)"). No emitirlo el arquitecto ni el
     implementador por su cuenta: es de `sdd-metricas`.
  2. **Set** `prompts-baseline.md`: **ninguna pregunta cambia** (congelado, CA-8). Solo la
     entradilla: la manual calibra `AV` y `AM` en ChatGPT y Gemini y `AR` en ChatGPT, Gemini
     y Google; `AG` solo lo mide el probe. `test_baseline_prompts.py` sigue comprobando `AV`
     y el set congelado sin cambios.
  3. **Protocolo** `protocolo-captura.md`: orden por app y bloque de CA-3 (c) — ChatGPT `AR`
     (5) → `AV` (15) → `AM` (2) (orden decidido en el gate); Gemini igual; Google solo `AR` (5), nunca `AV`/`AM`/`AG`;
     corte entre apps; las dos ventanas (CA-2 o, q) y las dos ejecuciones emparejadas; la
     limitación de ubicación reescrita para `AR` (preguntas formuladas desde Ferrolterra,
     Lugo o Asturias, hechas desde Vilaboa); qué capturar en Google para `AR`; ≤ 2 páginas;
     mismo tiempo estimado.
  4. **Plantilla** `plantilla-captura.csv`: sin cambios salvo que el dictamen pida una
     columna (p. ej. la ejecución del probe emparejada por nivel).
  5. **Procedimiento** `procedimiento-recuento.md`: §2 "lo que ve el paciente" por app **y
     por nivel**; §3 AI Overviews **solo `AR`** según CA-2 (r); §6 dividido en **6-AV** y
     **6-AR**, cada uno con su emparejamiento, casillas, acuerdo y veredicto (CA-2 q y p),
     reproducible a mano; ninguna cifra ni veredicto común; §7 con los dos veredictos y su
     efecto sobre SPEC-009 (frase comercial ↔ `AV`; frase del objetivo ↔ `AR`).
  6. **Herramienta** `tools/count_baseline.py`: recuento y comparación **por nivel**
     (`AV` y `AR` por separado; hoy `_core` filtra solo `AV` y `compare_with_probe` usa las
     constantes de (l) para 15 casillas); constantes de `AR` separadas de las de `AV` según
     CA-2 (p); AI Overviews solo `AR`; un `results.csv` por nivel (p. ej. `--probe-av` y
     `--probe-ar`, porque `AR` sale del directorio del "antes" de (C), SPEC-008 CA-12, si así
     lo fija el dictamen), con su ventana cada uno; `_check` exige el reparto de 49 filas y
     rechaza filas `AV`/`AM`/`AG` de Google y cualquier `AG`; render de
     `calibracion-antes.md` con dos tablas y dos veredictos, sin cifra combinada.
  7. **Prefill** (`baseline_docs.py --prefill`): `captura-antes-prerrellenada.csv` y
     `captura-despues-prerrellenada.csv` con **49 filas en el orden de CA-3 (c)**, y
     `preguntas-en-orden.txt` regenerado (ChatGPT 22, Gemini 22, Google 5) en
     `$PUSHLLM_PRIVADO/piloto-artica/baseline/`. Los de la enmienda (b) se **renombran** con
     sufijo `-obsoleto` (no se borran).
  8. **Tests** (`tools/tests/`): `test_baseline_protocol_template.py` (orden exacto de las 49
     entradas, sin `AV`/`AM` en Google, sin `AG`); `test_baseline_count.py` (fixtures
     ficticias por nivel: comparación `AV` y `AR` separadas, umbrales de CA-2 p/q, ventana por
     nivel, AI Overviews solo `AR`, **ningún número ni veredicto que combine niveles**,
     rechazo de filas Google `AV`); `test_baseline_procedure.py` (secciones 6-AV/6-AR);
     retirar o adaptar los tests de AI Overviews del núcleo (`test_google_*` sobre `AV`).
  9. **Este ledger**: matriz de CA-3, CA-5, CA-7 y CA-10; reescribir "Instrucciones para el
     humano — pasada 'antes'" (reparto nuevo, dos ejecuciones emparejadas y sus carpetas:
     `…\piloto-artica\probe\` para `AV` y la que fije el dictamen para `AR`; fecha límite de
     la ventana).
  No se toca `probe/` desde aquí. Regla ADR-004 §2: ni en el ledger ni en los tests del repo
  aparece ningún dato de visibilidad de Clínica Ártica; solo veredictos.
- **F-SPEC-007-12** (→ sdd-arquitecto, tras fusionar la PR #5): notas sin re-aprobación en
  **SPEC-009** (la frase "ya sois la clínica que la IA recomienda en A Mariña" se apoya en el
  veredicto `AV` de SPEC-007 CA-7 y la del objetivo en el veredicto `AR`; un "no" en un
  nivel revisa solo su frase; un veredicto `AR` débil, "sin discrepancia gruesa", basta
  para contar el objetivo sin garantía, como objetivo y no como dato: decisión del humano
  en el gate del 2026-09-29), **SPEC-012** CA-3 (3) (la calibración "después" es la de
  SPEC-007 CA-3 (c): 49 consultas por nivel; AI Overviews solo en `AR`; dos veredictos en el
  cierre) y **SPEC-011** (ya no hay capturas de AI Overviews del núcleo; sí de `AR`). No se
  editan en esta rama para no chocar con la PR #5, que ya enmienda esas specs.

## Cómo retomar (handoff)
- **2026-09-29 (c) (sdd-arquitecto)**: la spec vuelve a `borrador` por la enmienda (c): la
  calibración se reorienta al Go de ADR-009 (decisión del humano): `AR` en ChatGPT, Gemini y
  Google, `AV` y `AM` solo en ChatGPT y Gemini, 49 consultas; comparación y veredicto por
  nivel. La pasada "antes" no había empezado. **No empezar la pasada** (las instrucciones de
  arriba están obsoletas). Tras la re-aprobación: F-SPEC-007-11. Después de la PR #5:
  F-SPEC-007-12.
- **2026-09-29 (sdd-implementador, calibración)**: F-SPEC-007-8 hecho en
  `ft/SPEC-007-calibracion`. Spec en `en-progreso`: faltan las pasadas humanas. Hecho:
  segunda ampliación del dictamen (k)–(n) con su tabla; set (solo entradilla y congelación),
  protocolo de 49 consultas, procedimiento con la comparación app frente a probe,
  `count_baseline.py` (una pasada + `--probe`), `baseline_docs.py --prefill`, tests (200) y
  ficheros privados de 49 filas. P-5 cerrada sin cambios. Siguiente, en este orden:
  baseline oficial del probe (SPEC-008 CA-7; congela el set, CA-8) → pasada "antes" del
  humano dentro de 7 días → columnas de lectura, `calibracion-antes.md` (CA-7) con
  `count_baseline.py ANTES.csv --probe results.csv`, hoja de hallazgo (CA-10) y foto técnica
  completa (CA-9) → si el veredicto es "no", causa y decisión humana en este ledger antes de
  la propuesta. Después, `en-revision`. Abierta: P-6.
- **2026-09-29 (b) (sdd-arquitecto)**: la spec vuelve a `borrador` por la enmienda "la
  manual pasa a calibración" (decisión del humano; EPIC-002 criterios 1 y 4). Ninguna
  pasada se había hecho. **No empezar la pasada 1** (las instrucciones de arriba están
  obsoletas). Tras la re-aprobación: F-SPEC-007-8. P-5 (Mondoñedo) ya solo afecta al probe
  y debe cerrarse antes de la congelación (CA-8).
- **2026-09-29 (sdd-implementador, tras la re-aprobación)**: F-SPEC-007-6 hecho. Spec en
  `en-progreso`. Set de tres niveles publicado (24 de medición + 2 `AM`), dictamen ampliado
  (g)–(j), protocolo, procedimiento y herramienta por nivel, CSV prerrellenados de 76 filas y
  `preguntas-en-orden.txt` por bloques en privado. Siguiente: pasada 1 del humano. Abiertas:
  P-5 (Mondoñedo) y P-6 (Sarria/A Fonsagrada frente a la lista de ADR-005).
- **2026-09-29 (sdd-arquitecto)**: la spec está en `borrador` por la enmienda de tres
  niveles (ADR-005). La pasada 1 **no** debe empezar hasta la re-aprobación humana y
  F-SPEC-007-6 hecho. Lo de abajo describe el estado previo a la enmienda.
- Hecho (2026-09-29): CA-1, CA-3, CA-4 publicados; dictamen CA-2 en este ledger;
  procedimiento y herramienta de CA-7; foto técnica CA-9 salvo GBP y dominios de la
  pasada 1; CSV prerrellenados y preguntas en orden en privado.
- Falta, en este orden: pasada 1 (humano) → fecha de congelación (CA-8) y hoja de hallazgo
  `hallazgo-reunion.md` (CA-10, agente) + dominios de la pasada 1 y GBP en la foto técnica
  (CA-9) → pasada 2 (humano) → rellenar columnas de lectura y `recuento-antes.md` (CA-7,
  agente) → aviso de CA-8 si el ponderado ≥ 85 % → decisión humana si aplica.
- La spec queda **en-progreso**; pasa a `en-revision` cuando estén las dos pasadas, el
  recuento y la hoja de hallazgo.
