# Set de preguntas del baseline — piloto Clínica Ártica (SPEC-007 CA-1)

> Preguntas de paciente para medir, desde el móvil, qué recomiendan ChatGPT, Gemini y el
> resumen de IA de Google sobre medicina estética en Viveiro, A Mariña y Lugo.
> Se preguntan **con el texto literal**, una por conversación nueva y **en este orden**
> (ver `protocolo-captura.md`). Los ids `AV` se reutilizan en el probe (SPEC-008 CA-1).
>
> - **Línea**: `facial`, `corporal`, `capilar` (incluye trasplante DHI),
>   `cirugia_facial` (cirugía menor facial) o `general` (medicina estética sin tratamiento
>   concreto). Son las cuatro líneas de clinicaartica.es más la genérica.
> - **Intent**: vocabulario de `docs/fundacion/dominio.md` (discovery, price, comparison,
>   urgent, trust, specific).
> - **Ámbito**: lugar que nombra la pregunta. Ninguna depende de "cerca de mí": todas
>   nombran un lugar, para que la ubicación del móvil pese lo menos posible.
> - Ninguna pregunta `AV` nombra a la clínica ni a un competidor.

## Estado del set

- Publicado: 2026-09-29.
- **Congelación** (SPEC-007 CA-8): el set `AV` queda congelado en la fecha de inicio de la
  pasada 1, que se anota en el ledger de SPEC-007. Desde ese momento no se cambia ni una
  coma; una pregunta nueva lleva un id nuevo, se informa aparte y no cuenta para el
  criterio Go.

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

## Preguntas de marca (no cuentan para el SoV)

Solo en ChatGPT y Gemini, **nunca en Google** (regla anti-contaminación del protocolo).
Sirven para ver qué dice cada asistente de la clínica cuando se le pregunta por ella.

| id | pregunta | idioma |
|---|---|---|
| AM01 | ¿Qué sabes de Clínica Ártica de Viveiro? ¿Es de fiar? | es |
| AM02 | ¿Qué tratamientos ofrece Clínica Ártica en Viveiro, dónde está y cuánto cuestan? | es |
