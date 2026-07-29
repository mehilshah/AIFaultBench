#!/usr/bin/env python3
"""Offline reproduction for CAMEL issue #3422."""

from camel.agents import ChatAgent


def main() -> None:
    expected = (
        "ChatAgent.__init__() got an unexpected keyword argument "
        "'single_iteration'"
    )
    try:
        # Python rejects this before ChatAgent can construct a model backend.
        ChatAgent(single_iteration=True)
    except TypeError as error:
        if str(error) != expected:
            raise AssertionError(
                f"Unexpected TypeError: {error!s} (expected: {expected})"
            ) from error
        print(f"OBSERVED BUG: {error}")
        raise
    raise AssertionError("Bug not observed: ChatAgent accepted single_iteration")


if __name__ == "__main__":
    main()
