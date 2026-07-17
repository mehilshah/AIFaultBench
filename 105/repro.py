from __future__ import annotations

import argparse
import os
import random
import sys
import traceback
from datetime import timedelta
from pathlib import Path

import torch
import torch.distributed as dist
import torch.multiprocessing as mp


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))

from vector_quantize_pytorch import ResidualVQ  # noqa: E402


def build_model() -> ResidualVQ:
    return ResidualVQ(
        dim=512,
        num_quantizers=2,
        codebook_size=16 * 1024,
        stochastic_sample_codes=True,
        shared_codebook=True,
        commitment_weight=1.0,
        kmeans_init=True,
        threshold_ema_dead_code=2,
        quantize_dropout=True,
        quantize_dropout_cutoff_index=1,
        quantize_dropout_multiple_of=1,
    )


def run_loop(rank: int, world_size: int, steps: int, seq_len: int, batch_size: int) -> None:
    if world_size > 1 and not dist.is_initialized():
        port = os.environ.get("MASTER_PORT", "29571")
        os.environ.setdefault("MASTER_ADDR", "127.0.0.1")
        os.environ.setdefault("MASTER_PORT", port)
        dist.init_process_group(
            backend="gloo",
            rank=rank,
            world_size=world_size,
            timeout=timedelta(seconds=180),
        )

    torch.manual_seed(0)
    random.seed(0)

    model = build_model()
    model.train()

    for step in range(steps):
        x = torch.randn(batch_size, seq_len + rank + (step % 3), 512)
        try:
            quantized, indices, losses = model(x)
        except Exception:
            print(f"rank={rank} step={step} failed", flush=True)
            traceback.print_exc()
            raise

        if rank == 0:
            print(
                f"rank={rank} step={step} ok "
                f"quantized={tuple(quantized.shape)} "
                f"indices={tuple(indices.shape)} "
                f"losses={tuple(losses.shape)}",
                flush=True,
            )

    if dist.is_initialized():
        dist.barrier()
        dist.destroy_process_group()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("single", "ddp", "both"), default="both")
    parser.add_argument("--single-steps", type=int, default=20)
    parser.add_argument("--ddp-steps", type=int, default=8)
    parser.add_argument("--seq-len", type=int, default=1024)
    parser.add_argument("--batch-size", type=int, default=2)
    args = parser.parse_args()

    print("torch", torch.__version__)
    print("mode", args.mode)
    print("issue_config", {
        "dim": 512,
        "num_quantizers": 2,
        "codebook_size": 16 * 1024,
        "stochastic_sample_codes": True,
        "shared_codebook": True,
        "kmeans_init": True,
        "threshold_ema_dead_code": 2,
        "quantize_dropout": True,
    })

    if args.mode in ("single", "both"):
        print("single_process_start")
        run_loop(rank=0, world_size=1, steps=args.single_steps, seq_len=args.seq_len, batch_size=args.batch_size)
        print("single_process_done")

    if args.mode in ("ddp", "both"):
        print("ddp_start")
        world_size = 2
        mp.spawn(
            run_loop,
            args=(world_size, args.ddp_steps, args.seq_len, args.batch_size),
            nprocs=world_size,
            join=True,
        )
        print("ddp_done")

    print("repro_not_triggered")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
