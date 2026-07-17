from __future__ import annotations

import jax
import jax.numpy as jnp
import numpyro
import numpyro.distributions as dist
from numpyro.infer import MCMC, NUTS


JUMP = 1000.0
NUM_WARMUP = 2000
NUM_SAMPLES = 20000
TARGET_ACCEPT_PROB = 0.6
SEED = 0
MEAN_TOL = 0.03


def model():
    x = numpyro.sample("x", dist.Normal())
    numpyro.factor("jump", jnp.where(x > 0, JUMP, 0))


def main() -> None:
    kernel = NUTS(model, target_accept_prob=TARGET_ACCEPT_PROB)
    mcmc = MCMC(kernel, num_warmup=NUM_WARMUP, num_samples=NUM_SAMPLES, progress_bar=False)
    mcmc.run(jax.random.PRNGKey(SEED), extra_fields=["diverging"])

    xs = mcmc.get_samples()["x"]
    sample_mean = float(jnp.mean(xs))
    expected_halfnormal_mean = float(jnp.sqrt(2.0 / jnp.pi))
    mean_error = sample_mean - expected_halfnormal_mean
    sample_std = float(jnp.std(xs))
    frac_positive = float(jnp.mean(xs > 0))
    num_diverging = int(mcmc.get_extra_fields()["diverging"].sum())

    print(f"sample_mean={sample_mean:.6f}")
    print(f"expected_halfnormal_mean={expected_halfnormal_mean:.6f}")
    print(f"mean_error={mean_error:.6f}")
    print(f"sample_std={sample_std:.6f}")
    print(f"frac_positive={frac_positive:.6f}")
    print(f"num_diverging={num_diverging}")

    if not mean_error < -MEAN_TOL:
        raise AssertionError(
            "Expected a biased posterior mean below the half-normal mean, "
            f"but got mean_error={mean_error:.6f}."
        )


if __name__ == "__main__":
    main()
