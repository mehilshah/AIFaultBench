import jax
import jax.numpy as jnp

import numpyro
import numpyro.distributions as dist
from numpyro import infer


def model():
    numpyro.sample(
        "z",
        dist.Categorical(jnp.array([0.4, 0.6])),
        infer={"enumerate": "parallel"},
    )


def guide():
    numpyro.sample("aux", dist.Normal(0.0, 1.0), infer={"is_auxiliary": True})
    numpyro.sample("z", dist.Categorical(jnp.array([0.5, 0.5])))


if __name__ == "__main__":
    print("jax", jax.__version__, flush=True)
    print("running TraceEnum_ELBO.loss with an auxiliary guide site", flush=True)
    loss = infer.TraceEnum_ELBO().loss(jax.random.PRNGKey(0), {}, model, guide)
    print("loss", loss, flush=True)

