#!/usr/bin/env python3
"""Minimal source-level reproducer for DeepSpeed issue #7804.

The bug report describes a ZeRO-2 regression where the IPG buffer index does
not ping-pong between the two contiguous-gradient buffers when
`overlap_comm=True` and `contiguous_gradients=True`.

The relevant code path in `codebase/deepspeed/runtime/zero/stage_1_and_2.py`
does two things:
  1. `reduce_independent_p_g_buckets_and_remove_grads()` swaps the index after
     `reduce_ipg_grads()`.
  2. `IPGBucket.clear()` resets `index` back to 0.

This reproducer models just that state machine so the bug can be observed
without requiring a working multi-GPU CUDA environment.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "codebase" / "deepspeed" / "runtime" / "zero" / "stage_1_and_2.py"


@dataclass
class IPGBucketState:
    index: int = 0
    elements: int = 0

    def clear(self) -> None:
        # Mirrors the buggy behavior in the pinned DeepSpeed commit.
        self.elements = 0
        self.index = 0


def source_contains_index_reset() -> bool:
    text = SOURCE.read_text(encoding="utf-8")
    return bool(re.search(r"def clear\(self\):.*?self\.index = 0", text, re.S))


def simulate_ping_pong(cycles: int = 4, fixed: bool = False) -> list[int]:
    bucket = IPGBucketState()
    observed: list[int] = []

    for _ in range(cycles):
        if fixed:
            # Expected behavior after the upstream fix: preserve the current
            # buffer slot while only clearing payload bookkeeping.
            bucket.elements = 0
        else:
            bucket.clear()

        # This matches the caller-side swap in
        # `reduce_independent_p_g_buckets_and_remove_grads()`.
        bucket.index = 1 - bucket.index
        observed.append(bucket.index)

    return observed


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"Missing source file: {SOURCE}")

    bug_present = source_contains_index_reset()
    buggy_sequence = simulate_ping_pong(fixed=False)
    fixed_sequence = simulate_ping_pong(fixed=True)

    print("DeepSpeed source checked:", SOURCE)
    print("IPGBucket.clear() resets index to 0:", bug_present)
    print("Observed buffer index sequence with pinned code:", buggy_sequence)
    print("Expected ping-pong sequence after fix:", fixed_sequence)

    if bug_present and buggy_sequence == [1, 1, 1, 1]:
        print("BUG REPRODUCED: the buffer index never alternates, so ping-pong overlap is defeated.")
    else:
        print("BUG NOT REPRODUCED: source or simulation did not match the expected regression.")


if __name__ == "__main__":
    main()
