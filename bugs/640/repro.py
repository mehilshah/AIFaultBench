#!/usr/bin/env python3
"""Minimal reproduction for the timm eval transform crop behavior."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from torchvision.transforms.functional import resize as tv_resize


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))

from timm.data.transforms_factory import create_transform  # noqa: E402


def build_test_image(width: int = 500, height: int = 224) -> Image.Image:
    """Create a wide image with a strong left-edge feature."""
    img = Image.new("L", (width, height), color=255)
    draw = ImageDraw.Draw(img)

    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    font = None
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                font = ImageFont.truetype(font_path, 120)
                break
            except Exception:
                pass
    if font is None:
        font = ImageFont.load_default()

    draw.text((4, 28), "A", fill=0, font=font)
    return img


def dark_pixel_stats(image: Image.Image) -> dict[str, int]:
    arr = np.asarray(image)
    return {
        "total_dark_pixels": int((arr < 128).sum()),
        "left_dark_pixels": int((arr[:, :60] < 128).sum()),
        "right_dark_pixels": int((arr[:, -60:] < 128).sum()),
    }


def main() -> int:
    image = build_test_image()

    transform = create_transform(
        input_size=224,
        hflip=0.0,
        vflip=0.0,
        is_training=False,
        auto_augment=None,
        interpolation="bilinear",
        mean=(0.5,),
        std=(0.5,),
        crop_pct=1.0,
        normalize=False,
    )

    reference = tv_resize(image, (224, 224))
    reproduced = transform(image)

    if hasattr(reproduced, "numpy"):
        reproduced_arr = reproduced.numpy()
        if reproduced_arr.ndim == 3:
            reproduced_arr = reproduced_arr[0]
        reproduced_img = Image.fromarray(reproduced_arr.astype(np.uint8), mode="L")
    else:
        reproduced_img = reproduced

    reference_stats = dark_pixel_stats(reference)
    reproduced_stats = dark_pixel_stats(reproduced_img)

    result = {
        "input_size": image.size,
        "reference_size": reference.size,
        "reproduced_size": reproduced_img.size,
        "reference_stats": reference_stats,
        "reproduced_stats": reproduced_stats,
        "crop_detected": reproduced_stats["left_dark_pixels"] < reference_stats["left_dark_pixels"],
        "feature_removed_from_left_edge": reproduced_stats["left_dark_pixels"] == 0,
    }

    print(json.dumps(result, indent=2, sort_keys=True))

    # Return non-zero only if the crop did not happen, since the bug is the crop.
    return 0 if result["crop_detected"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
