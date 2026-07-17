#!/usr/bin/env python3
"""Minimal Lightning repro for the invalid `xpu` accelerator error."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase" / "src"))

from lightning.pytorch import Trainer  # noqa: E402
from lightning.pytorch.accelerators import AcceleratorRegistry  # noqa: E402


def main() -> int:
    available = sorted(AcceleratorRegistry.available_accelerators())
    print(f"available_accelerators={available}")
    print("attempting Trainer(accelerator='xpu', devices=1, max_epochs=1)")

    try:
        Trainer(accelerator="xpu", devices=1, max_epochs=1)
    except Exception as exc:  # noqa: BLE001
        print(f"caught_exception={type(exc).__name__}", file=sys.stderr)
        print(str(exc), file=sys.stderr)
        return 0

    print("unexpectedly accepted accelerator='xpu'")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
