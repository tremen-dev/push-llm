---
id: SPEC-008
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
  - {estado: en-progreso, fecha: 2026-09-29, por: sdd-implementador}
---
# SPEC-008 — Catálogo de Viveiro y A Mariña en el probe

> Cambio acotado en `probe/` (herramienta de medición del Ciclo 0, no producto de `src/`;
> mismo encuadre que SPEC-001 y SPEC-006 respecto a D-4). La implementación y sus tests
> son **offline** y pueden hacerse ya; solo la ejecución real (CA-7) necesita las claves
> de SPEC-002.

> **Enmienda 2026-09-29 (sdd-arquitecto) — tres niveles (ADR-005).** El set de SPEC-007
> pasa a tener núcleo (`AV`), área de influencia (`AR`) y Galicia (`AG`). Cambian CA-1,
> CA-2, CA-3, CA-4, CA-5, las entidades y Fuera de alcance. La spec vuelve a `borrador`
> (estaba `aprobada`, sin empezar) y necesita **nueva aprobación humana**.

## Problema
El piloto necesita medir su set de preguntas con el probe en cuanto haya claves, con
varias ejecuciones por pregunta y de forma repetible cada semana (SPEC-012). Hoy el probe
no puede: `probe_config.json` fija la ubicación del usuario en Vigo, `matching.py` fija
`LOCAL_CITIES = {"Vigo", "Pontevedra"}`, `prompts.csv` no tiene preguntas de Viveiro y
`brands.csv` no tiene ni a Clínica Ártica ni a sus competidores. ADR-003 exige que el lote
de Viveiro vaya **separado** del de Vigo y que el multi-ciudad sea configuración, no
código; además el resultado del lote de Vigo no puede cambiar.

## Usuarios / roles afectados
- Agente (sdd-implementador): cambia configuración, catálogos y el mínimo código de
  `probe/`, con TDD. [Agente]
- Consultadas: `sdd-probe` (dictamen obligatorio: ubicación por proveedor y coste, CA-5);
  `sdd-metricas` (alias de Ártica y de competidores, CA-2, puede reutilizar el dictamen de
  SPEC-007 CA-2).
- Humano: pone las claves y lanza la primera ejecución (CA-7). [Humano]
- sdd-verificador. [Verificador]

## Criterios de aceptación
- **CA-1 (preguntas del piloto en el catálogo) [Agente]**: Dado el set congelado de
  SPEC-007 (preguntas `AV`), cuando se añadan a `probe/prompts.csv`, entonces cada `AVnn`
  tiene el mismo id y el mismo texto literal que en `docs/piloto-artica/prompts-baseline.md`,
  `specialty = aesthetic`, el intent de SPEC-007 y `city = Viveiro` (ubicación del
  paciente; el lugar concreto va en el texto). Las preguntas de marca `AM` **no** entran en
  el probe. Lo mismo vale para las preguntas `AR` y `AG` congeladas (enmienda 2026-09-29):
  mismo id, texto literal, intent y `city = Viveiro`; el nivel se lee en el prefijo del id,
  sin columna nueva en `prompts.csv`. *Evidencia*: comparación automática id+texto entre
  ambos ficheros, para los tres prefijos.
- **CA-2 (marcas del piloto) [Agente; consulta sdd-metricas]**: Dado ADR-004 (el nombre de
  la clínica puede estar en el repo), cuando se actualice `probe/brands.csv`, entonces
  contiene Clínica Ártica (`aesthetic`, `Viveiro`, `independent`) con los alias que fije
  el dictamen de `sdd-metricas` (y ninguno que sea una palabra común suelta sin dictamen),
  y los competidores **verificados**: solo entra una marca si en el ledger consta una
  fuente pública (URL) consultada en fecha que muestra que ofrece medicina estética o
  capilar hoy en la ciudad indicada. Las candidatas no verificadas quedan en el ledger como
  pendientes, no en el CSV. Entran también, con la misma verificación, las competidoras
  que aparezcan en las respuestas `AR` y `AG` de las pasadas manuales (SPEC-007) o que el
  ledger justifique para esos niveles (Ferrolterra, occidente de Asturias y cadenas de
  capilar o blefaroplastia de Galicia), con la ciudad de su sede o sedes. Ningún alias nuevo colisiona con uno existente sin que el
  ledger lo justifique; no se añade ninguna sigla a `exact_aliases` sin citar ADR-002 §6.
  *Evidencia*: tabla marca → fuente → fecha en el ledger; carga de `brands.csv` sin error;
  test de colisiones.
