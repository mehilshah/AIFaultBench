#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import torch


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase" / "src"))

from diffusers.models.transformers.transformer_ideogram4 import IMAGE_POSITION_OFFSET, Ideogram4MRoPE


def main() -> None:
    device_type = "cpu"
    device = torch.device(device_type)

    rope = Ideogram4MRoPE(head_dim=256, base=5_000_000, mrope_section=(24, 20, 20)).to(device)
    position_ids = torch.tensor([[[0, 0, 0], [0, 0, 1], [0, 63, 63]]], device=device) + IMAGE_POSITION_OFFSET

    cos_ref, sin_ref = rope(position_ids)
    with torch.autocast(device_type=device_type, dtype=torch.bfloat16):
        cos_ac, sin_ac = rope(position_ids)

    ref_equal_01 = torch.equal(cos_ref[0, 0], cos_ref[0, 1])
    ref_equal_02 = torch.equal(cos_ref[0, 0], cos_ref[0, 2])
    ac_equal_01 = torch.equal(cos_ac[0, 0], cos_ac[0, 1])
    ac_equal_02 = torch.equal(cos_ac[0, 0], cos_ac[0, 2])
    max_diff = (cos_ac - cos_ref).abs().max().item()

    print(f"torch: {torch.__version__}")
    print(f"device_type: {device_type}")
    print(f"image_position_offset: {IMAGE_POSITION_OFFSET}")
    print(f"ref_equal_01: {ref_equal_01}")
    print(f"ref_equal_02: {ref_equal_02}")
    print(f"ac_equal_01: {ac_equal_01}")
    print(f"ac_equal_02: {ac_equal_02}")
    print(f"max_diff: {max_diff}")
    print(f"ref_sample: {cos_ref[0, 0, 0].item()} {cos_ref[0, 1, 0].item()} {cos_ref[0, 2, 0].item()}")
    print(f"ac_sample: {cos_ac[0, 0, 0].item()} {cos_ac[0, 1, 0].item()} {cos_ac[0, 2, 0].item()}")

    assert not ref_equal_01, "Reference path should preserve distinct positions."
    assert not ref_equal_02, "Reference path should preserve distinct positions."
    assert ac_equal_01, "Autocast path should collapse adjacent image positions."
    assert ac_equal_02, "Autocast path should collapse distant image positions."
    assert max_diff > 1.0, "Autocast path should diverge substantially from fp32."


if __name__ == "__main__":
    main()
