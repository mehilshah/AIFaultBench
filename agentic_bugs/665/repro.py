#!/usr/bin/env python3
"""Reproduce OpenAI Chat Completions tool-argument serialization bug."""

from llama_index.core.base.llms.types import ChatMessage, MessageRole, ToolCallBlock
from llama_index.llms.openai.utils import to_openai_message_dict


message = ChatMessage(
    role=MessageRole.ASSISTANT,
    blocks=[
        ToolCallBlock(
            tool_name="handoff",
            tool_kwargs={"agent_name": "worker"},
            tool_call_id="call_123",
        )
    ],
)
converted = to_openai_message_dict(message)
arguments = converted["tool_calls"][0]["function"]["arguments"]

if isinstance(arguments, str):
    print("NOT REPRODUCED: function.arguments was JSON string")
    raise SystemExit(0)

print(f"OBSERVED BUG: function.arguments is {type(arguments).__name__}: {arguments!r}")
assert isinstance(arguments, dict), "unexpected non-string tool arguments value"
raise AssertionError("OpenAI Chat Completions requires function.arguments to be a JSON string")
