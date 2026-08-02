#!/usr/bin/env python3
"""Offline reproducer for AutoGen issue #6906 using the reported OpenAI SDK."""

from autogen_ext.models.openai._openai_client import convert_tools


TOOL_SCHEMA = {
    "name": "echo",
    "description": "Echo the input text",
    "parameters": {
        "type": "object",
        "properties": {"text": {"type": "string"}},
        "required": ["text"],
    },
}


try:
    convert_tools([TOOL_SCHEMA])
except TypeError as exc:
    if str(exc) != "Cannot instantiate typing.Union":
        raise AssertionError(f"unexpected TypeError: {exc!s}") from exc
    print("BUG OBSERVED: valid tool schema raises TypeError: Cannot instantiate typing.Union")
    raise
else:
    raise AssertionError("BUG NOT OBSERVED: valid tool schema converted successfully")
