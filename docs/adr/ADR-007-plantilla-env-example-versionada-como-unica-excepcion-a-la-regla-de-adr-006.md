---
id: ADR-007
tipo: adr
estado: borrador
historial:
  - {estado: borrador, fecha: 2026-09-29, por: sdd-arquitecto}
---
# ADR-007: Plantilla .env.example versionada como única excepción a la regla de ADR-006

- Deciders: propone sdd-arquitecto (2026-09-29), a raíz de la petición del humano (Alberto
  Fojo, 2026-09-29) de versionar una plantilla `.env.example` en la raíz del repo, sin
  valores y con comentarios, manteniendo ese nombre estándar. Aprueba: humano (pendiente).
- Specs relacionadas: SPEC-002 (CA-1 (d), enmendada el 2026-09-29 para citar este ADR).
- **Amplía ADR-006 §3 (no lo supersede)**, con el mismo patrón que ADR-004 respecto a
  ADR-001. ADR-006 es inmutable y sigue vigente; este ADR solo fija cómo se lee su
  comprobación "`git ls-files` no lista ningún `.env` ni `.env.*`".

## Contexto
ADR-006 §3 exige que `git ls-files` no liste ningún `.env` ni `.env.*`. El humano quiere
una plantilla versionada que documente qué variables hacen falta, y ha elegido el nombre
estándar `.env.example`, que casa con el patrón `.env.*`. Ya está commiteada, con la
excepción `!.env.example` en `.gitignore`; el `.env` real sigue ignorado. Sin este ADR, la
comprobación de ADR-006 §3 falla literalmente.

## Decisión
1. `.env.example`, en la raíz del repo, es el **único** fichero `.env*` que puede estar
   versionado. Ningún otro (`.env`, `.env.local`, `probe/.env`, `.env.example` en otra ruta…).
2. La comprobación de ADR-006 §3 "`git ls-files` no lista ningún `.env` ni `.env.*`" se lee
   como: **`git ls-files` no lista ningún fichero `.env*` salvo exactamente `.env.example`**,
   y además:
   - `.env.example` no contiene valores de claves: toda variable `*_API_KEY` que aparece en
     él está vacía (nada tras el `=`);
   - la búsqueda de `sk-`, `sk-ant-` y `AIza` no da coincidencias ni en su contenido
     (`git grep` sobre `.env.example`) ni en su historial
     (`git log -p --all -- .env.example`).
3. El resto de ADR-006 no cambia.

## Consecuencias
### Positivas
- Quien clone el repo ve qué variables hacen falta sin leer la guía de claves.
- La excepción es un solo fichero con nombre exacto y tres comprobaciones mecánicas.

### Negativas / follow-ups
- `.env.example` casa con `.env.*`: la protección depende de que la excepción de
  `.gitignore` sea exactamente `!.env.example`. Un `.env.example` rellenado por error se
  subiría sin aviso; lo mitigan las comprobaciones del punto 2 y la revocación de
  ADR-006 §6.

## Alternativas consideradas
- **Otro nombre fuera de `.env.*` (p. ej. `env.template`)**: evitaría tocar la regla de
  ADR-006, pero el humano eligió el nombre estándar.
- **Supersedar ADR-006 entero**: desproporcionado; solo cambia una comprobación.
- **Sin plantilla (solo la guía de claves)**: lo vigente hasta hoy; rechazada por decisión
  del humano.
