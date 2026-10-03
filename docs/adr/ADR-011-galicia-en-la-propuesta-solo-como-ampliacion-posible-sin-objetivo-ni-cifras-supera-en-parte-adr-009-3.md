---
id: ADR-011
tipo: adr
estado: aprobada
historial:
  - {estado: borrador, fecha: 2026-10-03, por: sdd-arquitecto}
  - {estado: aprobada, fecha: 2026-10-03, por: Alberto Fojo}
aprobada-por: Alberto Fojo
---
# ADR-011: Galicia en la propuesta solo como ampliación posible, sin objetivo ni cifras; supera en parte ADR-009 §3

- Deciders: el **humano (Alberto Fojo) decidió el 2026-10-03**, al revisar el PDF borrador
  de la propuesta de SPEC-009 y antes del envío, que la frase del objetivo diga que el área
  de influencia "puede ampliarse al resto de Galicia". Propone este ADR sdd-arquitecto
  (2026-10-03), que fija **qué parte de ADR-009 §3 se supera, qué sigue vigente de ADR-005
  §6 y el único uso permitido de la palabra "Galicia" en la propuesta**. Aprueba: humano
  (Alberto Fojo), 2026-10-03.
- Specs relacionadas: SPEC-009 (CA-3 y CA-10, enmienda (e)), SPEC-008 y SPEC-012 (nivel `AG`
  sin cambio), SPEC-007 (set congelado, sin cambio).
- **Supera en parte ADR-009 §3**: solo la frase "no aparece en la propuesta". **ADR-005 §6
  sigue vigente entero**: Galicia "no es objetivo comprometido con la clínica ni aparece
  como tal en la propuesta". ADR-009 sigue `aprobada` y vigente en todo lo demás (Go de tres
  condiciones; `AG` indicador sin objetivo, fuera del Go, sin promesa).

## Contexto
ADR-005 §6 dice que el nivel Galicia no es objetivo comprometido ni aparece **como tal** en
la propuesta. SPEC-009 (enmienda de 2026-09-29) lo endureció a "no aparece en absoluto",
como "test simple y a prueba de despistes" (búsqueda de "Galicia" en `propuesta.md` sin
coincidencias), y ADR-009 §3 recogió esa lectura literal: "no aparece en la propuesta
(ADR-005 §6, sin cambio)". Su nota de gate ya avisaba: "si quieres poder decir 'pacientes de
toda Galicia para capilar' aunque sea sin compromiso, hay que relajar CA-3".

El humano ha querido exactamente eso, acotado: la propuesta describe el área de influencia
(Ferrolterra, norte e interior de Lugo y occidente de Asturias) y añade que hay **margen para
ampliarla al resto de Galicia**. No es un objetivo medido (el Go sigue siendo crecer en `AR`
y defender `AV`, ADR-009 §1), no lleva cifras ni garantía, y no cambia el catálogo ni la
congelación del set (SPEC-007 CA-8). Como ADR-009 es un ADR aceptado e inmutable y su §3 lo
prohíbe literalmente, hace falta este ADR; una nota al margen reabriría la inmutabilidad.

## Decisión
1. **Una sola mención, con una sola forma.** En `docs/piloto-artica/reunion/propuesta.md`
   la palabra "Galicia" puede aparecer **una vez**, dentro de la sección "Punto de partida y
   objetivo", en la frase de ampliación: **"con margen para ampliarla al resto de Galicia"**
   (o una variante que SPEC-009 CA-3 fije como literal comprobable), inmediatamente después
   de las tres zonas del área de influencia. Nada más: ni en "cómo sabremos si funciona", ni
   en "qué esperar", ni en "qué incluye", ni en el precio.
2. **Es ampliación posible, no objetivo.** El objetivo medido sigue siendo el área de
   influencia (`AR`), con "no se garantiza" al lado (ADR-009; SPEC-009 CA-3). Galicia no es
   entregable, no es condición de "cómo sabremos si funciona" y no se promete: ninguna
   frase de la propuesta puede unir "Galicia" a aparecer, salir, conseguir o llegar en
   sentido afirmativo (regla ya vigente de SPEC-009 CA-10).
