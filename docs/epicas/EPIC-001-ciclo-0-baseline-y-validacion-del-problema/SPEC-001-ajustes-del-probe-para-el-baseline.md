---
id: SPEC-001
tipo: spec
epica: EPIC-001
estado: en-revision
aprobada-por: Alberto Fojo
historial:
  - {estado: borrador, fecha: 2026-09-23, por: sdd-arquitecto}
  - {estado: aprobada, fecha: 2026-09-23, por: Alberto Fojo}
  - {estado: en-progreso, fecha: 2026-09-23, por: sdd-implementador}
  - {estado: en-revision, fecha: 2026-09-23, por: sdd-implementador}
---
# SPEC-001 — Ajustes del probe para el baseline

> Trabajo de **agente** (sdd-implementador) sobre `probe/`. `probe/` no está en
> las rutas vigiladas de `.sdd.json`, así que el hook no lo exige: esta spec lo
> gobierna igualmente. No es código de producto (`src/` no se toca; D-4 intacta).
> Todo se verifica **sin API keys ni red**.

## Problema
`probe/run_probe.py` nunca se ha ejecutado y, tal como está, no puede producir
la evidencia que pide EPIC-001:

- **Modelo por defecto contrario a D-5 / RN-10**: `CLAUDE_MODEL` cae por defecto
  en `claude-opus-5` (gama premium), cuando D-5, el README del probe y
  `06-models-costs-and-usage-share.md` §1A–§2 fijan gama media (Sonnet). Los ids
  de OpenAI (`gpt-5`) y Gemini (`gemini-2.5-flash`) no están contrastados con el
  modelo por defecto actual de cada app.
