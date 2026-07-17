#!/usr/bin/env python3
"""Minimal repro for PyTorch meshgrid indexing compatibility.

The checked-out Pyro codebase already contains the workaround for this issue in
`codebase/examples/neutra.py`, so this script reproduces the historical failure
directly against the Torch API version that the CI server installed.
"""

from __future__ import annotations

import sys

import torch


def main() -> int:
    xs = torch.linspace(-1, 1, 3)
    ys = torch.linspace(-2, 2, 4)

    print(f"torch={torch.__version__}")
    print("calling torch.meshgrid(xs, ys, indexing='xy')")
    try:
        torch.meshgrid(xs, ys, indexing="xy")
    except TypeError as exc:
        print(f"expected failure: {type(exc).__name__}: {exc}")
        return 1

    print("unexpected success: this environment does not reproduce the bug")
    return 0


if __name__ == "__main__":
    sys.exit(main())
