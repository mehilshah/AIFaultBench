#!/usr/bin/env python3
"""Offline regression check for nested Fireworks token usage aggregation."""

from langchain_fireworks import ChatFireworks


outputs = [
    {
        "token_usage": {
            "prompt_tokens": 32,
            "completion_tokens": 51,
            "total_tokens": 83,
            "prompt_tokens_details": {"cached_tokens": 0},
        },
        "model_name": "accounts/fireworks/models/kimi-k2-instruct",
    },
    {
        "token_usage": {
            "prompt_tokens": 44341,
            "completion_tokens": 10,
            "total_tokens": 44351,
            "prompt_tokens_details": {"cached_tokens": 41518},
        },
        "model_name": "accounts/fireworks/models/kimi-k2-instruct",
    },
]

try:
    # The combiner does not use self, so this exercises the exact code path without
    # constructing a provider client or providing credentials.
    combined = ChatFireworks._combine_llm_outputs(None, outputs)
except TypeError as exc:
    expected = "unsupported operand type(s) for +=: 'dict' and 'dict'"
    assert str(exc) == expected, f"unexpected TypeError: {exc}"
    print(f"OBSERVED BUG: ChatFireworks._combine_llm_outputs raised TypeError: {exc}")
    raise

assert combined["token_usage"]["prompt_tokens_details"] == {"cached_tokens": 41518}
print("PASS: nested token usage was combined correctly")
