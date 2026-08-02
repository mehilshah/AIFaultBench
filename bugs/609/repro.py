#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import torch


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase" / "src"))

from diffusers.loaders.lora_conversion_utils import _convert_non_diffusers_flux2_lora_to_diffusers


def build_state_dict() -> dict[str, torch.Tensor]:
    sd: dict[str, torch.Tensor] = {}

    # This mirrors the AI-toolkit / non-diffusers Flux2 format that enters
    # `_convert_non_diffusers_flux2_lora_to_diffusers` via Flux2Pipeline.lora_state_dict().
    # The issue report's failure is caused by these guidance keys surviving the conversion.
    for lora_key in ("lora_A", "lora_B"):
        for prefix in (
            "img_in",
            "txt_in",
            "time_in.in_layer",
            "time_in.out_layer",
            "final_layer.linear",
            "final_layer.adaLN_modulation.1",
            "single_blocks.0.linear1",
            "single_blocks.0.linear2",
            "double_blocks.0.img_mlp.0",
            "double_blocks.0.img_mlp.2",
            "double_blocks.0.txt_mlp.0",
            "double_blocks.0.txt_mlp.2",
            "double_blocks.0.img_attn.proj",
            "double_blocks.0.txt_attn.proj",
        ):
            sd[f"diffusion_model.{prefix}.{lora_key}.weight"] = torch.zeros((1, 1))

        # QKV projections are fused in the converter; the B matrix must split evenly.
        sd[f"diffusion_model.double_blocks.0.img_attn.qkv.{lora_key}.weight"] = (
            torch.zeros((1, 1)) if lora_key == "lora_A" else torch.zeros((3, 1))
        )
        sd[f"diffusion_model.double_blocks.0.txt_attn.qkv.{lora_key}.weight"] = (
            torch.zeros((1, 1)) if lora_key == "lora_A" else torch.zeros((3, 1))
        )

        # These are the keys reported in the issue. The current converter does not remove them.
        sd[f"diffusion_model.guidance_in.in_layer.{lora_key}.weight"] = torch.zeros((1, 1))
        sd[f"diffusion_model.guidance_in.out_layer.{lora_key}.weight"] = torch.zeros((1, 1))

    return sd


def main() -> int:
    state_dict = build_state_dict()
    _convert_non_diffusers_flux2_lora_to_diffusers(state_dict)
    print("conversion succeeded unexpectedly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
