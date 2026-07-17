from __future__ import annotations

import pathlib
import sys
import warnings


ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))

warnings.simplefilter("always", DeprecationWarning)

import jax.numpy as jnp
import numpyro
import numpyro.distributions as dist


def main() -> None:
    print(f"numpyro version: {numpyro.__version__}")
    print("testing Dirichlet forward sampling")
    with numpyro.handlers.seed(rng_seed=5):
        dirichlet_sample = numpyro.sample(
            "my_dirichlet", dist.Dirichlet(jnp.array([1]))
        )
    print(f"Dirichlet sample: {dirichlet_sample}")

    print("testing Beta forward sampling")
    with numpyro.handlers.seed(rng_seed=5):
        beta_sample = numpyro.sample("my_beta", dist.Beta(1, 1))
    print(f"Beta sample: {beta_sample}")


if __name__ == "__main__":
    main()
