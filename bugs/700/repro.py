#!/usr/bin/env python3
"""Reproduce the missing optional `ddgs` dependency in smolagents."""

import sys

EXPECTED_MESSAGE = "You must install package `ddgs` to run this tool: for instance run `pip install ddgs`."
EXPECTED_CAUSE = "No module named 'ddgs'"

from smolagents import DuckDuckGoSearchTool

try:
    DuckDuckGoSearchTool()
except ImportError as error:
    if str(error) != EXPECTED_MESSAGE:
        raise AssertionError(f"unexpected ImportError: {error!s}") from error
    if not isinstance(error.__cause__, ModuleNotFoundError) or str(error.__cause__) != EXPECTED_CAUSE:
        raise AssertionError(f"unexpected chained exception: {error.__cause__!r}") from error
    print(f"OBSERVED BUG: ImportError: {error}")
    sys.exit(1)
else:
    print("NOT REPRODUCED: DuckDuckGoSearchTool initialized without ddgs.")
