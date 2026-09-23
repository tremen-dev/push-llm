# Probe kit (Cycle 0 baseline)

Runs every prompt in `prompts.csv` N times against each configured provider (web search on, user location Vigo), stores the raw answer and its usage/cost metadata per row in `results.csv`, and writes `summary.md` with the analysis against the hypothesis in `../03-local-market-vigo-pontevedra.md` §2.

## Files

- `run_probe.py` — CLI (probe, resume, offline analysis).
- `probe_config.json` — **configuration, not code**: model id per provider, runs per provider, prices (USD per M input/output tokens and per web search, with date and source), USD/EUR rate, usage weights (RN-04), web search tool version, effort. Values follow the `sdd-probe` dictamen in the SPEC-001 ledger. **Re-check each app's default model before every run.**
- `providers.py` (adapters), `matching.py` (RN-01 matching + RN-11 short acronyms), `analysis.py` (coverage, weighted aggregate, leader, directories), `settings.py` (config loader).
- `prompts.csv`: 44 prompts (es + gl) across dental, fertility, ophthalmology, aesthetic, physio, hospital. `brands.csv`: 43 clinics/hospitals + 9 directories with aliases (columns `specialty, brand, city, type, aliases, exact_aliases`; see *Brand matching* below).
- `tests/` — offline tests (no keys, no network).

## Install (Windows PowerShell)

```powershell
cd probe
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

bash: `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`.

## Keys and output directory — never in a repo file

Keys live only in the shell session (or your user environment), never in a file inside the repo. Raw outputs go to the private space of ADR-001 (`$PUSHLLM_PRIVADO/probe`), outside the repo.

PowerShell (current session only):

```powershell
$env:ANTHROPIC_API_KEY = Read-Host "Anthropic key"
$env:OPENAI_API_KEY    = Read-Host "OpenAI key"
$env:GEMINI_API_KEY    = Read-Host "Gemini key"
$env:PUSHLLM_PRIVADO   = "D:\ruta\privada\fuera\del\repo"
```

bash (current session only; `read -s` keeps them out of the shell history):

```bash
read -rs ANTHROPIC_API_KEY && export ANTHROPIC_API_KEY
read -rs OPENAI_API_KEY && export OPENAI_API_KEY
read -rs GEMINI_API_KEY && export GEMINI_API_KEY
export PUSHLLM_PRIVADO=/ruta/privada/fuera/del/repo
```

Output directory precedence: `--out DIR` > `$PUSHLLM_PRIVADO/probe` > `probe/out/` (gitignored fallback). Providers are enabled by the presence of their key. Model ids can be overridden per run with `CLAUDE_MODEL`, `OPENAI_MODEL`, `GEMINI_MODEL`.

## Commands

```powershell
# Smoke: 4 prompts x 1 run x 3 providers = 12 calls (separate dir so the full run starts clean)
python run_probe.py --only D01,E01,F01,O01 --runs 1 --out "$env:PUSHLLM_PRIVADO\probe-smoke"

# Full run: 44 prompts x 3 runs x 3 providers = 396 calls (runs per provider from probe_config.json)
python run_probe.py

# Resume a cut run: only calls (prompt, provider, run) without a status=ok row; previous rows are kept
python run_probe.py --resume

# Offline analysis: recount summary.md from results.csv with the current brands.csv, no provider calls
python run_probe.py --analyze

# Tests (from the repo root)
python -m pytest probe/tests
```

The same commands work in bash (`--out "$PUSHLLM_PRIVADO/probe-smoke"`). Without `--resume`, the probe refuses to overwrite an existing `results.csv`.

## Output

`results.csv`, one row per call: `timestamp_utc, prompt_id, specialty, city, provider, run, model` (served model if the API exposes it, else configured), `status` (ok / error / refusal / empty), `input_tokens, output_tokens, web_searches` (blank if not exposed), `cost_eur` (from config prices), `brands_mentioned, directories_mentioned, cited_urls` (`;`-separated), `answer` (raw text).

`summary.md`: per specialty × provider, valid answers (status=ok only), answers naming ≥ 1 local clinic and %, excluded rows by status; weighted aggregate (RN-03/RN-04, normalised to the providers probed); per specialty, the leading brand of that specialty and its % of answers; directory mentions; answers where only a < 4-char alias (e.g. "MIA", or "ivi" in lower case) appeared, which RN-01 does not count, next to the list of active `exact_aliases` that do count (RN-11/ADR-002); estimated cost. Definitions: `sdd-metricas` dictamen in the SPEC-001 ledger.

## Brand matching (RN-01, RN-11)

- `aliases` (`;`-separated): compared on normalised text (no accents, no case), whole words; only names/aliases of ≥ 4 characters count (RN-01).
- `exact_aliases` (`;`-separated): short unambiguous acronyms, exception RN-11 / `docs/adr/ADR-002-excepcion-a-rn-01-para-siglas-cortas-inequivocas.md`. Each entry must be 2–3 characters, only uppercase A–Z or digits, and not a name, alias or acronym of any other brand; otherwise loading `brands.csv` fails with an error naming the brand and the acronym. They are matched on the raw answer text, case-sensitively and as a whole word (not glued to a letter, accented or not, or to a digit): `IVI`, `(IVI)`, `IVI.`, `IVI-RMA` count; `ivi`, `Ivi`, `IVIS`, `XIVI`, `IVI2` do not. A match counts as a mention of its brand like any other. An acronym listed in `exact_aliases` is not also listed in `aliases`. A `brands.csv` without the column still loads.
- Today only `IVI` → IVI Vigo. `MIA` (Clínica MIA) stays in `aliases` and does not count ("mía" is a common word); it is reported in the RN-01 bias section of `summary.md`. Adding a new acronym requires citing ADR-002 (§6).

## Caveats

- API + search tool approximates the consumer app, it is not identical (`../06-models-costs-and-usage-share.md` §1A).
- Gemini's Google Search grounding has no user-location parameter; location comes from the prompt text only. Gemini cited URLs are `vertexaisearch.cloud.google.com` redirects.
- Google AI Overviews and Perplexity are not covered.
