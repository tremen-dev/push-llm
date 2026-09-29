---
id: ADR-005
tipo: adr
estado: aprobada
historial:
  - {estado: borrador, fecha: 2026-09-29, por: sdd-arquitecto}
  - {estado: aprobada, fecha: 2026-09-29, por: Alberto Fojo}
aprobada-por: Alberto Fojo
---
# ADR-005: Catálogo del piloto de Clínica Ártica en tres niveles geográficos

- Deciders: propone sdd-arquitecto (2026-09-29), a raíz de la decisión del humano (Alberto
  Fojo, 2026-09-29) de medir el piloto en tres niveles geográficos, ya recogida por
  sdd-producto en EPIC-002, criterio de éxito 4. Aprueba: humano (pendiente). Este ADR no
  decide *si* se mide en tres niveles (eso ya lo decidió el humano); fija **cómo encaja**
  con ADR-003 y con el alcance de FOUNDATION.
- Specs relacionadas: SPEC-007, SPEC-008, SPEC-009, SPEC-011, SPEC-012 (EPIC-002).
- **Amplía ADR-003 §1 (no lo supersede)**, con el mismo patrón que ADR-004 respecto a
  ADR-001. El resto de ADR-003 sigue vigente sin cambios.

## Contexto
ADR-003 §1 permite un único piloto con Clínica Ártica "con su propio catálogo de prompts de
estética × {Viveiro, A Mariña, Lugo}". El humano ha decidido medir también, como
indicadores **separados** que no son el criterio Go:
- **Área de influencia**: Ferrolterra (provincia de A Coruña), norte de Lugo fuera de
  A Mariña y occidente de Asturias.
- **Galicia**, solo para tratamientos por los que el paciente se desplaza (trasplante
  capilar DHI, blefaroplastia).

Dos de esas geografías quedan fuera de la lista literal de ADR-003 §1, y una (occidente de
Asturias) queda fuera del alcance geográfico de FOUNDATION ("cualquier geografía distinta
de Galicia (configurable, pero no se vende)"). Un ADR aceptado es inmutable y su lista es
un límite comprobable, así que ampliarla por interpretación sería reabrir justo el agujero
que ADR-003 cerró ("el siguiente entraría por precedente").

A la vez, medir estas preguntas **no es prospección**: el cliente es el mismo, está en
Galicia, y lo que se mide es si **a él** lo recomiendan a pacientes que vienen de fuera de
su comarca. Pero el nivel Galicia tiene un efecto lateral: sus respuestas nombrarán
clínicas de Vigo, Pontevedra, A Coruña y Santiago (cadenas de capilar y cirugía
palpebral), es decir, generarán datos sobre el mercado del nicho oficial de D-2.

## Decisión
1. **Catálogo del piloto en tres niveles.** ADR-003 §1 se amplía: el catálogo propio del
   piloto de Clínica Ártica puede tener preguntas de estética de tres niveles, cada uno
   con prefijo de id propio (los fija SPEC-007 CA-1):
   - núcleo: Viveiro y A Mariña, más las preguntas que ya nombran Lugo o Galicia junto a
     ellas en el set vigente;
   - área de influencia: Ferrolterra, norte de Lugo fuera de A Mariña y occidente de
     Asturias;
   - Galicia: sin ciudad concreta, solo líneas de tratamiento de desplazamiento que la
     clínica ofrezca según su web.
2. **Mismo cliente, misma excepción.** Todo sigue siendo el único piloto de ADR-003: las
   prohibiciones de ADR-003 §2 se extienden a las nuevas geografías (nada de prospección en
   Ferrolterra, occidente de Asturias o resto de Galicia; nada de listas de objetivos ni
   mensajes de mercado sacados de estas respuestas). La caducidad de ADR-003 §6 aplica
   igual.
3. **Asturias no es un mercado.** Medir preguntas que nombran municipios del occidente de
   Asturias está permitido solo como indicador del cliente gallego. No convierte Asturias
   en geografía del producto ni de venta: el alcance de FOUNDATION no cambia.
4. **Indicadores separados, nunca mezclados.** Cada nivel se cuenta e informa por
   separado. El criterio Go (EPIC-002, criterio 4; RN-03) se calcula **solo con el
   núcleo**. Ninguna cifra de influencia o Galicia se suma, promedia ni pondera con el
   núcleo, ni en la medición manual ni en el probe.
5. **Los datos del nivel Galicia no alimentan el nicho de D-2.** Las clínicas de Vigo y
   Pontevedra que aparezcan en respuestas del piloto se registran como competidoras del
   piloto, en el lote del piloto; no se añaden por esta vía a la lista de objetivos de
   EPIC-001 ni al lote de Vigo, y su aparición no se usa como estudio del mercado de Vigo
   (ADR-003 §3 y §5). Si una marca de Vigo entra en el catálogo de marcas para el piloto,
   lo hace de forma que **no altere** el lote de Vigo (SPEC-008 CA-4).
6. **No se promete.** El nivel Galicia no es objetivo comprometido con la clínica ni
   aparece como tal en la propuesta (SPEC-009). El área de influencia se presenta, si se
   presenta, como algo que se mide e informa sin compromiso.

## Consecuencias
### Positivas
- La ampliación queda escrita y es comprobable: el verificador puede buscar agregados que
  mezclen niveles, marcas de Vigo del piloto dentro del lote de Vigo o promesas de nivel
  Galicia en la propuesta.
- Se mide lo que la clínica probablemente quiera saber (si capta pacientes de fuera en
  tratamientos de alto valor) sin contaminar el criterio Go.

### Negativas / follow-ups
- Cada pasada manual pasa de 49 a unas 75 consultas (SPEC-007 CA-5).
- Con 3–5 preguntas por nivel regional, las cifras de esos niveles son recuentos, no
  porcentajes con significado estadístico; lo fija `sdd-metricas` (SPEC-007 CA-2).
- El probe (SPEC-008) necesita que las marcas del piloto se seleccionen por pertenencia al
  lote y no solo por ciudad, porque habrá marcas del piloto con ciudad Vigo o Pontevedra.
- Coste del probe: más preguntas por lote; debe seguir cabiendo en ≤ 20 € por clínica y
  mes (SPEC-008 CA-5).
- SPEC-011 y SPEC-012 (borradores) deben informar por nivel y dejar el Go solo en el
  núcleo.

## Alternativas consideradas
- **Considerarlo cubierto por ADR-003 sin escribir nada**: rechazada. ADR-003 §1 enumera
  {Viveiro, A Mariña, Lugo}; ampliar una lista de un ADR aceptado por lectura amplia es lo
  que ADR-003 quería evitar, y el occidente de Asturias toca además el alcance de
  FOUNDATION.
- **Superseder ADR-003 con un ADR completo nuevo**: rechazada; solo cambia §1 y se añaden
  límites. Reescribir el resto no aporta y obliga a revalidar decisiones que no cambian.
- **Medir los niveles regionales en una pasada aparte**: rechazada por el humano (una sola
  pasada con el set ampliado); además duplicaría condiciones y desviaciones.
- **Meter las preguntas regionales en el núcleo**: rechazada; diluiría el criterio Go con
  preguntas donde el objetivo es "aparecer alguna vez", no +15 pts.
