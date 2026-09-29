---
id: SPEC-008
tipo: spec
epica: EPIC-002
estado: borrador
aprobada-por: Alberto Fojo
historial:
  - {estado: borrador, fecha: 2026-09-28, por: sdd-arquitecto}
  - {estado: aprobada, fecha: 2026-09-28, por: Alberto Fojo}
  - {estado: bloqueada, fecha: 2026-09-29, por: sdd-arquitecto}
  - {estado: borrador, fecha: 2026-09-29, por: sdd-arquitecto}
  - {estado: aprobada, fecha: 2026-09-29, por: Alberto Fojo}
  - {estado: en-progreso, fecha: 2026-09-29, por: sdd-implementador}
  - {estado: bloqueada, fecha: 2026-09-29, por: sdd-arquitecto}
  - {estado: borrador, fecha: 2026-09-29, por: sdd-arquitecto}
---
# SPEC-008 — Catálogo de Viveiro y A Mariña en el probe

> **Enmienda 2026-09-29 (b) (sdd-arquitecto) — el probe es el instrumento del criterio Go.**
> Decisión del humano (Alberto Fojo, 2026-09-29), recogida por sdd-producto en EPIC-002,
> criterios 1 y 4: el probe mide los tres niveles y su baseline (CA-7) pasa a ser **el
> baseline oficial del criterio Go**; la medición manual de SPEC-007 queda como calibración.
> Cambian: CA-5 (coste del mes de cierre), **CA-7** (baseline oficial: ya no espera a la
> pasada 1 manual, sino a SPEC-013 y a la congelación del set; sin baseline del probe no hay
> primera acción), **CA-9 nuevo** (dictamen de `sdd-metricas` sobre el Go con el probe:
> forma del baseline, dos mediciones "después" en semanas distintas, estabilidad, ruido e
> indicadores `AR`/`AG`), **CA-10 nuevo** (aviso de techo, que sale de SPEC-007 CA-8),
> dependencias, Fuera de alcance y notas. CA-1 a CA-4, CA-6 y CA-8 no cambian; lo ya
> implementado y verificado sigue valiendo. La spec vuelve a `borrador` (estaba
> `en-progreso`, con CA-7 sin ejecutar) y necesita **nueva aprobación humana**. Lo que el
> implementador debe rehacer está en el ledger (F-SPEC-008-9).

> **Nota 2026-09-29 (sdd-arquitecto) — cambio de nicho (ADR-008). No cambia ningún CA ni
> requiere re-aprobación.** Las citas a ADR-003 y ADR-005 de esta spec siguen valiendo en lo
> que usa (lote aparte, niveles `AV`/`AR`/`AG` sin mezclar, Go solo con `AV`, nivel Galicia
> sin prometer, marcas del piloto fuera del lote de Vigo). Lo que ADR-008 deroga es el
> encuadre como "excepción a D-2" y sus prohibiciones de prospección y de "Asturias no es
> mercado"; el lote de Vigo queda aparcado, intacto, como configuración por defecto.

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
  **Enmienda 2026-09-29 (b)**: el cálculo incluye también el **mes del cierre**, con las dos
  mediciones "después" que fije CA-9 (cada una sustituye a la ejecución `AV` semanal de su
  semana) y la ejecución `AR`/`AG` que le toque, recalculado con el coste medido en el humo
  (`c`); si no cabe en ≤ 20 €, el dictamen propone cómo, sin bajar los runs de las
  mediciones del Go por debajo de los del baseline.
  *Evidencia*: dictamen y cálculo en el ledger.
- **CA-6 (documentación) [Agente]**: Dado D-8, cuando se cierre la spec, entonces
  `probe/README.md` (en inglés) explica cómo lanzar el lote de Viveiro, dónde sale y que el
  lote de Vigo es el defecto. *Evidencia*: sección presente; comando de ejemplo coincide
  con el mecanismo de CA-3.
