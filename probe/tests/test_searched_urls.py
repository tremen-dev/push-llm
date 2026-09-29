"""SPEC-013 CA-3/CA-5: searched_urls (consulted) vs cited_urls (cited) in the three
adapters, Claude text joining rule, request parameters and the searched_urls column.

No network and no real keys: fake clients and the sanitized fixture
fixtures/claude_web_search_20260209.json (same shape as the CA-2 response, no real data).
"""
import csv
import json
import os
from types import SimpleNamespace as NS

import pytest

import providers
import run_probe
import settings
from fakes import (FIXTURES, FakeClaudeClient, FakeGeminiClient, FakeOpenAIClient, claude_resp,
                   gemini_resp, load_fixture, ns, openai_resp)
from test_run_probe import FakeAsk, read_rows, run

CFG = settings.load_config()
PROMPT = "¿Mejor clínica dental de Vigo?"


def call(name, client, prompt=PROMPT):
    return providers.ask(name, prompt, CFG, model=CFG["providers"][name]["model"], client=client)


# ---------------- Claude ----------------

FIXTURE_SEARCHED = [
    "https://clinica-ficticia.example.org/", "https://directorio.example.com/vigo/dentistas",
    "https://opiniones.example.net/clinica-ficticia", "https://noticias.example.org/salud-dental",
    "https://mapa.example.com/lugar/123", "https://otra-clinica.example.com/",
    "https://guia.example.net/dentistas-galicia", "https://foro.example.org/hilo/42",
    "https://colegio.example.org/buscador"]
FIXTURE_TEXT = ("Para una consulta dental en Vigo, una opción es Clínica Ficticia Example, "
                "con horario de mañana y tarde.\n\nOtra alternativa es Otra Clínica Example, "
                "en el centro.\n\nConviene revisar opiniones recientes antes de pedir cita.")


def test_fixture_has_the_ca2_shape():
    raw = json.loads((FIXTURES / "claude_web_search_20260209.json").read_text(encoding="utf-8"))
    code = "code_execution_20260120"
    shape = [(b["type"], (b.get("caller") or {}).get("type")) for b in raw["content"]]
    assert shape == [("server_tool_use", None), ("server_tool_use", code),
                     ("web_search_tool_result", code), ("code_execution_tool_result", None),
                     ("server_tool_use", None), ("code_execution_tool_result", None),
                     ("server_tool_use", None), ("code_execution_tool_result", None),
                     ("text", None)]
    results = raw["content"][2]["content"]
    assert len(results) == 10
    assert all(sorted(r) == ["encrypted_content", "page_age", "title", "type", "url"]
               for r in results)
    assert [b["content"]["type"] for b in raw["content"] if b["type"] == "code_execution_tool_result"] \
        == ["encrypted_code_execution_result", "code_execution_result", "code_execution_result"]
    assert raw["content"][8]["citations"] is None and raw["stop_reason"] == "end_turn"
    assert all(".example." in r["url"] for r in results)
    assert len({r["url"] for r in results}) == 9  # one repeated URL


def test_ca3a_claude_fixture_has_no_cited_urls():
    r = call("claude", FakeClaudeClient([load_fixture("claude_web_search_20260209.json")]))
    assert r.status == "ok" and r.cited_urls == []


def test_ca3b_claude_searched_urls_from_top_level_search_results():
    r = call("claude", FakeClaudeClient([load_fixture("claude_web_search_20260209.json")]))
    assert r.searched_urls == FIXTURE_SEARCHED
    assert (r.web_searches, r.input_tokens, r.output_tokens) == (1, 30000, 1200)


def test_ca3b_claude_searched_urls_across_pause_turn_with_and_without_caller():
    first = claude_resp("Busco.", stop_reason="pause_turn")
    first.content.append(NS(type="web_search_tool_result", tool_use_id="s1", content=[
        NS(type="web_search_result", url="https://a.example.org", title="A",
           encrypted_content="E", page_age=None)]))
    second = claude_resp("Resultado.", urls=["https://a.example.org"])
    second.content.insert(0, NS(type="web_search_tool_result", tool_use_id="s2",
                                caller=NS(type="code_execution_20260120", tool_id="c"),
                                content=[NS(type="web_search_result", url="https://b.example.com",
                                            title="B", encrypted_content="E", page_age=None)]))
    r = call("claude", FakeClaudeClient([first, second]))
    assert r.searched_urls == ["https://a.example.org", "https://b.example.com"]
    assert r.cited_urls == ["https://a.example.org"]
    assert set(r.cited_urls) <= set(r.searched_urls)  # inclusion when both are given


