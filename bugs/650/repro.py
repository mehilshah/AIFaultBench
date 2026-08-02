#!/usr/bin/env python3
"""Offline reproduction for GradioUI's incompatible gr.Blocks theme argument."""

from smolagents import GradioUI


class StubAgent:
    """Only the metadata GradioUI reads before creating its component tree."""

    name = "stub"
    description = None


try:
    GradioUI(StubAgent()).create_app()
except TypeError as exc:
    expected = "BlockContext.__init__() got an unexpected keyword argument 'theme'"
    assert str(exc) == expected, f"unexpected TypeError: {exc!r}"
    print(f"OBSERVED BUG: {type(exc).__name__}: {exc}")
    raise
else:
    print("BUG NOT OBSERVED: GradioUI.create_app() accepted theme='ocean'.")
