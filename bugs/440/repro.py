#!/usr/bin/env python3
"""Reproduce the PEFT deepcopy bug for `LoraConfig`.

The copied model keeps the adapter structure, but the copied `LoraConfig`
falls back to the default rank value instead of preserving the configured one.
"""

from __future__ import annotations

import copy
import json

import torch
from torch import nn

from peft import LoraConfig, get_peft_model


class TinyModel(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.linear = nn.Linear(4, 4)
        self.config = {"model_type": "tiny"}

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.linear(x)


def main() -> int:
    base_model = TinyModel()
    peft_config = LoraConfig(
        r=87,
        lora_alpha=32,
        lora_dropout=0.1,
        target_modules=["linear"],
        bias="none",
    )

    model = get_peft_model(base_model, peft_config)
    model_copy = copy.deepcopy(model)

    original_r = model.peft_config["default"].r
    copied_config = model_copy.peft_config["default"]
    copied_r = copied_config.r

    payload = {
        "original_r": original_r,
        "copied_r": copied_r,
        "copied_config": {
            "repr": repr(copied_config),
            "type": type(copied_config).__name__,
        },
        "expected": "deepcopy should preserve the configured LoRA rank",
        "reproducible": copied_r != original_r,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))

    assert copied_r == original_r, f"deepcopy lost LoraConfig.r: expected {original_r}, got {copied_r}"
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
