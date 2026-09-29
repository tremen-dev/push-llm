# Decision Log

ADR-style. Newest at the bottom. To change a decision, add a superseding entry; never edit an old one.

## D-001 — Narrow the generic "LLM SEO tool" to a vertical niche
**Date:** 2026-09-23. **Status:** accepted.
**Context:** the generic idea scored 5/10: 15+ funded competitors, incumbents bundling monitoring, no moat (`01-market-critique.md`).
**Decision:** build only for a vertical + geographic niche where horizontals will not go.
**Consequence:** the MVP must not be generalised to "any business".

## D-002 — Primary niche: private healthcare clinics, Vigo and Pontevedra first
**Date:** 2026-09-23. **Status:** accepted.
**Context:** segment scoring in `02-icp-and-niche.md`; local supply map in `03-local-market-vigo-pontevedra.md`.
**Decision:** dental as volume niche; ophthalmology and fertility as demo cases; aesthetic as second volume market; physio only via agencies; hospitals phase two. Secondary niche (year 2): private education.
**Consequence:** prompt catalogues, sources and brand lists are built per speciality × city.

## D-003 — Sell "patients from ChatGPT", not "AI visibility"
**Date:** 2026-09-23. **Status:** accepted.
**Context:** measurement without ROI churns (`01-market-critique.md` §1, §5).
**Decision:** attribution (referral tags + branded-search uplift + reception answer) is a day-one feature of every pilot and of the MVP.

## D-004 — Lean sequencing: no product code before Cycle 2 evidence
**Date:** 2026-09-23. **Status:** accepted.
**Context:** H1 (answers can be moved) is the riskiest and cheapest hypothesis to test (`05-lean-plan.md`).
**Decision:** Cycle 0 probe + interviews → Cycle 1 paid pilots sold on a manual report → Cycle 2 concierge delivery → Cycle 3 software of what was repeated by hand.

## D-005 — Probe with each app's default (mid-tier) model, not the premium one
**Date:** 2026-09-23. **Status:** accepted.
**Context:** ~94 % of ChatGPT users are on the free tier; for local questions the search backend, not model intelligence, decides the answer (`06-models-costs-and-usage-share.md`).
**Decision:** probe models = consumer defaults with web search and city location; internal processing = cheapest model that passes a labelled test set.

## D-006 — Weight all visibility metrics by assistant usage share
**Date:** 2026-09-23. **Status:** accepted.
**Context:** ChatGPT ≈ 55 %, Gemini ≈ 26 %, Claude ≈ 9 % of assistant traffic (Aug 2026); shares shift monthly.
**Decision:** headline metric is weighted SoV; weights are configuration refreshed monthly; local weights derived from own customers' referral data when available. Google AI Overviews tracked as a separate channel.

## D-007 — Pricing anchor for pilots
**Date:** 2026-09-23. **Status:** accepted (to be validated in Cycle 1).
**Decision:** 3-month pilot at 450 € prepaid or 199 €/month; never free beyond the one-page report.

## D-008 — Documentation language
**Date:** 2026-09-23. **Status:** accepted.
**Decision:** foundational and spec documents in English for agent consumption; customer-facing material in Galician/Spanish.

## D-009 — Niche moves to A Mariña first, then Galicia, Asturias and León; Vigo and Pontevedra parked
**Date:** 2026-09-29. **Status:** decided by the human (Alberto Fojo); formal record in `docs/adr/ADR-008-nicho-geografico-a-marina-primero-despues-galicia-asturias-y-leon-supera-d-2.md` (pending approval at the time of writing).
**Context:** the first real customer (Clínica Ártica, Viveiro) is in A Mariña, and in areas with little supply the competition to appear in AI answers is lower. A Mariña is a small market, so volume has to come from the rest of Galicia, Asturias and León.
**Decision:** supersedes the geographic part and the speciality order of D-002. Primary niche = private healthcare clinics in general, A Mariña first, then the rest of Galicia, Asturias and the province of León. Vigo and Pontevedra are parked, not abandoned. Hospitals phase two, physio only via agencies and private education in year 2 stay as in D-002. ADR-003 and ADR-005 are superseded in part (see ADR-008 §5–§6).
**Consequence:** EPIC-001 (Cycle 0 in Vigo) is closed unfinished; EPIC-002 (Clínica Ártica pilot) is the main validation. The documents `02-icp-and-niche.md` and `03-local-market-vigo-pontevedra.md` remain as history of the old niche.
