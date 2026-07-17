#!/usr/bin/env python3
"""Minimal repro for TorchRL issue 3515.

This uses a synthetic TensorDict with the same problematic batch layout as the
report: one environment, 2048 steps, one agent. The failure happens when the
replay buffer writes back the storage index and validates the batch shape.
"""

from __future__ import annotations

import traceback

import torch
from tensordict import TensorDict

from torchrl.data import TensorDictReplayBuffer
from torchrl.data.replay_buffers.storages import LazyTensorStorage


def main() -> int:
    batch_size = [1, 2048, 1]
    td = TensorDict(
        {
            "x": torch.zeros(*batch_size, dtype=torch.float32),
        },
        batch_size=batch_size,
    )

    rb = TensorDictReplayBuffer(
        storage=LazyTensorStorage(10_000, ndim=3),
        batch_size=64,
    )

    print(f"TensorDict batch_size: {td.batch_size}")
    print("Calling replay_buffer.extend(td)...")
    try:
        rb.extend(td)
    except Exception as exc:  # noqa: BLE001
        print(f"REPRODUCED: {type(exc).__name__}: {exc}")
        traceback.print_exc()
        return 1

    print("UNEXPECTED_SUCCESS: replay_buffer.extend(td) completed without error")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
