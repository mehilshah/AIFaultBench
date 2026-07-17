import torch

import pyro
import pyro.distributions as dist
from pyro.infer.mcmc import MCMC, NUTS


def model(data):
    x = pyro.sample("x", dist.Normal(0.0, 1.0))
    pyro.sample("obs", dist.Normal(x, 1.0), obs=data)


class ModelHolder:
    def __init__(self):
        self.mcmc = MCMC(
            NUTS(model),
            num_samples=2,
            warmup_steps=2,
            num_chains=2,
            mp_context="spawn",
            disable_progbar=True,
        )

    def fit(self, data):
        self.mcmc.run(data)
        return self.mcmc.get_samples()


def main():
    pyro.set_rng_seed(0)
    holder = ModelHolder()
    data = torch.tensor(0.0)

    print("first run")
    print(holder.fit(data))
    print("second run")
    print(holder.fit(data))


if __name__ == "__main__":
    main()
