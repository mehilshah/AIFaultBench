#!/usr/bin/env python3

"""Minimal repro for BlockDiagonalCausalMask.to() returning the wrong type."""

from __future__ import annotations

import sys
from pathlib import Path

import torch


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
sys.path.insert(0, str(CODEBASE))

from xformers.ops.fmha.attn_bias import BlockDiagonalCausalMask  # noqa: E402


def main() -> int:
    mask = BlockDiagonalCausalMask.from_seqlens([2, 2])
    expected = mask.materialize((1, 4, 4))
    moved = mask.to(device="cpu")
    actual = moved.materialize((1, 4, 4))

    print(f"original_type={type(mask).__name__}")
    print(f"moved_type={type(moved).__name__}")
    print("original_mask:")
    print(expected)
    print("moved_mask:")
    print(actual)
    print(f"preserves_subclass={isinstance(moved, BlockDiagonalCausalMask)}")

    if not isinstance(moved, BlockDiagonalCausalMask):
        raise AssertionError(
            "BlockDiagonalCausalMask.to() should preserve the subclass, "
            f"but returned {type(moved).__name__}"
        )

    if not torch.equal(expected, actual):
        raise AssertionError("Mask semantics changed after .to()")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
