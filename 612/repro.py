#!/usr/bin/env python3
"""Minimal source-level reproduction for DeepSpeed issue 7710.

The reported crash happens when ZeRO-2 attempts to read
``bucket.buffer[bucket.index]`` while the bucket buffer is still empty.

This harness keeps the behavior self-contained and deterministic so it can be
run in the standardized folder without requiring a full GPU training stack.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


SOURCE_FILE = Path("codebase/deepspeed/runtime/zero/stage_1_and_2.py")
TARGET_SNIPPET = "self.average_tensor(bucket.buffer[bucket.index].narrow(0, 0, bucket.elements), comm_dtype)"


@dataclass
class Bucket:
    buffer: list = field(default_factory=list)
    params: list = field(default_factory=list)
    grads: list = field(default_factory=list)
    elements: int = 1
    index: int = 0
    has_moe_params: bool = False


class Harness:
    def __init__(self) -> None:
        self.contiguous_gradients = True
        self.extra_large_param_to_reduce = {}
        self.ipg_buckets = {"fp16": Bucket()}

    def average_tensor(self, *_args, **_kwargs):
        raise AssertionError("This path should not be reached in the repro.")

    def reduce_ipg_grads(self) -> None:
        for comm_dtype in sorted(self.ipg_buckets.keys()):
            bucket = self.ipg_buckets[comm_dtype]

            if self.contiguous_gradients:
                if comm_dtype in self.extra_large_param_to_reduce:
                    raise AssertionError("unexpected extra-large path in repro")
                else:
                    # This is the bad access from the bug report.
                    self.average_tensor(bucket.buffer[bucket.index].narrow(0, 0, bucket.elements),
                                        comm_dtype)


def main() -> None:
    print(f"Source file: {SOURCE_FILE}")
    with SOURCE_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            if TARGET_SNIPPET in line:
                print(f"Offending line: {line.strip()}")
                break
        else:
            print("Offending line not found in source file.")

    print("Triggering the empty bucket access now.")
    Harness().reduce_ipg_grads()


if __name__ == "__main__":
    main()
