#!/usr/bin/env python3
"""Minimal reproduction for the missing GaussianDiffusion.device property."""

from __future__ import annotations

import sys
from pathlib import Path

import torch


ROOT = Path(__file__).resolve().parent
MODULE_DIR = ROOT / "codebase" / "denoising_diffusion_pytorch"
sys.path.insert(0, str(MODULE_DIR))

from classifier_free_guidance import GaussianDiffusion, Unet  # type: ignore  # noqa: E402


def main() -> int:
    torch.manual_seed(0)

    model = Unet(
        dim=8,
        num_classes=2,
        dim_mults=(1,),
        channels=3,
        cond_drop_prob=0.0,
        resnet_block_groups=8,
    )
    diffusion = GaussianDiffusion(
        model,
        image_size=8,
        timesteps=4,
        offset_noise_strength=0.1,
    )

    print(f"has_device_property={hasattr(diffusion, 'device')}")

    images = torch.randn(2, 3, 8, 8)
    classes = torch.tensor([0, 1], dtype=torch.long)

    try:
        loss = diffusion(images, classes=classes)
    except AttributeError as exc:
        print(f"EXPECTED_FAILURE: {type(exc).__name__}: {exc}")
        return 0

    print(f"UNEXPECTED_SUCCESS: loss={loss.item():.6f}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
