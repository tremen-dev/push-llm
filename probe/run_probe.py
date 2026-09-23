"""Probe which Vigo/Pontevedra clinics the main assistants recommend.

Runs every prompt in prompts.csv N times against each configured provider,
counts brand mentions (brands.csv), and writes results.csv + summary.md.

Providers are enabled by the presence of their API key:
  ANTHROPIC_API_KEY  -> Claude (Anthropic SDK, web search tool on)
  OPENAI_API_KEY     -> ChatGPT (openai SDK, Responses API, web_search tool)
  GEMINI_API_KEY     -> Gemini (google-genai SDK, Google Search grounding)

    pip install anthropic openai google-genai
    python run_probe.py --runs 3 --providers claude,openai,gemini
"""
from __future__ import annotations

import argparse
import csv
import os
import re
import sys
import time
import unicodedata
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent
SYSTEM = (
    "Eres un asistente que ayuda a una persona que vive en Galicia a elegir "
    "una clínica. Responde como lo harías normalmente, nombrando clínicas "
    "concretas cuando puedas."
)
USER_LOCATION = {"type": "approximate", "city": "Vigo", "region": "Galicia",
                 "country": "ES", "timezone": "Europe/Madrid"}


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def load_brands():
    rows = list(csv.DictReader(open(HERE / "brands.csv", encoding="utf-8")))
    for r in rows:
        names = [r["brand"]] + [a for a in r["aliases"].split(";") if a]
        r["patterns"] = [norm(n) for n in names if len(norm(n)) >= 4]
    return rows


def mentions(text: str, brands):
    t = norm(text)
    return [b for b in brands if any(f" {p} " in f" {t} " for p in b["patterns"])]


# ---------------- providers ----------------

def ask_claude(prompt: str, model: str) -> str:
    import anthropic
    client = anthropic.Anthropic()
    messages = [{"role": "user", "content": prompt}]
    tools = [{"type": "web_search_20260209", "name": "web_search",
              "max_uses": 5, "user_location": USER_LOCATION}]
    for _ in range(4):  # resume pause_turn if the server tool loop pauses
        resp = client.messages.create(
            model=model, max_tokens=4000, system=SYSTEM,
            tools=tools, messages=messages,
            output_config={"effort": "low"},
        )
        if resp.stop_reason == "refusal":
            return "[refusal]"
        if resp.stop_reason != "pause_turn":
            break
        messages.append({"role": "assistant", "content": resp.content})
    return "\n".join(b.text for b in resp.content if b.type == "text")


def ask_openai(prompt: str, model: str) -> str:
    from openai import OpenAI
    client = OpenAI()
    resp = client.responses.create(
        model=model, instructions=SYSTEM, input=prompt,
        tools=[{"type": "web_search",
                "user_location": {"type": "approximate", "city": "Vigo",
                                  "region": "Galicia", "country": "ES"}}],
    )
    return resp.output_text


def ask_gemini(prompt: str, model: str) -> str:
    from google import genai
    from google.genai import types
    client = genai.Client()
    resp = client.models.generate_content(
        model=model, contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM,
            tools=[types.Tool(google_search=types.GoogleSearch())]),
    )
    return resp.text or ""


PROVIDERS = {
    "claude": (ask_claude, "ANTHROPIC_API_KEY", os.getenv("CLAUDE_MODEL", "claude-opus-5")),
    "openai": (ask_openai, "OPENAI_API_KEY", os.getenv("OPENAI_MODEL", "gpt-5")),
    "gemini": (ask_gemini, "GEMINI_API_KEY", os.getenv("GEMINI_MODEL", "gemini-2.5-flash")),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--providers", default="claude,openai,gemini")
    ap.add_argument("--only", default="", help="comma list of prompt ids")
    args = ap.parse_args()

    brands = load_brands()
    prompts = list(csv.DictReader(open(HERE / "prompts.csv", encoding="utf-8")))
    if args.only:
        keep = set(args.only.split(","))
        prompts = [p for p in prompts if p["id"] in keep]

    active = []
    for name in args.providers.split(","):
        fn, key, model = PROVIDERS[name]
        if os.getenv(key):
            active.append((name, fn, model))
        else:
            print(f"skip {name}: {key} not set", file=sys.stderr)
    if not active:
        sys.exit("no provider configured")

    out = open(HERE / "results.csv", "w", newline="", encoding="utf-8")
    w = csv.writer(out)
    w.writerow(["prompt_id", "specialty", "city", "provider", "run",
                "brands_mentioned", "directories_mentioned", "answer"])
    tally = defaultdict(lambda: defaultdict(int))     # provider -> brand -> n
    coverage = defaultdict(lambda: defaultdict(int))  # provider -> specialty -> answers with >=1 clinic
    total = defaultdict(lambda: defaultdict(int))

    for p in prompts:
        for name, fn, model in active:
            for run in range(1, args.runs + 1):
                try:
                    answer = fn(p["prompt"], model)
                except Exception as e:  # keep going, log the failure
                    answer = f"[error] {e}"
                hits = mentions(answer, brands)
                clinics = [b["brand"] for b in hits if b["type"] != "directory"]
                dirs = [b["brand"] for b in hits if b["type"] == "directory"]
                w.writerow([p["id"], p["specialty"], p["city"], name, run,
                            ";".join(clinics), ";".join(dirs), answer.replace("\n", " ")])
                out.flush()
                for b in hits:
                    tally[name][b["brand"]] += 1
                total[name][p["specialty"]] += 1
                if clinics:
                    coverage[name][p["specialty"]] += 1
                print(f"{p['id']} {name} r{run}: {clinics or '-'} | dirs {dirs or '-'}")
                time.sleep(0.5)

    with open(HERE / "summary.md", "w", encoding="utf-8") as s:
        s.write("# Resumo da sonda Vigo/Pontevedra\n\n")
        for name, _, model in active:
            s.write(f"## {name} ({model})\n\n")
            s.write("| Especialidade | Respostas con clínica nomeada | Total |\n|---|---|---|\n")
            for sp in sorted(total[name]):
                s.write(f"| {sp} | {coverage[name][sp]} | {total[name][sp]} |\n")
            s.write("\n| Marca | Mencións |\n|---|---|\n")
            for brand, n in sorted(tally[name].items(), key=lambda x: -x[1]):
                s.write(f"| {brand} | {n} |\n")
            s.write("\n")
    print("wrote results.csv and summary.md")


if __name__ == "__main__":
    main()
