"""Fake SDK clients/responses shaped like the real ones. No network, no keys."""
from types import SimpleNamespace as NS


class FakeClaudeClient:
    def __init__(self, responses=None, exc=None):
        self.responses = list(responses or [])
        self.exc = exc
        self.calls = []
        self.messages = NS(create=self._create)

    def _create(self, **kw):
        self.calls.append(kw)
        if self.exc:
            raise self.exc
        return self.responses.pop(0)


def claude_resp(text="", stop_reason="end_turn", urls=(), inp=1000, out=200, searches=2,
                model="claude-served-1"):
    citations = [NS(type="web_search_result_location", url=u, title="t") for u in urls]
    content = [NS(type="server_tool_use", name="web_search"),
               NS(type="text", text=text, citations=citations or None)]
    usage = NS(input_tokens=inp, output_tokens=out,
               server_tool_use=NS(web_search_requests=searches))
    return NS(content=content, stop_reason=stop_reason, usage=usage, model=model)


class FakeOpenAIClient:
    def __init__(self, response=None, exc=None):
        self.response = response
        self.exc = exc
        self.calls = []
        self.responses = NS(create=self._create)

    def _create(self, **kw):
        self.calls.append(kw)
        if self.exc:
            raise self.exc
        return self.response


def openai_resp(text="", urls=(), refusal=None, inp=800, out=150, searches=1,
                model="openai-served-1"):
    output = [NS(type="web_search_call", action=NS(type="search")) for _ in range(searches)]
    if refusal:
        parts = [NS(type="refusal", refusal=refusal)]
    else:
        parts = [NS(type="output_text", text=text,
                    annotations=[NS(type="url_citation", url=u) for u in urls])]
    output.append(NS(type="message", content=parts))
    return NS(output=output, output_text=text, model=model,
              usage=NS(input_tokens=inp, output_tokens=out))


class FakeGeminiClient:
    def __init__(self, response=None, exc=None):
        self.response = response
        self.exc = exc
        self.calls = []
        self.models = NS(generate_content=self._gen)

    def _gen(self, **kw):
        self.calls.append(kw)
        if self.exc:
            raise self.exc
        return self.response


def gemini_resp(text="", urls=(), queries=("q1",), finish="STOP", block=None, inp=500,
                out=100, thoughts=50, tool_inp=20, model="gemini-served-1"):
    gm = NS(web_search_queries=list(queries),
            grounding_chunks=[NS(web=NS(uri=u, title="t")) for u in urls])
    cand = NS(finish_reason=finish, grounding_metadata=gm)
    usage = NS(prompt_token_count=inp, candidates_token_count=out, thoughts_token_count=thoughts,
               tool_use_prompt_token_count=tool_inp)
    return NS(text=text or None, candidates=[cand], usage_metadata=usage, model_version=model,
              prompt_feedback=NS(block_reason=block) if block else None)
