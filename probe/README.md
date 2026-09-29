# Probe kit (Cycle 0 baseline)

Runs every prompt of a **batch** in `prompts.csv` N times against each configured provider (web search on, user location of the batch; default batch: Vigo/Pontevedra), stores the raw answer and its usage/cost metadata per row in `results.csv`, and writes `summary.md` with the analysis against the hypothesis in `../03-local-market-vigo-pontevedra.md` §2.

## Files

- `run_probe.py` — CLI (probe, resume, offline analysis).
- `probe_config.json` — **configuration, not code**: model id per provider, runs per provider, prices (USD per M input/output tokens and per web search, with date and source), USD/EUR rate, usage weights (RN-04), web search tool version, effort. Values follow the **vigente** `sdd-probe` dictamen, the most recent dated one (today the SPEC-002 ledger, 2026-09-29; `tests/test_config.py` checks it). **Re-check each app's default model before every run.**
- `providers.py` (adapters), `matching.py` (RN-01 matching + RN-11 short acronyms), `analysis.py` (coverage, weighted aggregate, leader, directories), `settings.py` (config loader).
- `prompts.csv`: 44 prompts of the Vigo batch (es + gl) across dental, fertility, ophthalmology, aesthetic, physio, hospital, plus the 24 prompts of the Clínica Ártica pilot batch (`AV`, `AR`, `AG`; see *Batches*). `brands.csv`: clinics/hospitals and directories with aliases; which of them take part in a run is decided by the batch (columns `specialty, brand, city, type, aliases, exact_aliases`; see *Brand matching* below).
- `tests/` — offline tests (no keys, no network).

## Install (Windows PowerShell)

```powershell
cd probe
py -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
```

No `Activate.ps1` needed (avoids the PowerShell execution policy): call `.\.venv\Scripts\python` directly. Where this README writes `python run_probe.py`, PowerShell users can write `.\.venv\Scripts\python run_probe.py`.

bash: `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`.

## Keys and output directory — keys in the git-ignored `.env`, outputs outside the repo

Rule: ADR-006 (keys in a local `.env` ignored by git) and ADR-007 (`.env.example` is the only versioned `.env*`, a template with empty values). Raw outputs go to the private space of ADR-001 (`$PUSHLLM_PRIVADO/probe`), outside the repo.

**`.env` at the repo root (recommended).** Copy `.env.example` (repo root) to `.env` in the same folder and fill in `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY` (optionally `PUSHLLM_PRIVADO` and the `*_MODEL` overrides). `run_probe.py` loads that file by itself on start — no `Read-Host`, no PowerShell snippet:

- only `<repo root>/.env` is read (never `probe/.env`); no file → nothing changes;
- `NAME=value` per line; `#` comment lines, blank lines, `export NAME=value` and quoted values are accepted; a line with an empty value (`OPENAI_API_KEY=`) is not loaded;
- a variable already set in the session or the user environment is **never** overwritten: the session wins;
- values are never written to the console, `results.csv` or `summary.md`; only the names loaded are reported on stderr (`loaded from .env: … (values not shown)`).

Keep the `.env` content as a secure note in your password manager to move it to another machine; never by email, chat or an unencrypted synced folder (and keep the working tree out of such folders). No agent reads, opens or copies the `.env`. If a key leaks (git history, a log, a chat, an agent saw it): **revoke it** in its console and create a new one (ADR-006 §4–§6).

Checks before a real run (CA-1 of SPEC-002; no key values in any output), from the repo root:

```powershell
git check-ignore -v .env                 # must print a .gitignore rule
git log --all --oneline -- .env          # must be empty
git status --porcelain                   # must not list .env
git ls-files | Select-String '\.env'     # only .env.example
```

`PUSHLLM_PRIVADO` is a user environment variable on the usual machine. Commands that pass `--out "$env:PUSHLLM_PRIVADO\..."` need it in the session or user environment, because PowerShell expands it **before** Python reads the `.env` (if it is empty, the probe refuses the resulting `--out`). A `PUSHLLM_PRIVADO` set only in `.env` works for the commands without `--out`.

**Session only (alternative, no file).** PowerShell:

```powershell
$env:ANTHROPIC_API_KEY = Read-Host "Anthropic key"
$env:OPENAI_API_KEY    = Read-Host "OpenAI key"
$env:GEMINI_API_KEY    = Read-Host "Gemini key"
```

bash (`read -s` keeps them out of the shell history):

