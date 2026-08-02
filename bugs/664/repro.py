#!/usr/bin/env python3
"""Offline reproduction for Bedrock Converse streaming tool-input normalization."""

from llama_index.core.base.llms.types import ChatMessage, MessageRole, ToolCallBlock
from llama_index.llms.bedrock_converse import BedrockConverse
import llama_index.llms.bedrock_converse.base as bedrock_base


def fake_converse_with_retry(**_kwargs):
    """Return the shape emitted by Bedrock ConverseStream; no AWS call is made."""
    return {
        "stream": [
            {
                "contentBlockStart": {
                    "start": {
                        "toolUse": {"toolUseId": "call-1", "name": "lookup"}
                    }
                }
            },
            {
                "contentBlockDelta": {
                    "delta": {"toolUse": {"input": '{"document_'}}
                }
            },
            {
                "contentBlockDelta": {
                    "delta": {"toolUse": {"input": 'id":"123"}'}}
                }
            },
            {"metadata": {"usage": {"inputTokens": 1, "outputTokens": 1}}},
        ]
    }


bedrock_base.converse_with_retry = fake_converse_with_retry
llm = BedrockConverse(
    model="anthropic.claude-3-haiku-20240307-v1:0",
    client=object(),
    aws_access_key_id="offline",
    aws_secret_access_key="offline",
    region_name="us-east-1",
)
responses = list(
    llm.stream_chat([ChatMessage(role=MessageRole.USER, content="use lookup")])
)
tool_call = next(
    block
    for block in responses[-1].message.blocks
    if isinstance(block, ToolCallBlock)
)

if isinstance(tool_call.tool_kwargs, str):
    print(f"OBSERVED BUG: ToolCallBlock.tool_kwargs is str: {tool_call.tool_kwargs}")
    raise AssertionError("streaming tool input was not normalized to a dict")

raise AssertionError(f"bug absent: expected str, got {type(tool_call.tool_kwargs).__name__}")
