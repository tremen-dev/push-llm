"""Provider adapters for the probe (SPEC-001 CA-3).

Each adapter takes the prompt, the loaded config, the model id and an optional
SDK client (injected by tests; created lazily otherwise) and returns a
ProviderResult with the answer text plus the metadata written on every row:
served model, tokens, web searches, cited URLs and a status in
{ok, error, refusal, empty}. Model ids and prices come from probe_config.json.
"""
from __future__ import annotations

from dataclasses import dataclass, field

SYSTEM = (
    "Eres un asistente que ayuda a una persona que vive en Galicia a elegir "
    "una clínica. Responde como lo harías normalmente, nombrando clínicas "
    "concretas cuando puedas."
)
MAX_PAUSE_TURNS = 4
GEMINI_REFUSAL_REASONS = {"SAFETY", "PROHIBITED_CONTENT", "BLOCKLIST", "SPII", "RECITATION",
                          "IMAGE_SAFETY"}
STATUSES = ("ok", "error", "refusal", "empty")


@dataclass
class ProviderResult:
    status: str
    text: str = ""
    model: str = ""
    input_tokens: int | None = None
    output_tokens: int | None = None
    web_searches: int | None = None
    cited_urls: list[str] = field(default_factory=list)
    error: str = ""


def _dedupe(urls):
    seen, out = set(), []
    for u in urls:
        if u and u not in seen:
            seen.add(u)
            out.append(u)
    return out


def _status_for_text(text: str) -> str:
    return "ok" if text.strip() else "empty"


def _location(cfg: dict) -> dict:
    return {"type": "approximate", **cfg["user_location"]}


# ---------------- Claude ----------------

def _claude(prompt, cfg, model, client):
    if client is None:
        import anthropic
        client = anthropic.Anthropic()
    pcfg = cfg["providers"]["claude"]
    tools = [{"type": pcfg["web_search_tool"], "name": "web_search",
              "max_uses": pcfg["max_searches"], "user_location": _location(cfg)}]
    kwargs = {}
    if pcfg.get("effort"):
        kwargs["output_config"] = {"effort": pcfg["effort"]}
    messages = [{"role": "user", "content": prompt}]
    texts, urls = [], []
    tin = tout = searches = 0
    served = None
    for _ in range(MAX_PAUSE_TURNS):
        resp = client.messages.create(model=model, max_tokens=pcfg["max_tokens"], system=SYSTEM,
                                      tools=tools, messages=messages, **kwargs)
        served = getattr(resp, "model", None) or served
        usage = resp.usage
        tin += usage.input_tokens or 0
        tout += usage.output_tokens or 0
        stu = getattr(usage, "server_tool_use", None)
        searches += (getattr(stu, "web_search_requests", 0) or 0) if stu else 0
        for block in resp.content:
            if block.type == "text":
                texts.append(block.text)
                for c in getattr(block, "citations", None) or []:
                    urls.append(getattr(c, "url", None))
        if resp.stop_reason == "refusal":
            return ProviderResult("refusal", "\n".join(texts), served or model, tin, tout,
                                  searches, _dedupe(urls))
        if resp.stop_reason != "pause_turn":
            break
        messages.append({"role": "assistant", "content": resp.content})
    text = "\n".join(t for t in texts if t)
    return ProviderResult(_status_for_text(text), text, served or model, tin, tout, searches,
                          _dedupe(urls))


# ---------------- OpenAI ----------------

def _openai(prompt, cfg, model, client):
    if client is None:
        from openai import OpenAI
        client = OpenAI()
    pcfg = cfg["providers"]["openai"]
    loc = _location(cfg)
    kwargs = {}
    if pcfg.get("effort"):
        kwargs["reasoning"] = {"effort": pcfg["effort"]}
    resp = client.responses.create(model=model, instructions=SYSTEM, input=prompt,
                                   tools=[{"type": pcfg["web_search_tool"], "user_location": loc}],
                                   **kwargs)
    searches, urls, refused = 0, [], False
    for item in resp.output or []:
        if item.type == "web_search_call":
            action = getattr(item, "action", None)
            if action is None or getattr(action, "type", "search") == "search":
                searches += 1
        elif item.type == "message":
            for part in item.content or []:
                if part.type == "refusal":
                    refused = True
                for a in getattr(part, "annotations", None) or []:
                    if a.type == "url_citation":
                        urls.append(a.url)
    text = resp.output_text or ""
    usage = resp.usage
    status = "refusal" if refused else _status_for_text(text)
    return ProviderResult(status, text, getattr(resp, "model", None) or model,
                          usage.input_tokens, usage.output_tokens, searches, _dedupe(urls))


# ---------------- Gemini ----------------

def _enum_name(x) -> str:
    return getattr(x, "name", None) or str(x).split(".")[-1]


def _gemini(prompt, cfg, model, client):
    if client is None:
        from google import genai
        client = genai.Client()
    pcfg = cfg["providers"]["gemini"]
    config = {"system_instruction": SYSTEM, "tools": [{pcfg["web_search_tool"]: {}}]}
    resp = client.models.generate_content(model=model, contents=prompt, config=config)
    um = resp.usage_metadata
    tin = (um.prompt_token_count or 0) + (getattr(um, "tool_use_prompt_token_count", 0) or 0)
    tout = (um.candidates_token_count or 0) + (getattr(um, "thoughts_token_count", 0) or 0)
    served = getattr(resp, "model_version", None) or model
    feedback = getattr(resp, "prompt_feedback", None)
    cands = resp.candidates or []
    searches, urls = None, []
    gm = getattr(cands[0], "grounding_metadata", None) if cands else None
    if gm is not None:
        searches = len(gm.web_search_queries or [])
        urls = [ch.web.uri for ch in (gm.grounding_chunks or []) if getattr(ch, "web", None)]
    text = ""
    try:
        text = resp.text or ""
    except Exception:  # SDK raises when there is no text part
        text = ""
    blocked = feedback is not None and getattr(feedback, "block_reason", None)
    finish = _enum_name(cands[0].finish_reason) if cands and cands[0].finish_reason else ""
    status = "refusal" if blocked or finish in GEMINI_REFUSAL_REASONS else _status_for_text(text)
    return ProviderResult(status, text, served, tin, tout, searches, _dedupe(urls))


ADAPTERS = {"claude": _claude, "openai": _openai, "gemini": _gemini}


def ask(name: str, prompt: str, cfg: dict, model: str, client=None) -> ProviderResult:
    """Call one provider; never raises. Failures become status=error rows."""
    try:
        return ADAPTERS[name](prompt, cfg, model, client)
    except Exception as e:  # keep going, log the failure in the row
        return ProviderResult("error", "", model, error=f"{type(e).__name__}: {e}")


def cost_eur(r: ProviderResult, name: str, cfg: dict) -> float:
    price = cfg["providers"][name]["price"]
    usd = ((r.input_tokens or 0) * price["input_usd_per_mtok"]
           + (r.output_tokens or 0) * price["output_usd_per_mtok"]) / 1_000_000
    usd += (r.web_searches or 0) * price["search_usd"]
    return usd / cfg["currency"]["usd_per_eur"]
