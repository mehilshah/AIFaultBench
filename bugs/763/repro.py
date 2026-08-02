#!/usr/bin/env python3
"""Reproduce the missing dspy.AzureOpenAI public API in the pinned checkout."""

import dspy


def main() -> int:
    try:
        dspy.AzureOpenAI
    except AttributeError as exc:
        expected = "module 'dspy' has no attribute 'AzureOpenAI'"
        assert str(exc) == expected, f"unexpected AttributeError: {exc!s}"
        print(f"OBSERVED BUG: {type(exc).__name__}: {exc}")
        return 1

    print("BUG NOT OBSERVED: dspy.AzureOpenAI is present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
