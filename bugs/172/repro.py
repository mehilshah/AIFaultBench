from __future__ import annotations

import os
import sys

import torch


ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "codebase"))

import kornia.geometry.epipolar as epi  # noqa: E402


def main() -> int:
    F = torch.randn(1, 3, 3)
    P = epi.projections_from_fundamental(F)

    doc = epi.projections_from_fundamental.__doc__ or ""
    documented_shape = "(*, 4, 4, 2)"
    actual_shape = tuple(P.shape)

    print(f"torch_version={torch.__version__}")
    print(f"documented_shape={documented_shape}")
    print(f"docstring_mentions_shape={documented_shape in doc}")
    print(f"actual_shape={actual_shape}")
    print(f"sample_tensor_shape={P.shape}")
    print(f"matches_documented_shape={actual_shape == (1, 4, 4, 2)}")

    if actual_shape != (1, 3, 4, 2):
        raise SystemExit(f"Unexpected runtime shape: {actual_shape}")

    if documented_shape not in doc:
        raise SystemExit("Docstring does not advertise the expected shape")

    print("result=runtime shape differs from documented shape")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
