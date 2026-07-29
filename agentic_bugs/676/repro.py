#!/usr/bin/env python3
"""Trigger DSPy's buggy merge of optional token-detail usage entries."""

from dspy.utils.usage_tracker import UsageTracker


def main() -> None:
    tracker = UsageTracker()
    # The second entry turns this field into 0. The third entry has a dict for
    # the same field, so the recursive merge evaluates len(0).
    tracker.add_usage("stubbed-lm", {"completion_tokens": 1, "completion_tokens_details": None})
    tracker.add_usage("stubbed-lm", {"completion_tokens": 2, "completion_tokens_details": None})
    tracker.add_usage(
        "stubbed-lm",
        {"completion_tokens": 3, "completion_tokens_details": {"reasoning_tokens": 0}},
    )

    try:
        tracker.get_total_tokens()
    except TypeError as error:
        expected = "object of type 'int' has no len()"
        assert str(error) == expected, f"unexpected TypeError: {error!s}"
        print(f"OBSERVED BUG: TypeError: {error}", flush=True)
        raise
    raise AssertionError("Expected UsageTracker.get_total_tokens() to raise TypeError")


if __name__ == "__main__":
    main()
