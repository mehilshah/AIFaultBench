#!/usr/bin/env python3
"""Offline reproduction of the LangGraph Studio thread-history version mismatch."""

import asyncio
import os
import warnings
from importlib.metadata import version

from langchain_core._api.deprecation import (
    LangChainDeprecationWarning,
    LangChainPendingDeprecationWarning,
)

# These are only configuration strings needed while importing langgraph_api.  The
# repro replaces all persistence collaborators before the history code reaches any
# connection, so no database or Redis connection is opened.
os.environ.setdefault("DATABASE_URI", "postgresql://unused")
os.environ.setdefault("REDIS_URI", "redis://unused")
warnings.simplefilter("ignore", LangChainDeprecationWarning)
warnings.simplefilter("ignore", LangChainPendingDeprecationWarning)

import langgraph_api.store as api_store
import langgraph_runtime_inmem.ops as inmem_ops
from langgraph_runtime_inmem.ops import Threads


async def no_auth_filter(*_args, **_kwargs):
    return None


async def one_thread(*_args, **_kwargs):
    async def rows():
        yield {"metadata": {"graph_id": "example"}, "config": {}}

    return rows()


async def no_store():
    return None


async def main() -> None:
    assert version("langgraph-api") == "0.6.20"
    assert version("langgraph-runtime-inmem") == "0.21.0"

    # The production history path needs only these persistence collaborators
    # before it constructs `get_graph(...)`.  Stubbing them keeps this fully
    # local while executing the real incompatible call in Threads.State.list.
    Threads.handle_event = no_auth_filter
    Threads.get = staticmethod(one_thread)
    inmem_ops.Checkpointer = lambda *_args, **_kwargs: object()
    api_store.get_store = no_store

    try:
        await Threads.State.list(
            object(),
            config={
                "configurable": {
                    "thread_id": "00000000-0000-0000-0000-000000000001"
                }
            },
        )
    except TypeError as exc:
        expected = "get_graph() missing 1 required keyword-only argument: 'is_for_execution'"
        assert str(exc) == expected, f"unexpected TypeError: {exc}"
        print(f"OBSERVED BUG: {exc}")
        raise SystemExit(1)
    raise AssertionError("expected Threads.State.list to fail at get_graph")


asyncio.run(main())
