#!/usr/bin/env python3
import funsor
import jax.numpy as jnp
from jax import random

import numpyro
from numpyro import handlers
from numpyro.contrib.control_flow import scan
from numpyro.contrib.funsor import config_enumerate, infer_discrete
import numpyro.distributions as dist


funsor.set_backend("jax")


def hmm(data, hidden_dim=10):
    transition = 0.3 / hidden_dim + 0.7 * jnp.eye(hidden_dim)
    means = jnp.arange(float(hidden_dim))

    def transition_fn(state, y):
        state = numpyro.sample("states", dist.Categorical(transition[state]))
        y = numpyro.sample("obs", dist.Normal(means[state], 1.0), obs=y)
        return state, (state, y)

    _, (states, data) = scan(transition_fn, 0, data, length=2)
    return [0] + [s for s in states], data


def main():
    _, data = handlers.seed(hmm, 0)(None)
    decoder = infer_discrete(
        config_enumerate(hmm), temperature=0, rng_key=random.PRNGKey(1)
    )
    decoder(data)


if __name__ == "__main__":
    main()
