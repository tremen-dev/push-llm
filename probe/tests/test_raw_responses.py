"""SPEC-013 CA-1: raw provider responses saved privately in raw_responses.jsonl.

No network and no real keys: fake clients (fakes.py) and SDK types built offline.
"""
import json
import shutil
import subprocess

import pytest

import providers
import run_probe
import settings
from conftest import PROBE_DIR, REPO_DIR
from fakes import (FakeClaudeClient, FakeGeminiClient, FakeOpenAIClient, claude_resp,
                   gemini_resp, openai_resp)
from test_run_probe import KEYS, FakeAsk, read_rows, run

CFG = settings.load_config()
FORBIDDEN = {"headers", "sdk_http_response", "api_key", "authorization", "x-api-key"}
SECRET = "sk-test-FAKE-SECRET-0123456789"


def call(name, client, prompt="¿Mejor clínica dental de Vigo?"):
    return providers.ask(name, prompt, CFG, model=CFG["providers"][name]["model"], client=client)


def keys_at_any_depth(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield k
            yield from keys_at_any_depth(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from keys_at_any_depth(v)


def read_lines(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def claude_with_search_result(text="Clínica Torres", stop_reason="end_turn"):
    resp = claude_resp(text, stop_reason=stop_reason, urls=["https://a.example.org"])
    from types import SimpleNamespace as NS
    resp.content.insert(1, NS(type="web_search_tool_result", tool_use_id="srvtoolu_X", content=[
        NS(type="web_search_result", url="https://a.example.org", title="A",
           encrypted_content="ENC" * 5000, page_age=None)]))
    return resp


def gemini_with_http_headers(text="Villoria"):
    from types import SimpleNamespace as NS
    resp = gemini_resp(text, urls=["https://v.example.org"])
    resp.sdk_http_response = NS(headers={"x-goog-api-key": SECRET, "content-type": "json"},
                                body=None)
    return resp


# ---------- adapters capture request + every SDK response ----------

def test_claude_raw_keeps_request_and_full_response():
    r = call("claude", FakeClaudeClient([claude_with_search_result()]))
    assert r.request["model"] == CFG["providers"]["claude"]["model"]
    assert r.request["prompt"] == "¿Mejor clínica dental de Vigo?"
    assert r.request["system"] == providers.SYSTEM
    assert r.request["max_tokens"] == CFG["providers"]["claude"]["max_tokens"]
    assert r.request["tools"][0]["type"] == CFG["providers"]["claude"]["web_search_tool"]
    assert r.request["output_config"] == {"effort": CFG["providers"]["claude"]["effort"]}
    assert len(r.responses) == 1
    blocks = r.responses[0]["content"]
    assert [b["type"] for b in blocks] == ["server_tool_use", "web_search_tool_result", "text"]
    assert blocks[1]["content"][0]["encrypted_content"] == "ENC" * 5000  # not trimmed
    assert blocks[2]["citations"][0]["url"] == "https://a.example.org"
    json.dumps(r.responses)  # JSON-serializable


def test_claude_pause_turn_keeps_one_response_per_turn():
    client = FakeClaudeClient([claude_resp("Parte 1.", stop_reason="pause_turn"),
                               claude_resp("Parte 2.", stop_reason="pause_turn"),
                               claude_resp("Parte 3.")])
    r = call("claude", client)
    assert len(client.calls) == 3
    assert [x["stop_reason"] for x in r.responses] == ["pause_turn", "pause_turn", "end_turn"]
    assert "messages" not in r.request  # the continuation turns are in responses


def test_openai_raw_keeps_request_and_response():
    r = call("openai", FakeOpenAIClient(openai_resp("NIDA", urls=["https://n.example.org"])))
    assert r.request["model"] == CFG["providers"]["openai"]["model"]
    assert r.request["prompt"] == "¿Mejor clínica dental de Vigo?"
    assert r.request["instructions"] == providers.SYSTEM
    assert r.request["reasoning"] == {"effort": CFG["providers"]["openai"]["effort"]}
    assert len(r.responses) == 1 and r.responses[0]["output_text"] == "NIDA"


def test_gemini_raw_drops_sdk_http_response_and_headers():
    r = call("gemini", FakeGeminiClient(gemini_with_http_headers()))
    assert r.request["model"] == CFG["providers"]["gemini"]["model"]
    assert r.request["prompt"] == "¿Mejor clínica dental de Vigo?"
    assert r.request["config"]["tools"] == [{"google_search": {}}]
    assert len(r.responses) == 1
    assert not FORBIDDEN & set(keys_at_any_depth(r.responses))
    assert SECRET not in json.dumps(r.responses)
    assert r.responses[0]["model_version"] == "gemini-served-1"


def test_error_keeps_request_and_no_responses():
    r = call("claude", FakeClaudeClient(exc=RuntimeError("boom")))
    assert r.status == "error" and r.responses == []
    assert r.request["prompt"] == "¿Mejor clínica dental de Vigo?"


def test_real_sdk_objects_serialize_without_http_headers():
    """Offline: the real SDK types, as returned by the clients, dump to JSON without headers."""
    from anthropic.types import Message
    from google.genai import types as gtypes
    msg = Message.model_validate({
        "id": "msg_x", "type": "message", "role": "assistant", "model": "claude-x",
        "stop_reason": "end_turn", "stop_sequence": None,
        "usage": {"input_tokens": 1, "output_tokens": 2,
                  "server_tool_use": {"web_search_requests": 1,
                                      "web_fetch_requests": 0}},
        "content": [{"type": "text", "text": "Hola", "citations": [
            {"type": "web_search_result_location", "url": "https://a.example.org",
             "title": "A", "encrypted_index": "IDX", "cited_text": "c"}]}]})
    dumped = providers.raw_json(msg)
    assert dumped["content"][0]["citations"][0]["encrypted_index"] == "IDX"
    g = gtypes.GenerateContentResponse(
        sdk_http_response=gtypes.HttpResponse(headers={"x-goog-api-key": SECRET}),
        model_version="gemini-x")
    gd = providers.raw_json(g)
    assert gd["model_version"] == "gemini-x"
    assert not FORBIDDEN & set(keys_at_any_depth(gd)) and SECRET not in json.dumps(gd)


def test_forbidden_keys_removed_at_any_depth_case_insensitive():
    dirty = {"a": [{"Authorization": "x", "ok": 1, "deep": {"X-Api-Key": "y", "api_key": "z",
                                                              "Headers": {"h": 1}}}]}
    assert providers.scrub(dirty) == {"a": [{"ok": 1, "deep": {}}]}


# ---------- run_probe writes raw_responses.jsonl ----------

def ask_with_fakes(clients):
    """ask() of the real adapters with fake SDK clients, one per provider."""
    def _ask(name, prompt, cfg, model, client=None):
        return providers.ask(name, prompt, cfg, model, client=clients[name]())
    return _ask


FAKE_CLIENTS = {
    "claude": lambda: FakeClaudeClient([claude_with_search_result(stop_reason="pause_turn"),
                                        claude_resp("Parte 2.")]),
    "openai": lambda: FakeOpenAIClient(openai_resp("NIDA", urls=["https://n.example.org"])),
    "gemini": lambda: FakeGeminiClient(gemini_with_http_headers()),
}


def test_ca1a_one_line_per_call_with_the_row_keys(tmp_path):
    run(tmp_path, "--only", "D01,E01", "--runs", "2", ask=ask_with_fakes(FAKE_CLIENTS))
    rows = read_rows(tmp_path / "results.csv")
    lines = read_lines(tmp_path / "raw_responses.jsonl")
    assert len(rows) == len(lines) == 2 * 3 * 2
    for row, line in zip(rows, lines):
        for k in ("timestamp_utc", "prompt_id", "provider", "model", "status"):
            assert line[k] == row[k], k
        assert str(line["run"]) == row["run"]
        assert line["request"]["prompt"]
        assert line["responses"]
    assert list(rows[0]) == run_probe.COLUMNS  # results.csv columns unchanged


def test_ca1b_pause_turn_line_has_one_response_per_turn(tmp_path):
    run(tmp_path, "--only", "D01", "--providers", "claude", "--runs", "1",
        ask=ask_with_fakes(FAKE_CLIENTS))
    [line] = read_lines(tmp_path / "raw_responses.jsonl")
    assert [x["stop_reason"] for x in line["responses"]] == ["pause_turn", "end_turn"]
    enc = line["responses"][0]["content"][1]["content"][0]["encrypted_content"]
    assert enc == "ENC" * 5000


def test_ca1c_no_headers_nor_keys_in_the_file(tmp_path, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", SECRET)
    monkeypatch.setenv("GEMINI_API_KEY", SECRET)
    env = {**KEYS, "ANTHROPIC_API_KEY": SECRET, "GEMINI_API_KEY": SECRET}
    run(tmp_path, "--only", "D01", "--runs", "1", env=env, ask=ask_with_fakes(FAKE_CLIENTS))
    raw = (tmp_path / "raw_responses.jsonl").read_text(encoding="utf-8")
    assert SECRET not in raw
    for line in read_lines(tmp_path / "raw_responses.jsonl"):
        assert not FORBIDDEN & {k.lower() for k in keys_at_any_depth(line)}


def test_ca1_error_line_has_empty_responses_and_the_message(tmp_path):
    def boom():
        return FakeClaudeClient(exc=RuntimeError("boom"))
    run(tmp_path, "--only", "D01", "--providers", "claude", "--runs", "1",
        ask=ask_with_fakes({"claude": boom}))
    [line] = read_lines(tmp_path / "raw_responses.jsonl")
    assert line["status"] == "error" and line["responses"] == []
    assert "boom" in line["error"]


def test_ca1d_resume_appends_and_never_rewrites(tmp_path):
    run(tmp_path, "--only", "D01", "--providers", "openai", "--runs", "1",
        ask=FakeAsk(status="error", text=""))
    first = (tmp_path / "raw_responses.jsonl").read_bytes()
    run(tmp_path, "--resume", "--only", "D01", "--providers", "openai", "--runs", "2",
        ask=ask_with_fakes(FAKE_CLIENTS))
    data = (tmp_path / "raw_responses.jsonl").read_bytes()
    assert data.startswith(first)
    lines = read_lines(tmp_path / "raw_responses.jsonl")
    assert [(x["run"], x["status"]) for x in lines] == [(1, "error"), (1, "ok"), (2, "ok")]


def test_ca1e_analyze_neither_reads_nor_modifies_raw(tmp_path, monkeypatch):
    run(tmp_path, "--only", "D01", "--providers", "openai", "--runs", "1")
    raw = tmp_path / "raw_responses.jsonl"
    before, mtime = raw.read_bytes(), raw.stat().st_mtime_ns
    import builtins
    real_open = builtins.open

    def guarded(file, *a, **k):
        if str(file).endswith("raw_responses.jsonl"):
            raise AssertionError("--analyze opened raw_responses.jsonl")
        return real_open(file, *a, **k)
    monkeypatch.setattr(builtins, "open", guarded)
    run_probe.main(["--analyze", "--out", str(tmp_path)], env={}, ask=None)
    monkeypatch.undo()
    assert raw.read_bytes() == before and raw.stat().st_mtime_ns == mtime


def test_ca1f_default_output_raw_file_is_gitignored():
    if shutil.which("git") is None:
        pytest.skip("git not available")
    default = run_probe.output_dir(None, {})
    viveiro = run_probe.output_dir(None, {}, {"output_subdir": "piloto-artica/probe"})
    for path in (default / "raw_responses.jsonl", viveiro / "raw_responses.jsonl"):
        rel = path.relative_to(REPO_DIR).as_posix()
        assert rel.startswith("probe/out/")
        res = subprocess.run(["git", "check-ignore", "-q", rel], cwd=REPO_DIR)
        assert res.returncode == 0, f"{rel} not ignored"
    assert PROBE_DIR.name == "probe"


def test_ca2_diagnostic_command_makes_exactly_one_claude_call(tmp_path):
    """SPEC-013 CA-2 command, default (Vigo) batch, all keys present: 1 call, 1 raw line."""
    ask = run(tmp_path, "--providers", "claude", "--only", "D01", "--runs", "1")
    assert ask.calls == [("claude", ask.calls[0][1], CFG["providers"]["claude"]["model"])]
    assert len(read_lines(tmp_path / "raw_responses.jsonl")) == 1
