#!/usr/bin/env python3
"""Offline reproduction of camel-ai/camel#3602."""

from importlib.metadata import version

from camel.agents.chat_agent import ChatAgent, StreamContentAccumulator


class UsageWithMissingCompletionTokens:
    """A provider's streamed usage payload with a null completion count."""

    def model_dump(self):
        return {
            "prompt_tokens": 4,
            "completion_tokens": None,
            "total_tokens": 4,
        }


class UsageOnlyStreamChunk:
    choices = []
    id = "offline-usage-chunk"
    usage = UsageWithMissingCompletionTokens()


agent = object.__new__(ChatAgent)
usage_tracker = agent._create_token_usage_tracker()
print(f"camel-ai version: {version('camel-ai')}")

try:
    # This is the same streaming accumulator invoked by ChatAgent.step(); it
    # consumes an offline usage-only final chunk and makes no API request.
    list(
        agent._process_stream_chunks_with_accumulator(
            [UsageOnlyStreamChunk()],
            StreamContentAccumulator(),
            {},
            [],
            usage_tracker,
        )
    )
except TypeError as error:
    expected = "unsupported operand type(s) for +=: 'int' and 'NoneType'"
    assert str(error) == expected, f"unexpected TypeError: {error}"
    print(f"OBSERVED BUG: {type(error).__name__}: {error}")
    raise
else:
    raise AssertionError(
        "Expected streaming usage with completion_tokens=None to fail, "
        f"but tracker became {usage_tracker!r}"
    )
