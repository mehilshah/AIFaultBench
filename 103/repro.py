#!/usr/bin/env python3
"""Minimal reproduction for the LFQ commitment-loss masking bug."""

from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

import torch


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
sys.path.insert(0, str(CODEBASE))

from vector_quantize_pytorch import ResidualLFQ  # noqa: E402


def main() -> int:
    torch.manual_seed(0)
    warnings.simplefilter("always", UserWarning)

    model = ResidualLFQ(
        dim=14,
        num_quantizers=1,
        codebook_size=16384,
        commitment_loss_weight=1.0,
        entropy_loss_weight=0.0,
    )
    model.train()

    x = torch.randn(2, 1851, 14)
    mask = torch.ones(2, 1851, dtype=torch.bool)
    mask[0, 0] = False
    mask[1, 0] = False

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", UserWarning)
        quantized, indices, losses = model(x, mask=mask)

    print(f"input_shape={tuple(x.shape)}")
    print(f"mask_true={int(mask.sum().item())}")
    print(f"quantized_shape={tuple(quantized.shape)}")
    print(f"indices_shape={tuple(indices.shape)}")
    print(f"loss_shape={tuple(losses.shape)}")

    reproducible = False
    for item in caught:
        formatted = warnings.formatwarning(
            item.message,
            item.category,
            item.filename,
            item.lineno,
            line=item.line,
        )
        print(formatted, file=sys.stderr, end="")
        if "Using a target size" in str(item.message):
            reproducible = True

    result = {
        "reproducible": reproducible,
        "warning_count": len(caught),
    }
    print(json.dumps(result, sort_keys=True))
    return 0 if reproducible else 1


if __name__ == "__main__":
    raise SystemExit(main())
