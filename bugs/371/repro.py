from jax import numpy as jnp

from numpyro import distributions as dist
from numpyro import render_model, sample


def batched_uniform_model():
    mixture = dist.Mixture(
        dist.Categorical(probs=jnp.array([1 / 3, 2 / 3])),
        dist.Uniform(
            low=jnp.array([-1.0, 0.0]),
            high=jnp.array([0.0, 1.0]),
        ),
    )
    theta = sample("theta", mixture)
    print(theta.shape)
    return theta


def list_uniform_model():
    mixture = dist.Mixture(
        dist.Categorical(probs=jnp.array([1 / 3, 2 / 3])),
        [dist.Uniform(low=-1.0, high=0.0), dist.Uniform(low=0.0, high=1.0)],
    )
    theta = sample("theta", mixture)
    print(theta.shape)
    return theta


def main():
    render_model(batched_uniform_model)
    render_model(list_uniform_model)


if __name__ == "__main__":
    main()
