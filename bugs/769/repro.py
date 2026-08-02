#!/usr/bin/env python3
"""Offline reproduction for smolagents issue #1626 at d6b7191."""

from smolagents import tool


@tool
def multiline_signature_tool(
    text: str,
    suffix: str = "!",
) -> str:
    """Append a suffix to text.

    Args:
        text: Text to transform.
        suffix: Suffix to append.
    """
    return text + suffix


try:
    multiline_signature_tool.to_dict()
except SyntaxError as error:
    assert error.msg == "invalid syntax", repr(error)
    assert error.lineno == 2, repr(error)
    print(f"BUG REPRODUCED: to_dict() raised SyntaxError at line {error.lineno}: {error.msg}")
    raise
else:
    raise AssertionError("BUG NOT PRESENT: to_dict() accepted a multiline @tool signature")
