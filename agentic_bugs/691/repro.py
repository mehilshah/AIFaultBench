#!/usr/bin/env python3
"""Reproduce loss of AIMessage.tool_calls through a BaseMessage Pydantic field."""

from langchain_core.messages import AIMessage, BaseMessage, ToolCall
from pydantic import BaseModel


class State(BaseModel):
    messages: list[BaseMessage]


message = AIMessage(
    content="foo",
    tool_calls=[ToolCall(id="bar", args={"baz": "qux"}, name="quux")],
)
direct_dump = message.model_dump()
state_dump = State(messages=[message]).model_dump()

assert direct_dump["tool_calls"] == [
    {"name": "quux", "args": {"baz": "qux"}, "id": "bar", "type": "tool_call"}
]
serialized_message = state_dump["messages"][0]
if "tool_calls" not in serialized_message:
    print("BUG REPRODUCED: State.model_dump() dropped AIMessage.tool_calls")
    raise RuntimeError(f"serialized message lacks tool_calls: {serialized_message!r}")

raise AssertionError(f"bug no longer present: {serialized_message!r}")
