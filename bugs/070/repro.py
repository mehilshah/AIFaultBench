#!/usr/bin/env python3
"""Minimal reproduction for the DeepSpeed Domino communication backend bug.

The Domino code initializes `torch.distributed` in
`codebase/training/DeepSpeed-Domino/domino/initialize.py`, but later code in
`codebase/training/DeepSpeed-Domino/domino/training.py` calls
`deepspeed.comm.all_reduce(...)`. With DeepSpeed's comm backend (`cdb`) still
unset, that call fails with:

    AttributeError: 'NoneType' object has no attribute 'all_reduce'

This script reproduces the same failure mode directly.
"""

from __future__ import annotations

import os

os.environ.setdefault("MASTER_ADDR", "127.0.0.1")
os.environ.setdefault("MASTER_PORT", "29501")
os.environ.setdefault("RANK", "0")
os.environ.setdefault("WORLD_SIZE", "1")

import deepspeed
import torch


def main() -> None:
    print(f"torch={torch.__version__}")
    print(f"deepspeed={deepspeed.__version__}")
    print(f"torch.distributed.is_initialized() before={torch.distributed.is_initialized()}")

    torch.distributed.init_process_group(backend="gloo", init_method="env://")

    print(f"torch.distributed.is_initialized() after={torch.distributed.is_initialized()}")
    print(f"deepspeed.comm.cdb={getattr(deepspeed.comm.comm, 'cdb', None)}")
    print("calling deepspeed.comm.all_reduce(...)")
    deepspeed.comm.all_reduce(torch.tensor([1.0]))


if __name__ == "__main__":
    main()

