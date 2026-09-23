# 06 — Models, Costs and Usage Share

**Status:** v1 (2026-09-23). Prices and shares are snapshots; re-verify quarterly.

## 1. Two different uses of LLMs in the product, two different rules

### A. The probe (simulate what the patient sees)

Goal: reproduce the answer a normal person gets, not the best possible answer. That person overwhelmingly uses the free tier / default model of each app. ChatGPT: > 1 B weekly active users vs ~60 M paid → ~94 % on the free tier.

Also, for local questions the answer is decided by the search backend and the pages read, not by model intelligence. A cheap model with web search and an expensive model with web search read the same pages and name the same clinics.

**Rule:** for each brand, probe with the model its consumer app serves to free users by default, with web search enabled and user location set to the clinic's city. Today that is mid-tier everywhere: Sonnet on Claude, Flash on Gemini, the app default on ChatGPT. Re-check each app's default every few months; it changes.

Caveat: API + search tool approximates the consumer app, it is not identical (the app has user memory, real location, its own retrieval pipeline). Hence 3 runs per prompt and trend reading, plus a quarterly manual check: 10 questions in the real app from a phone in Vigo.

### B. Internal processing (extract brands from answers, classify sources, draft the gap diagnosis)

**Rule:** the cheapest model that does the job, measured. Extracting clinic names from text is a Haiku-class task. Drafting the weekly action plan for one clinic can go to Sonnet/Opus-class (few calls, quality matters).

Method: 50 hand-labelled answers; test each model against them; if the cheap one scores ≥ 98 %, use it. Keeps variable cost per customer < 20 €/month against a 199 €/month price.

### C. When the premium model is justified

Only: enterprise customer explicitly asking to probe the premium model (their patients are paid-tier users), or one-off deep analysis of "why does the LLM say this" on 5 answers, not 400.

## 2. Reference costs (Anthropic list prices, Sept 2026; others comparable by tier)

| Model | Input / output per M tokens | Approx. cost per probe question with web search |
|---|---|---|
| Claude Sonnet 5 | 2 $ / 10 $ | 3–5 ¢ |
| Claude Opus 5 | 5 $ / 25 $ | 8–12 ¢ |
| Claude Haiku 4.5 | 1 $ / 5 $ | 2–3 ¢ |

Web search is billed separately, ~1 ¢ per search. With mid-tier models, a full weekly probe for one clinic (40 prompts × 3 runs × 3 providers) costs ~15–20 €/month. Premium models triple it with no customer benefit.

## 3. Usage share: what can be known and what cannot

### Public sources

| Question | Source | Latest figure | Cadence |
|---|---|---|---|
| Web-traffic share among assistants (global) | Similarweb (free on X/blog) | Aug 2026: ChatGPT 55 %, Gemini 26 %, Claude 9 %, DeepSeek 3 %, Grok 2 %, Copilot 2 %, Perplexity 1 % | Monthly |
| Usage share incl. mobile apps (global) | Comscore AI Intelligence Report; Sensor Tower | Jun 2026: ChatGPT 50 %, Gemini 30 %, Claude 11 % | Monthly/quarterly; summary free |
| Penetration in Spain | GfK DAM (digital audience panel) | Jun 2026: ChatGPT reaches 79 % of Spanish AI users (down from 83 %) | Monthly, paid; press publishes headlines |
| Frequent use in Spanish population | Funcas annual survey | 2025: 28 % use ChatGPT frequently (4 % in 2023) | Annual |
| Gen-AI use in population | INE, ONTSI | 38 % of residents; 45 % of active population | Annual |
| Free vs paid ChatGPT users | OpenAI official figures | > 1 B WAU, ~60 M paid → ~94 % free | Ad hoc |

### Not knowable publicly

- **Which model version each user sees.** No provider publishes it. Indirect: free/paid ratio → the vast majority sees the free-tier default. Reinforces rule 1A.
- **Usage by city or sector.** No panel goes down to "how many people in Vigo ask an LLM about a dental clinic".
- **Share inside Google.** AI Overviews and AI Mode do not appear in chatbot shares because they sit inside the search engine. For local health questions they are probably the AI channel with the widest reach. **Include Google AI Overviews as a fourth provider in the probe.**

## 4. How to use this in the product

1. **Weight share of voice by assistant usage share.** Appearing in ChatGPT is worth ~6× appearing in Claude. Use GfK for Spain when available, Similarweb monthly as the fallback.
2. **Refresh weights monthly.** ChatGPT lost ~20 points in a year; Claude grew 5×. A fixed weight is stale in three months.
3. **Derive local mix from own customers.** Once pilots have attribution, referrers from chatgpt.com, gemini.google.com, claude.ai, perplexity.ai give the real assistant mix of Vigo patients. With 10 clinics this is a dataset no public panel has — and an asset in itself.

**Starting weights** until own data exists: ChatGPT 55 %, Gemini 25 %, Claude 10 %, Perplexity 5 %, Google AI Overviews tracked as a separate channel unweighted, rest ignored. Consequence: Claude can be probed 1 run per prompt; ChatGPT keeps 3.

## 5. Sources (accessed 2026-09-23)

- https://x.com/Similarweb/status/2096878021378466096
- https://momenticmarketing.com/blog/top-ai-chatbots
- https://www.similarweb.com/blog/marketing/geo/gen-ai-stats/
- https://www.infobae.com/tecno/2026/06/17/liderazgo-de-chatgpt-cae-por-debajo-del-50-gemini-y-claude-cada-vez-son-mas-usados/
- https://dircomfidencial.com/marketing/chatgpt-pierde-cuota-de-mercado-ante-gemini-y-claude-20260923-0400/
- https://www.funcas.es/prensa/el-uso-frecuente-de-chatgpt-en-espana-sube-del-4-al-28-entre-2023-y-2025/
- https://www.ontsi.es/sites/ontsi/files/2026-07/indicadores-de-uso-de-inteligencia-articifial_1.pdf
- https://techcrunch.com/2026/02/27/chatgpt-reaches-900m-weekly-active-users
- https://getairefs.com/blog/chatgpt-user-statistics/
