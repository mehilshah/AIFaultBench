#!/usr/bin/env python3
"""Minimal reproducer for the reported SDV import/collection failure.

The bug report describes a Windows-only crash while collecting the minimum test
suite after installing SDV with a torch 2.9.x / numpy<2 environment.

This script probes the local environment, then tries the same import path that
`tests/unit/version/test_version.py` exercises.
"""

from __future__ import annotations

import platform
import subprocess
import sys
import traceback
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def run_pytest() -> int:
    """Run the narrow version test that imports `sdv`."""
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        str(ROOT / "codebase" / "tests" / "unit" / "version" / "test_version.py"),
        "-q",
    ]
    print(f"$ {' '.join(cmd)}")
    completed = subprocess.run(cmd, cwd=ROOT, check=False)
    return completed.returncode


def main() -> int:
    print(f"platform: {platform.platform()}")
    print(f"python: {sys.version}")
    print(f"executable: {sys.executable}")

    try:
        import numpy  # type: ignore

        print(f"numpy: {numpy.__version__}")
    except Exception:
        print("numpy import failed:")
        traceback.print_exc()

    try:
        import torch  # type: ignore

        print(f"torch: {torch.__version__}")
    except Exception:
        print("torch import failed:")
        traceback.print_exc()

    if platform.system() != "Windows":
        print(
            "note: the reported WinError 1114 is Windows-specific; "
            "this host is not Windows."
        )

    try:
        import sdv  # type: ignore

        print(f"sdv: {sdv.__version__}")
    except Exception:
        print("sdv import failed:")
        traceback.print_exc()
        return 1

    return run_pytest()


if __name__ == "__main__":
    raise SystemExit(main())
