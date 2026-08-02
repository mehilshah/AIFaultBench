#!/usr/bin/env python3
"""Reproduce smolagents issue #1565 without contacting an LLM provider."""

from smolagents import LiteLLMModel


class NoNetworkClient:
    """Fails if execution gets past the local message-normalization bug."""

    def completion(self, **kwargs):
        raise AssertionError("unexpected inference request")


messages = [
    {"role": "user", "content": [{"type": "text", "text": "Hello, how are you?"}]}
]

try:
    LiteLLMModel(model_id="offline/fake", client=NoNetworkClient())(messages)
except AttributeError as error:
    expected = "'dict' object has no attribute 'role'"
    if str(error) != expected:
        raise AssertionError(f"unexpected AttributeError: {error}") from error
    print(f"OBSERVED BUG: AttributeError: {error}")
    raise
else:
    raise AssertionError("dict messages unexpectedly reached the inference client")
