#!/usr/bin/env python3
"""Reproduce the missing public CompiledStateGraph export in langgraph 1.0.3."""

import warnings

warnings.filterwarnings("ignore")

try:
    from langgraph.graph import CompiledStateGraph  # noqa: F401
except ImportError as exc:
    expected = "cannot import name 'CompiledStateGraph' from 'langgraph.graph'"
    if expected not in str(exc):
        raise AssertionError(f"unexpected ImportError: {exc}") from exc
    print(f"OBSERVED ImportError: {exc}")
    raise SystemExit(1)
else:
    raise AssertionError("bug not reproduced: CompiledStateGraph was exported")
