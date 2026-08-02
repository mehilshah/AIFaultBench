#!/usr/bin/env python3
"""Offline check for the Gemini 3 missing-thought-signature report."""

from camel.models.gemini_model import GeminiModel


def main() -> None:
    # This is the assistant tool-call history that Gemini rejected in the
    # report: its first function call does not carry a thought_signature.
    history = [
        {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": "call_1",
                    "type": "function",
                    "function": {"name": "shell_exec", "arguments": "{}"},
                }
            ],
        }
    ]

    # Invoke the real _run pre-request path, but replace its final transport
    # with a local recorder. Bypassing __init__ avoids credentials and the fake
    # transport guarantees that no provider request can occur.
    model = object.__new__(GeminiModel)
    model.model_config_dict = {}
    captured = {}

    def fake_request(messages, tools):
        captured["messages"] = messages
        return "fake-response"

    model._request_chat_completion = fake_request
    assert model._run(history, tools=[]) == "fake-response"

    signature = captured["messages"][0]["tool_calls"][0]["extra_content"]["google"][
        "thought_signature"
    ]

    assert signature == "skip_thought_signature_validator", signature
    assert "extra_content" not in history[0]["tool_calls"][0], (
        "message history was mutated"
    )
    print(
        "NOT REPRODUCED: missing Gemini tool-call thought_signature was "
        f"replaced with fallback {signature!r}."
    )


if __name__ == "__main__":
    main()
