#!/usr/bin/env python3
from pathlib import Path

import numpy as np
from PIL import Image
import torch


ROOT = Path(__file__).resolve().parent


def make_sample_image(path: Path) -> None:
    data = np.array(
        [
            [[10, 20, 30], [40, 50, 60]],
            [[70, 80, 90], [100, 110, 120]],
        ],
        dtype=np.uint8,
    )
    Image.fromarray(data, mode="RGB").save(path)


def read_image_bgr(path: Path) -> np.ndarray:
    # This mirrors detectron2.data.detection_utils.convert_PIL_to_numpy(..., "BGR").
    image = np.asarray(Image.open(path).convert("RGB"))
    return image[:, :, ::-1]


def main() -> int:
    sample_path = ROOT / "sample.png"
    make_sample_image(sample_path)

    image = read_image_bgr(sample_path)
    print(f"read_image shape: {image.shape}")
    print(f"read_image strides: {image.strides}")
    print(f"has negative stride: {any(stride < 0 for stride in image.strides)}")

    # This is the same conversion performed in
    # detectron2/modeling/test_time_augmentation.py::_maybe_read_image.
    torch_image = torch.from_numpy(image).permute(2, 0, 1)
    print(f"tensor shape: {tuple(torch_image.shape)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
