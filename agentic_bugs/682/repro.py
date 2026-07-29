#!/usr/bin/env python3
"""Offline reproduction for Azure providers mutating caller-owned messages."""

from types import SimpleNamespace

from mem0.llms.azure_openai import AzureOpenAILLM
from mem0.llms.azure_openai_structured import AzureOpenAIStructuredLLM


class FakeCompletions:
    def __init__(self):
        self.requests = []

    def create(self, **kwargs):
        self.requests.append(kwargs)
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content="offline response", tool_calls=None))]
        )


class FakeClient:
    def __init__(self):
        self.chat = SimpleNamespace(completions=FakeCompletions())


def offline_llm(provider_cls):
    """Avoid provider construction, which would create a real Azure client."""
    llm = object.__new__(provider_cls)
    llm.config = SimpleNamespace(model="deployment", temperature=0.1, top_p=0.1, max_tokens=20)
    llm.client = FakeClient()
    return llm


def assert_mutation_and_multimodal_crash(provider_cls):
    llm = offline_llm(provider_cls)
    messages = [{"role": "user", "content": "my assistant helps me schedule meetings"}]
    llm.generate_response(messages)
    assert messages[-1]["content"] == "my ai helps me schedule meetings", messages
    assert llm.client.chat.completions.requests[-1]["messages"] is messages
    assert llm.client.chat.completions.requests[-1]["messages"][-1]["content"] == "my ai helps me schedule meetings"

    multimodal = [{"role": "user", "content": [{"type": "text", "text": "describe my assistant"}]}]
    try:
        llm.generate_response(multimodal)
    except AttributeError as exc:
        assert "'list' object has no attribute 'replace'" in str(exc), repr(exc)
    else:
        raise AssertionError("expected AttributeError for list-valued multimodal content")


for provider in (AzureOpenAILLM, AzureOpenAIStructuredLLM):
    assert_mutation_and_multimodal_crash(provider)

print("BUG REPRODUCED: both Azure providers mutate caller content and raise AttributeError for multimodal lists")
raise SystemExit(1)
