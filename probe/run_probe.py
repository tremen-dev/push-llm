"""Probe which Vigo/Pontevedra clinics the main assistants recommend.

Runs every prompt in prompts.csv N times against each configured provider,
stores the raw answer plus usage/cost metadata per row in results.csv, and
writes summary.md with the offline analysis (see analysis.py).

Model ids, runs per provider, prices and weights: probe_config.json
(override the model with CLAUDE_MODEL / OPENAI_MODEL / GEMINI_MODEL).
Providers are enabled by the presence of their API key.
Output directory: --out, else $PUSHLLM_PRIVADO/probe, else probe/out (gitignored).

    python run_probe.py --only D01,E01,F01,O01 --runs 1   # smoke: 12 calls
    python run_probe.py                                   # full: 44 x 3 x 3
    python run_probe.py --resume                          # continue a cut run
    python run_probe.py --analyze                         # recount offline, no calls
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import analysis
import matching
import providers
import settings

HERE = Path(__file__).resolve().parent
COLUMNS = ["timestamp_utc", "prompt_id", "specialty", "city", "provider", "run", "model",
           "status", "input_tokens", "output_tokens", "web_searches", "cost_eur",
           "brands_mentioned", "directories_mentioned", "cited_urls", "answer"]


def output_dir(option: str | None, env) -> Path:
    if option:
        return Path(option)
    if env.get("PUSHLLM_PRIVADO"):
        return Path(env["PUSHLLM_PRIVADO"]) / "probe"
    return HERE / "out"


def parse_args(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs", type=int, default=None, help="runs per prompt (default: config per provider)")
    ap.add_argument("--providers", default="claude,openai,gemini")
    ap.add_argument("--only", default="", help="comma list of prompt ids")
    ap.add_argument("--out", default=None, help="output directory (default: $PUSHLLM_PRIVADO/probe or probe/out)")
    ap.add_argument("--config", default=None, help="config file (default: probe_config.json)")
    ap.add_argument("--resume", action="store_true",
                    help="append to existing results.csv; only call (prompt, provider, run) without a status=ok row")
    ap.add_argument("--analyze", action="store_true", help="recompute summary.md from results.csv; no provider calls")
    ap.add_argument("--sleep", type=float, default=0.5, help="seconds between calls")
    return ap.parse_args(argv)


def _blank(v):
    return "" if v is None else v


def write_summary(out: Path, cfg: dict, brands) -> None:
    res = analysis.analyze(analysis.read_results(out / "results.csv"), brands, cfg)
    (out / "summary.md").write_text(analysis.render_summary(res, cfg), encoding="utf-8")


def main(argv=None, env=None, ask=None):
    args = parse_args(argv)
    env = os.environ if env is None else env
    ask = ask or providers.ask
    cfg = settings.load_config(args.config)
    brands = matching.load_brands()
    out = output_dir(args.out, env)
    results = out / "results.csv"

    if args.analyze:
        if not results.exists():
            sys.exit(f"no results file at {results}")
        write_summary(out, cfg, brands)
        print(f"wrote {out / 'summary.md'}")
        return

    with open(HERE / "prompts.csv", encoding="utf-8") as f:
        prompts = list(csv.DictReader(f))
    if args.only:
        keep = set(args.only.split(","))
        prompts = [p for p in prompts if p["id"] in keep]

    active = []
    for name in args.providers.split(","):
        pcfg = cfg["providers"][name]
        if env.get(pcfg["api_key_env"]):
            active.append((name, settings.resolve_model(name, cfg, env), args.runs or pcfg["runs"]))
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

    with open(results, "a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        if new_file:
            w.writeheader()
        for p in prompts:
            for name, model, runs in active:
                for run in range(1, runs + 1):
                    if (p["id"], name, str(run)) in done:
                        continue
                    r = ask(name, p["prompt"], cfg, model)
                    hits = matching.find_mentions(r.text, brands, p["specialty"], p["city"])
                    clinics = [b["brand"] for b in hits if b["type"] != "directory"]
                    dirs = [b["brand"] for b in hits if b["type"] == "directory"]
                    answer = r.text if r.status != "error" else f"[error] {r.error}"
                    w.writerow({
                        "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "prompt_id": p["id"], "specialty": p["specialty"], "city": p["city"],
                        "provider": name, "run": run, "model": r.model or model, "status": r.status,
                        "input_tokens": _blank(r.input_tokens), "output_tokens": _blank(r.output_tokens),
                        "web_searches": _blank(r.web_searches),
                        "cost_eur": f"{providers.cost_eur(r, name, cfg):.6f}",
                        "brands_mentioned": ";".join(clinics), "directories_mentioned": ";".join(dirs),
                        "cited_urls": ";".join(r.cited_urls), "answer": answer,
                    })
                    fh.flush()
                    print(f"{p['id']} {name} r{run} [{r.status}]: {clinics or '-'} | dirs {dirs or '-'}")
                    if args.sleep:
                        time.sleep(args.sleep)

    write_summary(out, cfg, brands)
    print(f"wrote {results} and {out / 'summary.md'}")


if __name__ == "__main__":
    main()
