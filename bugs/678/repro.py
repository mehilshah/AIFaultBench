#!/usr/bin/env python3
"""Offline reproducer for Bedrock Converse's top-level-list tool result bug."""

from camel.models.aws_bedrock_converse_model import AWSBedrockConverseModel


class BedrockValidationException(Exception):
    """The validation response that Bedrock Converse gives for this request."""


class ValidatingBedrockClient:
    """Offline Bedrock double that enforces Bedrock's JSON-object requirement."""

    def converse(self, **request):
        json_value = request["messages"][1]["content"][0]["toolResult"][
            "content"
        ][0]["json"]
        if isinstance(json_value, list):
            raise BedrockValidationException(
                "ValidationException: The format of the value at "
                "messages.1.content.0.toolResult.content.0.json is invalid. "
                "Provide a json object for the field and try again."
            )
        return {
            "output": {"message": {"content": [{"text": "valid"}]}},
            "stopReason": "end_turn",
            "usage": {},
            "ResponseMetadata": {"RequestId": "offline-valid-response"},
        }


def main() -> None:
    model = AWSBedrockConverseModel(
        model_type="amazon.nova-lite-v1:0",
        model_config_dict={"temperature": 0.0, "max_tokens": 1},
        region_name="us-east-1",
        bedrock_client=ValidatingBedrockClient(),
    )
    messages = [
        {
            "role": "assistant",
            "content": "",
            "tool_calls": [
                {
                    "id": "call_1",
                    "type": "function",
                    "function": {"name": "search_papers", "arguments": "{}"},
                }
            ],
        },
        {"role": "tool", "tool_call_id": "call_1", "content": []},
    ]
    try:
        model._run(messages)
    except BedrockValidationException as exc:
        print(f"OBSERVED BUG: {exc}")
        raise
    raise AssertionError("Expected Bedrock to reject a top-level list tool result")


if __name__ == "__main__":
    main()
