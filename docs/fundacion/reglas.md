# Reglas de negocio — push-llm

> Numeradas y estables: las specs y ADRs las citan como RN-xx. No se borran;
> se marcan derogadas con fecha y motivo.
> Origen: `07-mvp-product-spec.md` §4 y §6, `06-models-costs-and-usage-share.md` §4.

- **RN-01**: Una mención cuenta si el nombre de la clínica o un alias de ≥ 4 caracteres aparece en la respuesta, comparando texto normalizado sin acentos ni mayúsculas.
- **RN-02**: El SoV bruto por proveedor = respuestas que mencionan la clínica ÷ total de respuestas del set de prompts de la clínica en las ejecuciones de la semana.
- **RN-03**: La cifra principal que ve la clínica es el SoV ponderado: Σ (SoV bruto × peso del proveedor), normalizado a los proveedores efectivamente sondeados.
- **RN-04**: Pesos iniciales hasta tener datos propios: ChatGPT 55 %, Gemini 25 %, Claude 10 %, Perplexity 5 %. Google AI Overviews se reporta como canal aparte, sin ponderar.
- **RN-05**: Los pesos se refrescan mensualmente; cuando haya datos de referrers de clientes, se derivan pesos locales de ellos.
- **RN-06**: Position = orden base 1 de la clínica entre las clínicas nombradas; se promedia sobre las respuestas donde aparece.
- **RN-07**: Los pacientes atribuidos son la suma mensual de AttributionEvents por señal, mostrada por señal y en total; nunca se infieren del SoV.
- **RN-08**: Los gaps se ordenan por (peso de citación de la fuente × déficit de presencia) y por intent de prompt sin página de clínica.
- **RN-09**: No se almacenan datos personales de pacientes; la atribución es agregada.
- **RN-10**: El probe usa el modelo por defecto de cada app de consumo, con búsqueda web y la ciudad de la clínica como ubicación.
