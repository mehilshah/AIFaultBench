import jax
import jax.random as random

import numpyro
import numpyro.distributions as dist
from numpyro.handlers import block, seed
from numpyro.infer import SVI, TraceEnum_ELBO
from numpyro.infer.autoguide import AutoDelta


def model():
    a = numpyro.sample("a", dist.Normal(0, 1))
    numpyro.sample("b", dist.Normal(0, 1))


def model_w_deterministic():
    a = numpyro.sample("a", dist.Normal(0, 1))
    numpyro.sample("b", dist.Normal(0, 1))
    numpyro.deterministic("test", a)


def main():
    print(f"jax={jax.__version__}")
    print(f"numpyro={numpyro.__version__}")

    keys = random.split(random.PRNGKey(0), 2)
    optimizer = numpyro.optim.Adam(step_size=0.01)

    baseline_guide = AutoDelta(block(seed(model, rng_seed=0), hide=["b"]))
    baseline_svi = SVI(model, baseline_guide, optimizer, loss=TraceEnum_ELBO())
    print("baseline_init_start")
    baseline_state = jax.vmap(baseline_svi.init)(keys)
    print("baseline_init_ok")
    print(baseline_state)

    failing_guide = AutoDelta(
        block(seed(model_w_deterministic, rng_seed=0), hide=["b"])
    )
    failing_svi = SVI(model_w_deterministic, failing_guide, optimizer, loss=TraceEnum_ELBO())
    print("deterministic_init_start")
    failing_state = jax.vmap(failing_svi.init)(keys)
    print("deterministic_init_ok")
    print(failing_state)


if __name__ == "__main__":
    main()
