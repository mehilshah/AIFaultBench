#!/usr/bin/env python3
"""Reproduce the strict-endpoint failure without making an HTTP request."""

import sys

import httpx
import openai
from autogen_core import FunctionCall
from autogen_core.models import AssistantMessage
from autogen_ext.models.openai._openai_client import to_oai_type


def strict_openai_compatible_endpoint(messages: list[dict[str, object]]) -> None:
    """Model the validation performed by the issue reporter's strict endpoint."""
    for index, message in enumerate(messages):
        if message.get("role") == "assistant" and "tool_calls" in message and "content" not in message:
            body = {
                "detail": [
                    {
                        "type": "missing",
                        "loc": ["body", "messages", index, "content"],
                        "msg": "Field required",
                        "input": message,
                    }
                ]
            }
            response = httpx.Response(422, json=body, request=httpx.Request("POST", "http://stub/v1/chat/completions"))
            raise openai.UnprocessableEntityError("Error code: 422 - " + str(body), response=response, body=body)


def main() -> int:
    tool_call_message = AssistantMessage(
        content=[
            FunctionCall(id="call_1", name="increment_number", arguments='{"number": 5}'),
            FunctionCall(id="call_2", name="increment_number", arguments='{"number": 6}'),
        ],
        source="looped_assistant",
    )
    payload = list(to_oai_type(tool_call_message))

    try:
        strict_openai_compatible_endpoint(
            [{"role": "system", "content": "use increment_number"}, {"role": "user", "content": "increment 5"}]
            + payload  # type: ignore[arg-type]
        )
    except openai.UnprocessableEntityError as error:
        assert error.status_code == 422
        assert error.body["detail"][0]["loc"] == ["body", "messages", 2, "content"]
        print("OBSERVED: UnprocessableEntityError 422: assistant tool_calls payload omitted required content")
        raise

    print("NOT OBSERVED: assistant tool_calls payload included content")
    return 0


if __name__ == "__main__":
    sys.exit(main())
