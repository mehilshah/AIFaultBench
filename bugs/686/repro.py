#!/usr/bin/env python3
"""Offline reproduction for langchain-ai/langchain#38644."""

from langchain_anthropic import ChatAnthropic


advisor_tool = {
    "type": "advisor_20260301",
    "name": "advisor",
    "model": "claude-sonnet-4-6",
    "max_uses": 3,
    "max_tokens": 1024,
}

try:
    # bind_tools performs the faulty conversion synchronously; invoke() is not
    # needed, so this never contacts Anthropic and the key is a dummy value.
    ChatAnthropic(
        model="claude-sonnet-4-6", api_key="offline-test-key"
    ).bind_tools([advisor_tool])
except KeyError as error:
    if error.args != ("parameters",):
        raise AssertionError(f"unexpected KeyError: {error!r}") from error
    print("OBSERVED BUG: bind_tools raised KeyError: 'parameters' for advisor_20260301")
    raise SystemExit(1)
else:
    raise AssertionError("BUG NOT REPRODUCED: advisor tool was accepted")
