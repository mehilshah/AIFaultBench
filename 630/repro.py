from __future__ import annotations

import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))

import torch
from torch.distributions import constraints

import pyro
import pyro.distributions as dist
import pyro.infer
import pyro.optim


def scale(guess):
    weight = pyro.sample("weight", dist.Normal(guess, 1.0))
    return pyro.sample("measurement", dist.Normal(weight, 0.75))


def scale_parametrized_guide(guess):
    a = pyro.param("a", torch.tensor(guess))
    b = pyro.param("b", torch.tensor(1.0), constraint=constraints.positive)
    return pyro.sample("weight", dist.Normal(a, b))


def main() -> int:
    pyro.set_rng_seed(101)
    guess = 8.5
    conditioned_scale = pyro.condition(scale, data={"measurement": 9.5})

    pyro.clear_param_store()
    svi = pyro.infer.SVI(
        model=conditioned_scale,
        guide=scale_parametrized_guide,
        optim=pyro.optim.SGD({"lr": 0.001, "momentum": 0.1}),
        loss=pyro.infer.Trace_ELBO(),
    )

    print(f"pyro={pyro.__version__}")
    print(f"torch={torch.__version__}")
    print(f"guess={guess}")

    try:
        svi.step(guess)
    except Exception as exc:
        print("expected failure observed", file=sys.stderr)
        traceback.print_exc()
        if "The value argument to log_prob must be a Tensor" in str(exc):
            return 0
        print("unexpected exception text", file=sys.stderr)
        return 1

    print("unexpected success", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
