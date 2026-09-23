---
id: SPEC-002
tipo: spec
epica: EPIC-001
estado: aprobada
aprobada-por: Alberto Fojo
historial:
  - {estado: borrador, fecha: 2026-09-23, por: sdd-arquitecto}
  - {estado: aprobada, fecha: 2026-09-23, por: Alberto Fojo}
---
# SPEC-002 — Ejecución del probe baseline y veredicto de la hipótesis

> Spec **mixta**. Cada CA indica quién actúa:
> **[Humano]** poner claves, decidir y crear el espacio privado, lanzar humo y ejecución
> completa, leer la facturación, contraste en móvil.
> **[Agente]** dictamen de modelos (sdd-probe), ajuste de config y tests, análisis offline,
> revisión de respuestas, ampliación de `brands.csv`, documento de veredicto.
> Los agentes trabajan sobre los ficheros del espacio privado (ADR-001); nunca llaman a las
> APIs de pago.

## Problema
EPIC-001 (criterios de éxito 1 y 2) necesita un baseline medido y una respuesta con dato a la
hipótesis de `03-local-market-vigo-pontevedra.md` §2: *en dental y estética, menos de la
mitad de las respuestas nombran una clínica local; en fertilidad y oftalmología aparece
siempre la misma clínica*. La pata dental/estética es una de las dos del criterio Go de la
épica (SPEC-005). El probe (SPEC-001, `hecho`) nunca ha corrido contra APIs reales y su coste
real es desconocido (estimación del dictamen sdd-probe: ~20–30 €).

## Usuarios / roles afectados
- Humano (Alberto Fojo): prerrequisitos, claves, humo, completa, facturación, contraste.
- sdd-probe: dictamen de modelos por defecto vigente justo antes de la completa.
- Agente (sdd-implementador): config y tests si cambia un modelo, análisis, revisión,
  `brands.csv`, documento de veredicto.
- sdd-verificador: recalcula cifras desde el CSV privado con `--analyze`.
- Consumidores: SPEC-003 (extractos), SPEC-005 (pata probe del criterio Go).

## Prerrequisitos (antes de cualquier CA)
- **P-1 [Humano] Ubicación del espacio privado.** El humano decide dónde vive físicamente
  `PUSHLLM_PRIVADO` (disco local cifrado, nube privada u otro) y su copia de seguridad
  (follow-up de ADR-001). Esta spec **no** lo fija. En el ledger se anota solo el tipo de
  ubicación y de respaldo, nunca la ruta literal.
- **P-2 [Humano] Claves** de Anthropic, OpenAI y Gemini con límite de gasto configurado en
  cada consola (recomendado ≤ 20 € por proveedor).
- **P-3** SPEC-006 en `hecho` (y por tanto ADR-002 aprobado) antes de CA-4. El humo (CA-3)
  puede lanzarse antes.
- **Convención de ejecución** (observaciones V-1/V-2 del verificador de SPEC-001): todos los
  comandos se lanzan con `PUSHLLM_PRIVADO` definido; **no** se usa `--out` con una ruta dentro
  del repo. Humo: `--out "$PUSHLLM_PRIVADO/probe-smoke"`; completa y análisis: sin `--out`
  (salida en `$PUSHLLM_PRIVADO/probe`). `results.csv` y `summary.md` son **privados** (V-3):
  nunca se copian al repo; el documento de veredicto se redacta a partir de ellos
  anonimizando.

## Criterios de aceptación
- **CA-1 (claves y salida fuera del repo) [Humano, comprueba el verificador]**: Dado P-1 y P-2,
  cuando se lance cualquier comando del probe, entonces las claves solo existen en variables
  de entorno de la sesión (como documenta `probe/README.md`, sin ficheros), `PUSHLLM_PRIVADO`
  apunta fuera del árbol de trabajo del repo, y ni `git ls-files` ni `git log -p` contienen
  claves. *Evidencia*: búsqueda de `sk-`, `sk-ant-` y `AIza` en `git log -p --all` sin
  coincidencias; `git -C "$PUSHLLM_PRIVADO" rev-parse --show-toplevel` no devuelve la raíz de
  este repo; tipo de ubicación y respaldo anotados en el ledger (P-1).
