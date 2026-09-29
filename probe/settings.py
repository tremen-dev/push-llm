"""Probe configuration loader (SPEC-001 CA-1/CA-2; batches: SPEC-008 CA-3, ADR-003 §3-§4).

Model ids, runs per provider, prices and weights live in probe_config.json;
the env vars named in each provider's `model_env` override the model id.

A batch file (e.g. batches/viveiro.json) may declare `"extends": "<path>"`, relative to
itself: the base config is loaded first and every top-level key of the batch file replaces
the base one as a whole (shallow merge). So a batch overrides `user_location` and `batch`
and inherits providers, prices and currency from probe_config.json (single source).
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent / "probe_config.json"
BATCH_KEYS = ("name", "title", "prompt_prefixes", "local_cities", "brands", "output_subdir")


def load_config(path: str | Path | None = None) -> dict:
    path = Path(path or CONFIG_PATH)
    with open(path, encoding="utf-8") as f:
        cfg = json.load(f)
    base = cfg.pop("extends", None)
    if base:
        merged = load_config((path.parent / base).resolve())
        merged.update(cfg)
        cfg = merged
    return cfg


def batch(cfg: dict) -> dict:
    """The batch section: which prompts, local cities, member brands and output subdir."""
    b = cfg.get("batch")
    if not b:
        raise ValueError("probe config has no 'batch' section (SPEC-008 CA-3)")
    missing = [k for k in BATCH_KEYS if k not in b]
    if missing:
        raise ValueError(f"probe config batch {b.get('name')!r} lacks {', '.join(missing)}")
    return b


def prompt_matcher(batch_or_prefixes):
    """Callable id -> bool: id is one of the prefixes followed by digits (D01, AV01...)."""
    prefixes = (batch_or_prefixes["prompt_prefixes"] if isinstance(batch_or_prefixes, dict)
                else batch_or_prefixes)
    alternatives = "|".join(re.escape(p) for p in prefixes)
    pat = re.compile(rf"(?:{alternatives})\d+")
    return lambda pid: bool(pat.fullmatch(pid or ""))


def resolve_model(provider: str, cfg: dict, env=None) -> str:
    env = os.environ if env is None else env
    pcfg = cfg["providers"][provider]
    return env.get(pcfg["model_env"]) or pcfg["model"]
