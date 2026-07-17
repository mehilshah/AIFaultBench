#!/usr/bin/env python3
"""Minimal reproduction attempt for issue #46.

The report claims that `norm.gamma` is treated as unused during backprop.
This script checks the same code path in a tiny local CPU setup and reports
whether any LayerNorm gamma parameters still miss gradients.
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP


ROOT_DIR = Path(__file__).resolve().parent
CODEBASE_DIR = ROOT_DIR / "codebase"
if str(CODEBASE_DIR) not in sys.path:
    sys.path.insert(0, str(CODEBASE_DIR))

from palm_rlhf_pytorch import PaLM  # noqa: E402


def format_missing(model: torch.nn.Module) -> list[str]:
    return [name for name, param in model.named_parameters() if param.grad is None]


def run_plain_backward() -> list[str]:
    torch.manual_seed(0)
    model = PaLM(num_tokens=32, dim=16, depth=2, flash_attn=False)
    seq = torch.randint(0, 32, (2, 8))
    loss = model(seq, return_loss=True)
    loss.backward()
    missing = format_missing(model)
    print("plain_backward_missing=", missing)
    for name, param in model.named_parameters():
        if name.endswith("norm.gamma"):
            grad_sum = None if param.grad is None else float(param.grad.abs().sum())
            print(f"{name}: grad_none={param.grad is None} grad_sum={grad_sum}")
    return missing


def run_ddp_backward() -> list[str] | str:
    torch.manual_seed(0)
    fd, path = tempfile.mkstemp(prefix="ddp_init_", suffix=".tmp")
    os.close(fd)
    try:
        dist.init_process_group(
            backend="gloo",
            init_method=f"file://{path}",
            rank=0,
            world_size=1,
        )

        model = DDP(PaLM(num_tokens=32, dim=16, depth=2, flash_attn=False))
        seq = torch.randint(0, 32, (2, 8))
        loss = model(seq, return_loss=True)
        loss.backward()
        missing = format_missing(model.module)
        print("ddp_backward_missing=", missing)
        return missing
    except Exception as exc:  # pragma: no cover - best-effort repro harness
        print("ddp_error=", repr(exc))
        return "error"
    finally:
        if dist.is_initialized():
            dist.destroy_process_group()
        if os.path.exists(path):
            os.remove(path)


def main() -> int:
    print("torch_version=", torch.__version__)
    print("python_version=", sys.version.split()[0])
    plain_missing = run_plain_backward()
    ddp_result = run_ddp_backward()

    if plain_missing or ddp_result == "error" or ddp_result:
        print("status=REPRODUCED")
    else:
        print("status=NOT_REPRODUCED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
