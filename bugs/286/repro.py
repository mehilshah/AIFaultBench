#!/usr/bin/env python3
"""Minimal Accelerate prepare() reproducer.

This mirrors the reported failure shape:
model, optimizer, dataloader, and lr scheduler are all passed to
Accelerator.prepare().

The real bug report needs 4 CUDA devices. In this environment we only have
one CUDA device, so the script can also run a smoke test locally to prove the
code path itself completes when the hardware constraint is removed.
"""

from __future__ import annotations

import argparse
import os
import sys

import torch
from torch.utils.data import DataLoader, TensorDataset

from accelerate import Accelerator


def build_components(batch_size: int = 1):
    torch.manual_seed(0)

    inputs = torch.randn(8, 4)
    targets = torch.randn(8, 2)
    dataset = TensorDataset(inputs, targets)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)

    model = torch.nn.Linear(4, 2)
    optimizer = torch.optim.SGD(model.parameters(), lr=1e-3)
    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda=lambda _: 1.0)
    return model, optimizer, dataloader, scheduler


def run_prepare(mixed_precision: str, batch_size: int):
    accelerator = Accelerator(mixed_precision=mixed_precision)
    model, optimizer, dataloader, scheduler = build_components(batch_size=batch_size)

    print(
        f"rank={accelerator.process_index} world_size={accelerator.num_processes} "
        f"device={accelerator.device} cuda_visible_devices={os.environ.get('CUDA_VISIBLE_DEVICES', '<unset>')}",
        flush=True,
    )
    print("before prepare()", flush=True)
    model, optimizer, dataloader, scheduler = accelerator.prepare(model, optimizer, dataloader, scheduler)
    print(
        "after prepare(): "
        f"{type(model).__name__} {type(optimizer).__name__} {type(dataloader).__name__} {type(scheduler).__name__}",
        flush=True,
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--world-size", type=int, default=4)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--mixed-precision", default="bf16")
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Skip the 4-GPU availability check and just verify local prepare() completes.",
    )
    args = parser.parse_args(argv)

    cuda_devices = torch.cuda.device_count()
    if not args.smoke and cuda_devices < args.world_size:
        print(
            f"BLOCKED: requested world size {args.world_size}, but only {cuda_devices} CUDA device(s) are available.",
            file=sys.stderr,
            flush=True,
        )
        return 2

    return run_prepare(args.mixed_precision, args.batch_size)


if __name__ == "__main__":
    raise SystemExit(main())
