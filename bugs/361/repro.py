#!/usr/bin/env python3
"""Repro for the Python conditional on a CUDA tensor in DeepSpeed SP loss aggregation.

The reported code path is:

    total_loss = sum(
        losses_per_rank[rank] * good_tokens_per_rank[rank]
        for rank in range(sp_world_size)
        if good_tokens_per_rank[rank] > 0
    )

That `if` clause evaluates a tensor in Python. On CUDA tensors, the truthiness
check can force a host-side synchronization.
"""

from __future__ import annotations

import time
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE_FILE = ROOT / "codebase" / "src" / "transformers" / "integrations" / "deepspeed.py"


def print_source_excerpt() -> None:
    print(f"source_file={SOURCE_FILE}")
    if not SOURCE_FILE.exists():
        print("blocked: source file missing")
        return

    lines = SOURCE_FILE.read_text(encoding="utf-8").splitlines()
    start = 733
    end = 742
    print("source_excerpt:")
    for lineno in range(start, end + 1):
        if 1 <= lineno <= len(lines):
            print(f"{lineno}: {lines[lineno - 1]}")


def try_import_torch():
    try:
        import torch
    except Exception as exc:  # pragma: no cover - environment dependent
        print(f"blocked: torch import failed: {type(exc).__name__}: {exc}")
        return None
    return torch


def smoke_test_on_cuda(torch) -> int:
    device = torch.device("cuda")
    print(f"cuda_device={torch.cuda.get_device_name(0)}")
    delay_label = "matmul_chain"
    warmup_a = torch.randn((4096, 4096), device=device)
    warmup_b = torch.randn((4096, 4096), device=device)
    delayed_scalar = torch.matmul(warmup_a, warmup_b).sum()
    compare_start = time.perf_counter()
    branch_taken = False
    if delayed_scalar > 0:
        branch_taken = True
    branch_end = time.perf_counter()
    torch.cuda.synchronize()
    sync_end = time.perf_counter()

    branch_ms = (branch_end - compare_start) * 1000.0
    sync_ms = (sync_end - compare_start) * 1000.0

    print(f"delay_source={delay_label}")
    print(f"branch_taken={branch_taken}")
    print(f"branch_elapsed_ms={branch_ms:.2f}")
    print(f"sync_elapsed_ms={sync_ms:.2f}")
    print("note: the branch elapsed time captures the Python truthiness check")

    if branch_ms < 20.0:
        print("BUG_NOT_REPRODUCED")
        return 2

    print("BUG_REPRODUCED")
    return 0


def main() -> int:
    print(f"python={sys.version.split()[0]}")
    print_source_excerpt()

    torch = try_import_torch()
    if torch is None:
        return 2

    print(f"torch={torch.__version__}")
    print(f"cuda_available={torch.cuda.is_available()}")
    if not torch.cuda.is_available():
        print("blocked: this container has no working CUDA PyTorch runtime")
        return 2

    return smoke_test_on_cuda(torch)


if __name__ == "__main__":
    raise SystemExit(main())
