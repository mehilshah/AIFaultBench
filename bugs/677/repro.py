#!/usr/bin/env python3
"""Offline reproduction of semantic-kernel issue #13174."""

import asyncio

from opentelemetry.instrumentation.openai_v2.patch import StreamWrapper
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.open_ai_prompt_execution_settings import (
    OpenAIChatPromptExecutionSettings,
)
from semantic_kernel.connectors.ai.open_ai.services.open_ai_handler import OpenAIHandler
from semantic_kernel.exceptions import ServiceResponseException


class EmptyAsyncStream:
    async def __anext__(self):
        raise StopAsyncIteration


class NoOpSpan:
    def end(self):
        pass

    def get_span_context(self):
        return type("SpanContext", (), {"trace_id": 0, "span_id": 0, "trace_flags": 0})()


class NoOpEventLogger:
    def emit(self, event):
        pass


class FakeCompletions:
    async def create(self, **kwargs):
        # This is the real wrapper returned by OpenAIInstrumentor for a stream.
        return StreamWrapper(EmptyAsyncStream(), NoOpSpan(), NoOpEventLogger(), False)


class FakeClient:
    class Chat:
        completions = FakeCompletions()

    chat = Chat()


async def reproduce() -> None:
    # model_construct bypasses AsyncOpenAI's type validation only; FakeClient has
    # the same chat.completions.create surface and never performs I/O.
    handler = OpenAIHandler.model_construct(client=FakeClient())
    settings = OpenAIChatPromptExecutionSettings(ai_model_id="offline-test", stream=True)
    await handler._send_completion_request(settings)


def main() -> None:
    try:
        asyncio.run(reproduce())
    except ServiceResponseException as error:
        cause = error.__cause__
        expected = "'StreamWrapper' object has no attribute 'usage'"
        if isinstance(cause, AttributeError) and str(cause) == expected:
            print(f"OBSERVED BUG: AttributeError: {cause}")
            raise SystemExit(1)
        raise
    raise AssertionError("Expected StreamWrapper usage AttributeError was not raised")


if __name__ == "__main__":
    main()
