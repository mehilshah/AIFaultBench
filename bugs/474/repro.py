#!/usr/bin/env python3
"""Reproduce the Pyro metaclass conflict in a deterministic way.

The original issue was triggered by a PyTorch nightly change to
torch.nn.ModuleList. The exact historical nightly wheel is no longer
available on the public index here, so this script patches ModuleList with an
incompatible metaclass to drive the same import-time failure path in Pyro.
"""

from __future__ import annotations

import traceback

import torch


class NightlyStyleMeta(type):
    pass


class PatchedModuleList(metaclass=NightlyStyleMeta):
    pass


def main() -> int:
    print(f"torch version: {torch.__version__}")
    print(f"original torch.nn.ModuleList metaclass: {torch.nn.ModuleList.__class__.__name__}")

    torch.nn.ModuleList = PatchedModuleList
    print(
        "patched torch.nn.ModuleList metaclass:",
        torch.nn.ModuleList.__class__.__name__,
    )

    try:
        import pyro.distributions as base_distributions  # noqa: F401
    except Exception:
        traceback.print_exc()
        return 1

    print("unexpected success: pyro.distributions imported")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
