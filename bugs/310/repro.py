#!/usr/bin/env python3
import math
import os
import sys


ROOT = os.path.dirname(os.path.abspath(__file__))
CODEBASE = os.path.join(ROOT, "codebase")
if CODEBASE not in sys.path:
    sys.path.insert(0, CODEBASE)

import pyro
import pyro.distributions as dist
import torch
from pyro.infer import SVI, Trace_ELBO, autoguide
from pyro.nn.module import PyroModule, PyroModuleList


class BNN(PyroModule):
    def __init__(
        self,
        input_size: int,
        hidden_layer_sizes,
        output_size: int,
        use_new_module_list_type: bool,
    ):
        super().__init__()

        layer_sizes = (
            [(input_size, hidden_layer_sizes[0])]
            + list(zip(hidden_layer_sizes[:-1], hidden_layer_sizes[1:]))
            + [(hidden_layer_sizes[-1], output_size)]
        )
        layers = [
            pyro.nn.module.PyroModule[torch.nn.Linear](in_size, out_size)
            for in_size, out_size in layer_sizes
        ]
        if use_new_module_list_type:
            self.layers = PyroModuleList(layers)
        else:
            self.layers = pyro.nn.module.PyroModule[torch.nn.ModuleList](layers)

        for layer_idx, layer in enumerate(self.layers):
            layer.weight = pyro.nn.module.PyroSample(
                dist.Normal(0.0, 5.0 * math.sqrt(2 / layer_sizes[layer_idx][0]))
                .expand([layer_sizes[layer_idx][1], layer_sizes[layer_idx][0]])
                .to_event(2)
            )
            layer.bias = pyro.nn.module.PyroSample(
                dist.Normal(0.0, 5.0).expand([layer_sizes[layer_idx][1]]).to_event(1)
            )

        self.activation = torch.nn.Tanh()
        self.output_size = output_size

    def forward(self, x: torch.Tensor, obs=None) -> torch.Tensor:
        mean = self.layers[-1](x)
        if obs is not None:
            with pyro.plate("data", x.shape[0]):
                pyro.sample(
                    "obs", dist.Normal(mean, 0.1).to_event(self.output_size), obs=obs
                )
        return mean


class SliceIndexingModuleListBNN(BNN):
    def forward(self, x: torch.Tensor, obs=None) -> torch.Tensor:
        for layer in self.layers[:-1]:
            x = layer(x)
            x = self.activation(x)
        return super().forward(x, obs=obs)


class NestedBNN(PyroModule):
    def __init__(self, bnns, use_new_module_list_type: bool):
        super().__init__()
        if use_new_module_list_type:
            self.bnns = PyroModuleList(bnns)
        else:
            self.bnns = pyro.nn.module.PyroModule[torch.nn.ModuleList](bnns)

    def forward(self, x: torch.Tensor, obs=None) -> torch.Tensor:
        mean = sum(bnn(x) for bnn in self.bnns) / len(self.bnns)
        with pyro.plate("data", x.shape[0]):
            pyro.sample("obs", dist.Normal(mean, 0.1).to_event(1), obs=obs)
        return mean


def main():
    pyro.clear_param_store()
    pyro.set_rng_seed(123)

    print(
        "module_list_alias_is_fix=",
        pyro.nn.module.PyroModule[torch.nn.ModuleList] is pyro.nn.PyroModuleList,
    )

    x = torch.linspace(0, 1, 20).reshape((-1, 1))
    y = torch.sin(2 * math.pi * x) + torch.randn(x.size()) * 0.1

    model = NestedBNN(
        [SliceIndexingModuleListBNN(1, [3, 3, 3], 1, False) for _ in range(2)],
        use_new_module_list_type=False,
    )
    guide = autoguide.AutoDiagonalNormal(model)
    svi = SVI(model, guide, pyro.optim.Adam({"lr": 0.03}), loss=Trace_ELBO())

    loss = svi.step(x, y)
    print(f"svi_loss={loss:.6f}")
    print("BUG_NOT_REPRODUCED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
