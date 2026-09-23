---
id: SPEC-002
tipo: spec
epica: EPIC-001
estado: borrador
aprobada-por:
historial:
  - {estado: borrador, fecha: 2026-09-23, por: sdd-arquitecto}
---
# SPEC-002 — Ejecución del probe baseline y veredicto de la hipótesis

> Spec **mixta**: la ejecución contra APIs reales, las claves, la lectura de las
> consolas de facturación y el contraste en app real son **acción del humano**; el
> análisis, la revisión de respuestas y el documento de veredicto los puede
> producir un **agente** sobre los ficheros del espacio privado (ADR-001).

## Problema
EPIC-001 (criterios de éxito 1 y 2) necesita un baseline medido y una respuesta
con dato a la hipótesis de `03-local-market-vigo-pontevedra.md` §2: *en dental y
estética, menos de la mitad de las respuestas nombran una clínica local; en
fertilidad y oftalmología aparece siempre la misma clínica*. La mitad de dental y
estética es además una de las dos patas del criterio Go de la épica (SPEC-005).
El probe nunca ha corrido y su coste real es desconocido (`06-…md` §2, estimación
15–30 €).

## Usuarios / roles afectados
- Humano: pone las claves, lanza humo y ejecución completa, lee la facturación,
  hace el contraste en app real.
- Agente (sdd-implementador): análisis, revisión de respuestas, ampliación de
  `brands.csv`, documento de veredicto.
- sdd-verificador: comprueba cifras recalculando desde el CSV privado.
- Consumidores: SPEC-003 (extractos), SPEC-005 (pata probe del criterio Go).

## Criterios de aceptación
- **CA-1 (claves fuera del repo)**: Dado que el humano configura las claves de OpenAI,
  Anthropic y Gemini, cuando se ejecute cualquier comando del probe, entonces las
  claves solo existen en variables de entorno o en un `.env` ignorado, y
  `git log -p` / `git ls-files` no contienen ninguna clave. *Evidencia*: `git
  check-ignore .env` y búsqueda de patrones de clave (`sk-`, `AIza`, `sk-ant-`) en el
  historial, sin coincidencias. **Acción humana.**
- **CA-2 (humo antes que completa)**: Dado SPEC-001 en `hecho`, cuando se lance el
  comando de humo documentado (12 llamadas), entonces antes de lanzar la ejecución
  completa consta en el ledger: nº de filas por proveedor (4 cada uno), cuántas en
  `status=ok` (se exige ≥ 3 de 4 por proveedor), una respuesta de ejemplo por proveedor
  revisada a ojo (texto en español coherente con la pregunta, con URLs citadas si el
  proveedor las da) y el coste estimado por llamada extrapolado a 396 llamadas. Si un
  proveedor falla o la extrapolación supera 30 €, **no se lanza la completa** y se
  escala al humano. *Evidencia*: registro en ledger + fichero de humo en el espacio
  privado. **Ejecución: humano.**
- **CA-3 (ejecución completa)**: Dado un humo aceptado, cuando termine la ejecución
  completa (reanudándola si se corta, SPEC-001 CA-7), entonces el fichero de
  resultados tiene 44 × 3 × 3 = 396 combinaciones (prompt, proveedor, run) y, por
  proveedor, ≤ 5 % de filas en `status` ≠ ok tras como mucho un reintento de las
  fallidas. *Evidencia*: salida del modo análisis con recuentos por proveedor en el
  ledger. **Ejecución: humano.**
- **CA-4 (coste real registrado)**: Dado que la facturación de cada proveedor tiene
  retraso, cuando hayan pasado al menos 48 h desde la ejecución completa, entonces
  consta en el ledger y en el documento de veredicto el coste real por proveedor leído
  de su consola (con fecha de lectura e intervalo), el total en €, el coste
  estimado por tokens (SPEC-001 CA-3) y la diferencia entre ambos; si el total
  supera 30 € o se desvía más de un 50 % de la estimación, se marca como desviación
  a comunicar a sdd-producto para revisar `06-…md` §2 y el No-negociable de coste.
  *Evidencia*: cifras en ledger; captura de cada consola en el espacio privado.
  **Lectura: humano.**
- **CA-5 (documento de veredicto en el repo)**: Dado el análisis de la ejecución
  completa, cuando se publique `docs/ciclo-0/baseline-probe.md`, entonces contiene:
  fecha, modelos efectivos por proveedor, nº de llamadas válidas, la tabla
  especialidad × proveedor de CA-5 de SPEC-001 (n/N y %), el agregado ponderado,
  el veredicto de cada pata de la hipótesis con la regla aplicada (ver CA-7), el
  reparto directorio/clínica por especialidad, el coste de CA-4 y una sección de
  limitaciones (API ≠ app, cobertura de `brands.csv`, alias cortos). Cumple ADR-001:
  **sin cifras junto a nombres de clínica** (la líder se nombra "clínica A").
  *Evidencia*: el verificador recalcula la tabla con el modo análisis sobre el CSV
  privado y coincide; búsqueda de nombres de `brands.csv` (tipo ≠ directory) en el
  documento, sin coincidencias.
