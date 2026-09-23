# Contexto maestro — push-llm

> Documento vivo: TODO lo que un agente (o una persona) necesita para situarse.
> Se actualiza al cambiar el rumbo; la historia fina vive en ADRs y specs.

## Qué es y en qué punto está
SaaS de visibilidad de clínicas privadas en asistentes de IA (ver `vision.md`).
Estado a 2026-09-23: **semilla, pre-producto**. Existen los documentos fundacionales (`README.md`, `00-…08-*.md`, `DECISIONS.md`) y el kit `probe/` del Ciclo 0, que **aún no se ha ejecutado** (faltan API keys). Nada validado con clientes de pago.

## Stack y arquitectura (resumen as-built)
- `probe/run_probe.py` (Python): lanza `prompts.csv` (44 prompts es/gl) N veces contra Anthropic, OpenAI y Gemini con búsqueda web y ubicación Vigo; cuenta menciones de `brands.csv` (43 clínicas + 9 directorios); escribe `results.csv` + `summary.md`.
- Producto (`src/`): no existe. Stack sin decidir — se registrará como ADR cuando llegue el Ciclo 3.

## Decisiones clave hasta hoy
- Decisiones fundacionales D-1…D-8 en `FOUNDATION.md` (origen: `DECISIONS.md`).
- ADRs: ninguno todavía.

## Riesgos y preguntas abiertas
- H1: ¿se puede mover una respuesta de LLM hacia una clínica en 8–12 semanas? (el riesgo que puede matar la idea)
- H2: ¿paga una clínica 150–400 €/mes? · H3: ¿se pueden atribuir pacientes? · H4: ¿revenden las agencias?
- Riesgo de plataforma: OpenAI/Google/Anthropic pueden lanzar analítica de marca o anuncios en respuestas.
- Preguntas abiertas del MVP (`07-mvp-product-spec.md` §8): qué señal de atribución mantienen las clínicas; si PresenceCheck necesita automatización; si AI Overviews es sondeable con fiabilidad; ticket medio por especialidad.
