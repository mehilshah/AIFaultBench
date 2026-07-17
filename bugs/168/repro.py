from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import torch


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))

import kornia.augmentation as K  # noqa: E402


def check_case(name: str, aug: torch.nn.Module, video: torch.Tensor) -> tuple[list[bool], bool]:
    out = aug(video)
    frame_flags = [bool(torch.all(out[i] == out[i][:, 0:1, :, :])) for i in range(out.shape[0])]
    videos_different = bool(not torch.all(out[0] == out[1]).item())

    print(f"{name}:")
    print(f"  output_shape: {tuple(out.shape)}")
    print(f"  frames_identical: {frame_flags}")
    print(f"  videos_different: {videos_different}")
    return frame_flags, videos_different


def main() -> int:
    torch.manual_seed(42)
    np.random.seed(42)

    frame_data = np.random.rand(100, 100).astype(np.float32)
    video = torch.from_numpy(frame_data)[None, None, None, :, :].repeat(2, 1, 20, 1, 1)

    print(f"input_shape: {tuple(video.shape)}")

    cases = [
        (
            "RandomCrop",
            K.VideoSequential(
                K.RandomCrop(size=(50, 50), same_on_batch=False),
                data_format="BCTHW",
                same_on_frame=True,
            ),
        ),
        (
            "RandomHorizontalFlip",
            K.VideoSequential(
                K.RandomHorizontalFlip(p=1.0, same_on_batch=False),
                data_format="BCTHW",
                same_on_frame=True,
            ),
        ),
        (
            "Combined RandomCrop + RandomHorizontalFlip",
            K.VideoSequential(
                K.RandomCrop(size=(50, 50), same_on_batch=False),
                K.RandomHorizontalFlip(p=1.0, same_on_batch=False),
                data_format="BCTHW",
                same_on_frame=True,
            ),
        ),
    ]

    failures: list[str] = []
    for name, aug in cases:
        frame_flags, videos_different = check_case(name, aug, video)
        if not all(frame_flags):
            failures.append(f"{name}: frames are not identical within each video")
        if not videos_different:
            failures.append(f"{name}: videos are not different across the batch")

    if failures:
        print("BUG_REPRODUCED")
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print("NO_BUG")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
