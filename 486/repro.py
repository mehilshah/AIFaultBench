#!/usr/bin/env python3
"""Minimal reproduction for accelerate issue 1200."""

from __future__ import annotations

import json
import sys

import torch
import torch.nn as nn
from torch.optim.lr_scheduler import LinearLR

from accelerate import Accelerator
from accelerate.scheduler import AcceleratedScheduler


def main() -> int:
    accelerator = Accelerator()

    dummy_model = nn.Linear(1, 1)
    dummy_optimizer = torch.optim.Adam(dummy_model.parameters(), 1.41e-5)
    scheduler = LinearLR(dummy_optimizer, 1.41e-5)

    dummy_model, dummy_optimizer, scheduler = accelerator.prepare(
        dummy_model, dummy_optimizer, scheduler
    )

    payload = {
        "python_version": sys.version.split()[0],
        "torch_version": torch.__version__,
        "accelerate_scheduler_type": type(scheduler).__name__,
        "is_accelerated_scheduler": isinstance(scheduler, AcceleratedScheduler),
        "has_scheduler_attr": hasattr(scheduler, "scheduler"),
    }
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
