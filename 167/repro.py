#!/usr/bin/env python3
from __future__ import annotations

import os
import sys

import torch


def main() -> int:
    root = os.path.dirname(os.path.abspath(__file__))
    codebase = os.path.join(root, "codebase")
    if codebase not in sys.path:
        sys.path.insert(0, codebase)

    from kornia.geometry import depth_to_3d_v2

    batch, height, width = 4, 512, 512
    depth = torch.rand(batch, height, width)
    intrinsics = torch.tensor(
        [
            [2262.52, 0.0, 1096.98],
            [0.0, 2265.3017905988554, 513.137],
            [0.0, 0.0, 1.0],
        ]
    )[None].repeat(batch, 1, 1)

    print(f"depth shape: {tuple(depth.shape)}")
    print(f"intrinsics shape: {tuple(intrinsics.shape)}")
    print("calling depth_to_3d_v2(...)")
    points_3d = depth_to_3d_v2(depth, intrinsics)
    print(f"points_3d shape: {tuple(points_3d.shape)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
