#!/usr/bin/env python3
"""Offline reproduction of CAMEL's invalid Bedrock multi-tool result payload."""

from camel.models.aws_bedrock_converse_model import AWSBedrockConverseModel


def main() -> None:
    model = AWSBedrockConverseModel(
        model_type="amazon.nova-lite-v1:0",
        model_config_dict={"temperature": 0.0, "max_tokens": 16},
        region_name="us-east-1",
        bedrock_client=object(),  # Request construction only; no AWS call.
    )
    request = model._build_converse_request(
        [
            {"role": "user", "content": "Call both tools."},
            {
                "role": "assistant",
                "content": None,
                "tool_calls": [
                    {
                        "id": "tooluse_a",
                        "type": "function",
                        "function": {"name": "tool_a", "arguments": "{}"},
                    },
                    {
                        "id": "tooluse_b",
                        "type": "function",
                        "function": {"name": "tool_b", "arguments": "{}"},
                    },
                ],
            },
            {"role": "tool", "tool_call_id": "tooluse_a", "content": "A"},
            {"role": "tool", "tool_call_id": "tooluse_b", "content": "B"},
        ]
    )

    messages = request["messages"]
    tool_uses = messages[1]["content"]
    first_results = messages[2]["content"]
    second_results = messages[3]["content"]
    assert len(tool_uses) == 2 and all("toolUse" in block for block in tool_uses)
    assert len(first_results) == len(second_results) == 1
    assert "toolResult" in first_results[0] and "toolResult" in second_results[0]

    print(
        "Observed Bedrock-invalid payload: 2 toolUse blocks are followed by "
        "two separate user toolResult messages (1 result each).",
        flush=True,
    )
    raise RuntimeError(
        "Bug reproduced: Bedrock requires both toolResult blocks in the immediately following user message."
    )


if __name__ == "__main__":
    main()
