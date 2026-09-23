# 03 — Local Market: Vigo and Pontevedra

**Status:** v1 desk research (2026-09-23). Built from public directories and clinic websites, not interviews.
The real multi-LLM probe has **not** been run yet (no API credentials in the research session); the kit is in `probe/`.

## 1. Supply map by speciality

| Speciality | Relevant players | Who dominates today | Marketing-spend signal |
|---|---|---|---|
| Dental | 175–180 clinics in Vigo (Páginas Amarillas); dozens in Pontevedra | Chains (Sanitas Milenium, Adeslas, Vitaldent) on volume; Torres, Grandío Pazos, Hernández Vallejo, Guitián, Titanium, Bastida on reputation | High. Several publish price pages and "best clinics" content |
| Fertility | 3 in Vigo (IVI, NIDA, Vithas); 0 in Pontevedra | IVI (national chain) | Very high per lead; NIDA is the independent competing against IVI |
| Ophthalmology | Villoria, Malvar y Pérez, Vithas Cadarso, Ribera Povisa, Fernández-Vigo; Quirónsalud Miguel Domínguez in Pontevedra | Villoria, overwhelmingly | Villoria already runs content, financing and price pages |
| Aesthetic medicine | 15–20 clinics in Vigo | Fragmented: MIA, Rey, Murillo, Helga Rivera, Villoria L'Essence, DeCastro, Garden Clinic, Bellum, Único Life, Femme, Centro Láser Vigo, Antesola | Medium. Many rely on Instagram |
| Physiotherapy | Dozens in Vigo and Pontevedra | Nobody. Gulpari, Vibar, C1dema, Losada Crespo, Ficas surface only via directories | Low per centre |
| Private hospitals | Ribera Povisa, Vithas Fátima, Quirónsalud Miguel Domínguez | Povisa (best private hospital in Galicia per MRS 2024) | High, but decided at group HQ |

## 2. Proxy test: which sources surface for patient questions

Assistants with browsing read the top search results, so the SERP for a patient-style question is a proxy for what the LLM will cite. Pattern varies sharply by speciality:

- **Fertility.** Two editorial directories dominate (reproduccionasistida.org, mundofertilidad) plus Top Doctors. Only IVI and NIDA are named. The LLM answer is already stable and predictable: IVI first, NIDA second, Vithas third with no reviews.
- **Dental.** Directories (docdental, zonadental, Top Doctors, Páginas Amarillas) plus clinic sites that publish "best clinics in Vigo" content to capture the question (e.g. HL Dental). Most clinics already playing SEO → easiest to sell a "next step".
- **Ophthalmology.** Villoria holds 5 of 9 results with its own site. The LLM recommends Villoria almost always. Villoria = customer to defend; the other four = customers to attack.
- **Aesthetic.** Local directories (mejoresdevigo, multiestetica, paxinasgalegas, todoestetica) and review aggregators. No clinic controls the answer; the LLM returns a different list each run.
- **Physiotherapy.** 100 % directories: Doctoralia, Top Doctors, mundofisio, fisiolocal. No clinic has its own voice.
- **Price questions.** For "how much is a dental implant in Vigo", Madrid clinics and national chains outrank Vigo clinics. Only Clínica Torres and Titanium have local price content. Direct gap.

Hypothesis for the real probe to confirm or reject: in dental and aesthetic fewer than half of answers name a Vigo clinic; in fertility and ophthalmology the same clinic appears every time.

## 3. Where the niche-within-the-niche is

1. **Dental in Vigo + Pontevedra is the primary niche.** ~200 potential customers in the province, implant ticket 1 200–1 700 €, LLM answers still in the hands of directories. Pitch: "who shows up when someone asks about implants in Vigo, and how we change it".
2. **Ophthalmology and fertility are the best demo cases.** Few players, very high ticket, answer crystallised around one leader. One success with NIDA or Malvar y Pérez is worth more than 20 physio customers.
3. **Aesthetic is the second market by volume.** Fragmented, no owner of the answer, LLMs answer at random — low effort to go from absent to always present.
4. **Physio discarded as direct customer.** Agency channel only.

## 4. First-contact list (ordered by close probability × case value)

| Target | Speciality | Why |
|---|---|---|
| Clínica Villoria (Vigo + Pontevedra) | Ophthalmology, aesthetic | Already invests, own marketing, has a position to defend → "defensive monitoring" customer |
| Clínica NIDA | Fertility | Independent vs national chain. Maximum pain, maximum ticket |
| Clínica Torres; Hernández Vallejo (multi-site) | Dental | Already produce implant/price content; will understand the play instantly |
| HL Dental (Pontevedra) | Dental | Publishes "best clinics in Vigo" articles; already doing GEO without knowing |
| Clínica Gamero; Garrido Madarnás | Dental, Pontevedra | Less competition in the city; neither surfaces in answers today |
| Clínica Murillo (Vigo + Pontevedra); Clínica MIA | Plastic surgery, aesthetic | High ticket, unowned answer |
| Malvar y Pérez; Fernández-Vigo | Ophthalmology | Villoria's challengers |
| Ribera Povisa, Vithas, Quirónsalud Pontevedra | Hospitals | Phase two: big ticket, corporate sales cycle |

## 5. Channel: agencies already selling marketing to clinics in Galicia

- **AMG Agency** — digital marketing for dental, aesthetic, hair, physio, psychology, plastic surgery clinics across Galicia. First meeting to book.
- **Axencia Hydra** — brand, web and social for dental clinics.
- **Quality Marketing Contents** — healthcare-marketing specialist, 10+ years.

One meeting with an agency is worth ten with individual clinics.

## 6. Sources (accessed 2026-09-23)

Fertility: reproduccionasistida.org (Pontevedra, NIDA, IVI Vigo pages), mundofertilidad.es, ivi.es/clinicas/vigo.
Dental: docdental.es/clinicas-dentales/vigo, hldental.es, clinicatorresvigo.com, implantesvigo.es, paginasamarillas.es, doctoralia.es, clinicagamero.com, garridomadarnasdental.es.
Ophthalmology: clinicavilloria.es, clinicaoftalmologicavigo.es, vithas.es (Cadarso), riberasalud.com/povisa, fernandez-vigo.com.
Aesthetic: mejoresdevigo.es, miamedicoestetica.com, plasticamurillo.com, helgarivera.com, clinicafemme.es, centrolaservigo.com, clinicarey.com, unicolifeclinics.com, centrosbellum.com.
Physio: doctoralia.es/fisioterapeuta/vigo, topdoctors.es/vigo/fisioterapia, mundofisio.es, fisiolocal.es.
Hospitals: galiciapress.es (MRS ranking 2024-12-03), atlantico.net (private beds 2024-04-26), ahosgal.es.
Agencies: amgagency.es, hydramarketing.es, qualitymarketingcontents.com.
Healthcare + AI: marketingmedico.es/puede-chatgpt-recomendar-clinica/, blog.hubspot.es (AEO tools for clinics), marketsurge.io (GEO for local businesses 2026), groupfractal.com (GEO local lead gen 2026).
