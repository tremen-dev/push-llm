# LLM Visibility SaaS — Foundational Documents

**Status:** seed (pre-product). **Date:** 2026-09-23. **Owner:** Alberto Fojo.
**Language:** documents in English for agent consumption; the business operates in Galician/Spanish.

This folder is the seed of a new product: a SaaS that measures and improves how
private healthcare clinics in Galicia are recommended by AI assistants
(ChatGPT, Gemini, Claude, Perplexity, Google AI Overviews). It was produced
from a single founder/VC/CPO working session and is meant to be read by
agents working under a spec-driven development (SDD) flow before any code
is written.

## Reading order

| # | File | What it answers | Read when |
|---|---|---|---|
| 0 | `00-vision.md` | What we are building, for whom, one-sentence pitch | Always, first |
| 1 | `01-market-critique.md` | Brutal VC/CPO assessment: pain, TAM/SAM/SOM, competition, moat, monetisation, risks, verdict | Before any strategic decision |
| 2 | `02-icp-and-niche.md` | Segment scoring and the chosen niche (private healthcare, Vigo/Pontevedra) | Before scoping any feature |
| 3 | `03-local-market-vigo-pontevedra.md` | Real clinic map, proxy test of which sources LLMs read, target list, agencies | Before outreach or prompt-catalog work |
| 4 | `04-mechanics-of-llm-visibility.md` | How LLMs pick clinics, the four levers, how a visit/patient arrives, what not to promise | Before designing gap analysis, actions or attribution |
| 5 | `05-lean-plan.md` | Riskiest hypotheses, build-measure-learn cycles, objectives, pivot signals | Before planning any sprint |
| 6 | `06-models-costs-and-usage-share.md` | Which LLM models to probe with and why, cost per call, market-share weighting, public data sources | Before implementing the probe |
| 7 | `07-mvp-product-spec.md` | Functional spec of the MVP: entities, flows, metric definitions, non-goals, acceptance criteria | Before writing any spec/task |
| 8 | `08-glossary.md` | Terms used across the documents | On demand |
| — | `DECISIONS.md` | Decision log (ADR-style) with rationale | Before reopening any decision |
| — | `probe/` | Runnable probe: prompt catalog, brand list, multi-provider script | Cycle 0 of the lean plan |

## Ground rules for agents

1. **Do not build product before Cycle 2 of `05-lean-plan.md` has produced evidence.** The first deliverables are the probe run, interviews and a manual (concierge) pilot. Code is Cycle 3.
2. **The niche is fixed until a pivot signal fires.** Private healthcare in Vigo and Pontevedra. Do not generalise the product to "any business" in the MVP.
3. **Attribution is a day-one feature, not a follow-up.** See `04-mechanics-of-llm-visibility.md` §3 and `07-mvp-product-spec.md` §5.
4. **Probe with the model each consumer app serves by default, not the premium model.** See `06-models-costs-and-usage-share.md`.
5. **Every metric shown to a clinic must be weighted by assistant usage share.** See `07-mvp-product-spec.md` §4.
6. Decisions live in `DECISIONS.md`. To change one, add a new entry that supersedes it; do not edit history.

## Provenance

Market and competitor figures were gathered on 2026-09-23 from public web sources
(cited inline in each file). Local clinic data comes from public directories and
clinic websites, not from interviews. Nothing here has yet been validated with a
paying customer — that is the point of the lean plan.
