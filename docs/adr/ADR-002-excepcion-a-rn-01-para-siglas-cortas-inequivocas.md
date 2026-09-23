---
id: ADR-002
tipo: adr
estado: aprobada
historial:
  - {estado: borrador, fecha: 2026-09-24, por: sdd-arquitecto}
  - {estado: aprobada, fecha: 2026-09-23, por: Alberto Fojo}
aprobada-por: Alberto Fojo
---
# ADR-002: Excepción a RN-01 para siglas cortas inequívocas

- Deciders: el humano (Alberto Fojo) decidió el 2026-09-24 que haya una excepción a RN-01 para
  alias cortos inequívocos (respuesta a F-SPEC-001-4). sdd-arquitecto propone la redacción
  operativa de este ADR (2026-09-24). Aprueba: humano (pendiente de revisar esta redacción).
  Antes de aprobar se pide dictamen de `sdd-metricas` (SPEC-006 CA-0).
- Specs relacionadas: SPEC-001 (origen: dictamen sdd-metricas punto 3 y F-SPEC-001-4),
  SPEC-006 (implementación), SPEC-002 (consume el matching en el baseline).

## Contexto
RN-01 cuenta una mención solo si aparece el nombre de la clínica o un alias de ≥ 4
caracteres, comparando texto normalizado sin acentos ni mayúsculas. El umbral evita falsos
positivos con palabras comunes, pero deja fuera siglas con las que una marca se conoce de
verdad. El caso motivador es **IVI** (IVI Vigo, fertilidad): una respuesta que dice "te
recomiendo IVI" no cuenta, y eso infravalora a la clínica líder previsible de fertilidad,
justo una de las dos patas de la hipótesis del probe (SPEC-002 CA-7). SPEC-001 ya mide ese
sesgo aparte (`short_alias_hits` en `summary.md`), pero no lo corrige.

En `probe/brands.csv` hoy hay exactamente dos alias de < 4 caracteres normalizados:
`IVI` (IVI Vigo) y `MIA` (Clínica MIA, estética).

## Decisión
Se añade una excepción a RN-01, registrada como **RN-11** en `docs/fundacion/reglas.md`:

1. **Qué es una sigla corta inequívoca.** Un alias de 2 o 3 caracteres que cumple todo esto:
   - (a) *forma*: escrito solo con mayúsculas A–Z y dígitos (p. ej. `IVI`);
   - (b) *uso real*: es la forma con la que la marca se nombra públicamente (su web o rótulo);
   - (c) *no es palabra*: en minúsculas y sin acentos no es una palabra de uso común en
     castellano ni en gallego, ni una sigla de uso general en el contexto sanitario;
   - (d) *exclusiva*: no es alias ni sigla de ninguna otra marca de `brands.csv`.
   (a) y (d) se comprueban automáticamente al cargar el catálogo; (b) y (c) son juicio y se
   deciden por marca en este ADR o en uno que lo supersede.
2. **Cómo se marca.** En `probe/brands.csv`, columna nueva `exact_aliases` (separada por `;`).
   Una sigla en `exact_aliases` no figura también en `aliases`. Si una entrada de
   `exact_aliases` incumple (a) o (d), la carga del catálogo falla con un error que nombra la
   marca y el alias (no se ignora en silencio).
3. **Cómo se compara (anti-falso-positivo).** Sobre el **texto original** de la respuesta, sin
   normalizar: coincidencia **sensible a mayúsculas** y **por palabra completa**, es decir, la
   sigla no puede ir pegada a una letra (acentuada o no) ni a un dígito. `IVI`, `(IVI)`,
   `IVI.` o `IVI-RMA` cuentan; `ivi`, `Ivi`, `IVIS`, `XIVI` o `IVI2` no.
4. **Qué cuenta.** Una coincidencia de sigla equivale a una mención de su marca a todos los
   efectos de RN-01 (cobertura, SoV, líder). Siguen aplicando la deduplicación (una marca
   cuenta como mucho una vez por respuesta) y el resto de reglas del dictamen de sdd-metricas
   de SPEC-001.
5. **A qué siglas aplica hoy.** Solo a **`IVI` → IVI Vigo**.
   **`MIA` (Clínica MIA) queda fuera**: incumple (c), "mía" es una palabra común en castellano
   y gallego, y una respuesta en mayúsculas (títulos, énfasis) la convertiría en falso
   positivo. Sigue sin contar y se sigue informando como sesgo en `summary.md`.
6. Añadir una sigla nueva a `exact_aliases` exige citar este ADR y dejar constancia de (b) y
   (c) en el ledger de la spec que la añade; si alguna es dudosa, se consulta a `sdd-metricas`.

RN-01 no se deroga: sigue siendo la regla general para todo lo demás.

## Consecuencias
### Positivas
- IVI Vigo deja de estar infravalorada en fertilidad; la pata fertilidad/oftalmología de la
  hipótesis (SPEC-002 CA-7) se mide con menos sesgo.
- La excepción es explícita, por marca y auditable en el catálogo público; los casos dudosos
  (MIA) siguen midiéndose como sesgo en vez de contarse a ciegas.

### Negativas / follow-ups
- IVI es una cadena con clínicas en muchas ciudades: "IVI" solo, en una respuesta a una
  pregunta sobre Vigo, se atribuye a IVI Vigo aunque la respuesta hable de la cadena en
  general. Es el mismo criterio que ya se aplica a `Vitaldent`; se acepta y se anota como
  limitación en el documento de veredicto (SPEC-002 CA-5).
- Una sigla en minúsculas o capitalizada ("Ivi") no cuenta: se pierde algún acierto real a
  cambio de no contar palabras. El recuento de sesgo de `summary.md` sigue cubriéndolo.
- El producto (Ciclo 3) hereda la regla: cuando exista, el alta de alias de clínica debe
  distinguir alias normales de siglas.

## Alternativas consideradas
- **Mantener RN-01 sin excepción y solo informar del sesgo** (lo hecho en SPEC-001):
  rechazada por el humano el 2026-09-24; deja sesgada la especialidad de fertilidad.
- **Bajar el umbral de RN-01 a 3 caracteres para todos los alias**: rechazada; contaría
  `MIA` ("mía") y cualquier alias corto futuro sin juicio previo.
- **Lista de siglas en `probe_config.json`**: rechazada; la sigla es un dato de la marca,
  como sus alias, y debe vivir junto a ella en el catálogo.
- **Coincidencia insensible a mayúsculas pero por palabra completa**: rechazada; "ivi" y
  "mia" en minúsculas son justo los falsos positivos que RN-01 quería evitar.

<!-- REGLA: un ADR aceptado es INMUTABLE. Para cambiar la decisión, escribe otro ADR que lo supersede (estado del viejo -> bloqueada + nota "superseded por ADR-NNN"). -->
