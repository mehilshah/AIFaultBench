#!/usr/bin/env python3
"""Minimal reproduction for adapters import failure with huggingface-hub 0.26.0."""

from __future__ import annotations

import os
import pathlib
import sys
import traceback


ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "codebase" / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def main() -> int:
    print("Repro start")
    print(f"Using adapters source from: {SRC}")
    try:
        from adapters import LoRAConfig  # noqa: F401

        print("Import succeeded unexpectedly")
        return 0
    except Exception as exc:
        print(f"Import failed: {exc!r}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
