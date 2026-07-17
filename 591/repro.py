import pathlib
import traceback

import torch

ROOT = pathlib.Path(__file__).resolve().parent

import sys
sys.path.insert(0, str(ROOT / "codebase"))

import pyro
import pyro.distributions as dist
from pyro.infer import TraceEnum_ELBO, config_enumerate
from torch.distributions import constraints


def main():
    print("torch", torch.__version__)
    print("pyro", pyro.__version__)
    pyro.set_rng_seed(0)

    @config_enumerate
    def model():
        p = pyro.param("p", torch.randn(3, 3).exp(), constraint=constraints.simplex)
        x = pyro.sample("x", dist.Categorical(p[0]))
        y = pyro.sample("y", dist.Categorical(p[x]))
        z = pyro.sample("z", dist.Categorical(p[y]))
        print("model x.shape = {}".format(x.shape))
        print("model y.shape = {}".format(y.shape))
        print("model z.shape = {}".format(z.shape))
        return x, y, z

    def guide():
        pass

    pyro.clear_param_store()
    elbo = TraceEnum_ELBO(max_plate_nesting=0)
    print("loss=", elbo.loss(model, config_enumerate(guide, "sequential")))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        raise
