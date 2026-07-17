from jax import random

import numpyro
from numpyro import optim
import numpyro.distributions as dist
from numpyro.infer import SVI, Trace_ELBO
from numpyro.primitives import mutable as numpyro_mutable


def model():
    x = numpyro.sample("x", dist.Normal(-1, 1))
    numpyro_mutable("x1p", x + 1)


def guide():
    loc = numpyro.param("loc", 0.0)
    p = numpyro_mutable("loc1p", {"value": None})
    p["value"] = loc + 2
    numpyro.sample("x", dist.Normal(loc, 0.1))


if __name__ == "__main__":
    svi = SVI(model, guide, optim.Adam(0.1), Trace_ELBO())
    svi.run(random.PRNGKey(0), 1, progress_bar=False)
