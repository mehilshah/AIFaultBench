#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import torch


def build_masked_target() -> torch.Tensor:
    """Mirror the CVAE example target shape and masking pattern.

    The example's `MaskImages` transform leaves ordinary MNIST pixels in
    `[0, 1]` and stamps masked regions with `-1`. PyTorch's BCE validation
    rejects that target domain.
    """

    target = torch.zeros((1, 28, 28), dtype=torch.float32)
    target[:, :14, :14] = 1.0
    target[:, 14:, :14] = -1.0
    return target


def main() -> int:
    root = Path(__file__).resolve().parent
    sys.path.insert(0, str(root / "codebase" / "examples" / "cvae"))

    from baseline import MaskedBCELoss

    criterion = MaskedBCELoss()
    input_tensor = torch.full((1, 1, 28, 28), 0.5, dtype=torch.float32)
    target = build_masked_target()

    try:
        criterion(input_tensor, target)
    except Exception as exc:  # noqa: BLE001 - expected bug trigger
        payload = {
            "reproducible": True,
            "exception_type": type(exc).__name__,
            "message": str(exc),
            "target_values": sorted(torch.unique(target).tolist()),
            "explanation": (
                "MaskedBCELoss forwards a target tensor containing -1 values into "
                "torch.nn.functional.binary_cross_entropy, which now validates that "
                "targets stay within [0, 1]."
            ),
        }
        print(json.dumps(payload, indent=2))
        return 1

    print(
        json.dumps(
            {
                "reproducible": False,
                "message": "binary_cross_entropy unexpectedly accepted the masked target",
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