- **CA-7 (baseline oficial del criterio Go) [Humano lanza; Agente revisa]**: Dado CA-1 a
  CA-5, el dictamen de CA-9, SPEC-013 en estado `hecho` (citas de Claude y respuesta cruda
  del proveedor), el set congelado (SPEC-007 CA-8: si no hay fecha anterior, esta ejecución
  lo congela) y las claves de SPEC-002 CA-1, cuando se ejecute el lote de Viveiro con la
  forma que fije CA-9 (propuesta: `AV` con 3 runs si el humo da `c ≤ 0,19 €` y 2 si no;
  `AR` y `AG` con 1 run) **antes de la primera acción del piloto**, entonces existen su
  `results.csv` y `summary.md` en el espacio privado con fecha, y el ledger recoge fecha,
  runs por nivel, número de llamadas por estado, coste, modelos por proveedor y la fecha de
  congelación del set. Esta ejecución es el **baseline oficial del criterio Go** (EPIC-002,
  criterio 4): el Go se calcula probe contra probe (SPEC-007 CA-2 e) y solo con `AV`
  (ADR-005 §4). **No depende** de ninguna pasada manual. Si no puede lanzarse antes de la
  primera acción, la primera acción espera: sin baseline del probe no hay criterio Go (ya
  no hay alternativa manual). *Evidencia*: fechas del baseline frente a la del `hecho` de
  SPEC-013, la de congelación y la de la primera acción del registro de SPEC-012; runs por
  nivel iguales a los de CA-9.
- **CA-8 (nada en bruto en el repo) [Verificador]**: Dado ADR-001, cuando se cierre la spec,
  entonces `git ls-files` no lista salidas del lote y `git status --ignored` no muestra
  `probe/out/` con datos. *Evidencia*: ambas salidas en el ledger.
- **CA-9 (dictamen del criterio Go con el probe) [Agente; consulta sdd-metricas]**: Dado que
  el probe pasa a ser el instrumento del Go (EPIC-002, criterio 4) y que el humano exige
  estabilidad (ledger de SPEC-007, P-3: la subida debe verse en las dos mediciones
  "después"), cuando se prepare el baseline y **antes de lanzarlo** (CA-7), entonces consta
  en el ledger un dictamen fechado de `sdd-metricas` (conclusión por punto, condiciones)
  que fija al menos:
  (a) **forma del baseline**: runs por nivel y si basta una ejecución o hacen falta dos en
  semanas distintas antes de la primera acción;
  (b) **cómo se agregan los runs**: SoV bruto por proveedor sobre todas las respuestas
  válidas de los runs (como `probe/analysis.py`) u otra regla, y SoV ponderado del núcleo
  con ChatGPT, Gemini y Claude normalizado a lo sondeado (RN-03/RN-04);
  (c) **forma de las dos mediciones "después"**: mismo número de runs que el baseline, en
  **semanas distintas** (separación mínima en días) y en qué semanas desde la primera
  acción (propuesta: semanas 11 y 12, ± 1, con al menos 7 días entre ellas); cada una
  sustituye a la ejecución `AV` semanal de su semana;
  (d) **regla de estabilidad del Go**: propuesta: Δ SoV ponderado del núcleo ≥ +15 pts
  frente al baseline **en cada una** de las dos mediciones "después" (no en su media), o la
  que el dictamen justifique, siempre decidible con sí/no desde los `results.csv`;
  (e) **ruido esperable** con 15 preguntas × runs × 3 proveedores frente a +15 pts, y si
  las ejecuciones `AV` semanales de 1 run sirven como medida del ruido;
  (f) **mismo instrumento**: qué debe ser idéntico entre baseline y "después" (set, runs,
  ubicación, prompts de sistema, configuración de búsqueda) y qué se hace si un proveedor
  cambia de modelo por defecto entre medias (D-5/RN-10: el probe debe usar el modelo por
  defecto; el cambio se anota y el dictamen dice si la comparación sigue valiendo);
  (g) **indicadores `AR` y `AG` con el probe**: traslada al probe las definiciones de
  SPEC-007 CA-2 (g)–(j) ("aparecer con cierta regularidad", "aparecer alguna vez", solo
  recuentos, posición en lista, cadenas como una marca) con la cadencia de CA-5 (cada 4
  semanas, 1 run) y define su periodo "antes" y "después";
  (h) el tratamiento en el probe de "Ártica" como adjetivo (F-SPEC-008-3).
  Cada condición se mapea a un cambio en `batches/viveiro.json`, `analysis.py`, el README o
  las instrucciones del ledger. El dictamen lo emite `sdd-metricas`; este CA no lo
  prejuzga. *Evidencia*: dictamen con fecha anterior al baseline y tabla condición →
  cambio en el ledger.