- **CA-2 (modelos por defecto re-comprobados) [Agente: sdd-probe + sdd-implementador]**: Dado
  F-SPEC-001-3 (GPT-6 Luna anunciado el 2026-09-22, aún no en Chat), antes del humo y a ≤ 2 días
  de lanzar la completa (si pasan más, se repite), entonces consta en el ledger de esta spec un
  `### Dictamen sdd-probe (AAAA-MM-DD)` con la misma tabla que el de SPEC-001 (proveedor,
  modelo, búsqueda web, effort, fuente) que: (a) dice, **con fuente fechada**, cuál es el
  modelo por defecto de ChatGPT Free/Go **en Chat** (web y móvil); si ya es GPT-6 Luna, el
  modelo de `openai` pasa a `gpt-6-luna` en `probe/probe_config.json` con precio, fecha y
  fuente actualizados; (b) confirma o actualiza Claude y Gemini igual; (c) mantiene effort
  `low` en Claude y OpenAI (aceptado por el humano el 2026-09-24, F-SPEC-001-5) y el default
  de la API en Gemini. `probe/tests/test_config.py` compara la config con **el dictamen
  vigente** (el de este ledger si existe; si no, el de SPEC-001) y `python -m pytest
  probe/tests` pasa. *Evidencia*: dictamen en el ledger, diff de `probe_config.json` (o
  "sin cambios") y salida de pytest.
- **CA-3 (humo antes que completa) [Humano lanza; Agente revisa]**: Dado CA-1 y CA-2, cuando el humano
  lance `python run_probe.py --only D01,E01,F01,O01 --runs 1 --out "$PUSHLLM_PRIVADO/probe-smoke"`
  (12 llamadas), entonces antes de la completa consta en el ledger: filas por proveedor (4
  cada uno), cuántas con `status=ok` (se exige ≥ 3 de 4 por proveedor), el modelo servido
  (columna `model`), una respuesta por proveedor revisada a ojo (español coherente con la
  pregunta; URLs en `cited_urls` si el proveedor las da) y la extrapolación de coste
  Σ `cost_eur` del proveedor ÷ 4 × 132, sumada a los tres. Si un proveedor no llega a 3 de 4,
  el modelo servido no coincide con el del dictamen de CA-2, o la extrapolación supera 30 €,
  **no se lanza la completa** y se escala al humano. *Evidencia*: registro en ledger
  (cifras, sin nombres de clínica junto a cifras).
- **CA-4 (ejecución completa) [Humano]**: Dado un humo aceptado, CA-2 con ≤ 2 días de
  antigüedad y SPEC-006 en `hecho`, cuando el humano lance `python run_probe.py` (y, si se
  corta o hay fallos, como mucho **una** pasada de `python run_probe.py --resume`), entonces
  `$PUSHLLM_PRIVADO/probe/results.csv` cubre las 44 × 3 × 3 = 396 combinaciones
  (prompt, proveedor, run) y, por proveedor, ≤ 5 % de sus 132 combinaciones (≤ 6) quedan sin
  ninguna fila `status=ok`. El recuento se hace por **combinación**, no por fila: tras
  `--resume` las filas fallidas antiguas siguen en el CSV y en "Excluidas" de `summary.md`
  (V-1), que se lee como intentos fallidos. *Evidencia*: recuento por proveedor de
  combinaciones con y sin `ok` en el ledger (el verificador lo recalcula desde el CSV).
- **CA-5 (coste real registrado) [Humano lee; Agente registra]**: Dado que la facturación
  tiene retraso, cuando hayan pasado ≥ 48 h desde la completa, entonces constan en el ledger y
  en el documento de veredicto: coste real por proveedor leído de su consola (fecha de lectura
  e intervalo), total en €, coste estimado (Σ `cost_eur` de `results.csv`, humo incluido
  aparte) y la diferencia. Si el total supera 30 € o se desvía > 50 % de la estimación, se
  marca como desviación a comunicar a sdd-producto (revisar `06-…md` §2 y el No-negociable de
  coste). *Evidencia*: cifras en ledger; captura de cada consola **en el espacio privado**.