- **Ids de modelo en código**, contra el No-negociable de FOUNDATION ("ids de
  modelo, runs por proveedor y catálogos son configuración, no código").
- **No registra coste**: sin tokens, búsquedas ni modelo efectivo por fila, el
  criterio de éxito 1 ("coste real registrado") no se puede cruzar con nada.
- **No guarda las URLs citadas**: el extracto de SPEC-003 y el Ciclo 1 ("estas son
  las 5 páginas que lee") las necesitan.
- **Los errores cuentan como respuestas sin clínica**: una llamada fallida
  (`[error] …`) entra en el denominador de cobertura y sesga la hipótesis a favor
  de "menos de la mitad nombra una clínica".
- **No calcula lo que la hipótesis pregunta**: `summary.md` da cobertura por
  proveedor, pero ni el agregado ponderado (RN-03/RN-04) ni la frecuencia de la
  clínica líder por especialidad (fertilidad/oftalmología).
- **Todo se calcula en caliente**: si se amplía `brands.csv` tras revisar
  respuestas, hay que volver a pagar 396 llamadas para recontar.
- **No es reanudable**: un corte a mitad de las 396 llamadas obliga a repetir
  todo, contra el No-negociable "llamadas idempotentes y seguras ante reintentos".
- **Matching con sesgos conocidos**: por RN-01 los alias de < 4 caracteres se
  descartan (`IVI`, `MIA`), así que una respuesta que solo diga "IVI" no cuenta;
  y alias compartidos entre especialidades (`Villoria`, `Povisa`, `Vitaldent`)
  cuentan una misma mención para varias marcas.
- El README solo documenta `export` (bash); el humano trabaja en Windows.

## Usuarios / roles afectados
- Humano (fundador): ejecutará el probe en SPEC-002.
- sdd-implementador: implementa. sdd-verificador: verifica con tests offline.
- Autoridades de dominio consultadas: `sdd-probe` (modelos, parámetros de llamada,
  precios), `sdd-metricas` (definiciones de cobertura, ponderación, líder).

## Criterios de aceptación
- **CA-1 (dictamen de modelos)**: Dado que D-5 exige el modelo por defecto de cada
  app de consumo, cuando se fijen los ids por defecto de Claude, OpenAI y Gemini y
  los parámetros de llamada (versión de la herramienta de búsqueda web, ubicación,
  `effort` u equivalentes), entonces consta en el ledger un dictamen de `sdd-probe`
  con fecha, id por proveedor y fuente citada, y los valores configurados coinciden
  literalmente con el dictamen. *Evidencia*: dictamen en el ledger + test que lee la
  configuración y compara con los ids del dictamen.
- **CA-2 (configuración, no código)**: Dado el No-negociable de FOUNDATION, cuando se
  lea `run_probe.py`, entonces no contiene ids de modelo ni precios literales: salen
  de un fichero de configuración versionado en `probe/` (ids, runs por proveedor,
  precio por M tokens de entrada/salida y por búsqueda, con fecha y fuente), y las
  variables de entorno `CLAUDE_MODEL`/`OPENAI_MODEL`/`GEMINI_MODEL` siguen
  sobrescribiéndolos. *Evidencia*: test que cambia la configuración y comprueba el
  modelo usado; test de precedencia de la variable de entorno; `grep` sin ids en el `.py`.
- **CA-3 (metadatos por fila)**: Dado un proveedor simulado, cuando el probe escriba
  una fila, entonces la fila incluye, además de las columnas actuales: marca de
  tiempo UTC, id de modelo efectivo (el devuelto por la API si lo expone, si no el
  configurado), tokens de entrada, tokens de salida, nº de búsquedas web (vacío si
  la API no lo expone), coste estimado en € según la configuración de CA-2,
  `status` ∈ {ok, error, refusal, empty} y `cited_urls` (lista separada por `;`,
  vacía si el proveedor no las devuelve). *Evidencia*: tests con los tres
  proveedores simulados, uno por `status`.
- **CA-4 (errores fuera del denominador)**: Dado un `results.csv` con filas en
  `status` ≠ ok, cuando se calculen coberturas, entonces esas filas no cuentan en
  numerador ni denominador y el resumen muestra su número por proveedor y
  especialidad. *Evidencia*: test con fixture de cifras conocidas.
- **CA-5 (análisis offline)**: Dado un `results.csv` existente y el `brands.csv`
  actual, cuando se ejecute el modo de análisis, entonces recalcula menciones desde
  el texto guardado **sin llamar a ningún proveedor** y produce, por especialidad ×
  proveedor: respuestas válidas, respuestas que nombran ≥ 1 clínica local (marca no
  directorio con ciudad Vigo o Pontevedra), su porcentaje, y el agregado ponderado por
  RN-03/RN-04 normalizado a los proveedores sondeados; y por especialidad: la marca
  de esa especialidad con mayor frecuencia de aparición y su % de respuestas, y el
  reparto de menciones de directorios. *Evidencia*: test con fixture y cifras
  esperadas calculadas a mano; test en el que los adaptadores de proveedor lanzan
  excepción si se invocan.
- **CA-6 (definiciones validadas)**: Dado que CA-5 operacionaliza la hipótesis de
  `03-local-market-vigo-pontevedra.md` §2, cuando se cierren las definiciones
  ("clínica local", tratamiento de alias < 4 caracteres, alias compartidos entre
  especialidades, deduplicación por respuesta, ponderación), entonces consta en el
  ledger un dictamen de `sdd-metricas` y el código lo sigue. Mínimo exigido con
  independencia del dictamen: una misma respuesta cuenta como mucho una vez por
  marca, y la marca líder de una especialidad solo se elige entre marcas de esa
  especialidad. *Evidencia*: dictamen en ledger + tests de casos límite
  ("IVI Vigo", "Villoria" en respuesta de estética y de oftalmología, marca repetida
  dos veces en una respuesta).
- **CA-7 (reanudable)**: Dado un fichero de resultados con parte de las llamadas
  hechas, cuando se relance con la opción de reanudar, entonces solo se llaman las
  combinaciones (prompt, proveedor, run) que no tienen fila `status=ok`, y las filas
  previas se conservan intactas. *Evidencia*: test con proveedor simulado que cuenta
  llamadas.
- **CA-8 (salida fuera del repo)**: Dado ADR-001, cuando se ejecute el probe o el
  análisis, entonces el directorio de salida es configurable (opción de línea de
  comandos o `PUSHLLM_PRIVADO`), el valor por defecto dentro del repo está en
  `.gitignore`, y ninguna ruta de salida queda versionada. *Evidencia*: test de la
  opción; `git check-ignore` sobre el directorio por defecto.
- **CA-9 (humo y dependencias)**: Dado un entorno limpio, cuando se sigan las
  instrucciones del README, entonces existe un `requirements.txt` con versiones
  fijadas de los SDK, un comando de humo documentado (4 prompts — `D01,E01,F01,O01` —
  × 1 run × 3 proveedores = 12 llamadas), el comando completo (44 × 3 × 3 = 396), el
  modo de análisis, la reanudación, y cómo poner las claves en **PowerShell** y en
  bash sin escribirlas en ficheros del repo. *Evidencia*: revisión del README contra
  esta lista; `pip install -r` en un venv limpio sin errores.
- **CA-10 (tests offline)**: Dado un checkout sin claves ni red, cuando se ejecute
  `python -m pytest probe/tests`, entonces todos los tests pasan. *Evidencia*: salida
  del comando en el ledger.

## Entidades y reglas afectadas
- Dominio (`docs/fundacion/dominio.md`): Probe / ProbeRun, Provider, Mention, Source,
  Usage share / weight, Prompt catalogue.
- RN-01 (matching), RN-03 y RN-04 (ponderación), RN-06 (position, lo consume
  SPEC-003), RN-10 (modelo por defecto con búsqueda y ubicación).
- D-5, D-6 (FOUNDATION); No-negociables de configuración e idempotencia.
- ADR-001 (frontera de datos).

## Fuera de alcance
- Adaptadores de Google AI Overviews y Perplexity (fuera de EPIC-001).
- Mover el probe a `src/` o convertirlo en producto (Ciclo 3).
- Ampliar o reescribir `prompts.csv`. Ampliar `brands.csv` es de SPEC-002 (CA-6 de
  aquella), no de esta.
- Ejecutar el probe contra APIs reales (SPEC-002).
- Clasificar fuentes por tipo (directory, clinic_site…): solo se guardan las URLs.

## Notas para el gate humano
- **Contradicción detectada**: el default `claude-opus-5` de `run_probe.py` viola D-5
  y contradice el README del propio probe ("defaults to mid-tier"). Esta spec lo
  corrige; no hace falta ADR porque aplica una decisión locked, no la cambia.
- **Sesgo de medición a mirar con lupa (CA-6)**: por RN-01 "IVI" solo no cuenta. Si
  los asistentes escriben "IVI" a secas, fertilidad saldría con menos menciones de la
  real. La salida puede ser un alias más largo, o una excepción a RN-01, que sería
  cambio de regla (lo decide `sdd-metricas` y, si toca RN-01, el humano).
- La lista `brands.csv` solo tiene 43 clínicas: una respuesta que nombra una clínica
  local no listada cuenta como "sin clínica", sesgando la hipótesis de dental/estética
  hacia el "sí". SPEC-002 CA-6 lo mitiga con una revisión manual y el recálculo
  offline de CA-5.
- Dependencias: ninguna. Bloquea a SPEC-002 y SPEC-003.
- Todo lo de esta spec lo produce un agente; el humano solo aprueba.
