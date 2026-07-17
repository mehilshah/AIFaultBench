import os
import sys
import traceback

sys.path.insert(0, os.path.abspath("codebase"))

from jax import numpy as jnp, random
from numpyro import deterministic
from numpyro.infer import MCMC, NUTS


def model():
    deterministic("x", jnp.array([1.0, 2.0]))


def main():
    mcmc = MCMC(NUTS(model), num_warmup=10, num_samples=10)
    mcmc.run(random.PRNGKey(0))

    samples = mcmc.get_samples()
    print("samples =", samples)

    try:
        mcmc.print_summary()
    except Exception:
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
