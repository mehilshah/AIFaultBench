#!/usr/bin/env python3
"""Benchmark the ZeRO-2 hook-count regression reported in DeepSpeed #7885.

The regression is a version-to-version performance bug:
  * 0.18.4 counts the active backward hooks once per backward pass.
  * 0.18.5 counts them once per parameter hook, which scales with model size.

This script assumes the desired DeepSpeed version is already installed in the
current environment. The surrounding shell script installs and compares the
affected releases.
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import time
from pathlib import Path


def build_model(torch, layers: int, hidden_dim: int):
    class TinyMLP(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.seq = torch.nn.Sequential(
                *[torch.nn.Linear(hidden_dim, hidden_dim, bias=False) for _ in range(layers)]
            )

        def forward(self, x):
            return self.seq(x).sum()

    return TinyMLP()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", required=True, help="Human-readable label for the installed DeepSpeed version.")
    parser.add_argument("--layers", type=int, default=64)
    parser.add_argument("--hidden-dim", type=int, default=64)
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--warmup-iters", type=int, default=1)
    parser.add_argument("--measure-iters", type=int, default=5)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    # Force the CPU accelerator path so the repro is portable and does not rely
    # on a GPU architecture matching the current PyTorch wheel.
    os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")
    os.environ.setdefault("MASTER_ADDR", "127.0.0.1")
    os.environ.setdefault("MASTER_PORT", "29500")
    os.environ.setdefault("RANK", "0")
    os.environ.setdefault("WORLD_SIZE", "1")
    os.environ.setdefault("LOCAL_RANK", "0")

    import torch

    torch.set_num_threads(1)
    try:
        torch.set_num_interop_threads(1)
    except Exception:
        pass

    import deepspeed

    if not torch.distributed.is_initialized():
        torch.distributed.init_process_group(backend="gloo", rank=0, world_size=1)

    # The regression lives in the ZeRO-2 backward hook path.
    import deepspeed.runtime.zero.stage_1_and_2 as zero_stage_1_and_2

    hook_call_count = {"n": 0}
    original_count_fn = zero_stage_1_and_2.count_used_parameters_in_backward

    def counted_count_used_parameters_in_backward(parameters):
        hook_call_count["n"] += 1
        return original_count_fn(parameters)

    zero_stage_1_and_2.count_used_parameters_in_backward = counted_count_used_parameters_in_backward

    model = build_model(torch, args.layers, args.hidden_dim)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)

    ds_config = {
        "train_batch_size": args.batch_size,
        "train_micro_batch_size_per_gpu": args.batch_size,
        "zero_optimization": {
            "stage": 2,
            "reduce_scatter": True,
            "allgather_bucket_size": 10_000_000,
            "reduce_bucket_size": 10_000_000,
        },
        "fp16": {"enabled": False},
    }

    engine, _, _, _ = deepspeed.initialize(
        model=model,
        model_parameters=model.parameters(),
        optimizer=optimizer,
        config=ds_config,
        dist_init_required=False,
    )

    step_times = []
    for i in range(args.warmup_iters + args.measure_iters):
        inputs = torch.randn(args.batch_size, args.hidden_dim)
        start = time.perf_counter()
        loss = engine(inputs)
        engine.backward(loss)
        engine.step()
        elapsed = time.perf_counter() - start
        if i >= args.warmup_iters:
            step_times.append(elapsed)

    result = {
        "label": args.label,
        "deepspeed_version": deepspeed.__version__,
        "torch_version": torch.__version__,
        "layers": args.layers,
        "hidden_dim": args.hidden_dim,
        "batch_size": args.batch_size,
        "warmup_iters": args.warmup_iters,
        "measure_iters": args.measure_iters,
        "hook_count_calls": hook_call_count["n"],
        "avg_step_seconds": sum(step_times) / len(step_times),
        "median_step_seconds": statistics.median(step_times),
    }

    print(json.dumps(result, sort_keys=True))
    if args.output is not None:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
