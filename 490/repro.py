#!/usr/bin/env python3
"""Minimal CUDA repro for the Detectron2 Docker runtime issue."""

from __future__ import annotations

import os
import traceback

import torch


def main() -> None:
    print(f"torch_version={torch.__version__}")
    print(f"cuda_is_available={torch.cuda.is_available()}")
    print(f"cuda_visible_devices={os.environ.get('CUDA_VISIBLE_DEVICES')!r}")

    # This matches the kind of GPU move Detectron2 performs in its default
    # predictor / launch paths when the Docker image is used without GPU access.
    try:
        torch.zeros(1).cuda()
    except Exception:
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
