#!/usr/bin/env python3

import numpy as np

import jax

import numpyro
import numpyro.distributions as dist
from numpyro.infer import AIES, ESS, MCMC, NUTS


def model(data):
    lam = numpyro.sample("lam", dist.Uniform(0, 100))
    numpyro.sample("obs", dist.Poisson(lam), obs=data)


def lag1_autocorr(samples):
    flat = np.asarray(samples).reshape(-1)
    return float(np.corrcoef(flat[:-1], flat[1:])[0, 1])


def run_kernel(name, kernel, rng_key, chain_method, counts):
    mcmc = MCMC(
        kernel,
        num_warmup=500,
        num_samples=250,
        num_chains=4,
        chain_method=chain_method,
        progress_bar=False,
    )
    mcmc.run(rng_key, data=counts)
    samples = mcmc.get_samples(group_by_chain=True)["lam"]
    lag1 = lag1_autocorr(samples)
    print(f"{name}: lag1_autocorr={lag1:.6f}")
    return lag1


def main():
    print(f"jax={jax.__version__} numpyro={numpyro.__version__}")
    print(f"device_count={jax.device_count()}")

    counts = np.random.default_rng(42).poisson(50, 100)

    nuts = run_kernel(
        "NUTS",
        NUTS(model),
        jax.random.PRNGKey(0),
        "parallel",
        counts,
    )
    aies = run_kernel(
        "AIES",
        AIES(model, randomize_split=False, moves={AIES.StretchMove(): 1.0}),
        jax.random.PRNGKey(1),
        "vectorized",
        counts,
    )
    ess = run_kernel(
        "ESS",
        ESS(model, randomize_split=False),
        jax.random.PRNGKey(1),
        "vectorized",
        counts,
    )

    print(f"comparison: ESS<{aies:.6f} AIES, ESS<{nuts:.6f} NUTS")
    print(f"summary: NUTS={nuts:.6f} AIES={aies:.6f} ESS={ess:.6f}")


if __name__ == "__main__":
    main()