- **CA-6 (revisión de respuestas "sin clínica")**: Dado el sesgo de `brands.csv`
  incompleto, cuando se calculen dental y estética, entonces antes del veredicto se
  han revisado al menos 20 respuestas clasificadas "sin clínica local" de cada una
  de esas dos especialidades (todas si hay menos), repartidas entre proveedores; toda
  clínica local de Vigo/Pontevedra encontrada se añade a `brands.csv` con sus alias y
  el análisis se recalcula offline. *Evidencia*: lista de ids de fila revisados (en
  el espacio privado) + diff de `brands.csv` + recuento antes/después en el ledger.
- **CA-7 (regla del veredicto)**: Dado el agregado, cuando se emita el veredicto,
  entonces se aplica esta regla, validada en el dictamen de `sdd-metricas` de SPEC-001
  CA-6: **pata dental/estética** = se cumple si el porcentaje ponderado (RN-03/RN-04)
  de respuestas que nombran ≥ 1 clínica local es < 50 % **en dental y en estética**
  (ambas); se informa también por proveedor. **Pata fertilidad/oftalmología** = se
  cumple en cada especialidad si una misma clínica de esa especialidad aparece en
  ≥ 80 % de sus respuestas válidas. El veredicto de la pata dental/estética queda
  como `cumple | no cumple` en el documento y en el ledger, porque SPEC-005 lo consume.
  *Evidencia*: el verificador aplica la regla a la tabla y obtiene el mismo resultado.
- **CA-8 (contraste en app real)**: Dado que la API aproxima pero no replica la app
  (`06-…md` §1A), cuando el humano haga en la app de ChatGPT desde un móvil en Vigo las
  preguntas `D01`, `D06`, `E01`, `F01` y `O01` (y, si puede, las mismas en la app de
  Gemini), entonces el detalle de las clínicas nombradas queda en el espacio privado y
  el documento de veredicto recoge, por pregunta, si la app coincide con el probe en
  "nombra / no nombra clínica local" y en la clínica líder, con una frase sobre
  la divergencia si la hay. *Evidencia*: tabla de contraste en
  `docs/ciclo-0/baseline-probe.md`. **Acción humana.**
- **CA-9 (nada en bruto en el repo)**: Dado ADR-001, cuando se cierre la spec,
  entonces `git ls-files` no lista ningún fichero de resultados, resumen, humo ni
  captura de facturación. *Evidencia*: salida de `git ls-files` + `git status --ignored`
  en el ledger.

## Entidades y reglas afectadas
- Dominio: Probe / ProbeRun, Provider, Mention, Share of voice, Weighted SoV,
  Usage share / weight.
- RN-01, RN-02 (aquí sobre un único lote, no semanal), RN-03, RN-04, RN-10.
- D-5, D-6; No-negociables de coste y de conservación de respuestas en bruto.
- ADR-001. Depende de SPEC-001.

## Fuera de alcance
- Extractos por clínica (SPEC-003).
- Ejecuciones periódicas o semanales (Ciclo 1–2).
- Google AI Overviews y Perplexity.
- Corregir `prompts.csv` tras ver resultados: si se detecta un prompt defectuoso se
  anota como follow-up; cambiarlo invalidaría el baseline.

## Notas para el gate humano
- **Umbrales que decido yo y debéis mirar con lupa** (CA-7): (a) la pata dental/estética
  usa el agregado **ponderado** y exige que **ambas** especialidades estén por debajo de
  50 %; (b) "aparece siempre la misma clínica" se operacionaliza como **≥ 80 %** de las
  respuestas. Alternativas razonables: sin ponderar, o "al menos una de las dos"; 100 %
  en vez de 80 %. Lo que se apruebe aquí fija la pata probe del Go de SPEC-005.
- Pesos de RN-04 normalizados a los tres proveedores sondeados: ChatGPT 55/90,
  Gemini 25/90, Claude 10/90.
- **Acciones del humano**: claves (CA-1), humo (CA-2), completa (CA-3), lectura de
  facturación ≥ 48 h después (CA-4), contraste en móvil (CA-8). También decidir dónde
  vive `PUSHLLM_PRIVADO` y su copia de seguridad (ADR-001).
- Riesgo de calendario: la lectura de coste real tarda ≥ 48 h; SPEC-003 puede empezar
  en cuanto CA-3 y CA-6 estén cerrados, sin esperar a CA-4.
- Depende de: SPEC-001. Bloquea: SPEC-003 y el veredicto de SPEC-005.
