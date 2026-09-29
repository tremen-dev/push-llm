---
id: EPIC-FIX
tipo: epica
estado: borrador
historial:
  - {estado: borrador, fecha: 2026-09-29, por: sdd-arquitecto}
---
# EPIC-FIX — Fixes

> Épica bucket, creada por sdd-arquitecto el 2026-09-29 a encargo del orquestador para
> alojar SPEC-013 (bug F-SPEC-002-7). No es una épica de producto: no tiene objetivo de
> negocio propio ni roadmap. sdd-producto puede reescribirla o reubicar sus specs.

## Objetivo
Alojar arreglos pequeños de defectos en herramientas ya entregadas (hoy, el probe) que no
pertenecen al alcance de ninguna épica de producto abierta, o cuya épica de origen está
cerrada o bloqueada. Cada fix es una spec normal (CA, TDD, verificador, gate humano).

## Criterios de éxito
1. Cada spec de esta épica corrige un defecto con evidencia (reproducción o respuesta
   grabada) y con un test que falla antes y pasa después.
2. Ningún fix cambia una métrica, un catálogo ni el modo de sondeo sin el dictamen de dominio
   y la aprobación humana que ya exigiría una spec de producto.

## Alcance
- Dentro: defectos del probe (`probe/`) y de sus herramientas auxiliares.
- Fuera (aparcado a propósito, no por descuido): funcionalidad nueva, cambios de modelo o de
  método de sondeo (van a su épica y a un dictamen de sdd-probe), cambios de métricas.

## Specs
<!-- El estado por spec vive en el frontmatter de cada spec; el tablero agregado se regenera con /sdd-tablero (docs/tablero.md). No mantengas listas de specs a mano aquí. -->

## Riesgos
- Que la épica bucket se use para colar funcionalidad nueva sin pasar por sdd-producto.
  Mitigación: el criterio 2 y el gate humano de cada spec.
