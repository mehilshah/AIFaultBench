#!/usr/bin/env python3
"""Reproduce the Pyro import failure against a torch build without _CorrCholesky."""

from __future__ import annotations

import importlib.util
import pathlib
import sys

import torch


ROOT = pathlib.Path(__file__).resolve().parent
TARGET = ROOT / "codebase" / "pyro" / "distributions" / "torch_patch.py"


def main() -> None:
    constraints = torch.distributions.constraints
    print(f"torch_version={torch.__version__}")
    print(f"corr_cholesky_before={hasattr(constraints, '_CorrCholesky')}")

    # The upstream PyTorch API in the bug report no longer exposes this symbol.
    # Delete it locally so the target commit exercises the same missing-attribute path.
    if hasattr(constraints, "_CorrCholesky"):
        delattr(constraints, "_CorrCholesky")
    if hasattr(constraints, "corr_cholesky"):
        delattr(constraints, "corr_cholesky")

    print(f"corr_cholesky_after={hasattr(constraints, '_CorrCholesky')}")
    print(f"loading={TARGET}")

    spec = importlib.util.spec_from_file_location("pyro_torch_patch_repro", TARGET)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {TARGET}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    print(f"loaded={module.__name__}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"{type(exc).__name__}: {exc}", file=sys.stderr)
        raise
