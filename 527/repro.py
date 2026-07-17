#!/usr/bin/env python3
"""Reproduce the import-time failure in pyro.distributions.torch_patch."""

from __future__ import annotations

import importlib.util
import pathlib
import sys
import traceback
from types import ModuleType


ROOT = pathlib.Path(__file__).resolve().parent
TARGET = ROOT / "codebase" / "pyro" / "distributions" / "torch_patch.py"


def install_fake_torch() -> None:
    torch = ModuleType("torch")
    torch.__version__ = "1.13.1"

    class _Linalg:
        @staticmethod
        def norm(value, dim=-1):
            return 0

        @staticmethod
        def eigvalsh(value):
            return 0

    torch.linalg = _Linalg()

    distributions = ModuleType("torch.distributions")
    constraints = ModuleType("torch.distributions.constraints")
    transforms = ModuleType("torch.distributions.transforms")
    utils = ModuleType("torch.distributions.utils")

    class Transform:
        def __getstate__(self):
            return {}

        def clear_cache(self):
            return None

    class TransformedDistribution:
        def clear_cache(self):
            return None

    class HalfCauchy:
        def log_prob(self, value):
            return value

    class _PositiveDefinite:
        def check(self, value):
            return True

    class _LowerCholesky:
        def check(self, value):
            return True

    class lazy_property:
        def __call__(self):
            raise NotImplementedError

    transforms.Transform = Transform
    distributions.TransformedDistribution = TransformedDistribution
    distributions.HalfCauchy = HalfCauchy
    constraints._PositiveDefinite = _PositiveDefinite
    constraints.lower_cholesky = _LowerCholesky()
    utils.lazy_property = lazy_property

    distributions.constraints = constraints
    distributions.transforms = transforms
    distributions.utils = utils
    torch.distributions = distributions

    sys.modules["torch"] = torch
    sys.modules["torch.distributions"] = distributions
    sys.modules["torch.distributions.constraints"] = constraints
    sys.modules["torch.distributions.transforms"] = transforms
    sys.modules["torch.distributions.utils"] = utils


def main() -> int:
    install_fake_torch()
    print("using fake torch version 1.13.1")
    print(
        "has torch.distributions.constraints._CorrCholesky:",
        hasattr(sys.modules["torch.distributions.constraints"], "_CorrCholesky"),
    )

    spec = importlib.util.spec_from_file_location(
        "pyro.distributions.torch_patch", TARGET
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {TARGET}")

    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception:
        traceback.print_exc()
        return 1

    print("unexpected success importing", TARGET)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

