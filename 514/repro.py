#!/usr/bin/env python3
"""
Minimal repro for DeepCompile's FX profiling memory blow-up on decomposed
cross-entropy backward graphs.

This script does not depend on DeepSpeed being installed. It reproduces the
same execution pattern that DeepCompile uses:
1. Build an FX graph for the backward of cross-entropy via torch.func.grad.
2. Force decompositions so the graph contains the same-shaped temporaries
   reported in the bug (full_like -> scatter -> mul -> exp -> sub).
3. Run the graph eagerly under a tighter memory cap so the dense intermediate
   cannot fit.
"""

from __future__ import annotations

import os
import resource
from typing import Iterable

import torch
import torch.nn.functional as F
from torch._decomp import decomposition_table
from torch.fx.experimental.proxy_tensor import make_fx
from torch.func import grad


TRACE_LIMIT_MB = int(os.environ.get("TRACE_LIMIT_MB", "1800"))
EXEC_LIMIT_MB = int(os.environ.get("EXEC_LIMIT_MB", "1000"))
N = int(os.environ.get("BATCH_TOKENS", "8192"))
V = int(os.environ.get("VOCAB_SIZE", "4096"))


def set_as_limit(limit_mb: int) -> None:
    limit_bytes = limit_mb * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (limit_bytes, limit_bytes))


def current_vm_lines() -> Iterable[str]:
    wanted = ("VmSize:", "VmRSS:", "VmData:")
    with open("/proc/self/status", encoding="utf-8") as handle:
        for line in handle:
            if line.startswith(wanted):
                yield line.strip()


def print_vm(prefix: str) -> None:
    print(prefix)
    for line in current_vm_lines():
        print(f"  {line}")


def main() -> int:
    torch.set_num_threads(1)
    torch.set_num_interop_threads(1)

    print(f"torch={torch.__version__}")
    print(f"cuda_available={torch.cuda.is_available()}")
    print(f"shape=({N}, {V})")
    print(f"trace_limit_mb={TRACE_LIMIT_MB}")
    print(f"exec_limit_mb={EXEC_LIMIT_MB}")

    # Keep the eager loss under the runtime cap so we can isolate the
    # decomposed profiling graph.
    x = torch.randn(N, V, dtype=torch.float32)
    y = torch.randint(0, V, (N,), dtype=torch.int64)

    print_vm("vm_before_eager")
    eager_loss = F.cross_entropy(x, y)
    print(f"eager_loss={float(eager_loss):.6f}")

    # Build the decomposed backward graph under a higher cap. This is the same
    # family of ops DeepCompile's profiling interpreter executes node-by-node.
    set_as_limit(TRACE_LIMIT_MB)
    backward_fn = grad(lambda logits, target: F.cross_entropy(logits, target), argnums=0)
    fx = make_fx(backward_fn, decomposition_table=decomposition_table)(x, y)
    print("decomposed_graph:")
    print(fx.graph)

    print_vm("vm_after_trace")
    set_as_limit(EXEC_LIMIT_MB)
    print("vm_after_lowering_cap")
    print_vm("vm_before_fx_run")

    try:
        out = fx(x, y)
    except Exception as exc:  # noqa: BLE001
        print(f"expected_failure={type(exc).__name__}: {exc}")
        return 0

    print(f"unexpected_success={tuple(out.shape)} {out.dtype}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
