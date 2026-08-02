#!/usr/bin/env python3
"""Exercise langgraph-api 0.4.46's UI-bundler launch on uvloop."""

import asyncio
import os
import sys
import tempfile
from pathlib import Path

# These are required while importing langgraph_api.config; no service is contacted.
os.environ.setdefault("DATABASE_URI", "postgresql://unused.invalid/db")
os.environ.setdefault("REDIS_URI", "redis://unused.invalid:6379/0")

import uvloop
from langgraph_api.js import ui


async def trigger() -> None:
    # Avoid Node/npm entirely.  uvloop rejects env=os.environ before it starts this
    # local Python process, which is the faulty UI-bundler call site.
    ui.shutil.which = lambda name: sys.executable if name == "npx" else None
    with tempfile.TemporaryDirectory() as directory:
        ui.UI_ROOT_DIR = Path(directory) / "ui"
        await ui._start_ui_bundler_process()


def main() -> None:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    try:
        asyncio.run(trigger())
    except TypeError as exc:
        expected = "Expected dict, got _Environ"
        if str(exc) != expected:
            raise AssertionError(f"unexpected TypeError: {exc!s}") from exc
        print(f"OBSERVED BUG: {type(exc).__name__}: {exc}")
        raise
    raise AssertionError("UI bundler unexpectedly accepted os.environ under uvloop")


if __name__ == "__main__":
    main()
