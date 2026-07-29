#!/usr/bin/env python3
"""Reproduce the unavailable PostgreSQL LangGraph runtime backend."""

import os


os.environ["LANGGRAPH_RUNTIME_EDITION"] = "postgres"

try:
    import langgraph_runtime  # noqa: F401
except ImportError as error:
    expected = (
        "Langgraph runtime backend not found. Please install with "
        '`pip install "langgraph-runtime-postgres"`'
    )
    assert str(error) == expected, f"unexpected ImportError: {error!r}"
    print(f"OBSERVED BUG: ImportError: {error}")
    raise SystemExit(1)
else:
    raise AssertionError("expected the unavailable postgres runtime to fail importing")
