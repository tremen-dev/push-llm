---
id: ADR-010
tipo: adr
estado: aprobada
historial:
  - {estado: borrador, fecha: 2026-10-03, por: sdd-arquitecto}
  - {estado: aprobada, fecha: 2026-10-03, por: Alberto Fojo}
aprobada-por: Alberto Fojo
---
# ADR-010: Modelo de pago del piloto: 450 € prepago los 3 primeros meses y 199 €/mes sin permanencia a partir del cuarto; supera en parte D-7

- Deciders: el **humano (Alberto Fojo) decidió el 2026-10-03**, al revisar el PDF borrador
  de la propuesta de SPEC-009 y **antes del envío** a la clínica, que la opción "199 €/mes
  desde el inicio" desaparece y que el pago es 450 € + IVA por los 3 primeros meses, por
  adelantado, y después 199 €/mes + IVA sin permanencia. Propone este ADR sdd-arquitecto
  (2026-10-03), que fija **qué parte de D-7 se supera y qué sigue vigente**, y registra la
  decisión donde SPEC-009 CA-3 exige que viva toda desviación de D-7 (ledger de SPEC-009,
  además de aquí). Aprueba: humano (Alberto Fojo), 2026-10-03. Matiz a confirmar en el gate: el alcance
  (§4) propone que el modelo nuevo sea el **ancla de pilotos** que sustituye a la fórmula de
  D-7, no solo el precio de la propuesta a Clínica Ártica; si el humano lo quiere acotado al
  piloto, se deja D-7 vigente para pilotos futuros y este ADR vale solo para EPIC-002.
- Specs relacionadas: SPEC-009 (CA-3 precio, CA-9 respuesta; enmienda (e)), EPIC-002
  (criterio de éxito 2, "propuesta anclada en D-7"), SPEC-004 (ancla de D-7 en el cierre,
  bloqueada), SPEC-012 (cierre: "renovar o no").
- **Supera en parte D-7** (FOUNDATION; origen DECISIONS.md D-007): la fórmula de precio.
  Siguen vigentes "nunca gratis más allá del informe de una página" y "pendiente de validar"
  (esta propuesta es su primera validación real). Mismo patrón que ADR-008 respecto a D-2.
  Registro fundacional: DECISIONS.md D-010.

## Contexto
D-7 (2026-09-23) fija el ancla de precio de pilotos como "3 meses a 450 € prepago **o**
199 €/mes", dos opciones que el cliente elige desde el inicio. SPEC-009 CA-3 exige el
"precio exacto de D-7 en sus dos opciones" y su CA-9 registra la respuesta como "acepta
prepago / acepta mensual / negocia / rechaza". La propuesta borrador (ledger de SPEC-009,
2026-09-30) las imprime como tabla de dos filas ("3 meses, pago por adelantado: 450 € + IVA"
y "Pago mensual, 3 meses: 199 €/mes + IVA") y deja abierto, en F-SPEC-009-2 punto 3, si en la
mensual se puede dejar antes de los 3 meses.

Al revisar el PDF, el humano decidió que la opción mensual desde el inicio no existe: el
piloto se paga por adelantado (compromiso de 3 meses, que es lo que la medición necesita,
RN-07 y SPEC-012) y la continuidad después es mensual sin permanencia. Eso cierra la pregunta
3 de F-SPEC-009-2 y simplifica la propuesta (una sola cifra de entrada). FOUNDATION dice que
una decisión locked solo la reinterpreta o supera un ADR aceptado; por eso hace falta este.

## Decisión
1. **Precio del piloto (EPIC-002, propuesta de SPEC-009)**: **450 € + IVA por los 3 primeros
   meses, pagados por adelantado**. El piloto empieza con los acuerdos aceptados y ese pago
   (SPEC-009 CA-9, sin cambio).
2. **Continuidad**: **a partir del cuarto mes, 199 €/mes + IVA**, y la clínica **puede dejarlo
   en cualquier momento**: sin permanencia. No hay opción mensual durante los 3 primeros
   meses.