def test_ca3b_claude_search_error_block_adds_nothing_and_does_not_break():
    resp = claude_resp("Sin resultados.")
    resp.content.insert(1, NS(type="web_search_tool_result", tool_use_id="s1",
                              content=NS(type="web_search_tool_result_error",
                                         error_code="unavailable")))
    r = call("claude", FakeClaudeClient([resp]))
    assert r.status == "ok" and r.searched_urls == [] and r.text == "Sin resultados."


def test_ca3c_claude_fixture_text_is_exact():
    r = call("claude", FakeClaudeClient([load_fixture("claude_web_search_20260209.json")]))
    assert r.text == FIXTURE_TEXT


def test_ca3c_consecutive_text_blocks_join_without_separator_spans_with_blank_line():
    resp = NS(stop_reason="end_turn", model="m",
              usage=NS(input_tokens=1, output_tokens=1, server_tool_use=None),
              content=[NS(type="text", text="Voy a buscar", citations=None),
                       NS(type="text", text=" clínicas.", citations=None),
                       NS(type="server_tool_use", name="web_search"),
                       NS(type="web_search_tool_result", tool_use_id="x", content=[]),
                       NS(type="text", text="Según la web, ", citations=None),
                       NS(type="text", text="Clínica Ficticia", citations=[
                           NS(type="web_search_result_location", url="https://c.example.org")]),
                       NS(type="text", text=" abre por la tarde.", citations=None),
                       NS(type="server_tool_use", name="web_search")])
    r = call("claude", FakeClaudeClient([resp]))
    assert r.text == ("Voy a buscar clínicas.\n\n"
                      "Según la web, Clínica Ficticia abre por la tarde.")
    assert r.cited_urls == ["https://c.example.org"]


def test_error_leaves_both_url_lists_empty():
    r = call("claude", FakeClaudeClient(exc=RuntimeError("boom")))
    assert r.status == "error" and r.searched_urls == [] and r.cited_urls == []


# ---------------- Gemini ----------------

G_URLS = ["https://vertexaisearch.cloud.google.com/grounding-api-redirect/A",
          "https://vertexaisearch.cloud.google.com/grounding-api-redirect/B",
          "https://vertexaisearch.cloud.google.com/grounding-api-redirect/C"]


def test_ca3ef_gemini_cited_are_supported_chunks_searched_are_all():
    r = call("gemini", FakeGeminiClient(gemini_resp("Villoria", urls=G_URLS,
                                                    supports=[[2], [0, 2]])))
    assert r.searched_urls == G_URLS
    assert r.cited_urls == [G_URLS[0], G_URLS[2]]  # chunk order, repeated index once
    assert set(r.cited_urls) <= set(r.searched_urls)


def test_ca3f_gemini_without_supports_cites_nothing():
    r = call("gemini", FakeGeminiClient(gemini_resp("Villoria", urls=G_URLS)))
    assert r.cited_urls == [] and r.searched_urls == G_URLS


def test_ca3f_gemini_out_of_range_index_is_ignored():
    r = call("gemini", FakeGeminiClient(gemini_resp("V", urls=G_URLS, supports=[[1, 7, -1]])))
    assert r.cited_urls == [G_URLS[1]]


def test_ca3f_gemini_chunk_without_web_counts_in_neither_list():
    resp = gemini_resp("V", urls=G_URLS[:1], supports=[[0, 1]])
    resp.candidates[0].grounding_metadata.grounding_chunks.append(NS(web=None))
    r = call("gemini", FakeGeminiClient(resp))
    assert r.searched_urls == G_URLS[:1] and r.cited_urls == G_URLS[:1]


def test_ca3g_gemini_redirects_are_kept_as_they_are():
    r = call("gemini", FakeGeminiClient(gemini_resp("V", urls=G_URLS, supports=[[0]])))
    assert all(u.startswith("https://vertexaisearch.cloud.google.com/") for u in r.searched_urls)


# ---------------- OpenAI ----------------

def test_ca3h_openai_asks_for_action_sources():
    client = FakeOpenAIClient(openai_resp("x"))
    r = call("openai", client)
    assert client.calls[0]["include"] == ["web_search_call.action.sources"]
    assert r.request["include"] == ["web_search_call.action.sources"]


