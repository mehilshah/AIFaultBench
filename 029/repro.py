#!/usr/bin/env python3
"""Reproduce the ImageNet example crash caused by unconditional MPS access."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MAIN = ROOT / "codebase" / "imagenet" / "main.py"


def _remove_mps_backend() -> None:
    import torch

    if hasattr(torch.backends, "mps"):
        delattr(torch.backends, "mps")

    # Force the code path that reaches the mps availability check in main.py.
    torch.cuda.is_available = lambda: True  # type: ignore[assignment]
    if hasattr(torch.cuda, "device_count"):
        torch.cuda.device_count = lambda: 1  # type: ignore[assignment]


def main() -> None:
    _remove_mps_backend()

    print("Running codebase/imagenet/main.py with --dummy")
    print("torch.backends.mps removed to emulate a build without MPS support")

    sys.argv = [str(MAIN), "-a", "resnet18", "--dummy"]
    runpy.run_path(str(MAIN), run_name="__main__")


if __name__ == "__main__":
    main()
