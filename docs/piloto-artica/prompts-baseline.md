# Set de preguntas del baseline — piloto Clínica Ártica (SPEC-007 CA-1)

> Preguntas de paciente sobre medicina estética, comunes a los dos instrumentos del piloto.
> **El probe mide `AV`, `AR` y `AG`** (SPEC-008) y es el instrumento del criterio Go.
> **La medición a mano calibra `AR` en ChatGPT, Gemini y Google, y `AV` y `AM` en ChatGPT y
> Gemini**: es la calibración de SPEC-007, desde el móvil (en Google, el resumen de IA;
> `AV` y `AM` nunca en Google). **`AG` solo lo mide el probe.** Hay **tres niveles
> geográficos** (ADR-005), cada uno medido e informado por separado:
>
> - **Núcleo `AV`** — Viveiro y A Mariña (más las preguntas del set que nombran también
>   Lugo o Galicia junto a ellas). **Es el único nivel que cuenta para el criterio Go.**
> - **Área de influencia `AR`** — pacientes de fuera de la comarca: Ferrolterra, norte de
>   Lugo fuera de A Mariña (Vilalba), interior de Lugo (Sarria y A Fonsagrada, al sur y al
>   este, no al norte) y occidente de Asturias. Indicador aparte.
> - **Galicia `AG`** — solo tratamientos por los que el paciente se desplaza (trasplante
>   capilar DHI y blefaroplastia), sin nombrar ciudad. Indicador aparte, sin objetivo.
>
> Se preguntan **con el texto literal**, una por conversación nueva y **en este orden**
> (ver `protocolo-captura.md`). Los ids se reutilizan en el probe (SPEC-008 CA-1).
>
> - **Línea**: `facial`, `corporal`, `capilar` (incluye trasplante DHI),
>   `cirugia_facial` (cirugía menor facial) o `general` (medicina estética sin tratamiento
>   concreto). Son las cuatro líneas de clinicaartica.es más la genérica.
> - **Intent**: vocabulario de `docs/fundacion/dominio.md` (discovery, price, comparison,
>   urgent, trust, specific).
> - **Ámbito**: lugar que nombra la pregunta. Ninguna depende de "cerca de mí": todas
>   nombran un lugar, para que la ubicación del móvil pese lo menos posible.
> - Ninguna pregunta de medición nombra a la clínica ni a un competidor.

## Estado del set

- Publicado: 2026-09-29 (`AV`, `AM`); niveles `AR` y `AG` añadidos el 2026-09-29 tras la
  enmienda de SPEC-007 (ADR-005). `AV01`–`AV15` no cambian.
- **Congelación** (SPEC-007 CA-8): los tres niveles (`AV`, `AR`, `AG`) quedan congelados,
  como tarde, cuando empieza la primera ejecución del **baseline oficial del probe**
  (SPEC-008 CA-7), o antes, en la fecha que fije el humano en el ledger de SPEC-007. La
  fecha se anota en ese ledger. Desde ese momento no se cambia ni una coma; una pregunta
  nueva lleva un id nuevo, se informa aparte y no cuenta para el criterio Go. `AR` y `AG`
  nunca cuentan para el criterio Go. La pasada "antes" a mano no empieza sin congelación.

## Preguntas de medición (cuentan para el SoV)

| id | pregunta | línea | intent | ámbito | idioma |
|---|---|---|---|---|---|
| AV01 | ¿Cuál es la mejor clínica de medicina estética en Viveiro? | general | discovery | Viveiro | es |
| AV02 | Recomiéndame una clínica de medicina estética en A Mariña lucense. | general | discovery | A Mariña | es |
| AV03 | ¿Merece la pena ir a Lugo o a A Coruña para hacerme tratamientos de medicina estética, o hay buenas clínicas en A Mariña? | general | comparison | Lugo; A Coruña; A Mariña | es |
| AV04 | ¿Dónde me pongo bótox en Viveiro con un médico de confianza? | facial | specific | Viveiro | es |
| AV05 | ¿Cuánto cuesta el ácido hialurónico en labios en Viveiro y dónde me lo hago? | facial | price | Viveiro | es |
| AV06 | Quiero quitarme las manchas de la cara con láser en Burela o en Foz. ¿Qué clínica me recomiendas? | facial | specific | Burela; Foz | es |
| AV07 | Tengo grasa localizada y flacidez en el abdomen. ¿Qué clínica de Viveiro me lo puede tratar sin cirugía? | corporal | specific | Viveiro | es |
| AV08 | ¿Cuánto cuesta un tratamiento médico para la celulitis en A Mariña y qué clínica me recomiendas? | corporal | price | A Mariña | es |
| AV09 | ¿Dónde puedo hacerme un trasplante capilar en la provincia de Lugo? | capilar | discovery | provincia de Lugo | es |
| AV10 | ¿Cuánto cuesta un injerto capilar con técnica DHI en Galicia y qué clínica me recomiendas cerca de Viveiro? | capilar | price | Galicia; Viveiro | es |
| AV11 | ¿Es mejor hacerme el injerto capilar en Turquía o en una clínica de Lugo? | capilar | comparison | Lugo | es |
| AV12 | ¿Dónde me puedo operar los párpados caídos (blefaroplastia) en Viveiro o en Lugo? | cirugia_facial | specific | Viveiro; Lugo | es |
| AV13 | ¿Qué clínica de medicina estética de Viveiro tiene médicos titulados y buenas opiniones? | general | trust | Viveiro | es |
| AV14 | Cal é a mellor clínica de medicina estética en Viveiro? | general | discovery | Viveiro | gl |
| AV15 | Onde me podo facer un transplante capilar preto de Viveiro? | capilar | discovery | Viveiro | gl |