def test_ca3i_openai_searched_urls_from_sources_skipping_feeds():
    sources = [[{"type": "url", "url": "https://n.example.org"},
                {"type": "api", "name": "oai-weather"},
                {"type": "url", "url": "https://m.example.com"}],
               [{"type": "url", "url": "https://n.example.org"},
                {"type": "url", "url": "https://z.example.net"}]]
    r = call("openai", FakeOpenAIClient(openai_resp("NIDA", urls=["https://m.example.com"],
                                                    searches=2, sources=sources)))
    assert r.searched_urls == ["https://n.example.org", "https://m.example.com",
                               "https://z.example.net"]
    assert r.cited_urls == ["https://m.example.com"]
    assert set(r.cited_urls) <= set(r.searched_urls)


def test_ca3i_openai_action_without_sources_adds_nothing():
    r = call("openai", FakeOpenAIClient(openai_resp("NIDA", urls=["https://n.example.org"])))
    assert r.status == "ok" and r.searched_urls == []


def test_ca3j_openai_citation_outside_sources_stays_cited_only():
    r = call("openai", FakeOpenAIClient(openai_resp(
        "NIDA", urls=["https://fuera.example.org"],
        sources=[[{"type": "url", "url": "https://n.example.org"}]])))
    assert r.cited_urls == ["https://fuera.example.org"]
    assert r.searched_urls == ["https://n.example.org"]


# ---------------- CA-5: request parameters ----------------

def test_ca5_claude_and_gemini_send_exactly_the_same_openai_only_adds_include():
    pc, po, pg = (CFG["providers"][n] for n in ("claude", "openai", "gemini"))
    loc = {"type": "approximate", **CFG["user_location"]}
    claude = FakeClaudeClient([claude_resp("x")])
    call("claude", claude)
    assert claude.calls[0] == {
        "model": pc["model"], "max_tokens": pc["max_tokens"], "system": providers.SYSTEM,
        "tools": [{"type": pc["web_search_tool"], "name": "web_search",
                   "max_uses": pc["max_searches"], "user_location": loc}],
        "messages": [{"role": "user", "content": PROMPT}],
        "output_config": {"effort": pc["effort"]}}
    assert "allowed_callers" not in claude.calls[0]["tools"][0]
    gemini = FakeGeminiClient(gemini_resp("x"))
    call("gemini", gemini)
    assert gemini.calls[0] == {"model": pg["model"], "contents": PROMPT, "config": {
        "system_instruction": providers.SYSTEM, "tools": [{pg["web_search_tool"]: {}}]}}
    openai = FakeOpenAIClient(openai_resp("x"))
    call("openai", openai)
    before = {"model": po["model"], "instructions": providers.SYSTEM, "input": PROMPT,
              "tools": [{"type": po["web_search_tool"], "user_location": loc}],
              "reasoning": {"effort": po["effort"]}}
    assert openai.calls[0] == {**before, "include": ["web_search_call.action.sources"]}


# ---------------- CA-3 (d): the real CA-2 response, offline ----------------

def _ca2_raw():
    priv = os.environ.get("PUSHLLM_PRIVADO")
    path = priv and os.path.join(priv, "diagnostico", "spec-013", "raw_responses.jsonl")
    if not path or not os.path.exists(path):
        pytest.skip("CA-2 raw response not available (private space, ADR-001)")
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def test_ca3d_reprocess_the_real_ca2_response_offline():
    """Counts only: no URL or text of the real answer is printed or asserted on."""
    [line] = [x for x in _ca2_raw() if x["provider"] == "claude"]
    r = call("claude", FakeClaudeClient([ns(x) for x in line["responses"]]))
    results = [x for resp in line["responses"] for b in resp["content"]
               if b["type"] == "web_search_tool_result" and isinstance(b["content"], list)
               for x in b["content"]]
    assert r.status == "ok" and r.cited_urls == []
    assert len(r.searched_urls) == len({x["url"] for x in results}) > 0
    assert not r.text.startswith(("\n", " ")) and not r.text.endswith(("\n", " "))
    assert "\n\n\n" not in r.text


# ---------------- CA-3 (k), (l): the column and old files ----------------

