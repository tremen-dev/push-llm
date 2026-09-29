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
# SPEC-013 CA-1 / ADR-006: never persisted, at any depth (Gemini's sdk_http_response carries
# the HTTP headers). Compared case-insensitively.
OPENAI_INCLUDE = ("web_search_call.action.sources",)
FORBIDDEN_KEYS = frozenset({"headers", "sdk_http_response", "api_key", "authorization",
                            "x-api-key"})


@dataclass
class ProviderResult:
    status: str
    text: str = ""
    model: str = ""
    input_tokens: int | None = None
    output_tokens: int | None = None
    web_searches: int | None = None
    cited_urls: list[str] = field(default_factory=list)  # linked to a piece of the answer
    error: str = ""
    request: dict = field(default_factory=dict)  # parameters sent (no client, no credentials)
    responses: list = field(default_factory=list)  # every SDK response, JSON-ready (SPEC-013)
    searched_urls: list[str] = field(default_factory=list)  # retrieved by the search (SPEC-013)


def scrub(obj):
    """Drop FORBIDDEN_KEYS at any depth (case-insensitive); returns a new structure."""
    if isinstance(obj, dict):
        return {k: scrub(v) for k, v in obj.items()
                if not (isinstance(k, str) and k.lower() in FORBIDDEN_KEYS)}
    if isinstance(obj, (list, tuple)):
        return [scrub(v) for v in obj]
    return obj


def _jsonable(obj):
    if obj is None or isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, dict):
        return {str(k): _jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set)):
        return [_jsonable(v) for v in obj]
    if hasattr(obj, "model_dump"):  # pydantic models of the three SDKs
        try:
            return _jsonable(obj.model_dump(mode="json", warnings=False))
        except Exception:  # fall back to the attributes
            pass
    if hasattr(obj, "__dict__"):
        return {k: _jsonable(v) for k, v in vars(obj).items() if not k.startswith("_")}
    name = getattr(obj, "name", None)  # enums
    return name if isinstance(name, str) else str(obj)


def raw_json(obj):
    """Full JSON form of an SDK response (nothing trimmed) without headers or keys."""
    return scrub(_jsonable(obj))


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

def _claude(prompt, cfg, model, client, rec):
    pcfg = cfg["providers"]["claude"]
    tools = [{"type": pcfg["web_search_tool"], "name": "web_search",
              "max_uses": pcfg["max_searches"], "user_location": _location(cfg)}]
    kwargs = {}
    if pcfg.get("effort"):
        kwargs["output_config"] = {"effort": pcfg["effort"]}
    rec["request"] = {"model": model, "max_tokens": pcfg["max_tokens"], "system": SYSTEM,
                      "tools": tools, **kwargs, "prompt": prompt}
    if client is None:
        import anthropic
        client = anthropic.Anthropic()
    messages = [{"role": "user", "content": prompt}]
    spans, span, cited, searched = [], [], [], []
    tin = tout = searches = 0
    served = None
    status = None
    for _ in range(MAX_PAUSE_TURNS):
        resp = client.messages.create(model=model, max_tokens=pcfg["max_tokens"], system=SYSTEM,
                                      tools=tools, messages=messages, **kwargs)
        rec["responses"].append(raw_json(resp))
        served = getattr(resp, "model", None) or served
        usage = resp.usage
        tin += usage.input_tokens or 0
        tout += usage.output_tokens or 0
        stu = getattr(usage, "server_tool_use", None)
        searches += (getattr(stu, "web_search_requests", 0) or 0) if stu else 0
        for block in resp.content:
            if block.type == "text":
                span.append(block.text or "")
                for c in getattr(block, "citations", None) or []:
                    cited.append(getattr(c, "url", None))
                continue
            span = _close_span(spans, span)
            if block.type == "web_search_tool_result":
                results = getattr(block, "content", None)
                if isinstance(results, list):  # otherwise a tool error: no URLs
                    searched.extend(getattr(x, "url", None) for x in results)
        span = _close_span(spans, span)  # a pause_turn continuation starts a new span
        if resp.stop_reason == "refusal":
            status = "refusal"
            break
        if resp.stop_reason != "pause_turn":
            break
        messages.append({"role": "assistant", "content": resp.content})
    text = "\n\n".join(spans)
    return ProviderResult(status or _status_for_text(text), text, served or model, tin, tout,
                          searches, _dedupe(cited), searched_urls=_dedupe(searched))


def _close_span(spans: list, span: list) -> list:
    """SPEC-013 CA-3 (c): consecutive text blocks are one span, joined without separator
    (citations split sentences into blocks); spans are later joined by a blank line."""
    joined = "".join(span)
    if joined:
        spans.append(joined)
    return []


# ---------------- OpenAI ----------------

