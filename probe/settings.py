"""Probe configuration loader (SPEC-001 CA-1/CA-2).

Model ids, runs per provider, prices and weights live in probe_config.json;
the env vars named in each provider's `model_env` override the model id.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent / "probe_config.json"


def load_config(path: str | Path | None = None) -> dict:
    with open(path or CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


def resolve_model(provider: str, cfg: dict, env=None) -> str:
    env = os.environ if env is None else env
    pcfg = cfg["providers"][provider]
    return env.get(pcfg["model_env"]) or pcfg["model"]
