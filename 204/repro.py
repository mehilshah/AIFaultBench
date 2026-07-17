from __future__ import annotations

import equinox as eqx
import jax
import jax.numpy as jnp
from jax import random
import jax.tree_util as jtu

import numpyro
from numpyro.contrib.module import eqx_module, random_eqx_module
import numpyro.distributions as dist


def main() -> None:
    print("jax", jax.__version__)
    print("equinox", eqx.__version__)
    print("numpyro", numpyro.__version__)

    rng_key = random.PRNGKey(seed=42)

    n = 32 * 10
    rng_key, _ = random.split(rng_key)
    x = jnp.linspace(1, jnp.pi, n)
    x_train = x[..., None]

    class LocMLP(eqx.Module):
        linear1: eqx.nn.Linear
        linear2: eqx.nn.Linear
        linear3: eqx.nn.Linear

        def __init__(self, din: int, dmid: int, dout: int, *, key):
            key1, key2, key3 = random.split(key, 3)
            self.linear1 = eqx.nn.Linear(din, dmid, key=key1)
            self.linear2 = eqx.nn.Linear(dmid, dmid, key=key2)
            self.linear3 = eqx.nn.Linear(dmid, dout, key=key3)

        def __call__(self, x):
            x = self.linear1(x)
            x = jax.nn.sigmoid(x)
            x = self.linear2(x)
            x = jax.nn.sigmoid(x)
            x = self.linear3(x)
            return x

    class ScaleMLP(eqx.Module):
        linear: eqx.nn.Linear

        def __init__(self, *, key) -> None:
            self.linear = eqx.nn.Linear(1, 1, key=key)

        def __call__(self, x):
            x = self.linear(x)
            return jax.nn.softplus(x)

    _, mu_key, sigma_key = random.split(rng_key, 3)
    mu_nn_module = LocMLP(din=1, dmid=8, dout=1, key=mu_key)
    sigma_nn_module = ScaleMLP(key=sigma_key)
    print(
        [jtu.keystr(path)[1:] for path, _ in jtu.tree_leaves_with_path(sigma_nn_module)]
    )

    def model(x):
        mu_nn = eqx_module("mu_nn", mu_nn_module)
        sigma_nn = random_eqx_module(
            "sigma_nn",
            sigma_nn_module,
            prior={
                "linear.weight": dist.HalfNormal(scale=1),
                "linear.bias": dist.Normal(loc=0, scale=1),
            },
        )

        mu = numpyro.deterministic("mu", jax.vmap(mu_nn)(x).squeeze())
        sigma = numpyro.deterministic("sigma", jax.vmap(sigma_nn)(x).squeeze())

        with numpyro.plate("data", x.shape[0]):
            numpyro.sample("likelihood", dist.Normal(loc=mu, scale=sigma))

    numpyro.render_model(
        model=model,
        model_args=(x_train,),
        render_distributions=True,
        render_params=True,
    )


if __name__ == "__main__":
    main()
