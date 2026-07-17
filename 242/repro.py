import numpy as np

import flax.linen as nn
from jax import random

import numpyro
import numpyro.distributions as dist
from numpyro.contrib.module import random_flax_module
from numpyro.infer import MCMC, NUTS


def main():
    rng = np.random.default_rng(99)
    n = 1000

    x = rng.normal(0, 1, size=(n, 1))
    mu = 1 + x @ np.array([0.5])
    y = rng.normal(mu, 0.5)

    class Linear(nn.Module):
        @nn.compact
        def __call__(self, x):
            return nn.Dense(1, use_bias=True, name="Dense")(x)

    def model(x, y=None):
        sigma = numpyro.sample("sigma", dist.HalfNormal(0.1))
        priors = {
            "Dense.bias": dist.Normal(0, 2.5),
            "Dense.kernel": dist.Normal(0, 1),
        }
        mlp = random_flax_module(
            "mlp",
            Linear(),
            prior=priors,
            input_shape=(x.shape[1],),
        )
        with numpyro.plate("data", x.shape[0]):
            mu = numpyro.deterministic("mu", mlp(x).squeeze(-1))
            numpyro.sample("y", dist.Normal(mu, sigma), obs=y)

    kernel = NUTS(model, target_accept_prob=0.95)
    mcmc = MCMC(kernel, num_warmup=10, num_samples=10, num_chains=1, progress_bar=False)
    mcmc.run(random.PRNGKey(0), x=x, y=y)

    samples = mcmc.get_samples()
    print("sample_keys", sorted(samples))
    print("calling log_likelihood")
    numpyro.infer.util.log_likelihood(model, samples, x=x, y=y)


if __name__ == "__main__":
    main()
