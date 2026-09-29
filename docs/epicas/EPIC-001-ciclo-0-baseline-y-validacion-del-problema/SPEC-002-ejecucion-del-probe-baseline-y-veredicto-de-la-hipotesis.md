---
id: SPEC-002
tipo: spec
epica: EPIC-001
estado: en-revision
aprobada-por: Alberto Fojo
historial:
  - {estado: borrador, fecha: 2026-09-23, por: sdd-arquitecto}
  - {estado: aprobada, fecha: 2026-09-23, por: Alberto Fojo}
  - {estado: bloqueada, fecha: 2026-09-29, por: sdd-arquitecto}
  - {estado: borrador, fecha: 2026-09-29, por: sdd-arquitecto}
  - {estado: aprobada, fecha: 2026-09-29, por: Alberto Fojo}
  - {estado: bloqueada, fecha: 2026-09-29, por: sdd-arquitecto}
  - {estado: borrador, fecha: 2026-09-29, por: sdd-arquitecto}
  - {estado: aprobada, fecha: 2026-09-29, por: Alberto Fojo}
  - {estado: en-progreso, fecha: 2026-09-29, por: sdd-implementador}
  - {estado: bloqueada, fecha: 2026-09-29, por: sdd-arquitecto}
  - {estado: borrador, fecha: 2026-09-29, por: sdd-arquitecto}
  - {estado: aprobada, fecha: 2026-09-29, por: Alberto Fojo}
  - {estado: en-progreso, fecha: 2026-09-29, por: sdd-implementador}
  - {estado: en-revision, fecha: 2026-09-29, por: sdd-implementador}
---
# SPEC-002 — Preparación del probe para ejecuciones reales: claves, modelos y humo

> **Alcance reducido 2026-09-29 (sdd-arquitecto) — cambio de nicho (ADR-008).** Título
> anterior: "Ejecución del probe baseline y veredicto de la hipótesis". El humano (Alberto
> Fojo) aparca Vigo y Pontevedra y cierra EPIC-001 sin completar. Esta spec se queda **solo**
> con lo que el probe necesita para cualquier ejecución real (y que el piloto de EPIC-002 usa
> ya): custodia de claves (CA-1), modelos por defecto re-comprobados (CA-2), humo (CA-3) y
> nada en bruto en el repo (CA-10). CA-4 a CA-9 (ejecución completa de Vigo, coste real,
> revisión "sin clínica", regla y documento del veredicto, contraste en app) **se retiran**
> y pasan a "Fuera de alcance". Los ids de CA no se renumeran. La spec vuelve a `borrador`
> y necesita **re-aprobación humana**. Se queda en EPIC-001 (y en su rama) porque
> `probe/tests/test_config.py` lee el dictamen vigente de este ledger por su ruta.

> Spec **mixta**. Cada CA indica quién actúa:
> **[Humano]** poner claves, decidir y crear el espacio privado, lanzar el humo.
> **[Agente]** dictamen de modelos (sdd-probe), ajuste de config y tests, revisión del humo.
> Los agentes trabajan sobre los ficheros del espacio privado (ADR-001); nunca llaman a las
> APIs de pago.

> **Enmienda 2026-09-29 (sdd-arquitecto) — claves en un `.env` local ignorado (ADR-006).**
> Por decisión del humano (Alberto Fojo, 2026-09-29), las claves pueden vivir en un `.env`
> en la raíz de la copia local del repo, ignorado por git, además de en la sesión. Cambian
> CA-1 y P-2; el resto de CA no cambia. La spec vuelve a `borrador` y necesita
> re-aprobación humana.

## Problema
El probe (SPEC-001, `hecho`) nunca había corrido contra APIs reales. Antes de cualquier
ejecución real —hoy, el lote de Viveiro del piloto de Clínica Ártica (SPEC-008 CA-7) y su
medición semanal (SPEC-012)— hace falta: que las claves estén custodiadas sin riesgo de
acabar en el repo público, que los modelos configurados sean los que sirven las apps de
consumo (D-5) y un humo que confirme que los tres proveedores responden, sirven el modelo
del dictamen y cuestan lo estimado. Ese trabajo nació para el baseline de Vigo (EPIC-001);
con el cambio de nicho (ADR-008) el baseline de Vigo no se ejecuta, pero el trabajo sirve
tal cual para el piloto.

