---
id: ADR-003
tipo: adr
estado: borrador
historial:
  - {estado: borrador, fecha: 2026-09-28, por: sdd-arquitecto}
---
# ADR-003: Piloto de Clínica Ártica en Viveiro como excepción acotada a D-2

- Deciders: propone sdd-arquitecto (2026-09-28, desglose de EPIC-002, a petición de
  sdd-producto en el apartado Riesgos de la épica). Aprueba: humano (pendiente). El humano
  ya decidió el 2026-09-28 hacer el piloto; este ADR solo fija **cómo encaja** con D-2.
- Specs relacionadas: SPEC-007, SPEC-008, SPEC-009, SPEC-010, SPEC-011, SPEC-012 (EPIC-002).

## Contexto
D-2 (FOUNDATION, locked; origen DECISIONS.md D-002) fija: "clínicas sanitarias privadas,
**Vigo y Pontevedra primero** […] estética = segundo mercado". Su consecuencia escrita es
que "los catálogos de prompts, las fuentes y las listas de marcas se construyen por
especialidad × ciudad".

EPIC-002 propone un piloto concierge de pago con Clínica Ártica (medicina estética, sede
única en Viveiro, Lugo). Choca con D-2 en dos ejes: **geografía** (A Mariña lucense, no
Vigo/Pontevedra) y **especialidad** (estética antes que dental, que es el nicho de
volumen). No choca con el alcance de FOUNDATION (Galicia, sanidad privada).

D-2 no solo está en FOUNDATION: está **cableado** en el probe. `probe/probe_config.json`
fija `user_location.city = "Vigo"` y `probe/matching.py` fija
`LOCAL_CITIES = {"Vigo", "Pontevedra"}`. Medir Viveiro con el probe tal cual daría
respuestas localizadas en Vigo y no contaría como "clínica local" a ninguna clínica de
A Mariña.

Hay dos lecturas posibles de "primero":
1. **Orden de salida comercial**: dónde se construye la lista de objetivos, el catálogo de
   prompts y el mensaje de mercado. Un cliente que llega solo, cálido y dispuesto a pagar
   no altera ese orden.
2. **Restricción de alcance**: no se trabaja fuera de Vigo/Pontevedra hasta haber
   validado allí.

La lectura 1 es la más plausible, pero es una interpretación de una decisión locked, y
FOUNDATION dice que solo un ADR aceptado puede reinterpretarla. Además, el piloto obliga a
cambiar código y configuración que encarnan D-2 (arriba). Por eso no basta con "argumentar
que D-2 no lo impide": hay que dejar escrito el límite.

## Decisión
Se registra el piloto como **excepción de aprendizaje acotada**, no como cambio de nicho.
D-2 no se deroga ni se reinterpreta en general.

1. **Qué se permite**: un único piloto concierge de pago con Clínica Ártica (EPIC-002),
   con su propio catálogo de prompts de estética × {Viveiro, A Mariña, Lugo} y su propia
   lista de competidores, medido a mano y, cuando haya claves, con el probe.
2. **Qué no se permite al amparo de este ADR**: prospección comercial en A Mariña o Lugo;
   añadir clínicas de Lugo a la lista de objetivos de EPIC-001/Ciclo 1; un segundo cliente
   fuera de Vigo/Pontevedra; mensajes de mercado ("trabajamos en Lugo"). Cualquiera de
   ellos requiere otro ADR.
3. **Separación de la medición**: los datos del piloto no se mezclan con los agregados de
   Vigo/Pontevedra. El catálogo de Viveiro se ejecuta como lote aparte (configuración y
   directorio de salida propios) y sus agregados se informan aparte. El veredicto de
   EPIC-001 (SPEC-002) no cambia por este ADR.
4. **Multi-ciudad como configuración, no como código**: el soporte que el probe necesita
   para otra ciudad (ubicación del usuario y conjunto de ciudades "locales") pasa a
   configuración por lote (SPEC-008), con los valores actuales (Vigo; Vigo+Pontevedra)
   como defecto. Es coherente con el No-negociable "catálogos de prompts son configuración"
   y con la consecuencia de D-2 (catálogos por especialidad × ciudad).
5. **Qué se transfiere y qué no**: el aprendizaje sobre H1 (¿se mueve la respuesta?) y H3
   (¿se atribuyen pacientes?) se considera transferible al nicho oficial. El aprendizaje de
   mercado (fuentes dominantes, competidores, volumen de búsquedas) se trata como **propio
   de Viveiro** y no se extrapola a Vigo sin medirlo allí. El cierre del piloto (SPEC-012)
   lo dice explícitamente.
6. **Caducidad**: la excepción vence al cerrar EPIC-002 (renovación incluida, si la
   hubiera, se reevalúa entonces con otro ADR o ampliando este mediante uno que lo
   supersede).

## Consecuencias
### Positivas
- Se aprovecha una oportunidad real de probar H1 y H3 (y H2 si paga) sin reescribir la
  estrategia de nicho.
- El límite es comprobable: el verificador puede buscar objetivos de Lugo en la lista de
  EPIC-001, prompts de Viveiro mezclados en el lote de Vigo o agregados conjuntos.
- El probe gana multi-ciudad por configuración, algo que el Ciclo 3 necesitará igualmente.

### Negativas / follow-ups
- El Criterio Go de Ciclo 2 del plan lean ("2 de 3 pilotos") no se puede evaluar con un
  solo piloto: EPIC-002 da evidencia de un caso, no el Go del ciclo. Lo dice SPEC-012.
- Mercado pequeño: bajo volumen de búsquedas y de pacientes, "≥ 1 paciente atribuido"
  puede depender del azar (riesgo ya escrito en la épica).
- Tiempo del fundador fuera del nicho principal mientras EPIC-001 sigue abierta.
- Cambio de código en `probe/` (SPEC-008): debe mantener los tests existentes en verde y
  el comportamiento por defecto idéntico para el lote de Vigo.

## Alternativas consideradas
- **Argumentar que "primero" no lo impide, sin ADR**: rechazada. Es una reinterpretación de
  una decisión locked (FOUNDATION exige ADR) y además hay que tocar código y configuración
  que encarnan D-2; sin límite escrito, el siguiente cliente de fuera entraría "por
  precedente".
- **Ampliar el nicho oficial a Lugo / A Mariña**: rechazada; la épica lo excluye y no hay
  evidencia de mercado que lo justifique (un cliente cálido no es un mercado).
- **Rechazar el piloto por estar fuera de D-2**: rechazada; H1 y H3 son las hipótesis que
  pueden matar la idea y un cliente dispuesto a pagar es la evidencia que busca el Ciclo 2
  (`05-lean-plan.md` §1).
- **Mezclar el catálogo de Viveiro en el catálogo general de estética**: rechazada; ensucia
  el veredicto de EPIC-001 y el agregado por especialidad de `summary.md`.

<!-- REGLA: un ADR aceptado es INMUTABLE. Para cambiar la decisión, escribe otro ADR que lo supersede (estado del viejo -> bloqueada + nota "superseded por ADR-NNN"). -->