def _openai(prompt, cfg, model, client, rec):
    pcfg = cfg["providers"]["openai"]
    loc = _location(cfg)
    tools = [{"type": pcfg["web_search_tool"], "user_location": loc}]
    kwargs = {}
    if pcfg.get("effort"):
        kwargs["reasoning"] = {"effort": pcfg["effort"]}
    kwargs["include"] = list(OPENAI_INCLUDE)  # SPEC-013 CA-3 (h), CA-5: only adds output data
    rec["request"] = {"model": model, "instructions": SYSTEM, "tools": tools, **kwargs,
                      "prompt": prompt}
    if client is None:
        from openai import OpenAI
        client = OpenAI()
    resp = client.responses.create(model=model, instructions=SYSTEM, input=prompt, tools=tools,
                                   **kwargs)
    rec["responses"].append(raw_json(resp))
    searches, urls, searched, refused = 0, [], [], False
    for item in resp.output or []:
        if item.type == "web_search_call":
            action = getattr(item, "action", None)
            if action is None or getattr(action, "type", "search") == "search":
                searches += 1
            # sources: URLs consulted; oai-* feed entries carry no url and stay in the raw file
            for src in getattr(action, "sources", None) or []:
                searched.append(getattr(src, "url", None))
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
                          usage.input_tokens, usage.output_tokens, searches, _dedupe(urls),
                          searched_urls=_dedupe(searched))


# ---------------- Gemini ----------------

def _enum_name(x) -> str:
    return getattr(x, "name", None) or str(x).split(".")[-1]


def _gemini(prompt, cfg, model, client, rec):
    pcfg = cfg["providers"]["gemini"]
    config = {"system_instruction": SYSTEM, "tools": [{pcfg["web_search_tool"]: {}}]}
    rec["request"] = {"model": model, "config": config, "prompt": prompt}
    if client is None:
        from google import genai
        client = genai.Client()
    resp = client.models.generate_content(model=model, contents=prompt, config=config)
    rec["responses"].append(raw_json(resp))
    um = resp.usage_metadata
    tin = (um.prompt_token_count or 0) + (getattr(um, "tool_use_prompt_token_count", 0) or 0)
    tout = (um.candidates_token_count or 0) + (getattr(um, "thoughts_token_count", 0) or 0)
    served = getattr(resp, "model_version", None) or model
    feedback = getattr(resp, "prompt_feedback", None)
    cands = resp.candidates or []
    searches, cited, searched = None, [], []
    gm = getattr(cands[0], "grounding_metadata", None) if cands else None
    if gm is not None:
        searches = len(gm.web_search_queries or [])
        cited, searched = _gemini_urls(gm)
    text = ""
    try:
        text = resp.text or ""
    except Exception:  # SDK raises when there is no text part
        text = ""
    blocked = feedback is not None and getattr(feedback, "block_reason", None)
    finish = _enum_name(cands[0].finish_reason) if cands and cands[0].finish_reason else ""
    status = "refusal" if blocked or finish in GEMINI_REFUSAL_REASONS else _status_for_text(text)
    return ProviderResult(status, text, served, tin, tout, searches, _dedupe(cited),
                          searched_urls=_dedupe(searched))


def _gemini_urls(gm) -> tuple[list, list]:
    """SPEC-013 CA-3 (e-g): searched = every web grounding chunk; cited = the chunks that some
    grounding_support links to the answer text. URIs are vertexaisearch redirects, kept as is."""
    chunks = gm.grounding_chunks or []
    linked = {i for sup in (getattr(gm, "grounding_supports", None) or [])
              for i in (getattr(sup, "grounding_chunk_indices", None) or [])}
    searched, cited = [], []
    for i, ch in enumerate(chunks):
        web = getattr(ch, "web", None)
        uri = getattr(web, "uri", None) if web else None
        if not uri:
            continue
        searched.append(uri)
        if i in linked:
            cited.append(uri)
    return cited, searched


ADAPTERS = {"claude": _claude, "openai": _openai, "gemini": _gemini}


def ask(name: str, prompt: str, cfg: dict, model: str, client=None) -> ProviderResult:
    """Call one provider; never raises. Failures become status=error rows.
    The result carries the request sent and every raw SDK response (SPEC-013 CA-1)."""
    rec = {"request": {}, "responses": []}
    try:
        r = ADAPTERS[name](prompt, cfg, model, client, rec)
    except Exception as e:  # keep going, log the failure in the row
        r = ProviderResult("error", "", model, error=f"{type(e).__name__}: {e}")
        rec["responses"] = []  # an error line keeps no partial responses
    r.request = scrub(_jsonable(rec["request"]))
    r.responses = rec["responses"]
    return r


def cost_eur(r: ProviderResult, name: str, cfg: dict) -> float:
    price = cfg["providers"][name]["price"]
    usd = ((r.input_tokens or 0) * price["input_usd_per_mtok"]
           + (r.output_tokens or 0) * price["output_usd_per_mtok"]) / 1_000_000
    usd += (r.web_searches or 0) * price["search_usd"]
    return usd / cfg["currency"]["usd_per_eur"]
