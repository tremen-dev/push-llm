# 01 — Market Critique (VC + CPO lens)

**Status:** v1 (2026-09-23). Written as a deliberately harsh assessment of the *generic* idea
("a tool to position companies in LLM answers, the new SEO") before it was narrowed to a niche.
The niche decision that followed is in `02-icp-and-niche.md`.

## 1. Problem and pain — painkiller or vitamin?

- **Painkiller for a concentrated segment:** brands that live on organic traffic (B2B SaaS, e-commerce, media, comparison sites) are watching CTR fall to AI Overviews and direct assistant answers. When a CMO sees the assistant recommending a competitor, that hurts and has budget.
- **Vitamin for everyone else.** SMBs do not yet know the problem exists; AI referral traffic is still a small fraction of total traffic.
- **The trap:** the customer feels the pain of "I don't appear" but what they are sold is *measurement*, and measurement does not cure. Unless the product closes the loop measure → act → prove impact, it becomes a vitamin within six months.

## 2. Market size (generic idea)

| Level | Definition | Order of magnitude |
|---|---|---|
| TAM | Global SEO spend (software share ≈ 10 B$) | 80–100 B$ |
| SAM | Mid-market and enterprise with an SEO/content team and tool budget, EU + US | 1.5–2.5 B$ |
| SOM (3 yr, realistic) | One vertical or geographic niche | 5–15 M$ ARR |

Generic ICP: 50–2 000 employees, a Head of SEO or Content, already paying Semrush/Ahrefs, in a category people ask an LLM "what is the best X for Y". Agencies are the second ICP and the best channel.

## 3. Competition and moat

The market stopped being a blue ocean in 2025. As of Sept 2026:

- **Funded specialists:** Profound (155 M$ raised, 1 B$ valuation, Fortune 500 clients), Peec AI (29 M$ raised, 4 M$+ ARR in ten months), Scrunch (26 M$, now owned by Sitecore), Otterly, Athena, Goodie. Category raised 300 M$+ between summer 2025 and spring 2026.
- **Incumbents bundling the feature:** Semrush AI Toolkit (Semrush now under Adobe), Ahrefs Brand Radar, Conductor, BrightEdge, Similarweb. They own the customer, the keyword data and the sales channel, and give the feature away inside existing plans.
- **Free / manual:** HubSpot AEO Grader; scripts that fire 200 prompts at an API and dump into a spreadsheet. The manual method is viable and cheap.
- **Spanish-market horizontals already exist:** Antropus.io, Surfeo (ES+EN, EU-based), Kime, Zerply, Dageno.

Published pricing (Aug 2026): Otterly 29/189/489 $; Peec 95/245/495 $; Profound 99/399 $ annual-only; Scrunch 300/500 $.

**Moat today: almost none.** Monitoring is a commodity because anyone can call the same APIs. Plausible moats: (a) a proprietary longitudinal dataset of real prompts per vertical — takes years; (b) deep integration into the content/PR workflow so the product *executes* actions; (c) a vertical or linguistic niche the big players ignore. Without one of these, the advantage lasts three months.

## 4. Monetisation and CAC/LTV

- Charge monthly subscription tiered by tracked prompts, models covered, brands/competitors. Never pure usage pricing: the customer cannot estimate their need and uncertainty kills conversion.
- Model variable cost (API calls to OpenAI/Anthropic/Google/Perplexity) carefully: a cheap plan with many daily prompts can have negative gross margin.
- **CAC/LTV risk is high** for the generic idea: "AI visibility" search terms are already expensive; at 200–500 €/mo and 5–8 % monthly churn if impact is not proven, LTV falls below a sales-assisted CAC. Escape routes: PLG with a free visibility report as the magnet, and the agency channel with per-seat pricing.

## 5. Technical and MVP risk

The biggest trap is building a pretty monitoring dashboard and believing that is the product. Real problems:

- **No true observability.** LLM answers are non-deterministic, personalised and change with each release. You sample and sell the illusion of a stable ranking.
- **No lever of action.** What moves LLM visibility is the usual: structured content, media mentions, Reddit, Wikipedia, reviews. Software does not do that; an agency does. If the product only says "the competitor gets cited more", the customer asks "so what do I do?".
- **API cost and dependency.** Terms of service may restrict scraping; APIs charge per token; the MVP cost model tends to break at scale.
- **Attribution.** Proving that more citations bring revenue is nearly impossible today. Without it there is no renewal.

Correct MVP: one vertical, ~50 expert-curated prompts, three models, and a flow of actionable recommendations linked to observed results week over week. Not 10 models and 5 000 prompts.

## 6. Verdict on the generic idea

**Score: 5 / 10.** Timing is good and the buyer exists, but "a new SEO" is generic, already has 15 funded competitors, and is being absorbed by incumbents. It rises to 7–8 only if reframed as "an agent that executes visibility actions in one concrete vertical", not "a measurement tool".

Three main reasons it could fail:

1. **Fast commoditisation.** Semrush, Ahrefs and HubSpot give monitoring away inside what the customer already pays. A standalone measurement product has nowhere to live.
2. **You measure but do not control.** Without a mechanism that moves visibility and proves it with data, the customer sees no ROI and cancels at the second renewal.
3. **Platform risk.** OpenAI, Google and Anthropic can launch brand analytics, change APIs or put ads in answers; any of those redefines the market overnight.

## Sources (accessed 2026-09-23)

- https://www.surmado.com/blog/best-ai-visibility-tools-2026
- https://www.get-ryze.ai/blog/ai-visibility-tools-pricing-compared-2026
- https://sanbi.ai/blog/ai-visibility-platform-comparison-peec-profound-scrunch
- https://www.inboundcycle.com/blog-de-inbound-marketing/guia-completa-de-herramientas-geo
- https://surfeo.ai/blog/herramientas-visibilidad-ia
- https://seranking.com/blog/chatgpt-referral-traffic-may-2026/
- https://elogic.co/blog/chatgpt-commerce-statistics/
- https://www.zeroclickproject.com/insights/research/chatgpt-shopping-ecommerce-discovery-research
- https://higoodie.com/blog/ai-search-traffic-report-2026/