```bash
read -rs ANTHROPIC_API_KEY && export ANTHROPIC_API_KEY
read -rs OPENAI_API_KEY && export OPENAI_API_KEY
read -rs GEMINI_API_KEY && export GEMINI_API_KEY
export PUSHLLM_PRIVADO=/ruta/privada/fuera/del/repo
```

Output directory precedence: `--out DIR` > `$PUSHLLM_PRIVADO/<batch output_subdir>` (`probe` for the Vigo batch, `piloto-artica/probe` for the pilot batch) > `probe/out/` (gitignored fallback). Providers are enabled by the presence of their key. Model ids can be overridden per run with `CLAUDE_MODEL`, `OPENAI_MODEL`, `GEMINI_MODEL`.

## Commands

From `probe\` (PowerShell, venv installed as above, keys in the repo-root `.env`):

```powershell
# Offline check first (no keys, no network): all green
.\.venv\Scripts\python -m pytest -q tests

# Smoke: 4 prompts x 1 run x 3 providers = 12 calls (separate dir so the full run starts clean)
.\.venv\Scripts\python run_probe.py --only D01,E01,F01,O01 --runs 1 --out "$env:PUSHLLM_PRIVADO\probe-smoke"

# Full run: 44 prompts x 3 runs x 3 providers = 396 calls (runs per provider from probe_config.json)
.\.venv\Scripts\python run_probe.py

# Resume a cut run: only calls (prompt, provider, run) without a status=ok row; previous rows are kept
.\.venv\Scripts\python run_probe.py --resume

# Offline analysis: recount summary.md from results.csv with the current brands.csv, no provider calls
.\.venv\Scripts\python run_probe.py --analyze
```

Tests from the repo root: `python -m pytest probe/tests`. The same commands work in bash (`python run_probe.py …`, `--out "$PUSHLLM_PRIVADO/probe-smoke"`). Without `--resume`, the probe refuses to overwrite an existing `results.csv`.

## Batches (SPEC-008, ADR-003, ADR-005)

A batch is configuration, not code. The default config `probe_config.json` **is the Vigo/Pontevedra batch** (EPIC-001, SPEC-002): user location Vigo, local cities Vigo and Pontevedra, prompts `D`, `F`, `O`, `E`, `P`, `H`, its listed member brands, output `$PUSHLLM_PRIVADO/probe`. Running without `--config` behaves exactly as before.

`batches/viveiro.json` is the **Clínica Ártica pilot batch**. It `extends` `probe_config.json` (models, prices, weights and currency are inherited) and replaces `user_location` (Viveiro, Galicia, ES) and `batch`:

- prompts: ids `AVnn` (core: Viveiro and A Mariña), `ARnn` (area of influence) and `AGnn` (Galicia), the same ids and literal texts as `docs/piloto-artica/prompts-baseline.md`; the level is the id prefix. Brand questions `AM` are not in the probe.
- brands: only those listed in `batch.brands` take part (membership, not city). Pilot competitors based in Vigo or Pontevedra are listed there and **not** in the Vigo batch, so they never change the Vigo results.
- `summary.md` reports each level apart: the client's answers per provider, the weighted SoV (RN-03) of `AV` computed only with `AV` rows, the weighted SoV of `AR` computed only with `AR` rows (only when the measurement has the 3 runs of the Go design; otherwise counts only) and only "x of n" counts for `AG`. No figure adds up levels (ADR-005 §4, ADR-009 §2).
- The Go of the pilot (ADR-009; SPEC-008 CA-11 dictamen, `batch.go`) is three yes/no conditions, reported apart: **(C) grow** in `AR` (weighted SoV of `AR` against its CA-12 "before": ≥ +12 pts in **each** of the two "after" measurements, and still > 0 leaving out any single `AR` question), **(D) defend** `AV` (a significant drop is ≥ 10 pts below the official baseline in **both** "after" measurements) and **(A)** ≥ 1 attributed patient (outside the probe). `analysis.growth_verdict`, `analysis.defense_verdict` and `analysis.render_go_verdict` compute them from the `analysis.analyze` result of each measurement (the offline command that runs them is SPEC-012 work).
- runs: per level in `batch.levels` (`AV` 3, `AR` 3, `AG` 1). The official baseline (2026-09-29) ran with `AR` 1, so it is **not** the base of (C): the base is the `AR` "before" of CA-12 (`--levels AR`, 3 runs). Each Go "after" measurement is `--levels AV,AR` (same 3 runs on both levels). `--runs N` overrides every selected level (tracking: `--levels AV --runs 1` weekly, `--levels AR,AG --runs 1` every 4 weeks; tracking figures are never compared with the Go measurements).
- Go measurements (`batch.go`, SPEC-008 CA-9/CA-10/CA-11): the `AV` section of `summary.md` also gives the weighted core SoV per run, per question × provider stability, whether the measurement is complete for condition (D) (every weighted provider with ≥ 90 % of its `AV` rows `ok`; otherwise `--resume` the same week) and a **ceiling warning** when the weighted core SoV is ≥ 85 % (decided by the human on 2026-09-29, ADR-009). The `AR` section says whether the measurement is complete for condition (C). `AR`/`AG` list the question × provider cells naming the client. Answers naming the client only through the bare alias "Ártica" still count (RN-01) and are listed for manual review. A "served models" table closes the summary (D-5/RN-10).
- `summary.md` ends with "observations to review by hand": sentences naming a clinic next to "sin médico", "esteticista", "no sanitario"… (`batch.review_terms`). Not a metric.
- output: `$PUSHLLM_PRIVADO/piloto-artica/probe/` (private, ADR-001/ADR-004).

`--only` must name prompts of the chosen batch; other ids are refused. `--out` empty or a drive root (e.g. `PUSHLLM_PRIVADO` unset) is refused. Order (SPEC-008 ledger, "Instrucciones para el humano (CA-7)"): smoke → official baseline, whose start **freezes the question set** (SPEC-007 CA-8) → ceiling warning check (decided on 2026-09-29, ADR-009) → `AR` "before" (CA-12) → first pilot action. The baseline does not wait for any manual pass. It must start in a new directory: `--resume` refuses a `results.csv` written before SPEC-013 (no `searched_urls` column). From `probe/` (PowerShell, keys in the repo-root `.env`, `PUSHLLM_PRIVADO` set as a user variable):

```powershell
# Pilot smoke: one prompt per level x 1 run x 3 providers = 9 calls (new directory)
.\.venv\Scripts\python run_probe.py --config batches/viveiro.json --only AV01,AR01,AG01 --runs 1 --out "$env:PUSHLLM_PRIVADO\piloto-artica\probe-smoke-spec013"

