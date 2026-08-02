#!/usr/bin/env python3
"""Offline reproduction of issue #2073's same-name module shadowing."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


SOURCE = "from smolagents import OpenAIServerModel, CodeAgent\n"
EXPECTED = "cannot import name 'OpenAIServerModel' from partially initialized module 'smolagents'"


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="smolagents-shadow-") as directory:
        script = Path(directory) / "smolagents.py"
        script.write_text(SOURCE, encoding="utf-8")
        completed = subprocess.run(
            [sys.executable, script.name],
            cwd=directory,
            text=True,
            capture_output=True,
            check=False,
        )

    if completed.returncode == 0 or EXPECTED not in completed.stderr or "smolagents.py" not in completed.stderr:
        raise AssertionError(
            "Expected local smolagents.py to shadow the package and raise the reported ImportError; "
            f"returncode={completed.returncode}, stderr={completed.stderr!r}"
        )

    print(f"OBSERVED: ImportError: {EXPECTED}")
    raise SystemExit(1)


if __name__ == "__main__":
    main()