3. **Sin cifras.** Ninguna cifra, porcentaje ni "puntos" junto a Galicia (ADR-004 §2–§3;
   SPEC-009 CA-3). El nivel `AG` se sigue midiendo e informando aparte, como "aparecer
   alguna vez", y no entra en el Go (ADR-005 §4 y §6, ADR-009 §2–§3, sin cambio).
4. **Alcance.** Vale para la propuesta de SPEC-009 (y su copia privada rellenada). El guion
   (CA-1) sigue diciendo el objetivo de `AR` sin obligación de nombrar Galicia; `apoyo.md` ya
   trata "¿y saldremos cuando alguien de Coruña o Vigo busque un injerto capilar?" con "no
   te lo prometo" (CA-5, sin cambio). Qué se informa a la clínica de `AG` durante el piloto
   lo fija SPEC-012, no esta decisión.
5. **Qué se supera y qué sigue vigente.** Superado: ADR-009 §3, la frase "no aparece en la
   propuesta". Vigente: ADR-009 §3 en lo demás (`AG` indicador sin objetivo, no entra en el
   Go, no se promete); ADR-005 §6 entero; ADR-005 §2 (nada de prospección en el resto de
   Galicia a partir de este piloto).

## Consecuencias
### Positivas
- La propuesta dice a la clínica lo que el humano quiere que sepa (que su alcance no termina
  en el área de influencia) sin convertirlo en promesa ni en objetivo.
- La regla sigue siendo comprobable por script: "Galicia" exactamente una vez, en una frase
  literal, en la sección del objetivo.

### Negativas / follow-ups
- El test "sin Galicia" pierde su simplicidad: `test_ca3_no_galicia_no_percent_no_points` y
  la regla `"menciona Galicia"` de `proposal_issues` en `docs/piloto-artica/tools/meeting_docs.py`
  pasan a comprobar "una vez, en la frase de ampliación, en la sección del objetivo"
  (SPEC-009 enmienda (e); lo aplica sdd-implementador). `GALICIA_PROMISE_RE` de `ca10_issues`
  no cambia: la frase de ampliación no debe dispararlo, y si la redacción final lo dispara,
  se cambia la redacción, no el detector.
- Una clínica que lee "resto de Galicia" puede preguntar por Coruña, Santiago o Vigo: la
  respuesta está en `apoyo.md` (cadenas con varias sedes, no se promete).
- Riesgo de deriva: la frase no autoriza acciones dirigidas a Galicia durante el piloto; las
  acciones las fija SPEC-011 sobre `AR` y `AV`.
- SPEC-009 necesita enmienda y re-aprobación (enmienda (e), CA-3 y CA-10).

## Alternativas consideradas
- **Mantener "Galicia no aparece" y decirlo solo de palabra en la reunión**: rechazada por el
  humano; quiere que conste en la propuesta.
- **Nota al margen en ADR-009 §3**: rechazada; un ADR aceptado es inmutable y la única
  excepción admitida son erratas que no cambian la decisión (ADR-009, "Erratas"). Esto
  cambia la decisión.
- **Permitir "Galicia" en cualquier sitio de la propuesta mientras no sea promesa**:
  rechazada; el detector de promesas (`GALICIA_PROMISE_RE`) es heurístico y una mención en
  "qué esperar" o en "cómo sabremos" se leería como objetivo. Una sola frase literal es
  comprobable sin ambigüedad.
- **Convertir Galicia en cuarto objetivo o en condición del Go**: rechazada; ADR-009 ya la
  rechazó ("Crecer en `AG`": cadenas con varias sedes, objetivo de un año) y no hay "antes"
  de `AG` con diseño de Go.

<!-- REGLA: un ADR aceptado es INMUTABLE. Para cambiar la decisión, escribe otro ADR que lo supersede (estado del viejo -> bloqueada + nota "superseded por ADR-NNN"). -->
