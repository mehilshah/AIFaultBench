import traceback

import jax
import jax.numpy as jnp
import numpyro
import numpyro.distributions as dist
from numpyro.infer import AIES, MCMC


def model(mu, sigma):
    with numpyro.plate("n_dim", mu.shape[0]):
        numpyro.sample("x", dist.Normal(mu, sigma))


def main():
    n_dim, num_chains = 5, 100
    mu, sigma = jnp.zeros(n_dim), jnp.ones(n_dim)

    kernel = AIES(
        model,
        moves={AIES.DEMove(): 0.5, AIES.StretchMove(): 0.5},
    )
    mcmc = MCMC(
        kernel,
        num_warmup=20,
        num_samples=10,
        num_chains=num_chains,
        chain_method="vectorized",
        progress_bar=False,
    )

    print(f"jax={jax.__version__}")
    print(f"numpyro={numpyro.__version__}")
    print(f"num_chains={num_chains}")

    mcmc.warmup(jax.random.PRNGKey(0), mu, sigma)
    print("warmup_ok=True")
    print(f"warmup_state_rng_shape={mcmc.post_warmup_state.rng_key.shape}")

    try:
        mcmc.run(jax.random.PRNGKey(1), mu, sigma)
    except Exception as exc:  # noqa: BLE001 - this is a repro harness
        print(f"run_failed={type(exc).__name__}: {exc}")
        traceback.print_exc()
        raise

    print("run_ok=True")
    print(f"samples_shape={mcmc.get_samples(group_by_chain=True)['x'].shape}")


if __name__ == "__main__":
    main()
