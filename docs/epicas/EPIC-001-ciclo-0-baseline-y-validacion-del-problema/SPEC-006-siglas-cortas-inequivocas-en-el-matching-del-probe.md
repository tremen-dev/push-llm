---
id: SPEC-006
tipo: spec
epica: EPIC-001
estado: en-revision
aprobada-por: Alberto Fojo
historial:
  - {estado: borrador, fecha: 2026-09-24, por: sdd-arquitecto}
  - {estado: aprobada, fecha: 2026-09-23, por: Alberto Fojo}
  - {estado: en-progreso, fecha: 2026-09-23, por: sdd-implementador}
  - {estado: en-revision, fecha: 2026-09-23, por: sdd-implementador}
---
# SPEC-006 — Siglas cortas inequívocas en el matching del probe

> Trabajo de **agente** (sdd-implementador) sobre `probe/`, con TDD y verificable **sin API
> keys ni red**, igual que SPEC-001. Se separa de SPEC-002 porque SPEC-002 es sobre todo
> ejecución humana y análisis; así el cambio de código tiene su propio ciclo de
> implementación y verificación y puede hacerse mientras el humano prepara claves y espacio
> privado. Precede a la ejecución completa de SPEC-002 (CA-3).

## Problema
RN-01 no cuenta alias de < 4 caracteres, así que "IVI" solo no cuenta para IVI Vigo y
fertilidad sale sesgada a la baja (F-SPEC-001-4). El humano decidió el 2026-09-24 hacer una
excepción; su forma operativa es ADR-002 / RN-11. Esta spec la implementa en
`probe/matching.py` y el catálogo `probe/brands.csv`.

## Usuarios / roles afectados
- sdd-implementador: cambia `matching.py`, `brands.csv`, `analysis.py` (resumen), tests y README.
- sdd-verificador: comprueba sin claves ni red.
- Consumidores: SPEC-002 (baseline y veredicto), SPEC-003 (extractos).

## Criterios de aceptación
- **CA-0 (dictamen previo)**: Dado ADR-002 en borrador, cuando se vaya a implementar, entonces
  consta en el ledger de esta spec un dictamen fechado de `sdd-metricas` sobre ADR-002 (reglas
  1–5) con veredicto correcto/incorrecto/dudoso, y ADR-002 está `aprobada`. *Evidencia*:
  sección de dictamen en el ledger + frontmatter de ADR-002.
- **CA-1 (catálogo)**: Dado `probe/brands.csv`, cuando se cargue con `matching.load_brands()`,
  entonces existe la columna `exact_aliases`; la única marca con valor es `IVI Vigo` con
  `IVI`; `IVI` ya no figura en su columna `aliases` (`IVIRMA` se mantiene); `Clínica MIA`
  conserva `MIA` en `aliases` (sin contar, ADR-002 §5). *Test*: carga del CSV real y
  comparación del mapa marca → siglas con `{"IVI Vigo": ["IVI"]}`.
- **CA-2 (validación al cargar)**: Dado un CSV temporal, cuando una entrada de
  `exact_aliases` no sea de 2–3 caracteres solo mayúsculas A–Z/dígitos (p. ej. `Ivi`, `IVIR`,
  `I`), o repita una sigla o alias (normalizado) de otra marca, entonces `load_brands` lanza
  `ValueError` cuyo mensaje contiene la marca y la sigla. Un CSV sin la columna
  `exact_aliases` sigue cargando (compatibilidad). *Test*: un caso por cada condición.
- **CA-3 (coincidencia sensible a mayúsculas y por palabra completa)**: Dado el catálogo real,
  cuando `find_mentions` reciba, con especialidad `fertility` y ciudad `Vigo`, los textos
  "Te recomiendo IVI, es la mejor.", "Opciones: (IVI) y NIDA", "IVI-RMA en Vigo" o
  "Mira IVI." entonces IVI Vigo figura entre las marcas; y con "te recomiendo ivi",
  "Ivi es buena", "IVIS", "XIVI" o "IVI2" entonces IVI Vigo **no** figura. *Test*:
  parametrizado con esos textos.
- **CA-4 (resto de RN-01 intacto)**: Dado el cambio, cuando se ejecute la suite, entonces
  "Te recomiendo MIA" no produce ninguna marca; "IVI Vigo, también conocida como IVI" cuenta
  IVI Vigo una sola vez; y el resto de casos de `test_matching.py` de SPEC-001 (Villoria,
  solapes, repetición, acentos, `is_local_clinic`) pasan sin cambios. Los tests de SPEC-001
  que afirmaban "IVI solo no cuenta" se sustituyen por los de CA-3 y este CA, dejando
  comentario con la referencia a ADR-002. *Test*: `test_matching.py`.
- **CA-5 (análisis y resumen)**: Dado un fixture con una respuesta `ok` de fertilidad que solo
  dice "IVI es la mejor opción." y una de estética que solo dice "Te recomiendo MIA.", cuando se ejecute
  `analysis.analyze`, entonces la primera cuenta como "con clínica local" y suma a IVI Vigo en
  el líder de fertilidad, y `short_alias_hits` no la reporta; la segunda
  sigue sin contar y sí se reporta como sesgo. `render_summary` incluye una línea que enumera
  las siglas activas de `exact_aliases` (`IVI → IVI Vigo`, citando RN-11/ADR-002) junto a la
  sección de sesgo de alias cortos. *Test*: `test_analysis.py` (actualizar la cifra de
  fertilidad del fixture de SPEC-001 que dependía de "IVI" sin contar, recalculada a mano en
  el ledger).
- **CA-6 (columna en ejecución)**: Dado `run_probe.main` con un `ask` falso que responde
  "IVI es la referencia" a un prompt de fertilidad, cuando se escriba la fila, entonces
  `brands_mentioned` contiene `IVI Vigo`. *Test*: `test_run_probe.py`.
- **CA-7 (documentación y suite)**: Dado el cambio, cuando se cierre la spec, entonces
  `probe/README.md` describe la columna `exact_aliases` y la regla (con referencia a
  RN-11/ADR-002), el docstring de `matching.py` la menciona, y `python -m pytest probe/tests`
  pasa entero sin claves ni red. *Evidencia*: salida de pytest en el ledger.

## Entidades y reglas afectadas
- Dominio: Mention, Probe.
- RN-01, RN-11 (nueva), ADR-002. Dictamen sdd-metricas de SPEC-001 (puntos 3–5).
- Depende de: SPEC-001 (hecho), aprobación de ADR-002.

## Fuera de alcance
- Añadir siglas distintas de `IVI` (una nueva exige ADR-002 §6).
- Orden exacto de aparición de una sigla respecto a los demás nombres (Position, RN-06, no se
  calcula en Ciclo 0): basta con que la marca figure y cuente una vez.
- Cambios de `prompts.csv` o de otras marcas de `brands.csv` (SPEC-002 CA-6 amplía el catálogo).

## Notas para el gate humano
- Mirad con lupa ADR-002 §1 y §5: el criterio "no es palabra común" deja fuera `MIA`. Si
  queréis contarla también, hay que decirlo ahora (ADR-002 cambiaría antes de aprobarse).
- IVI solo se atribuye a IVI Vigo aunque la respuesta hable de la cadena (misma lógica que
  `Vitaldent`); queda como limitación en el veredicto de SPEC-002.
- Bloquea: SPEC-002 CA-3 (ejecución completa). El humo de SPEC-002 puede lanzarse antes.
