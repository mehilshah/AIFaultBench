import jax.numpy as jnp
import jax.random as random

import numpyro
import numpyro.distributions as dist
from numpyro.handlers import block, seed
from numpyro.infer import SVI, TraceEnum_ELBO, autoguide


def model(data):
    weights = numpyro.sample("weights", dist.Dirichlet(0.5 * jnp.ones(K)))
    scale = numpyro.sample("scale", dist.LogNormal(0.0, 2.0))

    with numpyro.plate("components", K):
        locs = numpyro.sample("locs", dist.Normal(0.0, 10.0))

    with numpyro.plate("data", len(data)):
        assignment = numpyro.sample(
            "assignment",
            dist.Categorical(weights),
            infer={"enumerate": "parallel"},
        )
        numpyro.sample("obs", dist.Normal(locs[assignment], scale), obs=data)


def run_guide(guide_cls, data, label):
    print(f"running {label}")
    guide = guide_cls(block(seed(model, rng_seed=0), hide=["assignment"]))
    svi = SVI(model, guide, numpyro.optim.Adam(0.003), TraceEnum_ELBO())
    svi.run(random.PRNGKey(0), 1, data)
    print(f"{label} completed")


K = 2
DATA = jnp.array([0.0, 1.0, 10.0, 11.0, 12.0])


def main():
    import jax

    print(f"numpyro={numpyro.__version__}")
    print(f"jax={jax.__version__}")
    run_guide(autoguide.AutoNormal, DATA, "AutoNormal")
    run_guide(autoguide.AutoDiagonalNormal, DATA, "AutoDiagonalNormal")


if __name__ == "__main__":
    main()
