#!/usr/bin/env python3
"""Minimal reproduction for the ModelNet10 download failure."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import torch
from torch_geometric.datasets import ModelNet


def main() -> int:
    root = Path(__file__).resolve().parent / "repro_data" / "modelnet10"
    if root.exists():
        shutil.rmtree(root)
    root.parent.mkdir(parents=True, exist_ok=True)

    print(f"torch={torch.__version__}")
    print("creating ModelNet(root='repro_data/modelnet10', name='10', train=True)")

    try:
        ModelNet(str(root), "10", True)
    except Exception as exc:  # pragma: no cover
        print(f"observed {type(exc).__name__}: {exc}")
        raise

    print("unexpected success")
    return 0


if __name__ == "__main__":
    sys.exit(main())
