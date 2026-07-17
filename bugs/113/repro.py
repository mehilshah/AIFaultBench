#!/usr/bin/env python3
"""Minimal repro for repeated-axis diagonal patterns in einops."""

from __future__ import annotations

import os
import sys

import numpy as np


ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "codebase"))

from einops import EinopsError, rearrange, reduce  # noqa: E402


def expect_einops_error(label: str, func) -> tuple[str, str]:
    try:
        func()
    except EinopsError as exc:
        message = str(exc)
        print(f"{label}: EinopsError")
        print(message)
        return "EinopsError", message
    except Exception as exc:  # pragma: no cover - unexpected path
        print(f"{label}: unexpected {type(exc).__name__}")
        print(exc)
        raise
    else:  # pragma: no cover - unexpected path
        raise AssertionError(f"{label}: operation unexpectedly succeeded")


def main() -> int:
    matrix = np.arange(9).reshape(3, 3)
    tensor = np.arange(27).reshape(3, 3, 3)
    vector = np.arange(3)

    print(f"numpy={np.__version__}")
    print(f"matrix.shape={matrix.shape}")
    print(f"tensor.shape={tensor.shape}")

    results = [
        expect_einops_error("rearrange('ii->i')", lambda: rearrange(matrix, "ii->i")),
        expect_einops_error("rearrange('iii->i')", lambda: rearrange(tensor, "iii->i")),
        expect_einops_error("rearrange('i->ii')", lambda: rearrange(vector, "i->ii")),
        expect_einops_error("reduce('ii->i', 'sum')", lambda: reduce(matrix, "ii->i", "sum")),
        expect_einops_error("reduce('ii->i', 'max')", lambda: reduce(matrix, "ii->i", "max")),
    ]

    if not all(kind == "EinopsError" for kind, _message in results):
        raise AssertionError("Expected EinopsError for all diagonal patterns.")

    print("All reported diagonal patterns fail with EinopsError.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
