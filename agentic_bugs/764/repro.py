#!/usr/bin/env python3
"""Exercise uv's isolated hatchling build for the pinned langflow-base source."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
UV = ROOT / ".venv" / "bin" / "uv"
PACKAGE = ROOT / "codebase" / "src" / "backend" / "base"


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="bug764-uv-") as temporary:
        temp = Path(temporary)
        environment = os.environ | {
            "UV_CACHE_DIR": str(temp / "cache"),
            "UV_NO_PROGRESS": "1",
        }
        result = subprocess.run(
            [str(UV), "build", "--wheel", "--out-dir", str(temp / "wheel"), str(PACKAGE)],
            cwd=ROOT,
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )

    output = result.stdout
    if "ModuleNotFoundError: No module named 'hatchling.build'" in output:
        print("OBSERVED: ModuleNotFoundError: No module named 'hatchling.build'")
        print(output, end="")
        return 1
    if result.returncode != 0:
        print("UNEXPECTED UV BUILD FAILURE")
        print(output, end="")
        return 2

    print("NOT REPRODUCED: uv 0.9.1 built langflow-base with a fresh isolated cache")
    return 0


if __name__ == "__main__":
    sys.exit(main())
