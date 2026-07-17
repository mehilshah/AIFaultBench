#!/usr/bin/env python3
import traceback

import torch

import pyro
import pyro.distributions as dist
from pyro.infer import SVI, Trace_ELBO
from pyro.infer.autoguide import AutoNormal
from pyro.optim import ClippedAdam


def model():
    x = pyro.sample("x", dist.Normal(torch.zeros(85), torch.ones(85)).to_event(1))
    pyro.sample("obs", dist.Normal(x.sum(), 1.0), obs=torch.tensor(0.0))


def main():
    pyro.set_rng_seed(0)
    pyro.clear_param_store()

    guide = AutoNormal(model)
    svi = SVI(model, guide, ClippedAdam({"lr": 0.01}), loss=Trace_ELBO())

    for _ in range(2):
        svi.step()

    print(f"pyro={pyro.__version__} torch={torch.__version__}")
    print("calling AutoNormal.quantiles([0.05, 0.5, 0.95])")
    guide.quantiles([0.05, 0.5, 0.95])


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        raise SystemExit(1)
