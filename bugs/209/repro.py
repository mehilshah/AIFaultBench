#!/usr/bin/env python3
"""Minimal reproducer for torchao issue 3490.

Expected behavior:
`FqnToConfig` should swap `m.l` to the QAT module when the config targets the
module FQN `l`.

Observed behavior in this folder:
`m.l` remains `torch.nn.Linear` after `quantize_` returns.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))

import torch
from torchao.prototype.mx_formats import NVFP4DynamicActivationNVFP4WeightConfig
from torchao.quantization import FqnToConfig, quantize_
from torchao.quantization.qat import QATConfig


class M(torch.nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.l = torch.nn.Linear(16, 16)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.l(x)


def main() -> int:
    m = M()
    print(f"torch={torch.__version__}")
    print(f"before={type(m.l).__module__}.{type(m.l).__qualname__}")

    base_config = NVFP4DynamicActivationNVFP4WeightConfig()
    quantize_(
        m,
        FqnToConfig({"l": QATConfig(base_config, step="prepare")}),
        filter_fn=None,
    )

    after_type = f"{type(m.l).__module__}.{type(m.l).__qualname__}"
    print(f"after={after_type}")

    if isinstance(m.l, torch.nn.Linear):
        print("BUG: module was not swapped")
        return 1

    print("OK: module was swapped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
