"""Probe which Vigo/Pontevedra clinics the main assistants recommend.

Runs every prompt in prompts.csv N times against each configured provider,
stores the raw answer plus usage/cost metadata per row in results.csv, appends the full
raw SDK responses of every call to raw_responses.jsonl (private data, ADR-001; no headers
or keys) and writes summary.md with the offline analysis (see analysis.py).

Model ids, runs per provider, prices and weights: probe_config.json
(override the model with CLAUDE_MODEL / OPENAI_MODEL / GEMINI_MODEL).
Providers are enabled by the presence of their API key.
Keys: session/user environment, or a .env at the repo root (git-ignored, ADR-006/ADR-007;
template .env.example). The .env is loaded when present; it never overrides a variable
already set in the environment, empty values are skipped and values are never printed.
Output directory: --out, else $PUSHLLM_PRIVADO/<batch output_subdir>, else probe/out
(gitignored). Batches (SPEC-008, ADR-003): the default config is the Vigo/Pontevedra
batch; --config batches/viveiro.json runs the Clinica Artica pilot batch (AV/AR/AG
prompts, Viveiro location, its member brands, $PUSHLLM_PRIVADO/piloto-artica/probe).

    python run_probe.py --only D01,E01,F01,O01 --runs 1   # smoke: 12 calls
    python run_probe.py                                   # full: 44 x 3 x 3
    python run_probe.py --resume                          # continue a cut run
    python run_probe.py --analyze                         # recount offline, no calls
    python run_probe.py --config batches/viveiro.json     # pilot batch: 24 x 3 x 3
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath, PureWindowsPath

import analysis
import matching
import providers
import settings

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
DOTENV_NAME = ".env"
DOTENV_PATH = REPO_ROOT / DOTENV_NAME
_DOTENV_LINE = re.compile(r"^(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*?)\s*$")
COLUMNS = ["timestamp_utc", "prompt_id", "specialty", "city", "provider", "run", "model",
           "status", "input_tokens", "output_tokens", "web_searches", "cost_eur",
           "brands_mentioned", "directories_mentioned", "cited_urls", "answer"]
RAW_NAME = "raw_responses.jsonl"  # SPEC-013 CA-1: private raw responses, next to results.csv


def parse_dotenv(text: str) -> dict[str, str]:
    """Minimal NAME=value parser (F-SPEC-002-1): full-line # comments, blank lines, optional
    `export ` and matching quotes. Lines that do not parse and empty values are skipped."""
    out = {}
    for line in text.lstrip("\ufeff").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = _DOTENV_LINE.match(line)
        if not m:
            continue
        name, value = m.groups()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        if value:
            out[name] = value
    return out


def load_dotenv(path: Path, env) -> list[str]:
    """Copy the .env values into env for names not already in env; returns the names set.
    No file: nothing happens. Values are never printed or returned."""
    try:
        text = Path(path).read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        return []
    loaded = []
    for name, value in parse_dotenv(text).items():
        if name not in env:
            env[name] = value
            loaded.append(name)
    return loaded


def output_dir(option: str | None, env, batch: dict | None = None) -> Path:
    sub = (batch or {}).get("output_subdir", "probe")
    if option:
        return Path(option)
    if env.get("PUSHLLM_PRIVADO"):
        return Path(env["PUSHLLM_PRIVADO"]) / sub
    return HERE / "out" if sub == "probe" else HERE / "out" / sub


def unsafe_out(option: str, windows: bool = os.name == "nt") -> bool:
    """True for an --out that is empty, a drive or filesystem root, or (Windows) rooted
    without a drive, e.g. "$env:PUSHLLM_PRIVADO\\x" with the variable empty -> "\\x"."""
    s = (option or "").strip()
    if not s:
        return True
    p = PureWindowsPath(s) if windows else PurePosixPath(s)
    if windows and p.root and not p.drive:
        return True
    return bool(p.anchor) and len(p.parts) <= 1


def level_runs(batch: dict) -> dict[str, int]:
    """Runs per level prefix declared in the batch (SPEC-008 CA-5); empty if none."""
    return {lv["prefix"]: lv["runs"] for lv in batch.get("levels", []) if lv.get("runs")}


def batch_prompts(prompts: list[dict], batch: dict) -> list[dict]:
    """Prompts whose id is one of the batch prefixes followed by digits (e.g. D01, AV01)."""
    in_batch = settings.prompt_matcher(batch)
    return [p for p in prompts if in_batch(p["id"])]


def parse_args(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs", type=int, default=None, help="runs per prompt (default: config per provider)")
    ap.add_argument("--providers", default="claude,openai,gemini")
    ap.add_argument("--only", default="", help="comma list of prompt ids")
    ap.add_argument("--levels", default="",
                    help="comma list of level prefixes of a level batch (e.g. AV or AR,AG)")
    ap.add_argument("--out", default=None, help="output directory (default: $PUSHLLM_PRIVADO/probe or probe/out)")
    ap.add_argument("--config", default=None,
                    help="config or batch file (default: probe_config.json = Vigo batch)")
    ap.add_argument("--resume", action="store_true",
                    help="append to existing results.csv; only call (prompt, provider, run) without a status=ok row")
    ap.add_argument("--analyze", action="store_true", help="recompute summary.md from results.csv; no provider calls")
    ap.add_argument("--sleep", type=float, default=0.5, help="seconds between calls")
    return ap.parse_args(argv)


def _blank(v):
    return "" if v is None else v


def raw_line(row: dict, r) -> str:
    """One JSON line of raw_responses.jsonl for the call that produced `row`."""
    rec = {"timestamp_utc": row["timestamp_utc"], "prompt_id": row["prompt_id"],
           "provider": row["provider"], "run": row["run"], "model": row["model"],
           "status": r.status, "error": r.error, "request": r.request, "responses": r.responses}
    return json.dumps(providers.scrub(rec), ensure_ascii=False, separators=(",", ":")) + "\n"


def write_summary(out: Path, cfg: dict, brands) -> None:
    res = analysis.analyze(analysis.read_results(out / "results.csv"), brands, cfg)
    (out / "summary.md").write_text(analysis.render_summary(res, cfg), encoding="utf-8")


def main(argv=None, env=None, ask=None, dotenv=None):
    args = parse_args(argv)
    if args.out is not None and unsafe_out(args.out):
        sys.exit(f"refusing --out {args.out!r}: empty or a drive/filesystem root "
                 "(is PUSHLLM_PRIVADO set?)")
    if dotenv is None and env is None:
        dotenv = DOTENV_PATH  # only a real run reads the repo-root .env
    env = os.environ if env is None else env
    if dotenv is not None:
        loaded = load_dotenv(dotenv, env)
        if loaded:
            print(f"loaded from {DOTENV_NAME}: {', '.join(sorted(loaded))} (values not shown)",
                  file=sys.stderr)
    ask = ask or providers.ask
    cfg = settings.load_config(args.config)
    batch = settings.batch(cfg)
    brands = matching.batch_brands(matching.load_brands(), batch["brands"])
    out = output_dir(args.out, env, batch)
    results = out / "results.csv"

    if args.analyze:
        if not results.exists():
            sys.exit(f"no results file at {results}")
        write_summary(out, cfg, brands)
        print(f"wrote {out / 'summary.md'}")
        return

    with open(HERE / "prompts.csv", encoding="utf-8") as f:
        prompts = batch_prompts(list(csv.DictReader(f)), batch)
    if args.only:
        keep = set(args.only.split(","))
        outside = sorted(keep - {p["id"] for p in prompts})
        if outside:
            sys.exit(f"not in batch {batch['name']}: {','.join(outside)}")
        prompts = [p for p in prompts if p["id"] in keep]
    per_level = level_runs(batch)
    if args.levels:
        wanted = set(args.levels.split(","))
        known = {lv["prefix"] for lv in batch.get("levels", [])}
        if not known or wanted - known:
            sys.exit(f"--levels {args.levels}: batch {batch['name']} has levels "
                     f"{','.join(sorted(known)) or 'none'}")
        match = settings.prompt_matcher(sorted(wanted))
        prompts = [p for p in prompts if match(p["id"])]

    active = []
    for name in args.providers.split(","):
        pcfg = cfg["providers"][name]
        if env.get(pcfg["api_key_env"]):
            active.append((name, settings.resolve_model(name, cfg, env), pcfg["runs"]))
        else:
            print(f"skip {name}: {pcfg['api_key_env']} not set", file=sys.stderr)
    if not active:
        sys.exit("no provider configured")

    done = set()
    if results.exists():
        if not args.resume:
            sys.exit(f"{results} exists: use --resume to continue it or --out for a new directory")
        done = {(r["prompt_id"], r["provider"], r["run"]) for r in analysis.read_results(results)
                if r.get("status") == "ok"}
    out.mkdir(parents=True, exist_ok=True)
    new_file = not results.exists()

    with open(results, "a", newline="", encoding="utf-8") as fh, \
            open(out / RAW_NAME, "a", encoding="utf-8", newline="\n") as raw:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        if new_file:
            w.writeheader()
        for p in prompts:
            level = next((k for k in per_level if settings.prompt_matcher([k])(p["id"])), None)
            for name, model, default_runs in active:
                runs = args.runs or per_level.get(level) or default_runs
                for run in range(1, runs + 1):
                    if (p["id"], name, str(run)) in done:
                        continue
                    r = ask(name, p["prompt"], cfg, model)
                    hits = matching.find_mentions(r.text, brands, p["specialty"], p["city"])
                    clinics = [b["brand"] for b in hits if b["type"] != "directory"]
                    dirs = [b["brand"] for b in hits if b["type"] == "directory"]
                    answer = r.text if r.status != "error" else f"[error] {r.error}"
                    row = {
                        "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "prompt_id": p["id"], "specialty": p["specialty"], "city": p["city"],
                        "provider": name, "run": run, "model": r.model or model, "status": r.status,
                        "input_tokens": _blank(r.input_tokens), "output_tokens": _blank(r.output_tokens),
                        "web_searches": _blank(r.web_searches),
                        "cost_eur": f"{providers.cost_eur(r, name, cfg):.6f}",
                        "brands_mentioned": ";".join(clinics), "directories_mentioned": ";".join(dirs),
                        "cited_urls": ";".join(r.cited_urls), "answer": answer,
                    }
                    w.writerow(row)
                    fh.flush()
                    raw.write(raw_line(row, r))
                    raw.flush()
                    print(f"{p['id']} {name} r{run} [{r.status}]: {clinics or '-'} | dirs {dirs or '-'}")
                    if args.sleep:
                        time.sleep(args.sleep)

    write_summary(out, cfg, brands)
    print(f"wrote {results} and {out / 'summary.md'}")


if __name__ == "__main__":
    main()
