"""CA-3: metadatos por fila con los tres proveedores simulados, uno por status."""
import pytest

import providers
import settings
from fakes import (FakeClaudeClient, FakeGeminiClient, FakeOpenAIClient, claude_resp,
                   gemini_resp, openai_resp)

CFG = settings.load_config()


def call(name, client, prompt="¿Mejor clínica dental de Vigo?"):
    return providers.ask(name, prompt, CFG, model=CFG["providers"][name]["model"], client=client)


# ---------- ok ----------

def test_claude_ok_collects_usage_urls_and_served_model():
    client = FakeClaudeClient([claude_resp("Clínica Torres",
                                           urls=["https://a.es", "https://b.es", "https://a.es"])])
    r = call("claude", client)
    assert r.status == "ok" and r.text == "Clínica Torres"
    assert r.model == "claude-served-1"
    assert (r.input_tokens, r.output_tokens, r.web_searches) == (1000, 200, 2)
    assert r.cited_urls == ["https://a.es", "https://b.es"]
    kw = client.calls[0]
    assert kw["model"] == CFG["providers"]["claude"]["model"]
    assert kw["tools"][0]["type"] == CFG["providers"]["claude"]["web_search_tool"]
    assert kw["tools"][0]["max_uses"] == CFG["providers"]["claude"]["max_searches"]
    assert kw["tools"][0]["user_location"]["city"] == "Vigo"
    assert kw["output_config"] == {"effort": CFG["providers"]["claude"]["effort"]}


def test_claude_pause_turn_accumulates_usage_and_text():
    client = FakeClaudeClient([
        claude_resp("Parte 1.", stop_reason="pause_turn", urls=["https://a.es"]),
        claude_resp("Parte 2.", urls=["https://c.es"]),
    ])
    r = call("claude", client)
    assert r.status == "ok" and r.text == "Parte 1.\nParte 2."
    assert (r.input_tokens, r.output_tokens, r.web_searches) == (2000, 400, 4)
    assert r.cited_urls == ["https://a.es", "https://c.es"]
    assert len(client.calls) == 2


def test_openai_ok():
    client = FakeOpenAIClient(openai_resp("NIDA e IVI Vigo", urls=["https://n.es"], searches=3))
    r = call("openai", client)
    assert r.status == "ok" and r.model == "openai-served-1"
    assert (r.input_tokens, r.output_tokens, r.web_searches) == (800, 150, 3)
    assert r.cited_urls == ["https://n.es"]
    kw = client.calls[0]
    assert kw["model"] == CFG["providers"]["openai"]["model"]
    assert kw["tools"][0]["type"] == CFG["providers"]["openai"]["web_search_tool"]
    assert kw["tools"][0]["user_location"]["city"] == "Vigo"
    assert kw["reasoning"] == {"effort": CFG["providers"]["openai"]["effort"]}


def test_gemini_ok_sums_thoughts_and_tool_tokens():
    client = FakeGeminiClient(gemini_resp("Villoria", urls=["https://v.es"], queries=["a", "b"]))
    r = call("gemini", client)
    assert r.status == "ok" and r.model == "gemini-served-1"
    assert (r.input_tokens, r.output_tokens, r.web_searches) == (520, 150, 2)
    assert r.cited_urls == ["https://v.es"]
    kw = client.calls[0]
    assert kw["model"] == CFG["providers"]["gemini"]["model"]
    assert kw["config"]["tools"] == [{"google_search": {}}]


# ---------- error / refusal / empty ----------

@pytest.mark.parametrize("name,client", [
    ("claude", FakeClaudeClient(exc=RuntimeError("boom"))),
    ("openai", FakeOpenAIClient(exc=RuntimeError("boom"))),
    ("gemini", FakeGeminiClient(exc=RuntimeError("boom"))),
])
def test_error_status_on_exception(name, client):
    r = call(name, client)
    assert r.status == "error" and "boom" in r.error
    assert r.model == CFG["providers"][name]["model"]  # configured model when API gives none
    assert r.web_searches is None and r.cited_urls == []


@pytest.mark.parametrize("name,client", [
    ("claude", FakeClaudeClient([claude_resp("", stop_reason="refusal")])),
    ("openai", FakeOpenAIClient(openai_resp(refusal="No puedo ayudar"))),
    ("gemini", FakeGeminiClient(gemini_resp("", finish="SAFETY"))),
])
def test_refusal_status(name, client):
    assert call(name, client).status == "refusal"


def test_gemini_prompt_block_is_refusal():
    resp = gemini_resp("", block="SAFETY")
    resp.candidates = []
    assert call("gemini", FakeGeminiClient(resp)).status == "refusal"


@pytest.mark.parametrize("name,client", [
    ("claude", FakeClaudeClient([claude_resp("   ")])),
    ("openai", FakeOpenAIClient(openai_resp("  "))),
    ("gemini", FakeGeminiClient(gemini_resp(""))),
])
def test_empty_status(name, client):
    assert call(name, client).status == "empty"


def test_served_model_falls_back_to_configured_when_not_exposed():
    resp = openai_resp("x")
    resp.model = None
    r = call("openai", FakeOpenAIClient(resp))
    assert r.model == CFG["providers"]["openai"]["model"]


def test_gemini_searches_blank_when_no_grounding_metadata():
    resp = gemini_resp("x")
    resp.candidates[0].grounding_metadata = None
    r = call("gemini", FakeGeminiClient(resp))
    assert r.web_searches is None and r.cited_urls == []


# ---------- cost ----------

def test_cost_eur_from_config_prices():
    r = providers.ProviderResult(status="ok", text="x", model="m", input_tokens=1_000_000,
                                 output_tokens=100_000, web_searches=10)
    p = CFG["providers"]["claude"]["price"]
    usd = p["input_usd_per_mtok"] + 0.1 * p["output_usd_per_mtok"] + 10 * p["search_usd"]
    assert providers.cost_eur(r, "claude", CFG) == pytest.approx(usd / CFG["currency"]["usd_per_eur"])


def test_cost_eur_treats_missing_counts_as_zero():
    r = providers.ProviderResult(status="error", model="m")
    assert providers.cost_eur(r, "openai", CFG) == 0
