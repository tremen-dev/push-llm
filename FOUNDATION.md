# FOUNDATION — push-llm

> Constitución del proyecto. Las decisiones D-N están **locked**: solo un ADR
> aceptado puede reinterpretarlas o supersederlas. Dueños: sdd-arquitecto y
> sdd-producto (hook protege-verdad).

- Creado: 2026-09-23
- Dominio: SaaS que mide y mejora cómo los asistentes de IA (ChatGPT, Gemini, Claude, Perplexity, Google AI Overviews) recomiendan clínicas sanitarias privadas en Galicia, y atribuye los pacientes que llegan por ese canal.

## Decisiones locked
<!-- Origen: DECISIONS.md (D-001…D-008, 2026-09-23). El detalle y la justificación viven allí. -->
- **D-1** (2026-09-23): Nicho vertical + geográfico; el producto no se generaliza a "cualquier negocio" en el MVP. (DECISIONS.md D-001)
- **D-2** (2026-09-23): Nicho primario = clínicas sanitarias privadas, Vigo y Pontevedra primero. Dental = volumen; oftalmología y fertilidad = casos demo; estética = segundo mercado; fisio solo vía agencias; hospitales en fase 2. Nicho secundario (año 2): educación privada. (D-002)
- **D-3** (2026-09-23): Se vende "pacientes desde ChatGPT", no "visibilidad en IA". La atribución (referral tags + subida de búsqueda de marca + respuesta en recepción) es funcionalidad del día uno. (D-003)
- **D-4** (2026-09-23): Secuencia lean: nada de código de producto antes de la evidencia del Ciclo 2 (`05-lean-plan.md`). (D-004)
- **D-5** (2026-09-23): El probe usa el modelo por defecto (gama media) de cada app de consumo, con búsqueda web y ubicación de la ciudad; el procesamiento interno usa el modelo más barato que supere un test etiquetado. (D-005)
- **D-6** (2026-09-23): Toda métrica de visibilidad se pondera por cuota de uso del asistente; los pesos son configuración y se refrescan mensualmente; Google AI Overviews se trata como canal aparte. (D-006)
- **D-7** (2026-09-23): Ancla de precio de pilotos: 3 meses a 450 € prepago o 199 €/mes; nunca gratis más allá del informe de una página. Pendiente de validar en el Ciclo 1. (D-007)
- **D-8** (2026-09-23): Documentos fundacionales (00–08) en inglés; material para clientes en gallego/castellano. Artefactos tremen-sdd (épicas, specs, ADRs) en español. (D-008)

## Alcance
- Dentro (MVP, `07-mvp-product-spec.md` §1): probe semanal multi-asistente; SoV ponderado por uso; análisis de fuentes citadas; lista de gaps con acciones recomendadas; registro de atribución; vista multi-clínica para agencias.
- Fuera: generación masiva de contenido, integraciones con CMS/web, publicación automática en directorios, rank tracking en Google, cualquier vertical distinta de sanidad privada, cualquier geografía distinta de Galicia (configurable, pero no se vende).

## No-negociables
- RGPD: no se almacena ningún dato personal de pacientes; la atribución son agregados.
- No se promete posicionamiento garantizado ni movimiento en días (`04-mechanics-of-llm-visibility.md` §4).
- Las definiciones de métricas (`07-mvp-product-spec.md` §4) se implementan una sola vez, con tests, y se reutilizan en UI y exportaciones.
- Coste del probe ≤ 20 € por clínica y mes (40 prompts × 3 runs × 3 proveedores, modelos de gama media).
- Las respuestas en bruto de los proveedores se guardan siempre; las llamadas son idempotentes y seguras ante reintentos.
- Pesos, ids de modelo, runs por proveedor y catálogos de prompts son configuración, no código.

## Cómo se trabaja aquí
Este proyecto sigue el estándar **tremen-sdd**: nada se implementa sin una
SPEC aprobada; las decisiones técnicas se registran como ADR inmutables; la
evidencia de verificación vive en el ledger de cada spec. Roles: /sdd-orquestador
(entrada), /sdd-producto, /sdd-arquitecto, /sdd-implementador, /sdd-verificador,
/sdd-documentalista, /sdd-como-vamos.

Documentos fundacionales previos (fuente de verdad del porqué): `README.md`,
`00-vision.md` … `08-glossary.md`, `DECISIONS.md`, `probe/`.
