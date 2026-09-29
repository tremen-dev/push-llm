# Resumen del probe Vigo/Pontevedra

Recalculado offline desde results.csv con el brands.csv actual. Solo cuentan las respuestas con status=ok; las demás se listan como excluidas (SPEC-001 CA-4).

## Cobertura por especialidad × proveedor

| Especialidad | Proveedor | Válidas | Con clínica local | % | Excluidas |
|---|---|---|---|---|---|
| aesthetic | claude | 1 | 1 | 100.0 % | 0 |
| aesthetic | gemini | 1 | 1 | 100.0 % | 0 |
| aesthetic | openai | 4 | 1 | 25.0 % | 0 |
| dental | claude | 1 | 1 | 100.0 % | refusal: 1 |
| dental | gemini | 2 | 1 | 50.0 % | empty: 1 |
| dental | openai | 2 | 1 | 50.0 % | error: 1 |
| fertility | claude | 1 | 1 | 100.0 % | 0 |
| fertility | openai | 2 | 2 | 100.0 % | 0 |
| hospital | claude | 1 | 1 | 100.0 % | 0 |
| ophthalmology | openai | 1 | 1 | 100.0 % | 0 |

## Agregado ponderado (RN-03/RN-04; pesos: claude 0.10, openai 0.55, gemini 0.25)

| Especialidad | % ponderado de respuestas con clínica local |
|---|---|
| aesthetic | 54.2 % |
| dental | 55.6 % |
| fertility | 100.0 % |
| hospital | 100.0 % |
| ophthalmology | 100.0 % |

## Marca líder por especialidad (solo marcas de la especialidad)

| Especialidad | Marca(s) | Respuestas | Válidas | % |
|---|---|---|---|---|
| aesthetic | Clínica Villoria L'Essence | 2 | 6 | 33.3 % |
| dental | Clínica Torres | 3 | 5 | 60.0 % |
| fertility | IVI Vigo | 2 | 3 | 66.7 % |
| hospital | — | 0 | 1 | 0.0 % |
| ophthalmology | Clínica Villoria | 1 | 1 | 100.0 % |

## Menciones de directorios

| Especialidad | Directorio | Respuestas | % de válidas |
|---|---|---|---|
| aesthetic | Doctoralia | 1 | 16.7 % |
| aesthetic | Multiestetica | 1 | 16.7 % |
| dental | Doctoralia | 1 | 20.0 % |
| dental | Top Doctors | 1 | 20.0 % |
| fertility | reproduccionasistida.org | 1 | 33.3 % |

## Sesgo RN-01: respuestas con alias < 4 caracteres no contados (p. ej. "MIA")

Siglas cortas que sí cuentan (RN-11/ADR-002, columna exact_aliases, solo en mayúsculas y como palabra completa): IVI → IVI Vigo.

| Especialidad | Respuestas |
|---|---|
| aesthetic | 1 |

## Coste estimado (€)

| Proveedor | € |
|---|---|
| claude | 0.51 |
| gemini | 0.47 |
| openai | 0.92 |
| total | 1.90 |
