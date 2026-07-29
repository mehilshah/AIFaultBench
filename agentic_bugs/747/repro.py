#!/usr/bin/env python3
"""Probe langchain-ai/langchain#37723 without an OpenAI API call."""

import warnings
from types import SimpleNamespace

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from pydantic import BaseModel
from openai import NOT_GIVEN
from openai.lib._parsing._completions import parse_chat_completion
from openai.types.chat.chat_completion import ChatCompletion, ChatCompletionMessage, Choice


class IntentRecognitionOutput(BaseModel):
    classification: str


class FakeRawResponse:
    """Offline replacement for OpenAI's raw response wrapper."""

    def __init__(self, response: object) -> None:
        self.response = response

    def parse(self) -> object:
        return self.response


def main() -> None:
    # Build the same ParsedChatCompletion generic that OpenAI's local parser returns.
    raw_completion = ChatCompletion.model_construct(
        id="chatcmpl-local",
        object="chat.completion",
        created=0,
        model="gpt-4o-mini",
        choices=[
            Choice.model_construct(
                index=0,
                finish_reason="stop",
                message=ChatCompletionMessage.model_construct(
                    role="assistant", content='{"classification": "billing"}'
                ),
            )
        ],
    )
    response = parse_chat_completion(
        response_format=IntentRecognitionOutput,
        input_tools=NOT_GIVEN,
        chat_completion=raw_completion,
    )

    llm = ChatOpenAI(model="gpt-4o-mini", api_key="not-used")
    # The reported default is method="json_schema", which calls this parser route.
    llm.root_client = SimpleNamespace(
        chat=SimpleNamespace(
            completions=SimpleNamespace(
                with_raw_response=SimpleNamespace(
                    parse=lambda **_payload: FakeRawResponse(response)
                )
            )
        )
    )

    # Invoke the report's public structured-output API. The fake above prevents I/O.
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        result = llm.with_structured_output(IntentRecognitionOutput).invoke(
            [SystemMessage(content="Classify the intent.")]
        )

    parsed_warnings = [
        str(item.message) for item in caught if "field_name='parsed'" in str(item.message)
    ]
    if parsed_warnings:
        print(f"OBSERVED BUG: {parsed_warnings[0]}")
        raise SystemExit(1)
    if result != IntentRecognitionOutput(classification="billing"):
        raise AssertionError(f"Unexpected structured output: {result!r}")
    print("NOT REPRODUCED: structured output completed with no parsed-field serializer warning")


if __name__ == "__main__":
    main()
