#!/usr/bin/env python3
"""Minimal reproducer for the FSDP CPU full-state-dict crash."""

from __future__ import annotations

from pathlib import Path

import torch
from lightning.fabric import Fabric
from lightning.fabric.strategies import FSDPStrategy


class FSDPStrategySubclass(FSDPStrategy):
    """Bypass Fabric's exact-type CPU guard while keeping the same FSDP behavior."""


class MyModel(torch.nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.layer = torch.nn.Linear(10, 10)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.layer(x)


def main(fabric: Fabric) -> None:
    print(f"rank={fabric.global_rank} world_size={fabric.world_size} device={fabric.device}", flush=True)
    model = fabric.setup(MyModel())
    checkpoint_path = Path(f"fsdp_cpu_full_rank{fabric.global_rank}.ckpt")
    print(f"saving={checkpoint_path}", flush=True)
    fabric.save(checkpoint_path, {"model": model})
    print("save_completed", flush=True)


def run() -> None:
    strategy = FSDPStrategySubclass(state_dict_type="full")
    fabric = Fabric(accelerator="cpu", devices=2, strategy=strategy)
    print("launching", flush=True)
    fabric.launch(main)
    print("finished", flush=True)


if __name__ == "__main__":
    run()