## Usuarios / roles afectados
- Humano (Alberto Fojo): prerrequisitos, claves, humo.
- sdd-probe: dictamen de modelos por defecto (CA-2).
- Agente (sdd-implementador): config y tests, carga del `.env`, revisión del humo.
- sdd-verificador: comprobaciones de git (CA-1), pytest (CA-2), cifras del humo desde el CSV
  privado (CA-3), CA-10.
- Consumidores: SPEC-008 CA-7 (claves y modelos del lote de Viveiro), SPEC-012.

## Prerrequisitos (antes de cualquier CA)
- **P-1 [Humano] Ubicación del espacio privado.** El humano decide dónde vive físicamente
  `PUSHLLM_PRIVADO` (disco local cifrado, nube privada u otro) y su copia de seguridad
  (follow-up de ADR-001). Esta spec **no** lo fija. En el ledger se anota solo el tipo de
  ubicación y de respaldo, nunca la ruta literal.
- **P-2 [Humano] Claves** de Anthropic, OpenAI y Gemini con límite de gasto configurado en
  cada consola (recomendado ≤ 20 € por proveedor). Custodia según ADR-006: en la sesión o en
  el `.env` local ignorado; el contenido del `.env` se guarda como nota segura en el gestor
  de contraseñas (enmienda 2026-09-29).
- **Convención de ejecución** (observaciones V-1/V-2 del verificador de SPEC-001): todos los
  comandos se lanzan con `PUSHLLM_PRIVADO` definido; **no** se usa `--out` con una ruta dentro
  del repo. Humo: `--out "$PUSHLLM_PRIVADO/probe-smoke"`. `results.csv` y `summary.md` son
  **privados** (V-3): nunca se copian al repo.

## Criterios de aceptación
- **CA-1 (claves y salida fuera del repo) [Humano, comprueba el verificador]**: Dado P-1 y P-2,
  cuando se lance cualquier comando del probe, entonces las claves existen solo en variables
  de entorno de la sesión o de usuario, o en un `.env` en la raíz del árbol de trabajo local
  ignorado por git (ADR-006; ~~solo en variables de entorno de la sesión, sin ficheros~~,
  enmienda 2026-09-29); ningún otro fichero del árbol de trabajo contiene claves;
  `PUSHLLM_PRIVADO` apunta fuera del árbol de trabajo del repo, y ni `git ls-files` ni
  `git log -p` contienen claves. *Evidencia* (salidas en el ledger, sin valores de clave):
  (a) `git check-ignore -v .env` responde con una regla de `.gitignore`; (b)
  `git log --all --oneline -- .env` sale vacío; (c) `git status --porcelain` no lista `.env`;
  (d) `git ls-files` no lista ningún fichero `.env*` salvo exactamente `.env.example` en la
  raíz (ADR-007; ~~ningún `.env` ni `.env.*`~~, enmienda 2026-09-29), toda variable
  `*_API_KEY` de `.env.example` está vacía, y la búsqueda de `sk-`, `sk-ant-` y `AIza` no da
  coincidencias en su contenido ni en `git log -p --all -- .env.example`; (e) búsqueda de `sk-`, `sk-ant-` y
  `AIza` en `git log -p --all` sin coincidencias; (f) la misma búsqueda sobre los ficheros
  versionados (`git grep`) sin coincidencias; (g) `git -C "$PUSHLLM_PRIVADO" rev-parse
  --show-toplevel` no devuelve la raíz de este repo; tipo de ubicación y respaldo anotados en
  el ledger (P-1). Si el humano no usa `.env`, (a)–(c) se anotan igual (protegen contra uno
  creado más tarde).
