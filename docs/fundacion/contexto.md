# Contexto maestro — push-llm

> Documento vivo: TODO lo que un agente (o una persona) necesita para situarse.
> Se actualiza al cambiar el rumbo; la historia fina vive en ADRs y specs.

## Qué es y en qué punto está
SaaS de visibilidad de clínicas privadas en asistentes de IA (ver `vision.md`).
Estado a 2026-09-29: **semilla, pre-producto**. Nada validado con clientes de pago.

**Cambio de nicho (humano, 2026-09-29; ADR-008, DECISIONS.md D-009):** sanidad privada en
general, **A Mariña primero**, después resto de **Galicia**, **Asturias** y **provincia de
León**. **Vigo y Pontevedra quedan aparcados** (sin trabajo activo; no se abandonan).
- **EPIC-001** (Ciclo 0 en Vigo) cerrada sin completar (`bloqueada`). Queda de ella el probe
  preparado: SPEC-001 y SPEC-006 (`hecho`) y SPEC-002 reducida a claves, modelos y humo.
  SPEC-003, SPEC-004 y SPEC-005 `bloqueada`, con lo rescatable anotado en cada una.
- **EPIC-002** (piloto concierge con Clínica Ártica, medicina estética, Viveiro) es la
  **validación principal**: medición manual desde el móvil (SPEC-007) y lote de Viveiro del
  probe (SPEC-008).
- Humo del lote de Vigo ejecutado el 2026-09-29 (12/12 válidas; cifras en el espacio
  privado). El baseline completo de Vigo **no** se ejecuta.

## Stack y arquitectura (resumen as-built)
- `probe/` (Python; SPEC-001, SPEC-006, SPEC-008 y SPEC-002): `run_probe.py` (CLI) lanza un
  **lote** de preguntas contra Anthropic, OpenAI y Gemini con búsqueda web y ubicación del
  lote (Gemini: solo la del texto del prompt). Un proveedor se activa si su clave está en el
  entorno; `run_probe.py` carga solo el `.env` de la raíz del repo, sin sobrescribir el
  entorno ni mostrar valores (ADR-006, ADR-007).
  - Lotes por configuración (ADR-003 §3–§4): `probe_config.json` es el lote por defecto
    **Vigo/Pontevedra** (aparcado, intacto; 44 prompts es/gl); `batches/viveiro.json` es el
    lote del **piloto de Clínica Ártica** (ubicación Viveiro; niveles `AV` núcleo 3 runs,
    `AR` área de influencia 3 runs, `AG` Galicia 1 run, informados por separado; Go con tres
    condiciones tras ADR-009: (C) crecer en AR, (D) defender AV, (A) ≥1 paciente atribuido,
    veredictos (C) y (D) en `summary.md` ("no aplica" en la completitud de un nivel no medido);
    (A) sale de la atribución (SPEC-010) y el veredicto conjunto lo define SPEC-012; baseline
    oficial y medición "antes" de AR ya medidos en 2026-09-29; ADR-005 §4, ADR-009; marcas por
    pertenencia al lote; salida `$PUSHLLM_PRIVADO/piloto-artica/probe/`).
  - Modelos (dictamen sdd-probe vigente, 2026-09-29, ledger de SPEC-002): Claude
    `claude-sonnet-5-5` con effort `medium` y `max_tokens` 16000; OpenAI `gpt-5.6-luna` con
    effort `low`; Gemini `gemini-3.6-flash` con el default de la API.
  - Módulos: `settings.py` (config, precios con fecha y fuente, pesos RN-04, `extends` de
    lotes; override por `CLAUDE_MODEL`/`OPENAI_MODEL`/`GEMINI_MODEL`), `providers.py`
    (adaptadores → status ok/error/refusal/empty, tokens, búsquedas, `searched_urls` y `cited_urls`, `cost_eur`),
    `matching.py` (menciones RN-01 + RN-11 sobre `brands.csv`; siglas cortas en
    `exact_aliases`, ADR-002), `analysis.py` (cobertura, agregado ponderado, líder,
    directorios, sesgo de alias cortos, coste; por nivel en el lote del piloto).
  - Flags: `--config`, `--only`, `--runs`, `--levels`, `--providers`, `--resume`,
    `--analyze` (recuento offline), `--out`. Salida `results.csv` (respuesta en bruto), `raw_responses.jsonl` (respuestas completas sin cabeceras, SPEC-013 CA-1) y `summary.md`, todos **privados** (ADR-001, ADR-004). Tests offline en `probe/tests/`.
- Producto (`src/`): no existe. Stack sin decidir — se registrará como ADR cuando llegue el
  Ciclo 3.

## Decisiones clave hasta hoy
- Decisiones fundacionales D-1…D-8 en `FOUNDATION.md` (origen: `DECISIONS.md`); D-2 superada
  en parte por ADR-008 (D-009).
- ADR-001 (frontera de datos repo público / espacio privado) · ADR-002 (siglas cortas,
  RN-11) · ADR-003 (piloto de Clínica Ártica; vigentes §1, §3, §4 y §5 reinterpretado) ·
  ADR-004 (frontera de datos aplicada al piloto) · ADR-005 (catálogo del piloto en tres
  niveles; vigentes §1, §4, §5 técnico y §6) · ADR-006 (claves en `.env` local ignorado) ·
  ADR-007 (`.env.example` versionado) · ADR-008 (nicho nuevo).

## Riesgos y preguntas abiertas
- H1: ¿se puede mover una respuesta de LLM hacia una clínica en 8–12 semanas? (el riesgo que
  puede matar la idea). Hoy se prueba con un solo cliente (EPIC-002).
- H2: ¿paga una clínica 150–400 €/mes? · H3: ¿se pueden atribuir pacientes? · H4: ¿revenden
  las agencias?
- **Volumen del nicho nuevo**: A Mariña es pequeña; no hay ningún dato de mercado de resto de
  Galicia, Asturias ni León. Falta la épica de validación del nicho nuevo (sdd-producto).
- Normativa de publicidad sanitaria de Asturias y Castilla y León sin revisar
  (`sdd-sanidad-regulacion`, ADR-008 §7).
- Riesgo de plataforma: OpenAI/Google/Anthropic pueden lanzar analítica de marca o anuncios
  en respuestas.
- Preguntas abiertas del MVP (`07-mvp-product-spec.md` §8): qué señal de atribución mantienen
  las clínicas; si PresenceCheck necesita automatización; si AI Overviews es sondeable con
  fiabilidad; ticket medio por especialidad.
