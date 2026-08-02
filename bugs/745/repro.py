#!/usr/bin/env python3
"""Probe the import-order bug from langchain issue #37835 without any provider calls."""

try:
    import langchain.agents  # noqa: F401
    from langchain_core.language_models.llms import BaseLLM  # noqa: F401
except TypeError as error:
    if "'function' object is not subscriptable" not in str(error):
        raise
    print(f"BUG OBSERVED: {type(error).__name__}: {error}")
    raise SystemExit(1)

print("BUG NOT OBSERVED: BaseLLM imported after langchain.agents")
raise SystemExit(0)
