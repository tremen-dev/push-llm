# Probe kit (Cycle 0 baseline)

Runs every prompt in `prompts.csv` N times against each configured provider, counts brand mentions from `brands.csv`, and writes `results.csv` + `summary.md`.

```bash
pip install anthropic openai google-genai
export ANTHROPIC_API_KEY=... OPENAI_API_KEY=... GEMINI_API_KEY=...
python run_probe.py --runs 3                     # all providers with a key set
python run_probe.py --providers openai --only D01,F01,O01   # quick smoke
```

- Providers are enabled by the presence of their key. Model ids default to mid-tier per `../06-models-costs-and-usage-share.md` and can be overridden with `CLAUDE_MODEL`, `OPENAI_MODEL`, `GEMINI_MODEL`.
- Web search is enabled on every provider with user location set to Vigo, Galicia.
- `prompts.csv`: id, speciality, city, intent, prompt (es + gl). 44 prompts across dental, fertility, ophthalmology, aesthetic, physio, hospital.
- `brands.csv`: 43 clinics/hospitals + 9 directories with aliases; matching is accent/case-insensitive.
- Full run: 44 × 3 × 3 = 396 calls, ~15–30 €.
- Google AI Overviews is not yet covered; add an adapter before Cycle 3.

Output to read: per provider, share of answers naming at least one local clinic per speciality; mention count per brand; directory-vs-clinic citation pattern. Compare against the hypothesis in `../03-local-market-vigo-pontevedra.md` §2.
