#!/usr/bin/env python3
"""Run the formatter check that reproduces the bug."""

from __future__ import annotations

import pathlib
import subprocess
import sys


def main() -> int:
    root = pathlib.Path(__file__).resolve().parent
    codebase = root / "codebase"
    ruff = root / ".venv" / "bin" / "ruff"

    proc = subprocess.run(
        [str(ruff), "format", "--check", "--diff", "."],
        cwd=codebase,
        text=True,
        capture_output=True,
    )

    if proc.stdout:
        sys.stdout.write(proc.stdout)
    if proc.stderr:
        sys.stderr.write(proc.stderr)

    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
