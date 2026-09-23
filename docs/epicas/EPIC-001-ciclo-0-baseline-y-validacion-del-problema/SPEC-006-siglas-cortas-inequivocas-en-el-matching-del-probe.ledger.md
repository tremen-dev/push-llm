---
id: SPEC-006
tipo: ledger
epica: EPIC-001
---
# Ledger — SPEC-006 Siglas cortas inequívocas en el matching del probe

## Resumen
- Fase: <!-- refleja el estado de la spec; la fuente de verdad es el frontmatter de la spec -->
- Rama: `ft/SPEC-006-siglas-cortas-inequivocas-en-el-matching-del-probe`

## Matriz de criterios de aceptación
<!-- Escritores: sdd-implementador rellena Implementado y Test; sdd-verificador rellena Verif. y Estado. Nunca al revés. -->
<!-- Estados por CA: ✅ cerrado · ⚠️ parcial/con salvedad · 🚧 en curso · ❌ sin empezar · n-a -->
<!-- Un CA está ✅ solo cuando Implementado + Test + Verif. aplicables están en verde. Una salvedad se marca ⚠️, nunca ✅. -->
| CA | Implementado (fichero) | Test (fichero/caso) | Verif. | Estado |
|---|---|---|---|---|
| CA-0 | Dictamen sdd-metricas en este ledger (Notas); ADR-002 `estado: aprobada` | n-a (evidencia documental: sección Notas + frontmatter de ADR-002) | | ❌ |
| CA-1 | | | | ❌ |
| CA-2 | | | | ❌ |
| CA-3 | | | | ❌ |
| CA-4 | | | | ❌ |
| CA-5 | | | | ❌ |
| CA-6 | | | | ❌ |
| CA-7 | | | | ❌ |

## Veredicto del verificador
<!-- GREEN/RED + fecha + resumen. Lo escribe SOLO sdd-verificador. -->

## Evidencia visual
<!-- Tabla CA → captura en _qa/SPEC-006/. Informe HTML opcional: _qa/SPEC-006/informe.html -->

## Notas

### Dictamen sdd-metricas (2026-09-24) — ADR-002 reglas 1–5 (CA-0)
Emitido por sdd-implementador aplicando `.ai-context/skills/sdd-metricas.md`.
Veredicto global: **correcto**. Nada de lo que sigue cambia la regla ni el ADR; las notas
son de implementación o de documentación. Invariantes: RN-01, RN-02, RN-03, RN-06, RN-11,
D-6. Fuentes: `docs/fundacion/reglas.md` (RN-01, RN-11), `docs/fundacion/dominio.md`
(Mention), dictamen sdd-metricas de SPEC-001 (puntos 3–5), ADR-002.

1. **Definición de sigla corta inequívoca (§1)** — *correcto*. Los cuatro requisitos
   preservan el objetivo de RN-01 (evitar falsos positivos con palabras comunes) y (d)
   mantiene la atribución a una sola marca, así que una sigla nunca pasa por la resolución
   de alias compartidos (punto 4 del dictamen de SPEC-001). Para `IVI`: (b) es la forma con
   la que la marca se nombra públicamente (IVI / IVIRMA); (c) "ivi" no es palabra en
   castellano ni gallego ni sigla sanitaria de uso general (la de interrupción del
   embarazo es IVE); (d) ninguna otra marca de `brands.csv` la usa.
2. **Marcado en catálogo (§2)** — *correcto*. La sigla es dato de la marca; fallar al cargar
   si incumple (a) o (d) evita contar siglas no juzgadas en silencio.
3. **Comparación (§3)** — *correcto*. Sensible a mayúsculas y por palabra completa sobre el
   texto original; "palabra completa" debe tratar como letra cualquier letra Unicode
   (acentuada incluida) y los dígitos, y como frontera todo lo demás (espacio, puntuación,
   guion, paréntesis). Así "IVI-RMA" y "(IVI)" cuentan e "IVIS", "XIVI", "IVI2", "ÁIVI" no.
4. **Qué cuenta (§4)** — *correcto*. Una coincidencia de sigla es una Mention a efectos de
   cobertura (RN-02), agregado ponderado (RN-03) y líder. Nota de implementación: la
   ocurrencia de sigla debe entrar en la misma deduplicación por marca (punto 5 de SPEC-001)
   y en la regla de solapes (punto 4): si está contenida en un nombre más largo que también
   coincide ("IVI" dentro de "IVI Vigo"), cuenta la larga; el resultado es la misma marca
   una sola vez. El orden de aparición (RN-06, Position) no se calcula en Ciclo 0; basta con
   que el orden sea determinista.
5. **Alcance (§5)** — *correcto*. `MIA` incumple (c) ("mía"); en mayúsculas de énfasis o
   título sería falso positivo. Debe seguir sin contar y seguir apareciendo en el recuento
   de sesgo de `summary.md`. Ese recuento debe seguir incluyendo también las apariciones de
   `IVI` que no cuentan (minúsculas o capitalizada, p. ej. "ivi", "Ivi"), porque ADR-002
   (Consecuencias) confía en él para medir el acierto perdido.

Specs/documentos a revisar (sin bloquear): `docs/fundacion/dominio.md` (entidad Mention)
solo cita el umbral de ≥ 4 caracteres y no la excepción RN-11 → F-SPEC-006-1. El texto de
RN-01/RN-11 en `reglas.md` aún dice "ADR-002 en borrador" aunque ADR-002 está aprobada →
F-SPEC-006-2. SPEC-002 (veredicto) debe anotar la limitación "IVI cadena → IVI Vigo".

## Salvedades / follow-ups
<!-- IDs F-SPEC-006-1, F-SPEC-006-2… con destino (spec futura o EPIC-MEJORA). -->
- **F-SPEC-006-1** (drift de dominio): `docs/fundacion/dominio.md`, entidad Mention, no menciona la excepción RN-11 (siglas cortas). Destino: sdd-arquitecto / humano (documento de verdad, no lo edita el implementador).
- **F-SPEC-006-2** (drift de reglas): RN-01 y RN-11 en `docs/fundacion/reglas.md` dicen "ADR-002 en borrador"; ADR-002 está `aprobada`. Destino: sdd-arquitecto / humano.
- **F-SPEC-006-3** (historial): en SPEC-006 y ADR-002 la entrada `aprobada` (2026-09-23) tiene fecha anterior a la de `borrador` (2026-09-24). No afecta al código; revisar fechas. Destino: sdd-arquitecto / humano.

## Cómo retomar (handoff)
<!-- Estado real del trabajo para la siguiente sesión: qué está hecho, qué falta, dónde seguir. -->
