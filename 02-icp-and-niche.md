# 02 — ICP and Niche Selection

**Status:** decided v1 (2026-09-23). Supersedes the generic ICP in `01-market-critique.md` §2.

## Filter criteria

A segment qualifies only if it meets all five at once:

1. **Measurable pain** — it loses traffic or leads in the short term.
2. **Existing budget** for visibility/acquisition.
3. **Ability to act** on its own content and presence (does not depend on a third party such as an OTA).
4. **Weak coverage** by Profound, Peec, Semrush and the Spanish horizontals.
5. **Reachable** by a small team based in Galicia.

## Segment scoring

| Segment | Pain | Budget | Can act | Incumbent coverage | Reachable | Verdict |
|---|---|---|---|---|---|---|
| B2B SaaS mid-market (US/EU) | High | High | Yes | Saturated | Low | Discard |
| Generic DTC e-commerce | High | Medium | Yes | High (Semrush, Ahrefs, Triple Whale) | Medium | Discard |
| SEO/marketing agencies ES/LATAM | High | Medium | Yes (for clients) | Medium (Antropus, Surfeo, Kime) | High | **Channel, not niche** |
| Private healthcare clinics (dental, aesthetic, fertility, ophthalmology, physio) | High, growing | High per lead | Partial (regulated content) | Low | High | **Strong candidate** |
| Law firms, advisory, consulting | Medium | Medium | Yes | Low | High | Candidate |
| Hotels, rural houses, experiences | High (travel is the #1 LLM query) | Medium | Partial (OTA dependence) | Low outside big chains | High | Strong candidate |
| Private education (masters, VET, academies) | High | High per enrolment | Yes | Low | High | Candidate |
| Real estate, developers | Medium | Medium | Partial | Low | Medium | Reserve |
| Restaurants, local retail | Low today | Low | No | Google Maps solves it | High | Discard |
| Galician industry (canning, shipyards, textile, energy) | Medium | Medium | Yes | None | Very high | Candidate with caveats (long, educational sales cycle) |

## Decision: primary niche = private healthcare in Spain, starting in Vigo and Pontevedra

Sold in two layers: direct to clinics and groups of 3–30 centres, and through the handful of agencies specialised in healthcare marketing.

Why this niche wins where others do not:

1. **Closed, local prompt universe.** A patient's questions are finite and localised. Fifty prompts per speciality and city cover ~80 % of what matters. API cost becomes predictable and the proprietary longitudinal dataset (the only real moat) builds fast.
2. **Action tied to result.** We can tell the clinic exactly what to do (doctor profile, schema, reviews on three sources, a page with prices and data) and measure whether the LLM cites it in 8 weeks. The loop closes.
3. **Horizontals will not come down here.** Profound is not building a Spanish healthcare-advertising-regulation module. Neither is Semrush. Antropus and Surfeo are horizontal.
4. **We sell ROI in euros, not share of voice.** A first fertility consultation is worth 3 000–5 000 € of treatment. If the tool attributes one patient a month, the customer renews.

Supporting data points: 38 % of users have used an AI platform to make direct healthcare decisions; healthcare search has split into clinical-information queries and local-provider-acquisition queries; medical/local schema markedly increases the chance of being cited (sources in `03-local-market-vigo-pontevedra.md`).

**Secondary niche for year two:** private education (business schools, masters, VET, exam academies). Same product architecture (comparison prompts, high-value decision, own marketing team); reuse the engine, swap the prompt catalogue.

## Discarded as direct customers

- **Physiotherapy** — low ticket, no capacity to invest. Agency channel only.
- **Hospitals** (Povisa, Vithas, Quirónsalud) — big ticket but marketing decided in Madrid/Valencia; phase two.

## Trap to avoid in the niche

Do not sell "AI visibility" to clinics. Sell "patients who arrive through ChatGPT" and prove it with attribution from day one (dedicated phone number or landing, tagged referrals, branded-search uplift). Otherwise this falls into the same trap as the horizontals.

## Validation before writing code

- 15 interviews: 5 clinic directors, 5 healthcare-marketing agencies, 5 marketing leads at business schools. Single question: "how much would you pay to know and improve which clinics ChatGPT recommends in your city?"
- A free, manual visibility report for 10 clinics in Vigo or A Coruña, produced with scripts, to measure reaction and meeting-conversion rate.
- Count how many clinics appear today in LLM answers for 50 real prompts. If almost none do, the opportunity to be first to "teach them how to appear" is large.