- **CA-6 (revisión de respuestas "sin clínica") [Agente]**: Dado el sesgo por `brands.csv`
  incompleto, cuando se calculen dental y estética, entonces antes del veredicto se han
  revisado ≥ 20 respuestas `ok` clasificadas "sin clínica local" de cada una de esas dos
  especialidades (todas si hay menos), repartidas entre proveedores; toda clínica local de
  Vigo/Pontevedra encontrada se añade a `brands.csv` con sus alias (una sigla corta solo en
  `exact_aliases` y solo si cumple ADR-002, dejando constancia en el ledger), se revisan a
  mano los falsos positivos conocidos de F-SPEC-001-6 ("De Castro", "Clínica Villoria" en
  estética) y se recalcula con `python run_probe.py --analyze`. *Evidencia*: lista de
  (prompt_id, proveedor, run) revisados en el espacio privado; diff de `brands.csv`;
  recuento antes/después por especialidad en el ledger; `python -m pytest probe/tests` pasa.
- **CA-7 (regla del veredicto) [Agente]**: Dado el agregado tras CA-6, cuando se emita el
  veredicto, entonces se aplica esta regla (definiciones del dictamen sdd-metricas de
  SPEC-001 CA-6 y RN-01 + RN-11): **pata dental/estética** = se cumple si el porcentaje
  ponderado (RN-03/RN-04) de respuestas válidas que nombran ≥ 1 clínica local es < 50 % **en
  dental y en estética** (ambas); se informa también por proveedor. **Pata
  fertilidad/oftalmología** = se cumple en cada especialidad si una misma marca de esa
  especialidad aparece en ≥ 80 % de sus respuestas válidas (líder de `summary.md`). El
  resultado de la pata dental/estética queda como `cumple | no cumple` en el documento y en
  el ledger (lo consume SPEC-005). *Evidencia*: el verificador aplica la regla a la salida de
  `--analyze` y obtiene lo mismo.
- **CA-8 (documento de veredicto en el repo) [Agente]**: Dado el análisis final, cuando se
  publique `docs/ciclo-0/baseline-probe.md`, entonces contiene: fecha de la completa, modelo
  servido y effort por proveedor, nº de combinaciones válidas, la tabla especialidad ×
  proveedor (válidas, con clínica local, %), el agregado ponderado, el veredicto de cada pata
  con la regla de CA-7, el reparto directorio/clínica por especialidad, el coste de CA-5 y
  una sección de limitaciones que incluya al menos: API ≠ app (`06-…md` §1A); effort `low`
  elegido por coste sin fuente pública del effort de las apps; Gemini sin ubicación en el
  grounding, solo la del texto del prompt, y `F04` y `P04` solo dicen "Galicia"
  (F-SPEC-001-1); cobertura de `brands.csv`; siglas (RN-11: IVI cuenta y se atribuye a IVI
  Vigo aunque hable de la cadena; `MIA` no cuenta, con el recuento de sesgo que da
  `summary.md`). Cumple ADR-001: **sin cifras junto a nombres de clínica** (la líder se cita
  "clínica A"). *Evidencia*: el verificador recalcula la tabla con `--analyze` sobre el CSV
  privado y coincide; búsqueda en el documento de los nombres y alias de `brands.csv` con
  `type ≠ directory`, sin coincidencias.
- **CA-9 (contraste en app real) [Humano hace; Agente redacta]**: Dado que la API aproxima pero
  no replica la app, cuando el humano haga en la app de ChatGPT desde un móvil en Vigo las
  preguntas `D01`, `D06`, `E01`, `F01` y `O01` (y, si puede, las mismas en la app de Gemini,
  prioritario por F-SPEC-001-1), entonces el detalle con nombres queda en el espacio privado y
  `docs/ciclo-0/baseline-probe.md` recoge por pregunta si la app coincide con el probe en
  "nombra / no nombra clínica local" y en la líder ("clínica A"), con una frase sobre la
  divergencia si la hay. *Evidencia*: tabla de contraste en el documento.
