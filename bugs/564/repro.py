import sys
import types

import jax
import jax.experimental.pjit as pjit
import jax.interpreters.pxla as pxla
import jax.core as core
import jax.sharding as sharding
import jax.numpy as jnp

if not hasattr(pjit, "pjit_p"):
    pjit.pjit_p = object()
if not hasattr(pxla, "xla_pmap_p"):
    pxla.xla_pmap_p = object()
if not hasattr(sharding, "AbstractMesh"):
    sharding.AbstractMesh = type("AbstractMesh", (), {})
if not hasattr(core, "get_opaque_trace_state"):
    from jax.extend.core import get_opaque_trace_state

    core.get_opaque_trace_state = get_opaque_trace_state

if "jax.util" not in sys.modules:
    util_mod = types.ModuleType("jax.util")

    def safe_map(f, *args):
        return list(map(f, *args))

    util_mod.safe_map = safe_map
    sys.modules["jax.util"] = util_mod

from flax import nnx

import numpyro
import numpyro.distributions as dist
from numpyro.contrib.module import random_nnx_module
from numpyro import handlers


class MLP(nnx.Module):
    def __init__(self, din, dout, hidden_layers, *, rngs):
        self.activation = jax.nn.relu
        self.layers = []

        layer_dims = [din] + list(hidden_layers) + [dout]
        for in_dim, out_dim in zip(layer_dims[:-1], layer_dims[1:]):
            self.layers.append(nnx.Linear(in_dim, out_dim, rngs=rngs))

    def __call__(self, x):
        for layer in self.layers[:-1]:
            x = self.activation(layer(x))
        return self.layers[-1](x)


def prior(name, shape):
    del name, shape
    return dist.Normal()


def model():
    module = MLP(2, 1, hidden_layers=[8, 8], rngs=nnx.Rngs(0))
    nn = random_nnx_module("nn", module, prior)
    x = jnp.ones((3, 2))
    y = nn(x).squeeze(-1)
    numpyro.sample("obs", dist.Normal(y, 1.0))


if __name__ == "__main__":
    with handlers.trace() as tr, handlers.seed(rng_seed=0):
        model()
    print("trace_keys", sorted(tr.keys()))