- **CA-3 (lote por configuración) [Agente]**: Dado ADR-003 §3–§4, cuando se lance el probe
  con una configuración de lote de Viveiro (fichero de configuración propio pasado con
  `--config`, o el mecanismo equivalente que el implementador proponga en el ledger),
  entonces: la ubicación del usuario enviada a los proveedores que la aceptan es Viveiro,
  Galicia, ES; el conjunto de ciudades "locales" y el subconjunto de preguntas del lote
  salen de la configuración; solo participan las marcas del lote (ciudades del lote y
  directorios); y la salida por defecto es `$PUSHLLM_PRIVADO/piloto-artica/probe/`.
  *Evidencia*: tests offline que construyen las peticiones de cada proveedor con la
  configuración de Viveiro y comprueban ubicación, preguntas y marcas.
  **Enmienda 2026-09-29**: (i) las marcas del lote se seleccionan por **pertenencia
  declarada al lote** (lista o fichero de marcas del lote en su configuración, u otro
  mecanismo equivalente propuesto en el ledger), no solo por su ciudad, porque habrá marcas
  del piloto con sede en Vigo o Pontevedra (ADR-005 §5); (ii) el `summary.md` del lote
  informa **por nivel** (prefijo `AV`, `AR`, `AG`) por separado y el SoV ponderado del
  núcleo se calcula solo con `AV`; ninguna cifra agrega niveles (ADR-005 §4). *Evidencia
  adicional*: test con un `results.csv` de prueba en el que borrar las filas `AR`/`AG` no
  cambia el ponderado del núcleo; test de que una marca del piloto con ciudad Vigo participa
  en el lote de Viveiro.
- **CA-4 (el lote de Vigo no cambia) [Agente]**: Dado que el veredicto de EPIC-001 no puede
  moverse por este piloto, cuando se lance el probe sin configuración de lote (o con la de
  Vigo), entonces la ubicación sigue siendo Vigo, las ciudades locales Vigo y Pontevedra,
  no se ejecuta ninguna pregunta `AV` y `--analyze` sobre un `results.csv` de prueba del
  lote de Vigo produce un `summary.md` **idéntico** al de antes del cambio (las marcas de
  Viveiro/Lugo no alteran recuentos, líder ni sesgos). Todos los tests previos siguen en
  verde. En particular, las marcas del piloto con ciudad Vigo o Pontevedra (enmienda
  2026-09-29) **no** participan en el lote de Vigo ni cambian su `summary.md`.
  *Evidencia*: test de regresión con fixture que incluye una marca del piloto con ciudad
  Vigo; salida de `python -m pytest probe/tests`.
- **CA-5 (coste y cadencia dentro del presupuesto) [Agente; consulta sdd-probe]**: Dado el
  No-negociable "coste del probe ≤ 20 € por clínica y mes", cuando `sdd-probe` emita su
  dictamen (fecha, fuentes), entonces el ledger recoge: el coste estimado de una ejecución
  del lote (preguntas × runs × proveedores con los precios de `probe_config.json`); una
  cadencia y número de runs para la medición del piloto (SPEC-012) cuyo coste mensual sea
  ≤ 20 €; y si la ubicación Viveiro es aceptada por cada proveedor (Gemini: solo por el
  texto, como hoy). El cálculo usa el set completo congelado (`AV`+`AR`+`AG`, hasta 24
  preguntas con el set propuesto); si no cabe en ≤ 20 €/mes, el dictamen propone una
  cadencia menor para `AR`/`AG` que para `AV`, nunca al revés (enmienda 2026-09-29).
  *Evidencia*: dictamen y cálculo en el ledger.
- **CA-6 (documentación) [Agente]**: Dado D-8, cuando se cierre la spec, entonces
  `probe/README.md` (en inglés) explica cómo lanzar el lote de Viveiro, dónde sale y que el
  lote de Vigo es el defecto. *Evidencia*: sección presente; comando de ejemplo coincide
  con el mecanismo de CA-3.