- **CA-2 (modelos por defecto re-comprobados) [Agente: sdd-probe + sdd-implementador]**: Dado
  F-SPEC-001-3 (GPT-6 Luna anunciado el 2026-09-22, aún no en Chat), antes del humo, entonces
  consta en el ledger de esta spec un `### Dictamen sdd-probe (AAAA-MM-DD)` con la misma
  tabla que el de SPEC-001 (proveedor, modelo, búsqueda web, effort, fuente) que: (a) dice,
  **con fuente fechada**, cuál es el modelo por defecto de ChatGPT Free/Go **en Chat** (web y
  móvil); si ya es GPT-6 Luna, el modelo de `openai` pasa a `gpt-6-luna` en
  `probe/probe_config.json` con precio, fecha y fuente actualizados; (b) confirma o actualiza
  Claude y Gemini igual; (c) effort: **Claude `medium`** con `max_tokens` 16000 (decisión
  del humano del 2026-09-29, F-SPEC-002-4: como en la app, D-5), **OpenAI `low`**
  (F-SPEC-001-5) y el default de la API en Gemini (~~mantiene effort `low` en Claude y
  OpenAI~~, alcance reducido 2026-09-29). `probe/tests/test_config.py` compara la config con
  **el dictamen vigente** (el fechado más reciente entre este ledger y el de SPEC-001) y
  `python -m pytest probe/tests` pasa. (~~a ≤ 2 días de lanzar la completa~~: ya no hay
  completa; la vigencia del dictamen antes de una ejecución real del piloto es
  F-SPEC-002-6.) *Evidencia*: dictamen en el ledger, diff de `probe_config.json` y salida
  de pytest.
- **CA-3 (humo) [Humano lanza; Agente revisa]**: Dado CA-1 y CA-2, cuando el humano lance
  `python run_probe.py --only D01,E01,F01,O01 --runs 1 --out "$PUSHLLM_PRIVADO/probe-smoke"`
  (12 llamadas, lote por defecto), entonces consta en el ledger: filas por proveedor (4
  cada uno), cuántas con `status=ok` (se exige ≥ 3 de 4 por proveedor; ninguna fila de
  Claude `empty` o cortada, por el effort `medium`), el modelo servido (columna `model`)
  igual al del dictamen de CA-2, una respuesta por proveedor revisada a ojo (español
  coherente con la pregunta; URLs en `cited_urls` si el proveedor las da) y el **coste
  medido por pregunta × ejecución** con los tres proveedores (Σ `cost_eur` ÷ 4), por
  proveedor y total. Si un proveedor no llega a 3 de 4 o el modelo servido no coincide, el
  humo no se acepta y se escala al humano antes de cualquier ejecución real del piloto.
  (~~extrapolación Σ `cost_eur` ÷ 4 × 132 y tope de 30 € para lanzar la completa~~,
  alcance reducido 2026-09-29.) *Evidencia*: registro en ledger (cifras, sin nombres de
  clínica junto a cifras); el verificador recalcula desde el `results.csv` del humo.
- **CA-10 (nada en bruto en el repo) [Verificador]**: Dado ADR-001, cuando se cierre la spec,
  entonces `git ls-files` no lista `results.csv`, `summary.md`, ficheros de humo, listas de
  revisión ni capturas de facturación, y `git status --ignored` no muestra `probe/out/` con
  datos de esta ejecución. *Evidencia*: ambas salidas en el ledger.

### CA retirados (alcance reducido 2026-09-29, ADR-008)
En el ledger se marcan `n-a` con la causa "retirado por cambio de nicho (ADR-008)". El texto
aprobado queda en el historial de git (versión anterior de este fichero).
- ~~**CA-4** (ejecución completa del lote de Vigo, 396 combinaciones)~~.
- ~~**CA-5** (coste real de la completa leído en las consolas)~~.
- ~~**CA-6** (revisión de respuestas "sin clínica" y ampliación de `brands.csv` de Vigo)~~.
- ~~**CA-7** (regla del veredicto de la hipótesis de Vigo)~~.
- ~~**CA-8** (`docs/ciclo-0/baseline-probe.md`)~~.
- ~~**CA-9** (contraste en la app desde un móvil en Vigo)~~.

