#!/usr/bin/env python3
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import torch
from torch.autograd import gradcheck


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
if str(CODEBASE) not in sys.path:
    sys.path.insert(0, str(CODEBASE))

warnings.filterwarnings("ignore", category=DeprecationWarning)

from kornia.testing import tensor_to_gradcheck_var  # noqa: E402


def to_tensor_2d(batched_boxes: torch.Tensor) -> torch.Tensor:
    batched_boxes = batched_boxes if batched_boxes.ndim == 4 else batched_boxes.unsqueeze(0)
    boxes = torch.stack([batched_boxes.amin(dim=-2), batched_boxes.amax(dim=-2)], dim=-2).view(
        batched_boxes.shape[0], batched_boxes.shape[1], 4
    )
    return boxes


def to_tensor_3d(batched_boxes: torch.Tensor) -> torch.Tensor:
    batched_boxes = batched_boxes if batched_boxes.ndim == 4 else batched_boxes.unsqueeze(0)
    boxes = torch.stack([batched_boxes.amin(dim=-2), batched_boxes.amax(dim=-2)], dim=-2).view(
        batched_boxes.shape[0], batched_boxes.shape[1], 6
    )
    return boxes


def main() -> int:
    print(f"torch={torch.__version__}")
    print(f"codebase={CODEBASE}")

    t_boxes2d = torch.tensor([[[1.0, 1.0], [3.0, 1.0], [3.0, 2.0], [1.0, 2.0]]])
    t_boxes2d = tensor_to_gradcheck_var(t_boxes2d)
    ok_2d = gradcheck(to_tensor_2d, t_boxes2d, raise_exception=True)
    print(f"gradcheck_2d={ok_2d}")

    t_boxes3d = torch.tensor(
        [[[0, 1, 2], [10, 1, 2], [10, 21, 2], [0, 21, 2], [0, 1, 32], [10, 1, 32], [10, 21, 32], [0, 21, 32]]],
        dtype=torch.float,
    )
    t_boxes3d = tensor_to_gradcheck_var(t_boxes3d)
    try:
        ok_3d = gradcheck(to_tensor_3d, t_boxes3d, raise_exception=True)
        print(f"gradcheck_3d={ok_3d}")
    except Exception as exc:
        print(f"gradcheck_3d_failed={type(exc).__name__}: {exc}")
        return 0

    print("unexpected: 3D gradcheck passed")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