Cobertura: 15 preguntas; líneas facial 3, corporal 2, capilar 4, cirugia_facial 1, general 5; intents discovery 5, price 3, comparison 2, trust 1, specific 4; 9 nombran Viveiro, 4 nombran A Mariña, Burela, Foz o Ribadeo, 4 nombran Lugo; 2 en gallego.

## Área de influencia — AR (indicador aparte, no cuenta para el criterio Go)

Pacientes de fuera de la comarca, preguntando desde su lugar y abiertos a desplazarse.
Mondoñedo no está aquí: es A Mariña (núcleo), y el núcleo no se toca.

| id | pregunta | línea | intent | ámbito | idioma |
|---|---|---|---|---|---|
| AR01 | Vivo en Ferrol. Que clínica de medicina estética con médicos me recomendas pola zona, aínda que teña que desprazarme un pouco? | general | discovery | Ferrol (Ferrolterra) | gl |
| AR02 | Vivo entre Narón y Ortigueira. ¿Dónde me pongo bótox con un médico de confianza por la zona, aunque tenga que desplazarme un poco? | facial | specific | Narón; Ortigueira (Ferrolterra) | es |
| AR03 | Vivo en Vilalba. ¿Qué clínica con médicos titulados y buenas opiniones me recomiendas para ponerme ácido hialurónico, aunque tenga que desplazarme? | facial | trust | Vilalba (Terra Chá, norte de Lugo) | es |
| AR04 | Vivo entre Sarria y A Fonsagrada. ¿Cuánto cuesta un injerto capilar y qué clínica me recomiendas, aunque tenga que desplazarme? | capilar | price | Sarria; A Fonsagrada (interior de Lugo) | es |
| AR05 | Vivo en Tapia de Casariego (Asturias). ¿Qué clínica de medicina estética me recomiendas cerca, aunque tenga que desplazarme un poco? | general | discovery | Tapia de Casariego (occidente de Asturias) | es |

Cobertura AR: 5 preguntas; 2 nombran Ferrolterra, 1 el norte de Lugo fuera de A Mariña, 1 el interior de Lugo, 1 el occidente de Asturias; 0 nombran Viveiro o A Mariña; 5 desde el lugar del paciente con apertura a desplazarse; líneas capilar, facial, general; intents discovery, price, specific, trust; 1 en gallego.

## Galicia — AG (indicador aparte, no cuenta para el criterio Go)

Solo tratamientos que la clínica ofrece según su web (URL y fecha en el ledger) y por los
que el paciente se desplaza. Sin ciudad ni comarca. No es un objetivo ni una promesa.

| id | pregunta | línea | intent | ámbito | idioma |
|---|---|---|---|---|---|
| AG01 | ¿Cuál es la mejor clínica de Galicia para hacerme un injerto capilar con técnica DHI? | capilar | discovery | Galicia | es |
| AG02 | ¿Cuánto cuesta un trasplante capilar con técnica DHI en Galicia y dónde me recomiendas hacerlo? | capilar | price | Galicia | es |
| AG03 | ¿Dónde me recomiendas operarme los párpados superiores caídos (blefaroplastia) en Galicia? | cirugia_facial | discovery | Galicia | es |
| AG04 | Cal é a mellor clínica de Galicia para operarme as pálpebras superiores caídas (blefaroplastia)? | cirugia_facial | discovery | Galicia | gl |

Cobertura AG: 4 preguntas; líneas capilar 2, cirugia_facial 2; intents discovery 3, price 1; 1 en gallego; ninguna nombra ciudad ni comarca.

## Preguntas de marca (no cuentan para el SoV)

Solo en ChatGPT y Gemini, **nunca en Google** (regla anti-contaminación del protocolo).
Sirven para ver qué dice cada asistente de la clínica cuando se le pregunta por ella.

| id | pregunta | idioma |
|---|---|---|
| AM01 | ¿Qué sabes de Clínica Ártica de Viveiro? ¿Es de fiar? | es |
| AM02 | ¿Qué tratamientos ofrece Clínica Ártica en Viveiro, dónde está y cuánto cuestan? | es |
