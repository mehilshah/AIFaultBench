import jax
import jax.numpy as jnp

import numpyro
import numpyro.distributions as dist
from numpyro.infer import Predictive


def model():
    loc = numpyro.sample("loc", dist.Normal(0.0, 1.0))
    numpyro.sample("obs", dist.Normal(loc, 1.0))


posterior_samples = {"loc": jnp.array([0.1, 0.2, 0.3])}


def run_with_key(key):
    predictive = Predictive(model, posterior_samples, parallel=True)
    return predictive(key)


def main():
    print(f"jax={jax.__version__}")
    print(f"numpyro={numpyro.__version__}")

    legacy_key = jax.random.PRNGKey(0)
    modern_key = jax.random.key(0)

    print("legacy_key_type=", type(legacy_key).__name__)
    print("modern_key_type=", type(modern_key).__name__)

    legacy_out = run_with_key(legacy_key)
    print("legacy_parallel_ok=", legacy_out)

    print("running modern typed key path...")
    modern_out = run_with_key(modern_key)
    print("modern_parallel_ok=", modern_out)


if __name__ == "__main__":
    main()
