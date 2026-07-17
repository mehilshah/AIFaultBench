#!/usr/bin/env python3
from pathlib import Path
import sys

import torch


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase" / "src"))

from transformers.models.eomt.image_processing_eomt import convert_segmentation_map_to_binary_masks


def main() -> None:
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required to reproduce this bug.")

    image = torch.randn(3, 8, 8, device="cuda")
    segmentation_map = torch.randint_like(image[0], 0, 10)

    print(f"image_device={image.device}")
    print(f"segmentation_map_device={segmentation_map.device}")
    convert_segmentation_map_to_binary_masks(segmentation_map)


if __name__ == "__main__":
    main()
