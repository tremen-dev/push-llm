# 07 — MVP Product Specification

**Status:** draft v1 (2026-09-23). This is the seed spec for Cycle 3 of `05-lean-plan.md`.
**Precondition:** do not implement until Cycle 2 go-criteria are met. Until then, the "product" is `probe/` + a spreadsheet + a fortnightly call.

## 1. Scope

**In:** weekly multi-assistant probe; usage-weighted share of voice; cited-source analysis; gap list with recommended actions; attribution log; multi-clinic view for agencies.
**Out (explicit non-goals for MVP):** content generation at scale, CMS/website integrations, automated publishing to directories, rank tracking on Google, any vertical other than private healthcare, any geography other than Galicia (config-driven, but not sold).

## 2. Actors

| Actor | Needs |
|---|---|
| Clinic owner / manager | See in one screen: am I recommended, versus whom, what do I do next, how many patients came |
| Agency account manager | Same, across 5–30 clinics; export for client reports |
| Operator (us) | Run probes, curate prompt catalogues, label answers, adjust weights, see cost |

## 3. Domain entities

- **Clinic** — name, aliases (for mention matching), speciality, city, website, competitors[], attribution config.
- **Speciality** — enum (dental, fertility, ophthalmology, aesthetic, physio, hospital, …); owns a default prompt catalogue and a default list of dominant sources.
- **Prompt** — id, speciality, city, intent (discovery, price, comparison, urgent, trust, specific), language (es, gl), text. Clinic can add private prompts.
- **Provider** — enum (chatgpt, gemini, claude, perplexity, google_ai_overviews); model id used; usage-share weight; runs per prompt.
- **ProbeRun** — weekly batch: timestamp, provider, prompt, run index, raw answer, cited URLs[], mentions[] (brand, position), cost.
- **Source** — normalised domain/page cited by providers; type (directory, clinic_site, press, review_aggregator, other); per-speciality citation count.
- **PresenceCheck** — clinic × source: present / incomplete / absent, last checked, evidence.
- **Gap** — derived: source with high citation weight where clinic presence ≠ present; or prompt-intent with no clinic page; or technical (robots, schema, NAP).
- **Action** — gap → recommended task: title, owner (clinic / agency / tool), effort, expected impact, status, completed_at.
- **AttributionEvent** — clinic, date, channel signal (referral_tag | branded_search | reception_answer | dedicated_line), count, value estimate.

## 4. Metric definitions (must be identical in code, docs and UI)

- **Mention:** the clinic (or an alias) is named in a provider answer. Matching is accent- and case-insensitive on normalised text; aliases ≥ 4 chars.
- **Share of voice (SoV), raw, per provider:** answers mentioning the clinic ÷ total answers for the clinic's prompt set, over the week's runs.
- **Weighted SoV:** Σ_provider (raw SoV_provider × weight_provider), weights from `06-models-costs-and-usage-share.md` §4, normalised to the providers actually probed. This is the headline number shown to the clinic.
- **Position:** 1-based order of the clinic among clinics named in an answer; averaged over answers where mentioned.
- **Competitor SoV:** same computation for each configured competitor.
- **Source citation weight:** Σ over answers citing the source of the provider weight; ranked per speciality+city.
- **Coverage of cited sources:** share of the top-10 sources (by citation weight) where the clinic's presence = present.
- **Attributed patients:** monthly sum of AttributionEvents by signal, shown separately and as a total; never inferred from SoV.

## 5. Core flows

1. **Onboarding** (≤ 5 min): clinic data, speciality, city, competitors → default prompt catalogue loaded → attribution setup checklist (UTM/referrer tagging snippet, Search Console access, reception question or dedicated number).
2. **Weekly probe** (scheduled): for each provider × prompt × run → call provider with web search + city location → store ProbeRun → extract mentions and cited URLs (cheap model or regex) → update Sources, SoV, positions.
3. **Gap analysis** (after probe): top sources by citation weight → PresenceCheck (manual in MVP, assisted later) → Gaps → Actions ranked by (source weight × presence deficit) and by prompt-intent without matching clinic page.
4. **Action tracking:** clinic/agency marks actions done; the system annotates the SoV timeline with completion dates so movement can be read against actions. This timeline is the dataset that becomes the moat.
5. **Attribution log:** weekly import of tagged referrals and branded-search counts; manual entry of reception answers; monthly summary in euros using a per-speciality average ticket.
6. **Agency view:** table of clinics with weighted SoV, delta vs last month, open actions, attributed patients; CSV/PDF export.

## 6. Non-functional

- Probe cost per clinic-month ≤ 20 € at 40 prompts × 3 runs × 3 providers with mid-tier models.
- All provider calls idempotent and retry-safe; store raw answers forever (audit + future training data).
- Provider adapters isolated behind one interface; adding Google AI Overviews must not touch scoring.
- Weights, model ids, runs-per-provider and prompt catalogues are configuration, not code.
- Spanish and Galician UI; data model language-agnostic.
- GDPR: no patient PII stored; attribution counts are aggregates.

## 7. Acceptance criteria for "MVP done"

- [ ] A clinic can be onboarded and sees a weighted SoV, competitor SoV and top-10 cited sources within one probe cycle.
- [ ] Gap list produces at least one concrete action per top-3 missing source.
- [ ] Action completion is visible on the SoV timeline.
- [ ] Attribution summary shows the three signals separately for the month.
- [ ] Agency user sees ≥ 5 clinics in one table and exports it.
- [ ] Weekly probe for 10 clinics runs unattended within budget and logs cost per clinic.
- [ ] Definitions in §4 are implemented once, unit-tested, and reused by UI and exports.

## 8. Open questions (to resolve during Cycle 2, not by assumption)

- Which attribution signal do clinics actually keep up (reception question vs dedicated line)?
- Does PresenceCheck need automation in MVP, or is a monthly manual check sufficient for ≤ 30 clinics?
- Is Google AI Overviews probe-able reliably enough to weight, or only to report?
- Per-speciality average ticket values for the euro estimate (to be confirmed in interviews).
