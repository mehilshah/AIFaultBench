#!/usr/bin/env python3
"""Minimal reproduction for jaxtyping issue 231."""

from __future__ import annotations

import sys
import traceback

import numpy as np
from beartype import beartype
from jaxtyping import AnnotationError, Integer


@beartype
def append_one(array: Integer[np.ndarray, "dim"]) -> Integer[np.ndarray, "dim+1"]:
    return np.append(array, 1)


def main() -> int:
    print("Running direct @beartype repro for jaxtyping symbolic return axis handling.")
    print("Input array: [1, 2]")
    try:
        result = append_one(np.array([1, 2]))
    except AnnotationError as exc:
        print("Reproduced jaxtyping.AnnotationError.")
        print(f"Message: {exc}")
        traceback.print_exc()
        expected = "Cannot process symbolic axis 'dim+1'"
        if expected in str(exc):
            print("Observed the misleading symbolic-axis error message from the report.")
            return 0
        print("AnnotationError was raised, but the message differed from the report.")
        return 1
    except Exception:
        print("Unexpected exception type.")
        traceback.print_exc()
        return 1

    print(f"Unexpected success: {result!r}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
