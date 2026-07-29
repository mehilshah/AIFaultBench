#!/usr/bin/env python3
"""Offline reproducer for OpenAILike structured completion tool_choice forwarding."""

from pydantic import BaseModel

from llama_index.llms.openai_like import OpenAILike


class Invoice(BaseModel):
    total: int


class Completions:
    # Deliberately models an OpenAI-compatible completion endpoint without tools.
    def create(self, prompt, stream, model, temperature):
        raise AssertionError("completion endpoint should reject tool_choice before handling")


class FakeOpenAIClient:
    def __init__(self):
        self.completions = Completions()


def main() -> None:
    client = OpenAILike(
        model="offline-model",
        api_key="not-used",
        is_function_calling_model=False,
        openai_client=FakeOpenAIClient(),
        max_retries=0,
    )
    try:
        client.as_structured_llm(Invoice).complete("Return an invoice total.")
    except TypeError as exc:
        expected = "Completions.create() got an unexpected keyword argument 'tool_choice'"
        if str(exc) != expected:
            raise AssertionError(f"unexpected TypeError: {exc!s}") from exc
        print(f"OBSERVED BUG: {exc}")
        raise SystemExit(1)
    raise AssertionError("Expected tool_choice to be forwarded to a non-tool completion endpoint")


if __name__ == "__main__":
    main()
