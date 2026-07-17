#!/usr/bin/env python3
"""Minimal repro for DeepSpeed issue #7708.

This reproduces the failing backward hook path directly:
DeepSpeedEngine._backward_prologue_per_tensor(None) -> TypeError.
"""

from __future__ import annotations

import os
import sys


ROOT = os.path.dirname(os.path.abspath(__file__))
CODEBASE = os.path.join(ROOT, "codebase")
if CODEBASE not in sys.path:
    sys.path.insert(0, CODEBASE)


import torch  # noqa: E402
from deepspeed.runtime.engine import DeepSpeedEngine  # noqa: E402
from deepspeed.runtime.utils import OutputBackwardHookManager  # noqa: E402


class EngineStub:

    def gradient_accumulation_steps(self) -> int:
        return 4

    def _backward_prologue_per_tensor(self, grad):
        return DeepSpeedEngine._backward_prologue_per_tensor(self, grad)


def main() -> None:
    engine = EngineStub()

    manager = OutputBackwardHookManager(
        preprocess_once_fn=lambda: print("pre-backward hook ran"),
        preprocess_per_tensor_fn=engine._backward_prologue_per_tensor,
    )

    tensor = torch.tensor(1.0, requires_grad=True)
    hook = manager._make_backward_hook(tensor)

    print("Triggering backward hook with grad=None")
    hook(None)


if __name__ == "__main__":
    main()