## Entidades y reglas afectadas
- Dominio: Probe / ProbeRun, Provider.
- RN-10 (modelo por defecto de la app); D-5; No-negociables de coste y de conservación de
  respuestas en bruto.
- ADR-001 (frontera de datos), ADR-006 (custodia de claves), ADR-007 (`.env.example`),
  ADR-008 (cambio de nicho: alcance reducido).
- Follow-ups de SPEC-001: F-SPEC-001-3 (CA-2), F-SPEC-001-5 (superado para Claude por
  F-SPEC-002-4), F-SPEC-001-7 (el probe se niega a sobrescribir: humo en directorio propio).
- Depende de: SPEC-001 (hecho). El dictamen de CA-2 cubre también el lote de Viveiro, que
  hereda modelos y precios de `probe_config.json` (SPEC-008).

## Fuera de alcance
- **Todo lo del veredicto de Vigo** (antes CA-4 a CA-9): ejecución completa del lote de
  Vigo, coste real de esa ejecución, revisión "sin clínica", regla y documento del
  veredicto, contraste en la app. Motivo: cambio de nicho (ADR-008); EPIC-001 cerrada. Si
  el humano retoma Vigo (roadmap), se especifica de nuevo con el dictamen de modelos de ese
  momento.
- La ejecución real del lote de Viveiro (SPEC-008 CA-7) y la medición semanal (SPEC-012).
- Resolver las URLs de Gemini (F-SPEC-001-2). Google AI Overviews y Perplexity.
- Corregir `prompts.csv` del lote de Vigo; deduplicar filas fallidas antiguas en
  `analysis.py` (V-1).

## Notas para el gate humano
- **Alcance reducido 2026-09-29 (re-aprobación)**: solo **se quita** trabajo y se ajustan
  CA-2 (c) y CA-3 a lo ya decidido y hecho: (i) CA-2 (c) recoge el effort `medium` de
  Claude y `max_tokens` 16000 que ya decidiste el 2026-09-29 (F-SPEC-002-4) y quita la
  caducidad ligada a la completa; (ii) CA-3 cambia la extrapolación a 132 preguntas y el
  tope de 30 € (que solo servían para decidir la completa de Vigo) por el coste medido por
  pregunta × ejecución, que es lo que usa SPEC-008 (umbral `c ≤ 0,19 €`); (iii) CA-4 a CA-9
  se retiran. CA-1 y CA-10 no cambian. Nada nuevo que implementar: el código ya está hecho
  y probado (F-SPEC-002-1, CA-2).
- **Lo que queda tras la re-aprobación**: [Humano] las comprobaciones de git de CA-1
  (a)–(g) (comandos en `probe/README.md`) y anotar tipo de ubicación y respaldo del espacio
  privado; [Agente] rellenar CA-3 en el ledger con el humo ya ejecutado hoy (12/12, modelos
  servidos iguales al dictamen, 0,105 € por pregunta × ejecución; cifras en
  `$PUSHLLM_PRIVADO/probe-smoke`); [Verificador] CA-1, CA-2, CA-3, CA-10 y `n-a` en CA-4 a
  CA-9.
- **Por qué no una spec nueva**: la rama, el ledger (dictamen vigente, follow-ups) y los
  tests (`test_config.py` lee este ledger por su ruta) ya apuntan aquí; una spec nueva
  obligaría a mover el dictamen y a tocar código solo para cambiar una ruta, y también
  necesitaría aprobación humana.
- **Por qué sigue en EPIC-001 (`bloqueada`)**: por la misma ruta; una spec puede cerrarse
  `hecho` dentro de una épica cerrada sin completar.
- Pesos RN-04 normalizados a los tres proveedores sondeados: ChatGPT 55/90, Gemini 25/90,
  Claude 10/90 (sin cambios).
- Ya no bloquea SPEC-003 ni SPEC-005 (ambas `bloqueada` por ADR-008).
