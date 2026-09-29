---
id: ADR-009
tipo: adr
estado: borrador
historial:
  - {estado: borrador, fecha: 2026-09-29, por: sdd-arquitecto}
---
# ADR-009: Criterio Go del piloto: crecer en el área de influencia y defender el núcleo; supera en parte ADR-005 y ADR-008

- Deciders: el **humano (Alberto Fojo) decidió el 2026-09-29**, tras el aviso de techo del
  baseline oficial y **antes de la primera acción**, como exige SPEC-008 CA-10, que el Go del
  piloto pasa a "crecer fuera, defender dentro". sdd-producto lo recogió en EPIC-002,
  criterio de éxito 4 (commit `f40637f`). Propone este ADR sdd-arquitecto (2026-09-29). Fija
  **qué parte de ADR-005 y ADR-008 se supera, qué sigue vigente y qué se deja a
  `sdd-metricas`**. Aprueba: humano (pendiente).
- Specs relacionadas: SPEC-008 (CA-10, decisión; CA-11 y CA-12 nuevos), SPEC-012 (CA-3 y
  CA-7, veredicto), SPEC-009 (propuesta, nota), SPEC-007 (set congelado).
- **Supera en parte ADR-005 §4 y §6 y ADR-008 §6** (lo que confirma de ADR-005 §4). Los tres
  siguen `aprobada` y vigentes en lo que se enumera en la Decisión §6. Mismo patrón de
  "supera en parte" que ADR-008 respecto a ADR-003 y ADR-005.

## Contexto
ADR-005 §4 dice: "El criterio Go (EPIC-002, criterio 4; RN-03) se calcula **solo con el
núcleo**". ADR-008 §6 lo mantiene vigente. El Go era "+15 pts de SoV ponderado del núcleo
`AV` frente al baseline, en cada una de las dos mediciones 'después'" (SPEC-008 CA-9 (d)).

El baseline oficial del probe (SPEC-008 CA-7, lote de Viveiro, 2026-09-29; set congelado a
las 15:30:43Z en el commit `60863af`; todas las respuestas `ok`; modelos servidos iguales al
dictamen) dio, en veredictos frente a umbral (las cifras están solo en el espacio privado,
ADR-004 §2 y §3):
- **Núcleo `AV`**: el SoV ponderado **supera el umbral de techo de CA-10 (≥ 85 %)**.
- **Área de influencia `AR`**: presencia minoritaria de la clínica; **con margen de
  crecimiento**.
- **Galicia `AG`**: **sin presencia** de la clínica.

Saltó por tanto el **aviso de techo** de SPEC-008 CA-10. Con el núcleo a ≥ 85 %, el margen
hasta el 100 % es menor de 15 pts, así que "+15 pts en el núcleo" es **imposible por
construcción**, no difícil. CA-10 obliga al humano a decidir antes de la primera acción entre
mantener el criterio, medir sobre un subconjunto de `AV` o cambiar el umbral. El humano ha
elegido una cuarta vía: mover el crecimiento al nivel donde hay margen (`AR`) y convertir el
núcleo en condición de defensa. Eso contradice ADR-005 §4 ("solo con el núcleo"), que es un
ADR aceptado e inmutable. Por eso hace falta este ADR.

## Decisión
1. **El Go del piloto son tres condiciones, cada una sí/no, y se exige que se cumplan las
   tres** (EPIC-002, criterio 4):
   - **(C) Crecer**: la cifra del área de influencia `AR` sube frente a su "antes" con el
     umbral y la regla de estabilidad que fije `sdd-metricas` (SPEC-008 CA-11). Es la
     condición de **H1** del piloto.
   - **(D) Defender**: la cifra del núcleo `AV` (SoV ponderado, RN-03/RN-04, como hoy) **no
     cae de forma significativa** frente al del baseline oficial. El umbral de caída lo
     fija `sdd-metricas` (SPEC-008 CA-11).
   - **(A) Atribución**: ≥ 1 paciente atribuido al canal IA (RN-07; H3). Sin cambio.
2. **Los niveles siguen sin mezclarse en un mismo número.** (C) se calcula solo con filas
   `AR` y (D) solo con filas `AV`. No existe ninguna cifra que sume, promedie, pondere o
   combine `AV`, `AR` y `AG`, ni un "índice del Go". El Go es la conjunción lógica de tres
   sí/no, no una cifra. Un buen resultado en un nivel no compensa uno malo en otro.
3. **`AG` sigue siendo un indicador sin objetivo** ("aparecer alguna vez"): no entra en el
   Go, no se promete a la clínica y no aparece en la propuesta (ADR-005 §6, sin cambio).
4. **Antes de la primera acción, y nunca después de ver el efecto**, quedan fijados por
   escrito:
   - el diseño de medición de `AR` (preguntas, runs, ejecuciones "después");
   - el umbral de (C) y su regla de estabilidad;
   - el umbral de (D);
   - un **"antes" de `AR` medido con el mismo diseño** que sus mediciones "después". El
     "antes" actual (5 preguntas × 1 run) no sirve como base del Go si el diseño pide más
     runs o más preguntas: se completa antes de la primera acción (SPEC-008 CA-12).
   Si el diseño exige preguntas `AR` nuevas, se reabre la congelación del set (SPEC-007
   CA-8) **solo para añadir** ids nuevos; las 24 preguntas congeladas no cambian de texto ni
   de id.