- **CA-10 (nada en bruto en el repo) [Verificador]**: Dado ADR-001, cuando se cierre la spec,
  entonces `git ls-files` no lista `results.csv`, `summary.md`, ficheros de humo, listas de
  revisión ni capturas de facturación, y `git status --ignored` no muestra `probe/out/` con
  datos de esta ejecución. *Evidencia*: ambas salidas en el ledger.

## Entidades y reglas afectadas
- Dominio: Probe / ProbeRun, Provider, Mention, Share of voice, Weighted SoV, Usage share /
  weight.
- RN-01, RN-11 (ADR-002), RN-02 (aquí sobre un único lote, no semanal), RN-03, RN-04, RN-10.
- D-5, D-6; No-negociables de coste y de conservación de respuestas en bruto.
- ADR-001 (frontera de datos), ADR-002 (siglas).
- Follow-ups de SPEC-001: F-SPEC-001-1 (limitación en CA-8 y contraste Gemini en CA-9),
  F-SPEC-001-3 (CA-2), F-SPEC-001-4 (resuelto por ADR-002 / SPEC-006), F-SPEC-001-5
  (aceptado, CA-2 y CA-8), F-SPEC-001-6 (CA-6), F-SPEC-001-7 (el probe se niega a
  sobrescribir: humo y completa van a directorios distintos).
- Depende de: SPEC-001 (hecho), SPEC-006 (antes de CA-4).

## Fuera de alcance
- Resolver las URLs de Gemini (`vertexaisearch.cloud.google.com`, F-SPEC-001-2): el veredicto
  se basa en menciones en el texto, no en URLs citadas. Va a SPEC-003.
- Extractos por clínica (SPEC-003).
- Ejecuciones periódicas o semanales (Ciclo 1–2). Google AI Overviews y Perplexity.
- Corregir `prompts.csv` tras ver resultados (incluidos F04/P04 sin ciudad): se anota como
  follow-up; cambiarlo invalidaría el baseline.
- Deduplicar filas fallidas antiguas en `analysis.py` (V-1): se resuelve contando por
  combinación en CA-4.

## Notas para el gate humano
- **Umbrales que decido yo y debéis mirar con lupa** (CA-7): (a) la pata dental/estética usa
  el agregado **ponderado** y exige que **ambas** especialidades estén < 50 %; (b) "aparece
  siempre la misma clínica" = **≥ 80 %** de las respuestas válidas. Alternativas: sin
  ponderar, "al menos una de las dos", o 100 %. Lo que se apruebe fija la pata probe del Go
  de SPEC-005.
- Pesos RN-04 normalizados a los tres proveedores sondeados: ChatGPT 55/90, Gemini 25/90,
  Claude 10/90.
- **Lo que tienes que hacer tú, en orden**: P-1 (decidir dónde vive `PUSHLLM_PRIVADO` y su
  respaldo), P-2 (claves y límites de gasto), aprobar ADR-002 y SPEC-006, lanzar el humo
  (CA-3), lanzar la completa tras el dictamen de CA-2 (CA-4), leer la facturación ≥ 48 h
  después (CA-5) y hacer el contraste en el móvil (CA-9).
- CA-2 puede cambiar el modelo de OpenAI (y su precio): si GPT-6 Luna ya es el default de
  Chat, cambian modelo y precio; por eso CA-2 va antes del humo (y se repite si pasan > 2 días
  hasta la completa) y CA-3 exige que el modelo servido coincida.
- Riesgo de calendario: la lectura de coste real tarda ≥ 48 h; SPEC-003 puede empezar en
  cuanto CA-4 y CA-6 estén cerrados, sin esperar a CA-5.
- Bloquea: SPEC-003 y el veredicto de SPEC-005.
