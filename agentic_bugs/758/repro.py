#!/usr/bin/env python3
"""Deterministically reproduce #1674 without contacting Amazon Bedrock."""

import sys

from smolagents import AmazonBedrockServerModel


class FakeBedrockClient:
    """Simulated DeepSeek-style Bedrock response: text precedes reasoning content."""

    def __init__(self):
        self.called = False

    def converse(self, **kwargs):
        self.called = True
        assert kwargs["modelId"] == "us.deepseek.r1-v1:0"
        return {
            "output": {
                "message": {
                    "role": "assistant",
                    "content": [
                        {"text": "The requested answer."},
                        {
                            "reasoningContent": {
                                "reasoningText": {"text": "Internal reasoning."},
                                "signature": "recorded-signature",
                            }
                        },
                    ],
                }
            },
            "usage": {"inputTokens": 3, "outputTokens": 7},
        }


def main() -> None:
    client = FakeBedrockClient()
    model = AmazonBedrockServerModel(model_id="us.deepseek.r1-v1:0", client=client)
    try:
        model.generate([{"role": "user", "content": "Hello"}])
    except KeyError as error:
        expected = '"text" field not found in the last element of response["output"]["message"]["content"]'
        assert client.called, "the fake Bedrock client was not called"
        assert expected in str(error), f"unexpected KeyError: {error}"
        print(f"OBSERVED BUG: {type(error).__name__}: {error}")
        raise SystemExit(1)

    raise AssertionError("Bug absent: a response with trailing reasoningContent did not raise KeyError")


if __name__ == "__main__":
    main()
