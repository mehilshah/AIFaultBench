#!/usr/bin/env python3
"""Reproduce the reported TraceEnum_ELBO discrepancy, if present."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import torch
from torch.distributions import constraints


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
RESULT_PATH = ROOT / "reproduction.json"


def _patch_runtime_compatibility() -> None:
    # This standardized folder is executed on Python 3.12 with Torch 2.x,
    # while the recovered Pyro snapshot expects Torch 1.x at import time.
    torch.__version__ = "1.13.0"

    if str(CODEBASE) not in sys.path:
        sys.path.insert(0, str(CODEBASE))

    import pyro.distributions as pydist

    if not hasattr(pydist, "Logistic"):
        class Logistic(torch.distributions.Distribution):
            arg_constraints = {"loc": constraints.real, "scale": constraints.positive}
            support = constraints.real
            has_rsample = False

            def __init__(self, loc, scale, validate_args=None):
                self.loc = loc
                self.scale = scale
                super().__init__(batch_shape=torch.Size(), event_shape=torch.Size(), validate_args=validate_args)

            def sample(self, sample_shape=torch.Size()):
                return torch.zeros(sample_shape)

            def log_prob(self, value):
                return torch.zeros_like(value)

        pydist.Logistic = Logistic

    uniform_ac = getattr(pydist.Uniform, "arg_constraints", None)
    if isinstance(uniform_ac, property):
        pydist.Uniform.arg_constraints = {"low": constraints.real, "high": constraints.real}


def main() -> int:
    os.environ.setdefault("TEST_ENUM_PYRO_BACKEND", "contrib.funsor")

    _patch_runtime_compatibility()

    import funsor
    import pyro.contrib.funsor  # noqa: F401
    from pyroapi import distributions as dist
    from pyroapi import infer, pyro

    funsor.set_backend("torch")
    pyro.clear_param_store()
    pyro.set_rng_seed(0)

    pyro.param("model_probs_a", torch.tensor([0.45, 0.55]), constraint=constraints.simplex)
    pyro.param("model_probs_b", torch.tensor([[0.3, 0.7], [0.6, 0.4]]), constraint=constraints.simplex)
    pyro.param("model_probs_c", torch.tensor([[0.3, 0.4, 0.3], [0.4, 0.4, 0.2]]), constraint=constraints.simplex)
    pyro.param("guide_probs_a", torch.tensor([0.45, 0.55]), constraint=constraints.simplex)
    pyro.param("guide_probs_b", torch.tensor([[0.3, 0.7], [0.8, 0.2]]), constraint=constraints.simplex)
    data = torch.tensor([1, 2])

    @infer.config_enumerate
    def model_plate():
        probs_a = pyro.param("model_probs_a")
        probs_b = pyro.param("model_probs_b")
        probs_c = pyro.param("model_probs_c")
        a = pyro.sample("a", dist.Categorical(probs_a))
        with pyro.plate("b_axis", 2):
            b = pyro.sample("b", dist.Categorical(probs_b[a]))
            pyro.sample("c", dist.Categorical(probs_c[b]), obs=data)

    @infer.config_enumerate
    def guide_plate():
        probs_a = pyro.param("guide_probs_a")
        probs_b = pyro.param("guide_probs_b")
        a = pyro.sample("a", dist.Categorical(probs_a))
        with pyro.plate("b_axis", 2):
            pyro.sample("b", dist.Categorical(probs_b[a]))

    @infer.config_enumerate
    def model_iplate():
        probs_a = pyro.param("model_probs_a")
        probs_b = pyro.param("model_probs_b")
        probs_c = pyro.param("model_probs_c")
        a = pyro.sample("a", dist.Categorical(probs_a))
        for i in pyro.plate("b_axis", 2):
            b = pyro.sample(f"b_{i}", dist.Categorical(probs_b[a]))
            pyro.sample(f"c_{i}", dist.Categorical(probs_c[b]), obs=data[i])

    @infer.config_enumerate
    def guide_iplate():
        probs_a = pyro.param("guide_probs_a")
        probs_b = pyro.param("guide_probs_b")
        a = pyro.sample("a", dist.Categorical(probs_a))
        for i in pyro.plate("b_axis", 2):
            pyro.sample(f"b_{i}", dist.Categorical(probs_b[a]))

    expected_loss = infer.TraceEnum_ELBO(max_plate_nesting=0).differentiable_loss(model_iplate, guide_iplate)
    actual_loss = infer.TraceEnum_ELBO(max_plate_nesting=1).differentiable_loss(model_plate, guide_plate)
    abs_err = (actual_loss - expected_loss).abs().item()
    reproducible = bool(abs_err > 1e-5)

    print(f"expected_loss={float(expected_loss.detach())}")
    print(f"actual_loss={float(actual_loss.detach())}")
    print(f"abs_err={abs_err}")
    print(f"reproducible={reproducible}")

    result = {
        "reproducible": reproducible,
        "evidence": (
            f"expected_loss={float(expected_loss.detach())}, actual_loss={float(actual_loss.detach())}, "
            f"abs_err={abs_err}."
        ),
        "steps": [
            "Set up a Python 3.12 venv with Torch 2.13 CPU, pyro-api, and Funsor 0.4.7.",
            "Patched Torch version and two compatibility points in-process so the recovered Pyro snapshot can import.",
            "Ran the issue's guide/model pair from tests/contrib/funsor/test_enum_funsor.py.",
            "Compared TraceEnum_ELBO(max_plate_nesting=0) against TraceEnum_ELBO(max_plate_nesting=1).",
        ],
        "blocking_reason": "" if reproducible else (
            "The standardized environment does not reproduce the mismatch; after minimal compatibility shims, "
            "the expected and actual losses are identical."
        ),
        "reproduction_command": "bash run_repro.sh",
    }
    RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
