# 05 — Lean Plan: Hypotheses, Cycles, Objectives

**Status:** v1 (2026-09-23). Governing principle: **no product code until clinics are paying for a manual service that proves LLM answers can be moved.**

## 1. Riskiest hypotheses (leap-of-faith), in order of danger

| # | Hypothesis | If it fails… | Test |
|---|---|---|---|
| H1 | We can move an LLM answer toward a specific clinic within 8–12 weeks using content and presence actions | No product, only a commodity measurement panel | Manual pilot with 3 clinics, measured weekly |
| H2 | A clinic pays 150–400 €/month for this | No business in the niche | Charge from the pilot; never free |
| H3 | We can attribute patients to LLM recommendations | Customer does not renew for lack of visible ROI | Three attribution signals installed on day one of the pilot |
| H4 | Healthcare-marketing agencies resell the tool | CAC explodes selling clinic by clinic | One agency with 3 of its clinics in the pilot |

H1 can kill the idea and is the cheapest to check. It goes first.

## 2. Build–measure–learn cycles

### Cycle 0 — Baseline and problem (weeks 1–2). Build nothing.

- Run the probe in `probe/` across 6 specialities, 3 runs, 3 LLMs. Cost 15–30 €.
- 15 problem interviews: 6 dental clinic directors, 3 aesthetic, 2 fertility/ophthalmology, 4 agencies (AMG, Hydra, Quality Marketing Contents, one more). 20-minute script, no product shown: "do you know what ChatGPT recommends in your city?", "what is a new implant patient worth to you?", "what do you pay today for acquisition?".
- **Go criterion:** ≥ 6 of 15 say they would pay > 150 €/month, **and** the probe shows that in dental and aesthetic fewer than half of answers name a local clinic. If neither holds, stop here.

### Cycle 1 — Sell before building (weeks 3–6)

- Send a free visibility report to 12 clinics from the target list in `03-local-market-vigo-pontevedra.md` §4, generated with the scripts: "ChatGPT recommends IVI 9 of 9 times and NIDA 2 of 9. These are the 5 pages it reads." One page, no product branding.
- Offer a 3-month pilot at 450 € prepaid, or 199 €/month. Includes weekly probe, action plan and attribution follow-up. All manual: scripts, a spreadsheet, a fortnightly call.
- **Go criterion:** 3 clinics pay. Ideally one fertility/ophthalmology (demo case), one dental (volume), one via agency (H4). If after 4 weeks only one pays, pain is insufficient → revisit price or segment before continuing.

### Cycle 2 — Concierge pilot (weeks 7–18). Tests H1 and H3, the heart of the business.

- Week 7: per-clinic baseline and attribution install: AI-traffic tagging in analytics, Search Console for branded queries, "how did you hear about us" field at reception or in the booking software.
- Weeks 7–10: execute highest-impact actions with each clinic: complete profiles on the 3 most-cited directories for the speciality, a price-and-criteria page per flagship treatment, structured data, robots.txt open to AI crawlers, 2 external mentions (local press or "best clinics" list).
- Weeks 10–18: measure weekly and adjust. Log which action moved which answer in which LLM. **That log is the future product.**
- **Go criterion:** 2 of 3 pilots gain ≥ 15 points of share of voice on their prompt set, and each has ≥ 1 attributed patient. If nothing moves, H1 fails → pivot to "report + consultancy" or abandon.

### Cycle 3 — Minimum product (weeks 19–30). Only what was done by hand three times in the pilots.

- Automated weekly probe, dashboard with share of voice and cited sources, gap list with recommended action, attribution log. Nothing else: no content generation, no integrations.
- Renew the 3 pilots to subscription and reach 10 paying clinics, 5 via agency.
- **Go criterion:** 10 customers, monthly churn < 5 %, the agency asks for a multi-client licence.

## 3. Objectives

| Horizon | Objective | Key result |
|---|---|---|
| Week 6 | Prove paid pain | 3 paid pilots, 1 350 € collected |
| Week 18 | Prove the answer moves | 2 of 3 pilots +15 pts share of voice and 1 attributed patient each |
| Month 7 | Prove repeatability | 10 customers, 2 500 € MRR, 1 agency as channel |
| Month 12 | Prove the niche scales beyond Vigo | 30 customers in Galicia + northern Portugal, 8 000 € MRR, churn < 4 % |

## 4. Metrics that matter (and those that do not)

**Matter:** share of voice per clinic (usage-weighted), number of cited sources where the clinic is present, attributed patients per month, MRR, churn.
**Do not matter yet:** dashboard users, product landing visits, number of probed prompts. If a number does not change a decision, do not measure it.

## 5. Pivot signals

- Clinics want the report but will not pay for follow-up → pivot to a one-off 300 € report sold through agencies.
- The answer moves, but only through actions the agency performs, not the tool → pivot to an agency tool, not a clinic tool.
- The answer does not move in 12 weeks for any pilot → abandon the niche, probably the idea.

## 6. Resources for the first 6 months

Founder part-time on development and interviews; one person on commission for sales or a revenue-share with AMG Agency; 200–400 €/month in API calls. No external investment until Cycle 2 results exist — those results are what is worth money in a round.

## 7. Immediate next actions

1. Obtain API keys (OpenAI, Anthropic, Google) and run `probe/run_probe.py` for the baseline.
2. Write the 15-interview script and the free visibility-report template.
3. Book the first meeting with AMG Agency.