- **CA-7 (baseline con el probe) [Humano lanza; Agente revisa]**: Dado CA-1 a CA-5 y las
  claves de SPEC-002 CA-1, cuando se ejecute el lote de Viveiro **antes de la primera
  acción del piloto**, entonces existe su `results.csv` y `summary.md` en el espacio
  privado con fecha, y el ledger recoge fecha, número de llamadas, estado y coste. Si las
  claves llegan después de la primera acción, este CA se marca n-a con esa causa y el
  probe solo sirve para tendencia, no para el criterio Go (SPEC-007 CA-2 e). *Evidencia*:
  fechas frente a la primera acción del registro de SPEC-012.
- **CA-8 (nada en bruto en el repo) [Verificador]**: Dado ADR-001, cuando se cierre la spec,
  entonces `git ls-files` no lista salidas del lote y `git status --ignored` no muestra
  `probe/out/` con datos. *Evidencia*: ambas salidas en el ledger.

## Entidades y reglas afectadas
- Dominio: Prompt, Prompt catalogue, Clinic, Provider, Probe / ProbeRun, Mention.
- RN-01, RN-11 (ADR-002), RN-02–RN-04, RN-10.
- D-4, D-5, D-6; No-negociables de coste y de "catálogos y configuración, no código".
- ADR-001, ADR-002, ADR-003, ADR-004, ADR-005 (niveles separados; marcas del piloto fuera
  del lote de Vigo). Depende de SPEC-007 CA-1/CA-8 (set congelado) y,
  solo para CA-7, de SPEC-002 CA-1 (claves).

## Fuera de alcance
- Google AI Overviews y Perplexity en el probe (siguen fuera; AI Overviews se mide a mano).
- Ejecución semanal y su análisis (SPEC-012).
- Cualquier código en `src/`.
- Ubicación del usuario distinta por nivel (Ferrol, Asturias…): todo el lote usa Viveiro,
  como la medición manual usa un único municipio; el lugar va en el texto.
- Añadir al lote de Vigo o a la lista de objetivos de EPIC-001 marcas encontradas por el
  nivel Galicia (ADR-005 §5).

## Notas para el gate humano
- **Competidoras candidatas** (búsqueda pública del 2026-09-28, **no verificadas** salvo
  donde se indica; el implementador las verifica según CA-2):
  - Luxury Clínica Médico Estética — Viveiro (Covas) — luxuryclinica.com; aparece en
    Páxinas Galegas como clínica de medicina estética de Viveiro. *Web propia vista.*
  - Clínica Ribera Polusa Viveiro — incorporó medicina estética en 2024 (aquidiario.com,
    18-06-2024). *Vigencia no verificada.*
  - Clínica Virxe da Mariña — Burela — ficha en Multiestetica con medicina estética.
    *No verificada.*
  - Gaia Pro Aging — Lugo — gaiaproaging.com. *No verificada.*
  - Dorsia Lugo — cadena — dorsia.es/clinicas-dorsia/lugo. *No verificada* (ojo: Dorsia
    también tiene clínica en Vigo; alias compartido, ver CA-4).
  - Clínica Pío Vila — Lugo — clinicapiovila.com. *No verificado que sea medicina
    estética y no solo estética.*
  - Capilar: CapMédica Lugo (capmedica.com/lugo), Avance Capilar (Galicia, ciudad no
    verificada). *No verificadas.*
  - Directorios a valorar: Páxinas Galegas, todoestetica.com, miclinicacapilar.com
    (Multiestetica y Doctoralia ya están).
- **Alias delicados**: "Ártica" es palabra común (adjetivo) y "Luxury" es palabra inglesa
  común; por eso el alias lo fija `sdd-metricas`, no el implementador.
- **Enmienda 2026-09-29 — a mirar**: (1) selección de marcas por pertenencia al lote y no
  por ciudad: es el cambio de diseño que evita que las cadenas de Vigo del nivel Galicia
  ensucien el lote de Vigo. (2) El lote entero sigue con ubicación Viveiro. (3) Competidoras
  de contexto para `AG` (búsqueda del orquestador, 2026-09-29, **no verificadas**): capilar
  — Clínica Novoa, Avance Capilar, Medical Hair, Hospital Capilar, Dr. Torres; párpados —
  cirujanos de A Coruña y Vigo y Dorsia Lugo. Se verifican según CA-2 como las demás.
- **Decisión a mirar**: la verificación de competidores vive en el ledger, no en una
  columna nueva de `brands.csv`, para no cambiar el formato del catálogo.
