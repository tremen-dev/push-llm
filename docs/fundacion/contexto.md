# Contexto maestro — push-llm

> Documento vivo: TODO lo que un agente (o una persona) necesita para situarse.
> Se actualiza al cambiar el rumbo; la historia fina vive en ADRs y specs.

## Qué es y en qué punto está
SaaS de visibilidad de clínicas privadas en asistentes de IA (ver `vision.md`).
Estado a 2026-09-24: **semilla, pre-producto**. Existen los documentos fundacionales (`README.md`, `00-…08-*.md`, `DECISIONS.md`) y el kit `probe/` del Ciclo 0, que **aún no se ha ejecutado** (faltan API keys). Nada validado con clientes de pago.

## Stack y arquitectura (resumen as-built)
- `probe/` (Python, as-built tras SPEC-001, 2026-09-23): `run_probe.py` (CLI) lanza `prompts.csv` (44 prompts es/gl) contra Anthropic, OpenAI y Gemini con búsqueda web y ubicación Vigo (Gemini: solo la del texto del prompt); un proveedor se activa si está su clave en el entorno. Módulos: `settings.py` (carga `probe_config.json`: modelo, runs, effort, precios con fecha y fuente, pesos RN-04; override por `CLAUDE_MODEL`/`OPENAI_MODEL`/`GEMINI_MODEL`), `providers.py` (adaptadores → status ok/error/refusal/empty, tokens, búsquedas, URLs, `cost_eur`), `matching.py` (menciones RN-01 + RN-11 sobre `brands.csv`: 43 clínicas + 9 directorios; siglas cortas inequívocas en la columna `exact_aliases`, hoy solo `IVI` → IVI Vigo, sensibles a mayúsculas y por palabra completa; SPEC-006, ADR-002), `analysis.py` (cobertura, agregado ponderado, líder, directorios, sesgo de alias cortos, coste).
- Flags: `--only`, `--runs`, `--providers`, `--resume` (solo combinaciones sin fila ok; sin él no sobrescribe), `--analyze` (recuento offline sin llamadas), `--out`, `--config`. Salida `results.csv` (16 columnas, respuesta en bruto) + `summary.md`, ambos **privados** (ADR-001): `--out` > `$PUSHLLM_PRIVADO/probe` > `probe/out/` (gitignored). Tests offline en `probe/tests/`. Pendiente: primera ejecución real (SPEC-002).
- Producto (`src/`): no existe. Stack sin decidir — se registrará como ADR cuando llegue el Ciclo 3.

## Decisiones clave hasta hoy
- Decisiones fundacionales D-1…D-8 en `FOUNDATION.md` (origen: `DECISIONS.md`).
- ADRs: ADR-001 (frontera de datos repo público / espacio privado, aprobada); ADR-002 (excepción a RN-01 para siglas cortas, aprobada 2026-09-24).

## Riesgos y preguntas abiertas
- H1: ¿se puede mover una respuesta de LLM hacia una clínica en 8–12 semanas? (el riesgo que puede matar la idea)
- H2: ¿paga una clínica 150–400 €/mes? · H3: ¿se pueden atribuir pacientes? · H4: ¿revenden las agencias?
- Riesgo de plataforma: OpenAI/Google/Anthropic pueden lanzar analítica de marca o anuncios en respuestas.
- Preguntas abiertas del MVP (`07-mvp-product-spec.md` §8): qué señal de atribución mantienen las clínicas; si PresenceCheck necesita automatización; si AI Overviews es sondeable con fiabilidad; ticket medio por especialidad.
