#!/usr/bin/env python3
"""Offline reproduction for DSPy issue #9032."""

import dspy


try:
    dspy.LM("azure/gpt-5-chat", temperature=0.7, max_tokens=1000)
except ValueError as exc:
    expected = "OpenAI's reasoning models require passing temperature=1.0 or None and max_tokens >= 16000 or None"
    assert expected in str(exc), f"unexpected ValueError: {exc}"
    print(f"BUG REPRODUCED: gpt-5-chat was classified as a reasoning model: {exc}")
    raise SystemExit(1)

raise AssertionError("gpt-5-chat was not incorrectly classified as a reasoning model")
