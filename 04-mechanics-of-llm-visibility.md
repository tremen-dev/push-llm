# 04 — Mechanics of LLM Visibility

**Status:** v1 (2026-09-23). Conceptual foundation for gap analysis, actions and attribution. Read before designing any of those.

## 1. How an assistant answers "best dental clinic in Vigo"

An LLM has two ways to answer:

- **From memory** (training data). For local, concrete questions this memory is poor and stale. It almost never knows anything reliable about a clinic in Vigo.
- **By searching.** ChatGPT, Gemini, Claude and Perplexity detect a local/recommendation question, run one or more web searches underneath, read the 5–10 best-ranked pages, and write an answer from them, citing those pages.

For our niche ~95 % of answers come from the second path. **The LLM does not decide which clinic is best; it decides which pages to read and repeats what those pages say.** Think of a journalist in a hurry: three searches, read what is on top, write the article.

Because the question is comparative ("which is the best"), the LLM prefers pages that already compare several options (directories, "best clinics" lists) over a clinic's own site that only talks about itself. That is why directories dominate the proxy test in `03-local-market-vigo-pontevedra.md`.

## 2. The four levers that make a clinic appear

All four are actionable; none can be bought.

1. **Be in the sources the LLM reads.** If for "fertility clinic in Vigo" the LLM reads reproduccionasistida.org and mundofertilidad, and the clinic has no complete profile there, the clinic does not exist for the LLM. First action: complete presence (data + reviews) on the 3–4 directories that dominate each speciality. Google Business Profile and its reviews count as a source.
2. **Have pages that literally answer the question.** The LLM looks for quotable text. "Dental implant in Vigo: 1 290 € with zirconia crown, includes study and check-ups" is quotable. A home page saying "smiles that change lives" is not. Every frequent patient question needs a page that answers it with data, prices and criteria.
3. **Have others talk about you.** "Best clinics in Vigo" lists, local press, professional associations, forums. The LLM trusts three independent sources more than one own page.
4. **Be machine-readable.** Identical name/address/phone everywhere (NAP consistency); structured data (schema.org MedicalClinic / Physician / Offer); robots.txt not blocking AI crawlers (GPTBot, ClaudeBot, Google-Extended, PerplexityBot); content in plain HTML, not only in video or images.

This is local-SEO-style work aimed at the sources LLMs read rather than at Google directly.

## 3. How the visit or patient arrives

The answer includes the clinic name and usually a link. Three things then happen:

- **Click on the link.** ChatGPT tags these visits with a URL parameter (`utm_source=chatgpt.com`); other assistants send a referrer. Countable in analytics if configured. Caveat: studies estimate ~70 % of AI referrals show up as "direct" in a default GA4 setup.
- **Search the name on Google.** The user reads "Clínica NIDA" and googles it. Shows as branded-search uplift in Search Console, not as AI traffic. This is the majority path and the one almost nobody measures.
- **Call or book directly.** Captured only if reception asks "how did you hear about us" or there is a dedicated phone number / landing page for AI traffic.

The product must combine all three signals from day one, or the clinic never sees the ROI even when it exists.

## 4. What the MVP must not promise

- **No guaranteed placement.** There are no ads in LLM answers today; you cannot pay to appear.
- **No movement in days.** Underlying search engines must re-index; expect 4–12 weeks. What we measure weekly is trend.
- **No control over the model.** Each assistant uses a different search backend and changes without notice. Hence: probe several assistants, several runs per prompt, and read the weighted average, not a single answer.

## 5. Concrete example (Clínica NIDA, fertility, Vigo)

1. Onboarding: clinic, speciality, city, competitors (IVI Vigo, Vithas). Two minutes.
2. Prompt catalogue: ~30–40 real patient questions for fertility in Vigo, Spanish and Galician; clinic can add its own.
3. Weekly probe across ChatGPT, Gemini, Claude, Perplexity, several runs each, located in Vigo. Store full answer, clinics named, order, sources cited.
4. Dashboard: share of voice, position vs IVI, top-10 pages the LLMs cite for the sector.
5. Gap diagnosis: cross cited sources with NIDA's presence → "reproduccionasistida.org is the most cited source and your profile has no success rates or reviews", "for 'ovodonación Vigo' LLMs cite price pages and you have none", "your robots.txt blocks GPTBot".
6. Action plan: each gap becomes a prioritised task; some for the clinic, some for the agency, some drafted by the tool (price page draft, schema block ready to paste).
7. Re-measure the following week; typical movement window 4–12 weeks.
8. Attribution: tagged clicks + branded-search uplift + "how did you hear about us" → euros per month.