# AR "before" of condition (C) (SPEC-008 CA-12): AR 5 prompts x 3 runs x 3 providers = 45 calls, new directory
.\.venv\Scripts\python run_probe.py --config batches/viveiro.json --levels AR --runs 3 --out "$env:PUSHLLM_PRIVADO\piloto-artica\probe-AR-antes"

# Each Go "after" measurement (SPEC-012): AV and AR with 3 runs, 60 prompt-runs x 3 providers = 180 calls, dated directory
.\.venv\Scripts\python run_probe.py --config batches/viveiro.json --levels AV,AR --out "$env:PUSHLLM_PRIVADO\piloto-artica\probe-go-AAAA-MM-DD"

# Tracking every 4 weeks (SPEC-012): AR/AG with 1 run, 9 prompt-runs x 3 providers = 27 calls
.\.venv\Scripts\python run_probe.py --config batches/viveiro.json --levels AR,AG --runs 1 --out "$env:PUSHLLM_PRIVADO\piloto-artica\probe-AAAA-MM-DD"

# Offline recount of the pilot batch (no calls)
.\.venv\Scripts\python run_probe.py --config batches/viveiro.json --analyze
```

## Output

`results.csv`, one row per call: `timestamp_utc, prompt_id, specialty, city, provider, run, model` (served model if the API exposes it, else configured), `status` (ok / error / refusal / empty), `input_tokens, output_tokens, web_searches` (blank if not exposed), `cost_eur` (from config prices), `brands_mentioned, directories_mentioned, cited_urls` (`;`-separated), `answer` (raw text; with Claude, consecutive text blocks are joined without separator and text spans split by a search or a `pause_turn` by a blank line), `searched_urls` (`;`-separated, last column since SPEC-013).

**Consulted vs cited URLs (SPEC-013, 2026-09-29), same meaning for the three providers.** `searched_urls` = the pages the provider declares it retrieved with the search for that answer; `cited_urls` = the ones it links to a piece of the answer text. Both deduplicated, in order of appearance, empty on `status=error`; a cited URL is also in `searched_urls` when the provider gives both (exception: an OpenAI citation to a URL outside its `sources` stays only in `cited_urls`). Only `cited_urls` counts for source citation weight (07 §4, RN-04, RN-08).

| Provider | `searched_urls` | `cited_urls` |
|---|---|---|
| Claude | `url` of every `web_search_result` of every top-level `web_search_tool_result` (with or without `caller`, all turns). With dynamic filtering (`web_search_20260209`) these are the results *before* the filter | `url` of the citations of the `text` blocks (often none with dynamic filtering) |
| OpenAI | `url` of every `web_search_call.action.sources` entry, requested with `include=["web_search_call.action.sources"]` (the only request change; `oai-*` feed entries have no URL and stay only in `raw_responses.jsonl`) | `url_citation` annotations |
| Gemini | `web.uri` of every `grounding_chunks` entry | `web.uri` of the chunks referenced by some `grounding_supports[].grounding_chunk_indices` (out-of-range indices ignored) |

Gemini URIs are `https://vertexaisearch.cloud.google.com/…` **redirects, stored as they are** (not resolved: that would mean extra HTTP requests to third-party sites; `raw_responses.jsonl` keeps `uri` and `title` to resolve them later, F-SPEC-001-2). Until then Gemini URLs **cannot be compared by domain** with Claude or OpenAI; counts (how many consulted, how many cited) can.