def test_ca3k_searched_urls_is_the_last_column_and_filled_for_each_provider(tmp_path):
    assert run_probe.COLUMNS[-3:] == ["cited_urls", "answer", "searched_urls"]
    clients = {
        "claude": lambda: FakeClaudeClient([load_fixture("claude_web_search_20260209.json")]),
        "openai": lambda: FakeOpenAIClient(openai_resp(
            "NIDA", sources=[[{"type": "url", "url": "https://n.example.org"}]])),
        "gemini": lambda: FakeGeminiClient(gemini_resp("V", urls=G_URLS, supports=[[0]])),
    }

    def ask(name, prompt, cfg, model, client=None):
        return providers.ask(name, prompt, cfg, model, client=clients[name]())
    run(tmp_path, "--only", "D01", "--runs", "1", ask=ask)
    rows = {r["provider"]: r for r in read_rows(tmp_path / "results.csv")}
    assert rows["claude"]["searched_urls"] == ";".join(FIXTURE_SEARCHED)
    assert rows["openai"]["searched_urls"] == "https://n.example.org"
    assert rows["gemini"]["searched_urls"] == ";".join(G_URLS)
    assert rows["gemini"]["cited_urls"] == G_URLS[0]


OLD_COLUMNS = [c for c in run_probe.COLUMNS if c != "searched_urls"]  # pre-SPEC-013 header


def _write_old_results(path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=OLD_COLUMNS)
        w.writeheader()
        w.writerow({c: "" for c in OLD_COLUMNS} | {
            "timestamp_utc": "2026-09-01T00:00:00Z", "prompt_id": "D01", "specialty": "dental",
            "city": "Vigo", "provider": "gemini", "run": "1", "model": "g", "status": "ok",
            "cost_eur": "0.01", "cited_urls": "https://old.example.org", "answer": "x"})


@pytest.mark.parametrize("with_raw", [True, False])
def test_ca3l_resume_refuses_an_old_results_csv(tmp_path, capsys, with_raw):
    _write_old_results(tmp_path / "results.csv")
    before = (tmp_path / "results.csv").read_bytes()
    raw = tmp_path / "raw_responses.jsonl"
    if with_raw:
        raw.write_text('{"old": 1}\n', encoding="utf-8")
    ask = FakeAsk()
    with pytest.raises(SystemExit) as exc:
        run(tmp_path, "--resume", "--only", "D01", "--runs", "1", ask=ask)
    msg = str(exc.value.code)
    assert exc.value.code not in (0, None)
    assert "searched_urls" in msg and "--out" in msg and "SPEC-013" in msg
    assert ask.calls == []
    assert (tmp_path / "results.csv").read_bytes() == before
    if with_raw:
        assert raw.read_text(encoding="utf-8") == '{"old": 1}\n'
    else:
        assert not raw.exists()


def test_ca3l_resume_on_a_new_results_csv_still_appends(tmp_path):
    run(tmp_path, "--only", "D01", "--providers", "openai", "--runs", "1",
        ask=FakeAsk(status="error", text=""))
    first = (tmp_path / "results.csv").read_bytes()
    again = FakeAsk()
    run(tmp_path, "--resume", "--only", "D01", "--providers", "openai", "--runs", "1", ask=again)
    assert len(again.calls) == 1 and (tmp_path / "results.csv").read_bytes().startswith(first)


def test_ca3l_analyze_same_summary_with_or_without_the_column(tmp_path):
    old = tmp_path / "old"
    new = tmp_path / "new"
    old.mkdir()
    new.mkdir()
    src = FIXTURES / "vigo_results.csv"
    (old / "results.csv").write_bytes(src.read_bytes())
    with open(src, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    with open(new / "results.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=[*rows[0], "searched_urls"])
        w.writeheader()
        w.writerows({**r, "searched_urls": "https://s.example.org"} for r in rows)
    for d in (old, new):
        run_probe.main(["--analyze", "--out", str(d)], env={})
    assert (old / "summary.md").read_bytes() == (new / "summary.md").read_bytes()


def test_ca6_confirmation_command_makes_exactly_three_calls(tmp_path):
    """SPEC-013 CA-6 command, default (Vigo) batch, all keys present: 1 call per provider."""
    ask = run(tmp_path, "--providers", "claude,openai,gemini", "--only", "D01", "--runs", "1")
    assert sorted(c[0] for c in ask.calls) == ["claude", "gemini", "openai"]
    assert len((tmp_path / "raw_responses.jsonl").read_text(encoding="utf-8").splitlines()) == 3
    assert list(read_rows(tmp_path / "results.csv")[0])[-1] == "searched_urls"