- **CA-10 (margen para el criterio Go) [Agente avisa; Humano decide]**: Dado que la clínica
  podría ya aparecer mucho en las preguntas de Viveiro, cuando el baseline oficial (CA-7)
  deje el SoV ponderado del núcleo `AV` a menos de 15 pts de su techo (≥ 85 %), entonces,
  antes de la primera acción, el humano decide y deja registrado en el ledger si se
  mantiene el criterio, se mide sobre un subconjunto de `AV` (p. ej. preguntas de Lugo o
  capilar) o se cambia el umbral; nunca después de ver el efecto. El aviso se calcula solo
  con `AV` y solo con el probe (sale de SPEC-007 CA-8, enmienda 2026-09-29 (b)).
  *Evidencia*: cifra del ponderado del núcleo en el `summary.md` privado; si aplica,
  decisión fechada en el ledger anterior a la primera acción.

## Entidades y reglas afectadas
- Dominio: Prompt, Prompt catalogue, Clinic, Provider, Probe / ProbeRun, Mention.
- RN-01, RN-11 (ADR-002), RN-02–RN-04, RN-10.
- D-4, D-5, D-6; No-negociables de coste y de "catálogos y configuración, no código".
- ADR-001, ADR-002, ADR-003, ADR-004, ADR-005 (niveles separados; marcas del piloto fuera
  del lote de Vigo). Depende de SPEC-007 CA-1/CA-8 (set congelado; la congelación la
  hace, como tarde, el propio baseline de CA-7) y, solo para CA-7: de SPEC-002 CA-1
  (claves), de **SPEC-013 en `hecho`** (EPIC-FIX: `cited_urls` de Claude y respuesta cruda
  del proveedor; sin ello el baseline oficial no tiene fuentes de Claude para SPEC-011 ni
  cumple el No-negociable de guardar la respuesta en bruto) y del dictamen de CA-9. Ya
  **no** depende de ninguna pasada manual de SPEC-007.

## Fuera de alcance
- Google AI Overviews y Perplexity en el probe (siguen fuera; AI Overviews se mide a mano
  en la calibración de SPEC-007, solo en `AV`).
- La comparación app frente a probe (SPEC-007 CA-7) y el veredicto del Go (SPEC-012 CA-7):
  aquí solo el baseline, el dictamen que fija cómo se mide y el aviso de techo.
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
- **Enmienda 2026-09-29 (b) — a mirar con lupa**: (1) **sin baseline del probe no hay
  primera acción**: antes, si las claves llegaban tarde, el Go se medía a mano; ahora no hay
  plan B, y el baseline espera a SPEC-013 (`hecho`). Si SPEC-013 se alarga, retrasa el
  arranque del piloto. (2) La propuesta de estabilidad (dos mediciones "después" en semanas
  distintas, cada una ≥ +15 pts) la confirma o cambia `sdd-metricas` en CA-9 **antes** del
  baseline, no después de ver datos. (3) La regla de runs (`AV` 3 runs si `c ≤ 0,19 €`) se
  mantiene; con el humo medido (`c` = 0,1142 €) salen 3 runs, y las dos mediciones
  "después" usan los mismos 3 runs. (4) El cierre concentra coste: dos ejecuciones `AV` de
  3 runs en el mismo mes; con el `c` medido, el mes de cierre se estima en ≈ 15 € (unas 129
  preguntas × ejecución), dentro de los 20 €; CA-5 lo recalcula. (5) Claude sí entra en el
  ponderado del Go con el probe (RN-04 normalizado), aunque la calibración manual solo
  contraste ChatGPT y Gemini.