**Change of meaning of Gemini `cited_urls` (SPEC-013, 2026-09-29):** before, it held every grounding chunk (i.e. consulted URLs); now it holds only the cited ones. Files written before SPEC-013 (their header has no `searched_urls`) keep the old meaning: `--analyze` still works on them and gives the same `summary.md` (it reads no URL), but **`--resume` refuses them** (exit with error, no call, no file touched) so that one file never mixes both meanings; use `--out` with a new directory.

`raw_responses.jsonl` (SPEC-013 CA-1), next to `results.csv`: one JSON line per call, appended as each call ends (`--resume` only appends; `--analyze` never reads or touches it). Fields: `timestamp_utc, prompt_id, provider, run, model` (same values as the call's row in `results.csv`, to join them), `status`, `error` (message when `status=error`), `request` (parameters sent: model, `tools`, `system`/`instructions`/`config`, `max_tokens`, effort and the question as `prompt`; never the client or its credentials) and `responses`: every SDK response of the call, one per turn (Claude `pause_turn` continuations included), as full JSON, nothing trimmed (`encrypted_content` and `encrypted_index` are kept, so a line weighs tens of KB). An error line has `responses: []`. No HTTP headers or keys: keys named `headers`, `sdk_http_response` (Gemini), `api_key`, `authorization` or `x-api-key` are dropped at any depth. **Private data (ADR-001, ADR-004 §2)**: it contains the raw answers, so it lives only in `$PUSHLLM_PRIVADO` (or the git-ignored `probe/out/`) and is never committed or copied into the repo.

`summary.md`: per specialty × provider, valid answers (status=ok only), answers naming ≥ 1 local clinic and %, excluded rows by status; weighted aggregate (RN-03/RN-04, normalised to the providers probed); per specialty, the leading brand of that specialty and its % of answers; directory mentions; answers where only a < 4-char alias (e.g. "MIA", or "ivi" in lower case) appeared, which RN-01 does not count, next to the list of active `exact_aliases` that do count (RN-11/ADR-002); estimated cost. Definitions: `sdd-metricas` dictamen in the SPEC-001 ledger.

## Brand matching (RN-01, RN-11)

- `aliases` (`;`-separated): compared on normalised text (no accents, no case), whole words; only names/aliases of ≥ 4 characters count (RN-01).
- `exact_aliases` (`;`-separated): short unambiguous acronyms, exception RN-11 / `docs/adr/ADR-002-excepcion-a-rn-01-para-siglas-cortas-inequivocas.md`. Each entry must be 2–3 characters, only uppercase A–Z or digits, and not a name, alias or acronym of any other brand; otherwise loading `brands.csv` fails with an error naming the brand and the acronym. They are matched on the raw answer text, case-sensitively and as a whole word (not glued to a letter, accented or not, or to a digit): `IVI`, `(IVI)`, `IVI.`, `IVI-RMA` count; `ivi`, `Ivi`, `IVIS`, `XIVI`, `IVI2` do not. A match counts as a mention of its brand like any other. An acronym listed in `exact_aliases` is not also listed in `aliases`. A `brands.csv` without the column still loads.
- Today only `IVI` → IVI Vigo. `MIA` (Clínica MIA) stays in `aliases` and does not count ("mía" is a common word); it is reported in the RN-01 bias section of `summary.md`. Adding a new acronym requires citing ADR-002 (§6).

## Caveats

- API + search tool approximates the consumer app, it is not identical (`../06-models-costs-and-usage-share.md` §1A).
- Gemini's Google Search grounding has no user-location parameter; location comes from the prompt text only. Gemini cited URLs are `vertexaisearch.cloud.google.com` redirects.
- Google AI Overviews and Perplexity are not covered.
