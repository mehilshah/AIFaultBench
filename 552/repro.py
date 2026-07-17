import os
import sys


ROOT = os.path.dirname(os.path.abspath(__file__))
CODEBASE = os.path.join(ROOT, "codebase")
if CODEBASE not in sys.path:
    sys.path.insert(0, CODEBASE)


import pyro
import pyro.distributions as dist
import torch
from pyro.infer import MCMC, NUTS


def build_model(labels, dim):
    def model(data):
        coefs_mean = torch.zeros(dim)
        coefs = pyro.sample("beta", dist.Normal(coefs_mean, torch.ones(3)))
        return pyro.sample(
            "y", dist.Bernoulli(logits=(coefs * data).sum(-1)), obs=labels
        )

    return model


def main():
    pyro.set_rng_seed(0)
    torch.manual_seed(0)

    print("pyro", pyro.__version__)
    print("torch", torch.__version__)

    true_coefs = torch.tensor([1.0, 2.0, 3.0])
    data = torch.randn(2000, 3)
    labels = dist.Bernoulli(logits=(true_coefs * data).sum(-1)).sample()

    model = build_model(labels, dim=3)
    nuts_kernel = NUTS(model, adapt_step_size=True)
    mcmc = MCMC(nuts_kernel, num_samples=10, warmup_steps=5)
    print("starting run")
    mcmc.run(data)
    print("done")


if __name__ == "__main__":
    main()
