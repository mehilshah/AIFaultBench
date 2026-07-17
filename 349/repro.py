#!/usr/bin/env python3
"""Minimal reproducer for Accelerate issue 3140."""

from __future__ import annotations

import os
import shutil
from pathlib import Path

from accelerate import Accelerator
from accelerate.state import DistributedType


class FakeCheckpointEngine:
    def makedirs(self, save_dir: str, exist_ok: bool = True):
        os.makedirs(save_dir, exist_ok=exist_ok)


class FakeDeepSpeedEngine:
    def __init__(self, name: str, frozen: bool):
        self.name = name
        self.frozen = frozen
        self.checkpoint_engine = None if frozen else FakeCheckpointEngine()

    def save_checkpoint(self, output_dir: str, ckpt_id: str | None = None, **kwargs):
        save_dir = os.path.join(output_dir, ckpt_id) if ckpt_id is not None else output_dir
        print(f"save_checkpoint({self.name!r}, frozen={self.frozen}) -> {save_dir}")
        self.checkpoint_engine.makedirs(save_dir, exist_ok=True)


def main() -> None:
    output_dir = Path("repro_output")
    if output_dir.exists():
        shutil.rmtree(output_dir)

    accelerator = Accelerator(cpu=True)
    accelerator.state.distributed_type = DistributedType.DEEPSPEED
    accelerator._models = [
        FakeDeepSpeedEngine("trainable_model", frozen=False),
        FakeDeepSpeedEngine("frozen_model", frozen=True),
    ]
    accelerator._optimizers = []
    accelerator._schedulers = []

    print(f"distributed_type={accelerator.distributed_type}")
    print("about to call Accelerator.save_state()")
    accelerator.save_state(str(output_dir))
    print("unexpected success: the bug did not reproduce")


if __name__ == "__main__":
    main()
