#!/usr/bin/env python3
"""Reproduce DSPy's failure merging Anthropic prompt-cache usage objects.

No provider is contacted: CacheCreationTokenDetails is a local Pydantic stand-in
for the non-addable object returned by Anthropic's usage payload.
"""

from pydantic import BaseModel

from dspy.utils.usage_tracker import UsageTracker


class CacheCreationTokenDetails(BaseModel):
    ephemeral_1h_input_tokens: int
    ephemeral_5m_input_tokens: int


def cache_usage() -> dict[str, object]:
    return {
        "prompt_tokens": 100,
        "completion_tokens": 50,
        "prompt_tokens_details": {
            "cache_creation_token_details": CacheCreationTokenDetails(
                ephemeral_1h_input_tokens=1024,
                ephemeral_5m_input_tokens=512,
            )
        },
    }


def main() -> None:
    tracker = UsageTracker()
    tracker.add_usage("anthropic/claude-with-caching", cache_usage())
    tracker.add_usage("anthropic/claude-with-caching", cache_usage())

    try:
        tracker.get_total_tokens()
    except TypeError as error:
        expected = "unsupported operand type(s) for +: 'CacheCreationTokenDetails' and 'CacheCreationTokenDetails'"
        assert str(error) == expected, f"unexpected TypeError: {error!s}"
        print(f"BUG REPRODUCED: {error}")
        raise

    raise AssertionError("Bug not reproduced: UsageTracker merged non-addable cache details")


if __name__ == "__main__":
    main()
