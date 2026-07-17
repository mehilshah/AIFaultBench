from __future__ import annotations

import json
import time
from pathlib import Path
import sys

import jax
import jax.numpy as jnp

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))

import numpyro
import numpyro.distributions as dist
from numpyro.infer import MCMC, NUTS

RESULT_PATH = ROOT / "reproduction.json"


def model(x, y=None):
    amp = numpyro.sample("amp", dist.Uniform(-8, -5))
    scale = numpyro.sample("scale", dist.Uniform(-1, 1))
    noise = numpyro.sample("noise", dist.Uniform(-8, -5))
    kernel = jnp.exp(amp) * jnp.exp(
        -0.5 * ((x[:, None] - x[None, :]) / jnp.exp(scale)) ** 2
    )
    kernel = kernel + jnp.exp(noise) * jnp.eye(len(x))
    numpyro.sample("y", dist.MultivariateNormal(jnp.zeros(len(x)), kernel), obs=y)


def sync_pytree(tree):
    return jax.tree.map(lambda value: value.block_until_ready(), tree)


def timed_run(mcmc, rng_key, x, y, init_params=None):
    start = time.perf_counter()
    mcmc.run(rng_key, x, y=y, init_params=init_params)
    sync_pytree(mcmc.get_samples(group_by_chain=True))
    return time.perf_counter() - start


def main():
    key = jax.random.PRNGKey(0)
    x = jnp.linspace(0, 10, 100)
    y = jnp.sin(x) + 0.1 * jax.random.normal(key, (100,))

    warmup_steps = 100
    sample_steps = 100
    num_chains = 4

    kernel = NUTS(model)
    mcmc = MCMC(
        kernel,
        num_warmup=warmup_steps,
        num_samples=sample_steps,
        num_chains=num_chains,
        chain_method="vectorized",
        progress_bar=False,
    )

    warmup_s = timed_run(mcmc, jax.random.PRNGKey(1), x, y)
    init_params = {
        name: values[:, -1] for name, values in mcmc.get_samples(group_by_chain=True).items()
    }
    same_first_run_s = timed_run(mcmc, jax.random.PRNGKey(2), x, y)

    fresh_kernel = NUTS(model)
    fresh = MCMC(
        fresh_kernel,
        num_warmup=0,
        num_samples=sample_steps,
        num_chains=num_chains,
        chain_method="vectorized",
        progress_bar=False,
    )

    fresh_first_run_s = timed_run(fresh, jax.random.PRNGKey(3), x, y, init_params=init_params)

    mcmc.post_warmup_state = mcmc.last_state
    same_second_run_s = timed_run(mcmc, jax.random.PRNGKey(4), x, y)

    fresh.post_warmup_state = fresh.last_state
    fresh_second_run_s = timed_run(fresh, jax.random.PRNGKey(5), x, y, init_params=init_params)

    same_second_ratio = same_second_run_s / fresh_second_run_s if fresh_second_run_s else float("inf")
    same_first_ratio = same_first_run_s / fresh_first_run_s if fresh_first_run_s else float("inf")

    reproducible = same_second_ratio >= 2.0
    evidence = (
        f"backend={jax.default_backend()}, device={jax.devices()[0]}; "
        f"warmup={warmup_s:.3f}s; "
        f"first post-warmup run same_object={same_first_run_s:.3f}s vs fresh num_warmup=0={fresh_first_run_s:.3f}s "
        f"(ratio={same_first_ratio:.2f}x); "
        f"second batch same_object={same_second_run_s:.3f}s vs fresh num_warmup=0={fresh_second_run_s:.3f}s "
        f"(ratio={same_second_ratio:.2f}x)."
    )
    blocking_reason = (
        ""
        if reproducible
        else (
            "The reported slowdown did not reproduce here; the same-object path was "
            "roughly equal to or slightly faster than the fresh num_warmup=0 path."
        )
    )
    result = {
        "reproducible": reproducible,
        "evidence": evidence,
        "steps": [
            "Create the local venv and install JAX 0.9.0 CUDA 13 wheels plus the editable NumPyro checkout.",
            "Run the issue's GP-style NUTS benchmark with 4 vectorized chains on the local GPU.",
            "Compare a post-warmup run on the same MCMC object against a fresh num_warmup=0 restart.",
            "Repeat the comparison for a second steady-state batch after setting post_warmup_state.",
        ],
        "blocking_reason": blocking_reason,
        "reproduction_command": "bash run_repro.sh",
    }

    RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
