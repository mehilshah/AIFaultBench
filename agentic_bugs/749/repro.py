#!/usr/bin/env python3
"""Reproduce custom invocation omitting LangGraph's injected ToolRuntime."""

from langchain_core.tools import tool
from langgraph.prebuilt import ToolRuntime
from pydantic import ValidationError


@tool
def get_greeting_rules(runtime: ToolRuntime) -> str:
    """Return greeting guidance using the runtime supplied by ToolNode."""
    return runtime.state.get("user_query", "")


try:
    # This is the custom-node pattern from the report: tool.invoke(tool_call["args"])
    # does not supply the system-owned ToolRuntime argument.
    get_greeting_rules.invoke({})
except ValidationError as exc:
    message = str(exc)
    assert "runtime" in message and "Field required" in message, message
    print("OBSERVED: ValidationError: runtime Field required")
    raise
else:
    raise AssertionError("Expected ValidationError for missing ToolRuntime")
