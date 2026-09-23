# Dominio y lenguaje ubicuo — push-llm

> Glosario canónico. Estos términos NO se traducen ni se anglicizan en código,
> UI ni documentación. Si un término falta, se añade aquí antes de usarse.
> Origen: `08-glossary.md` y `07-mvp-product-spec.md` §3–4. Las entidades del
> modelo se nombran en inglés (código); aquí se fija su significado.

| Término | Definición | Notas |
|---|---|---|
| Clinic | Clínica cliente o competidora: nombre, alias, especialidad, ciudad, web, competidores, config. de atribución | Entidad |
| Speciality | dental, fertility, ophthalmology, aesthetic, physio, hospital… Tiene catálogo de prompts y fuentes dominantes por defecto | Enum |
| Prompt | Pregunta real de paciente: especialidad, ciudad, intent (discovery, price, comparison, urgent, trust, specific), idioma (es, gl) | Entidad |
| Prompt catalogue | Conjunto curado de prompts por especialidad × ciudad × idioma | |
| Provider | Asistente sondeado: chatgpt, gemini, claude, perplexity, google_ai_overviews; con modelo, peso y runs por prompt | "Asistente" en UI |
| Probe / ProbeRun | Lote programado de prompts a proveedores / una respuesta concreta con menciones, URLs citadas y coste | |
| Mention | La clínica (o un alias ≥ 4 caracteres) aparece nombrada en una respuesta; matching sin acentos ni mayúsculas | |
| Position | Orden (base 1) de la clínica entre las clínicas nombradas en una respuesta | |
| Share of voice (SoV) | Respuestas que mencionan la clínica ÷ total de respuestas de su set de prompts, por proveedor y semana | |
| Weighted SoV | Σ SoV_proveedor × peso_proveedor, normalizado a los proveedores sondeados. Métrica principal | |
| Usage share / weight | Fracción de uso de cada asistente (Similarweb, Comscore, GfK); configuración mensual | |
| Source | Dominio/página citada por los proveedores; tipo: directory, clinic_site, press, review_aggregator, other | |
| Source citation weight | Σ pesos de proveedor de las respuestas que citan la fuente | |
| PresenceCheck | Clínica × fuente: present / incomplete / absent | |
| Coverage of cited sources | Fracción del top-10 de fuentes donde la clínica está present | |
| Gap | Fuente citada donde la clínica falta o está incompleta; intent sin página de la clínica; bloqueo técnico (robots, schema, NAP) | |
| Action | Tarea recomendada derivada de un gap: responsable (clinic/agency/tool), esfuerzo, impacto, estado | |
| AttributionEvent | Señal agregada de paciente por canal IA: referral_tag, branded_search, reception_answer, dedicated_line | Sin PII |
| Branded-search uplift | Subida de búsquedas del nombre de la clínica en Search Console | |
| NAP | Name, Address, Phone: consistencia en toda la web | |
| AEO / GEO | Answer / Generative Engine Optimisation | Términos de mercado |
| Concierge MVP | Servicio manual a los primeros clientes antes de construir software | |
