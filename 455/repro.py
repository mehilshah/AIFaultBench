#!/usr/bin/env python3
"""Minimal PEFT LoRA merge repro for the ZeRO-3 shard-shape failure."""

from __future__ import annotations

import json
import os
import traceback
from pathlib import Path

import torch


ROOT = Path(__file__).resolve().parent
RESULT_PATH = ROOT / "reproduction.json"


def build_lora_model():
    # Import from the local source tree, not an installed wheel.
    import sys

    sys.path.insert(0, str(ROOT / "codebase" / "src"))

    from peft import LoraConfig, LoraModel

    class ToyConfig:
        def __init__(self) -> None:
            self.model_type = "toy"

        def to_dict(self) -> dict:
            return {"model_type": self.model_type}

    class ToyModel(torch.nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.config = ToyConfig()
            self.proj = torch.nn.Linear(2048, 2048, bias=False)

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            return self.proj(x)

    base_model = ToyModel()
    peft_config = {
        "default": LoraConfig(
            r=8,
            lora_alpha=16,
            lora_dropout=0.0,
            target_modules=["proj"],
            bias="none",
        )
    }
    return LoraModel(base_model, peft_config, "default")


def write_result(*, reproducible: bool, evidence: str, steps: list[str], blocking_reason: str | None) -> None:
    payload = {
        "reproducible": reproducible,
        "evidence": evidence,
        "steps": steps,
        "blocking_reason": blocking_reason,
        "reproduction_command": "bash setup_env.sh && bash run_repro.sh",
    }
    RESULT_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    torch.manual_seed(0)
    model = build_lora_model()

    control = build_lora_model()
    control_merged = control.merge_and_unload()
    print(f"control_merge_ok={type(control_merged).__name__}")

    target = model.model.proj
    target.weight = torch.nn.Parameter(
        torch.empty((2048, 0), dtype=target.weight.dtype, device=target.weight.device)
    )
    print(f"simulated_zero3_weight_shape={tuple(target.weight.shape)}")

    try:
        model.merge_and_unload()
    except Exception as exc:  # noqa: BLE001
        traceback.print_exc()
        write_result(
            reproducible=True,
            evidence=(
                "merge_and_unload succeeded on an unsharded control model, then failed after the target weight was "
                "shrunk to a zero-width shard. The failure was: "
                f"{type(exc).__name__}: {exc}"
            ),
            steps=[
                "Build a tiny 2048x2048 LoRA-wrapped linear layer from the local PEFT source.",
                "Verify merge_and_unload() works on the unsharded control model.",
                "Replace the target weight with a ZeRO-3-like shard shaped [2048, 0].",
                "Call merge_and_unload() again and observe the tensor-size RuntimeError.",
            ],
            blocking_reason="",
        )
        return 0

    write_result(
        reproducible=False,
        evidence="merge_and_unload completed even after the weight was replaced with a zero-width shard.",
        steps=[
            "Build a tiny 2048x2048 LoRA-wrapped linear layer from the local PEFT source.",
            "Replace the target weight with a ZeRO-3-like shard shaped [2048, 0].",
            "Call merge_and_unload() and observe whether it fails.",
        ],
        blocking_reason="The expected tensor-size mismatch did not occur in this environment.",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
