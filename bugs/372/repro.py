#!/usr/bin/env python3
"""Reproduce the MixtureOfDiagNormals bugs from pyro issue 3274."""

from __future__ import annotations

import os
import sys
import traceback
from dataclasses import dataclass
from typing import Any


ROOT = os.path.dirname(os.path.abspath(__file__))
CODEBASE = os.path.join(ROOT, "codebase")
if CODEBASE not in sys.path:
    sys.path.insert(0, CODEBASE)

import torch

import pyro
import pyro.distributions as dist
from pyro.infer.autoguide import AutoNormal


@dataclass
class CheckResult:
    name: str
    reproduced: bool
    details: str


def check_missing_support() -> CheckResult:
    locs = torch.tensor([[0.0, 0.0], [1.0, 1.0]])
    scales = torch.ones(2, 2)
    logits = torch.zeros(2)

    def model():
        pyro.sample("z", dist.MixtureOfDiagNormals(locs, scales, logits))

    guide = AutoNormal(model)
    try:
        guide()
    except Exception:
        details = traceback.format_exc()
        return CheckResult("missing_support", True, details)

    return CheckResult("missing_support", False, "AutoNormal() completed without error")


def check_rsample_shape() -> CheckResult:
    locs = torch.tensor([[0.0, 0.0], [1.0, 1.0]])
    scales = torch.ones(2, 2)
    logits = torch.zeros(2)
    d = dist.MixtureOfDiagNormals(locs, scales, logits)

    sample_shape = torch.Size([2, 3])
    try:
        value = d.rsample(sample_shape)
    except Exception:
        details = traceback.format_exc()
        return CheckResult("rsample_shape", True, details)

    expected_shape = tuple(sample_shape) + tuple(d.batch_shape) + tuple(d.event_shape)
    actual_shape = tuple(value.shape)
    if actual_shape != expected_shape:
        return CheckResult(
            "rsample_shape",
            True,
            f"expected {expected_shape}, got {actual_shape}",
        )

    return CheckResult(
        "rsample_shape",
        False,
        f"sample_shape {tuple(sample_shape)} returned {actual_shape}",
    )


def main() -> int:
    print(f"python={sys.version.split()[0]}")
    print(f"torch={torch.__version__}")
    print(f"pyro={getattr(pyro, '__version__', 'unknown')}")

    results = [check_missing_support(), check_rsample_shape()]
    for result in results:
        print(f"\n[{result.name}] reproduced={result.reproduced}")
        print(result.details)

    reproducible = all(result.reproduced for result in results)
    print(f"\nreproducible={reproducible}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