3. **Lo que no cambia de D-7**: nunca gratis más allá del informe de una página; sin
   descuentos ni paquetes con otros servicios (SPEC-009 CA-3, "no hay opción gratuita ni
   descuento"); el IVA se dice explícito junto a cada importe ("+ IVA"), sin cifrar el tipo.
4. **Alcance (propuesta del arquitecto, a confirmar por el humano)**: este modelo pasa a ser
   el **ancla de pilotos** en lugar de la fórmula de D-7 ("450 € prepago o 199 €/mes"). Sigue
   "pendiente de validar": la aceptación o no de Clínica Ártica a este precio es la hipótesis
   H2 de EPIC-002 (criterio de éxito 2), y lo que se aprenda se registra en el cierre
   (SPEC-012). Si el humano acota el alcance a EPIC-002, D-7 sigue vigente para pilotos
   futuros y aquí solo se supera para este.
5. **Cómo se cuenta a la clínica** (lo fija SPEC-009 CA-3, enmienda (e)): en la propuesta
   el cliente lee las dos frases de §1 y §2 en lenguaje llano, sin la frase "Precios sin
   IVA: la factura suma el IVA vigente" (redundante con "+ IVA"), y "sin permanencia"
   aparece junto al precio y en "Al terminar".

## Consecuencias
### Positivas
- Una sola cifra de entrada: la propuesta pierde la tabla de dos opciones y gana espacio
  (la propuesta está en el límite de 450 palabras).
- Cierra F-SPEC-009-2 punto 3 sin inventar nada: la pregunta "¿se puede dejar antes de los
  3 meses?" deja de existir porque los 3 primeros meses se pagan por adelantado.
- La respuesta de CA-9 se simplifica a "acepta / negocia / rechaza".
- El compromiso de 3 meses coincide con la duración mínima que la medición necesita
  (movimiento en 4–12 semanas; SPEC-012).

### Negativas / follow-ups
- Sin opción mensual de entrada, el "no" de la clínica puede ser por el prepago y no por el
  precio; H2 se valida con menos matiz. Si la clínica negocia la forma de pago, el humano lo
  registra en el ledger de SPEC-009 como decisión (CA-3) y, si cambia el modelo, otro ADR.
- SPEC-009 necesita enmienda y re-aprobación (enmienda (e)): CA-3 (texto del precio), CA-9
  (respuesta). El comprobador `docs/piloto-artica/tools/meeting_docs.py` (`proposal_issues`,
  que exige "450 € + iva" y "199 €/mes + iva" sin saber en qué frase) y el test
  `test_ca3_prices_equal_d7` de `docs/piloto-artica/tools/tests/test_meeting_kit.py` deben
  comprobar el modelo nuevo (lo aplica sdd-implementador).
- `apoyo.md` ("¿Cuánto cuesta?") y el README del kit ("precio de D-7") deben decir el modelo
  nuevo. EPIC-002 nombra D-7 en premisas y criterio 2: sdd-producto lo anota al cerrar la
  épica; no hace falta reabrirla.
- FOUNDATION.md D-7 lleva una nota "superada en parte por ADR-010" cuando este ADR se apruebe
  (como D-2 con ADR-008); DECISIONS.md recoge D-010.

## Alternativas consideradas
- **Mantener las dos opciones de D-7**: rechazada por el humano (2026-10-03). Una opción
  mensual de entrada invita a dejarlo antes de que haya nada que medir y duplica preguntas
  (F-SPEC-009-2 punto 3).
- **Solo 450 € por 3 meses, sin continuidad definida**: rechazada; la clínica preguntaría qué
  pasa al terminar y SPEC-009 CA-3 exige decirlo ("renovar o no, sin permanencia").
- **Continuidad con permanencia (p. ej. trimestres)**: rechazada; contradice "sin
  permanencia" de SPEC-009 CA-3 y el tono de cliente cálido de EPIC-002.
- **Registrarlo solo en el ledger de SPEC-009 sin ADR**: rechazada; el ledger es donde CA-3
  pide registrar la desviación, pero D-7 es una decisión locked de FOUNDATION y solo un ADR
  aceptado puede superarla.

<!-- REGLA: un ADR aceptado es INMUTABLE. Para cambiar la decisión, escribe otro ADR que lo supersede (estado del viejo -> bloqueada + nota "superseded por ADR-NNN"). -->
