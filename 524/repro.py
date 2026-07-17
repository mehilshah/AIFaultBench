#!/usr/bin/env python3
"""Minimal repro for BF16_Optimizer.destroy() on DummyOptim."""

from __future__ import annotations

import sys
import types

import torch
import torch.nn as nn

import deepspeed.comm.comm as ds_comm
from deepspeed.runtime.bf16_optimizer import BF16_Optimizer
from deepspeed.runtime.utils import DummyOptim


class FakeBackend:
    """Single-rank backend shim for the pure-Python repro."""

    def is_initialized(self):
        return True

    def get_rank(self, group=None):
        return 0

    def get_world_size(self, group=None):
        return 1

    def get_world_group(self):
        return None


def main() -> int:
    # The bug triggers when BF16_Optimizer is constructed around DummyOptim.
    ds_comm.cdb = FakeBackend()

    model = nn.Sequential(nn.Linear(4, 4), nn.ReLU(), nn.Linear(4, 2))
    optimizer = DummyOptim(list(model.parameters()))
    config = types.SimpleNamespace(
        enabled=True,
        immediate_grad_update=False,
        check_grad_overflow=False,
        bf16_master_weights_and_grads=False,
        bf16_optimizer_states=False,
    )

    bf16_optimizer = BF16_Optimizer(
        optimizer,
        param_names={param: f"param_{idx}" for idx, param in enumerate(model.parameters())},
        bfloat16_config=config,
        grad_acc_dtype=torch.float32,
    )

    print(f"constructed={type(bf16_optimizer).__name__} bf16_groups={len(bf16_optimizer.bf16_groups)}")

    try:
        bf16_optimizer.destroy()
    except IndexError as exc:
        print(f"BUG REPRODUCED: {type(exc).__name__}: {exc}")
        return 1

    print("BUG NOT REPRODUCED: destroy() completed without IndexError")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
