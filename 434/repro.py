#!/usr/bin/env python3
"""Minimal reproduction for Gemma4's unsafe dtype cast.

The bug report describes two forward methods that cast floating-point inputs
to the dtype of quantized weights:

  - pixel_values.to(self.input_proj.weight.dtype)
  - hidden_states.to(self.conv.weight.dtype)

If the weight dtype is an integer type, the float input is silently truncated.
This script demonstrates the failure mode locally without downloading the full
Gemma4 model.
"""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parent
CODEBASE_FILE = ROOT / "codebase" / "src" / "transformers" / "models" / "gemma4" / "modeling_gemma4.py"


def print_source_context() -> None:
    lines = CODEBASE_FILE.read_text(encoding="utf-8").splitlines()
    targets = [
        "hidden_states = self.conv(hidden_states.to(self.conv.weight.dtype))",
        "hidden_states = self.input_proj(pixel_values.to(self.input_proj.weight.dtype))",
    ]
    print("Local source context:")
    for target in targets:
        for idx, line in enumerate(lines, start=1):
            if target in line:
                print(f"  {CODEBASE_FILE}:{idx}: {line.strip()}")
                break
        else:
            print(f"  MISSING: {target}")


def cast_like_bug(values: np.ndarray, weight_dtype: np.dtype) -> np.ndarray:
    # Mirrors the buggy pattern in Gemma4: cast the activations to the weight dtype.
    return values.astype(weight_dtype)


def cast_like_fix(values: np.ndarray, weight_dtype: np.dtype) -> np.ndarray:
    # This is the intended behavior: only cast when the target dtype is floating-point.
    if np.issubdtype(weight_dtype, np.floating):
        return values.astype(weight_dtype)
    return values


def main() -> int:
    print_source_context()
    print()

    pixel_values = np.array([0.73, 1.25, -0.4], dtype=np.float32)
    quantized_weight_dtype = np.dtype(np.int8)

    buggy = cast_like_bug(pixel_values, quantized_weight_dtype)
    fixed = cast_like_fix(pixel_values, quantized_weight_dtype)

    print("Input activations:       ", pixel_values, pixel_values.dtype)
    print("Quantized weight dtype:  ", quantized_weight_dtype)
    print("Buggy cast result:       ", buggy, buggy.dtype)
    print("Fixed-path result:       ", fixed, fixed.dtype)

    if np.array_equal(buggy, np.array([0, 1, 0], dtype=np.int8)):
        print()
        print(
            "BUG REPRODUCED: float activations are silently truncated when cast to an integer weight dtype.",
            file=sys.stderr,
        )
        return 1

    print()
    print("BUG NOT REPRODUCED: unexpected cast behavior.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
