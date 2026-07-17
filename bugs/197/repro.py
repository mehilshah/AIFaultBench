#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))

from monai.metrics import DiceMetric  # noqa: E402


def main() -> int:
    torch.manual_seed(0)

    n_batches = 3
    batch_size, n_classes, h, w = 4, 5, 128, 128

    y_pred_batches = [torch.rand(batch_size, n_classes, h, w) for _ in range(n_batches)]
    y_batches = [torch.rand(batch_size, n_classes, h, w) for _ in range(n_batches)]

    dm = DiceMetric()
    for i in range(n_batches):
        dm(y_pred_batches[i], y_batches[i])

    buffer = dm.get_buffer()
    print(f"buffer_shape={tuple(buffer.shape)}")

    batch_reduced = dm.aggregate(reduction="mean_batch")
    channel_reduced = dm.aggregate(reduction="mean_channel")

    print(f"mean_batch_shape={tuple(batch_reduced.shape)}")
    print(f"mean_channel_shape={tuple(channel_reduced.shape)}")

    expected_batch_shape = (3,)
    expected_channel_shape = (5,)

    if tuple(batch_reduced.shape) != expected_batch_shape or tuple(channel_reduced.shape) != expected_channel_shape:
        print(
            "shape_mismatch="
            f"expected mean_batch={expected_batch_shape}, mean_channel={expected_channel_shape}; "
            f"got mean_batch={tuple(batch_reduced.shape)}, mean_channel={tuple(channel_reduced.shape)}"
        )
        return 1

    print("repro_not_triggered")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
