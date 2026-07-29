#!/usr/bin/env python3
"""Offline reproduction for langgraph-cli 0.4.29's incompatible in-memory deps."""

import asyncio
import os

# langgraph_api reads these at import time.  They name unreachable local services;
# the corresponding startup routines below are replaced before the lifespan runs.
os.environ.setdefault("DATABASE_URI", "postgresql://unused:unused@127.0.0.1:1/unused")
os.environ.setdefault("REDIS_URI", "redis://127.0.0.1:1/0")

import langgraph_api._checkpointer as checkpointer
import langgraph_api.http as http
import langgraph_api.js.ui as ui
import langgraph_runtime_inmem.lifespan as runtime_lifespan


async def _no_network_startup(*_args: object, **_kwargs: object) -> None:
    """Keep the real lifespan on its compatibility-check path, fully offline."""


http.start_http_client = _no_network_startup
checkpointer.start_checkpointer = _no_network_startup
ui.start_ui_bundler = _no_network_startup
runtime_lifespan.start_pool = _no_network_startup


async def reproduce() -> bool:
    try:
        async with runtime_lifespan.lifespan():
            raise AssertionError("lifespan unexpectedly started")
    except AttributeError as exc:
        expected = "module 'langgraph_api.config' has no attribute 'LSD_PROM_METRICS_ENABLED'"
        assert str(exc) == expected, f"unexpected AttributeError: {exc!r}"
        print(f"OBSERVED BUG: AttributeError: {exc}")
        return True


if __name__ == "__main__":
    if reproduce_result := asyncio.run(reproduce()):
        # A non-zero exit is the benchmark verdict: the faulty behavior exists.
        raise SystemExit(1)
    raise AssertionError(f"unexpected reproduction result: {reproduce_result!r}")