5. **Qué cifra mide `AR`** (recuento de casillas, SoV bruto o ponderado de `AR` solo) lo
   decide `sdd-metricas` en SPEC-008 CA-11. Este ADR no la prejuzga. Sea cual sea, se calcula
   solo con `AR` y con las mismas reglas de mención (RN-01, RN-02, RN-11) que el núcleo.
6. **Qué se supera y qué sigue vigente.**
   - **Superado**: ADR-005 §4, la frase "El criterio Go (EPIC-002, criterio 4; RN-03) se
     calcula solo con el núcleo"; ADR-008 §6, en cuanto mantiene vigente esa frase ("el
     criterio Go se calcula solo con `AV`"); ADR-005 §6, la frase "El área de influencia se
     presenta, si se presenta, como algo que se mide e informa sin compromiso", solo en
     cuanto `AR` pasa a ser condición interna del Go. Cómo se cuenta eso a la clínica es
     decisión pendiente del humano en SPEC-009 (ver Consecuencias).
   - **Vigente**: ADR-005 §1 (tres niveles), §4 en todo lo demás (cada nivel se cuenta e
     informa por separado; ninguna cifra `AR` o `AG` se suma, promedia ni pondera con el
     núcleo), §5 en su parte técnica, §6 en todo lo que dice del nivel Galicia; ADR-008 en
     todo lo demás. Sin garantía de aparecer ni de número de pacientes (D-3; `04-…md` §4).
7. **Alcance.** Vale para el piloto de Clínica Ártica (EPIC-002). No fija el Go de otros
   pilotos ni el del Ciclo 2 ("2 de 3 pilotos"): eso se decide en su épica.

## Consecuencias
### Positivas
- El Go vuelve a ser alcanzable y medible. Mide lo que el baseline dice que falta: Ártica ya
  es la clínica que la IA recomienda en su comarca, y el crecimiento posible está fuera.
- (D) protege frente a un efecto perverso: que las acciones para fuera empeoren lo de dentro.
- La separación de niveles sigue siendo comprobable por el verificador con los mismos tests
  (`test_ca3_core_weighted_sov_uses_only_av`, resumen por nivel).

### Negativas / follow-ups
- **`AR` hoy tiene demasiado ruido para decidir**: 5 preguntas × 1 run × 3 proveedores
  (15 casillas pregunta × proveedor en total). Hace falta más runs, más preguntas o ambas, un "antes" nuevo y medir más a menudo
  al final del piloto. Coste extra, y posible reapertura de la congelación (SPEC-008 CA-11 y
  CA-12).
- **Retrasa la primera acción** hasta que existan el dictamen (CA-11) y el "antes" de `AR`
  con el diseño nuevo (CA-12).
- El "antes" de `AR` se medirá **después** del baseline del núcleo (días de diferencia). Se
  acepta: sigue siendo anterior a la primera acción.
- `probe/analysis.py` y `batches/viveiro.json` hablan hoy de "Go" solo en `AV` (líneas
  "Medición completa para el criterio Go", aviso de techo). Lo que haya que cambiar lo mapea
  el dictamen CA-11 a cambios concretos. `docs/fundacion/contexto.md` ("Go solo con `AV`")
  se actualiza cuando se implemente (sdd-documentalista).
- **SPEC-009**: su CA-3 pide que "cómo sabremos si funciona" use los criterios de la épica
  "referidos al núcleo" y que `AR` aparezca sin objetivo. Con este ADR el núcleo es solo
  defensa. Si la propuesta debe contar el Go nuevo a la clínica, SPEC-009 necesita enmienda y
  re-aprobación. Decisión del humano.
- SPEC-012 (CA-3, CA-7) cambia la cadencia de `AR` y la regla del veredicto.
- Con (C) el crecimiento se mide en zonas con poca demanda propia (Ferrolterra, norte e
  interior de Lugo, occidente de Asturias). Un Go de visibilidad no garantiza pacientes; (A)
  sigue siendo la condición que conecta con D-3.

## Alternativas consideradas
- **Mantener el criterio (+15 pts en el núcleo)**: rechazada. Con el núcleo por encima del
  umbral de techo, el margen hasta el 100 % es menor de 15 pts; el Go no se podría cumplir
  nunca.
- **Medir el crecimiento sobre un subconjunto de `AV`** (p. ej. Lugo o capilar, la opción
  de CA-10): rechazada por el humano. Además, elegir el subconjunto después de ver en qué
  preguntas falla la clínica sesga el Go hacia donde hay margen, y un subconjunto de `AV` es
  todavía menos preguntas que `AR`.
- **Bajar el umbral del núcleo** (p. ej. +5 pts): rechazada. La diferencia entre runs del mismo día
  ya es del orden de ese umbral (dato solo en el espacio privado) y el techo comprime la
  subida posible; un Go así mediría ruido.
- **Un índice que combine `AV` y `AR`** (media, suma o ponderado de niveles): rechazada. Es
  justo lo que ADR-005 §4 prohíbe y sigue prohibiendo: un buen núcleo escondería un `AR` sin
  movimiento, y al revés.
- **Crecer en `AG`**: rechazada. Compiten cadenas con varias sedes; es un objetivo de un año
  y no se promete (ADR-005 §6).
