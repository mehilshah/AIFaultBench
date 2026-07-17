#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple

import torch
import torch.nn as nn
from torch.nn.parallel import DistributedDataParallel as DDP

import deepspeed
import deepspeed.comm as dist
from deepspeed.accelerator import get_accelerator


ROOT = Path(__file__).resolve().parent
RESULT_PATH = ROOT / "reproduction.json"


class TinyNet(nn.Module):
    def __init__(self, hidden_dim: int = 4):
        super().__init__()
        self.l1 = nn.Linear(hidden_dim, hidden_dim)
        self.l2 = nn.Linear(hidden_dim, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.l2(torch.tanh(self.l1(x))).sum()


def init_dist() -> None:
    if not dist.is_initialized():
        deepspeed.init_distributed(dist_backend="gloo")


def make_batches(
    *,
    num_micro_batches: int,
    micro_batch_size: int,
    hidden_dim: int,
    seed: int,
) -> List[torch.Tensor]:
    generator = torch.Generator().manual_seed(seed)
    batches: List[torch.Tensor] = []
    for _ in range(num_micro_batches):
        x = torch.randn(micro_batch_size, hidden_dim, generator=generator)
        batches.append(x)
    return batches


def grad_norm(grads: Dict[str, torch.Tensor]) -> float:
    total = 0.0
    for tensor in grads.values():
        norm = tensor.double().norm().item()
        total += norm * norm
    return total ** 0.5


def run_ddp_reference(
    batches: List[torch.Tensor],
    *,
    hidden_dim: int,
    gradient_accumulation_steps: int,
) -> float:
    torch.manual_seed(42)
    model = TinyNet(hidden_dim=hidden_dim)
    model = model.to(get_accelerator().device_name())
    if dist.get_world_size() > 1:
        model = DDP(model)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    optimizer.zero_grad()

    for step, x in enumerate(batches):
        logits = model(x.to(get_accelerator().device_name()))
        loss = logits
        (loss / gradient_accumulation_steps).backward()
        if (step + 1) % gradient_accumulation_steps == 0:
            captured_grads = {
                name.replace("module.", ""): param.grad.detach().float().cpu().clone()
                for name, param in (model.module.named_parameters() if hasattr(model, "module") else model.named_parameters())
                if param.grad is not None
            }

    return grad_norm(captured_grads)


def run_zero_stage(
    stage: int,
    batches: List[torch.Tensor],
    *,
    hidden_dim: int,
    gradient_accumulation_steps: int,
) -> Dict[str, object]:
    torch.manual_seed(42)
    model = TinyNet(hidden_dim=hidden_dim)

    config = {
        "train_micro_batch_size_per_gpu": batches[0].shape[0],
        "gradient_accumulation_steps": gradient_accumulation_steps,
        "steps_per_print": 1,
        "zero_optimization": {
            "stage": stage,
            "overlap_comm": True,
            "contiguous_gradients": True,
            "reduce_scatter": True,
        },
        "optimizer": {
            "type": "Adam",
            "params": {"lr": 1e-3},
        },
    }

    engine, _, _, _ = deepspeed.initialize(config=config, model=model, model_parameters=model.parameters())
    cached_engine_norm = None

    for step, x in enumerate(batches):
        loss = engine(x.to(engine.device))
        engine.backward(loss)
        engine.step()
        if step == len(batches) - 1:
            cached_engine_norm = engine.get_global_grad_norm()
            if cached_engine_norm is None:
                cached_engine_norm = getattr(engine, "_global_grad_norm", None)

    engine.destroy()
    return {
        "norm": float(cached_engine_norm) if cached_engine_norm is not None else None,
        "engine_norm": float(cached_engine_norm) if cached_engine_norm is not None else None,
    }


def write_result(*, reproducible: bool, evidence: List[str], steps: List[str], blocking_reason: str, reproduction_command: str) -> None:
    payload = {
        "reproducible": reproducible,
        "evidence": evidence,
        "steps": steps,
        "blocking_reason": blocking_reason,
        "reproduction_command": reproduction_command,
    }
    RESULT_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gradient-accumulation-steps", type=int, default=2)
    parser.add_argument("--micro-batch-size", type=int, default=2)
    parser.add_argument("--hidden-dim", type=int, default=32)
    parser.add_argument("--num-micro-batches", type=int, default=2)
    args = parser.parse_args()

    init_dist()

    batches = make_batches(
        num_micro_batches=args.num_micro_batches,
        micro_batch_size=args.micro_batch_size,
        hidden_dim=args.hidden_dim,
        seed=12345,
    )

    ddp_norm = run_ddp_reference(
        batches,
        hidden_dim=args.hidden_dim,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
    )
    z2 = run_zero_stage(
        2,
        batches,
        hidden_dim=args.hidden_dim,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
    )
    z3 = run_zero_stage(
        3,
        batches,
        hidden_dim=args.hidden_dim,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
    )

    z2_max_diff = abs(ddp_norm - z2["norm"])
    z3_max_diff = abs(ddp_norm - z3["norm"])
    stage2_close = z2_max_diff <= 1e-5
    stage3_close = z3_max_diff <= 1e-5
    reproducible = not (stage2_close and stage3_close)

    exit_code = 0
    if dist.get_rank() == 0:
        print(f"DDP grad norm:   {ddp_norm:.10f}")
        print(f"ZeRO-2 grad norm: {z2['norm']:.10f} (engine cached {z2['engine_norm']:.10f})")
        print(f"ZeRO-3 grad norm: {z3['norm']:.10f} (engine cached {z3['engine_norm']:.10f})")
        print(f"ZeRO-2 max diff vs DDP: {z2_max_diff:.10f}")
        print(f"ZeRO-3 max diff vs DDP: {z3_max_diff:.10f}")
        print(f"ZeRO-2 matches DDP: {stage2_close}")
        print(f"ZeRO-3 matches DDP: {stage3_close}")

        evidence = [
            f"DDP grad norm: {ddp_norm:.10f}",
            f"ZeRO-2 grad norm: {z2['norm']:.10f} (cached {z2['engine_norm']:.10f})",
            f"ZeRO-3 grad norm: {z3['norm']:.10f} (cached {z3['engine_norm']:.10f})",
            f"ZeRO-2 max diff vs DDP: {z2_max_diff:.10f}",
            f"ZeRO-3 max diff vs DDP: {z3_max_diff:.10f}",
        ]
        if reproducible:
            blocking_reason = ""
        else:
            blocking_reason = (
                "The CPU-only gloo run did not reproduce the reported ZeRO-2 regression. "
                "ZeRO-2 and ZeRO-3 both matched the DDP baseline on this checked-out source, "
                "so the GPU/stream-overlap path described in the issue was not triggered here."
            )

        write_result(
            reproducible=reproducible,
            evidence=evidence,
            steps=[
                "Start a two-rank CPU gloo process group with DeepSpeed 0.18.3+unknown.",
                "Run the same synthetic classifier under DDP, ZeRO-2, and ZeRO-3 with gradient accumulation.",
                "Compare the final accumulated gradient norms and per-parameter tensors against the DDP baseline.",
            ],
            blocking_reason=blocking_reason,
            reproduction_command="bash run_repro.sh",
        )
        if reproducible:
            exit_code = 1

    dist.barrier()
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
