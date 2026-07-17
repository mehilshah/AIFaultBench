#!/usr/bin/env python3
"""Reproduce the ConvNeXt batch-size dependent output on CUDA."""

from __future__ import annotations

import sys
from pathlib import Path

import torch


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
if str(CODEBASE) not in sys.path:
    sys.path.insert(0, str(CODEBASE))

from timm import create_model  # noqa: E402


def main() -> int:
    if not torch.cuda.is_available():
        raise SystemExit("CUDA is required for this repro; no CUDA device is available.")

    device = torch.device("cuda")

    torch.manual_seed(0)
    model = create_model("convnext_tiny.fb_in22k", pretrained=True)
    model.to(device)
    model.eval()

    batch_inp = torch.randn(4, 3, 224, 224, device=device)
    single_inp = batch_inp[0].unsqueeze(0)

    with torch.inference_mode():
        batch_out = model(batch_inp)
        single_out = model(single_inp)

    first_batch = batch_out[0][0].item()
    first_single = single_out[0][0].item()
    abs_diff = abs(first_batch - first_single)
    max_abs_diff = (batch_out[0] - single_out[0]).abs().max().item()

    print(f"torch {torch.__version__}")
    print(f"cuda_available {torch.cuda.is_available()}")
    print(f"cuda_device {torch.cuda.get_device_name(0)}")
    print(f"batch_out[0][0] {first_batch}")
    print(f"single_out[0][0] {first_single}")
    print(f"abs_diff {abs_diff}")
    print(f"max_abs_diff {max_abs_diff}")
    print(f"allclose_default {torch.allclose(batch_out[0], single_out[0])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
