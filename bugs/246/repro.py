from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR / "codebase"))

import pyro
import pyro.distributions as dist
import torch
from pyro.infer.inspect import render_model


data = torch.tensor([1.0, 2.0, 3.0])


def deterministic_model(data):
    value = pyro.param("param", torch.tensor(0.0))
    with pyro.plate("plate", len(data)):
        pyro.deterministic("deterministic", data + value)


def probabilistic_model(data):
    value = pyro.param("param", torch.tensor(0.0))
    with pyro.plate("plate", len(data)):
        pyro.sample("probabilistic", dist.Normal(value, 1), obs=data)


det_graph = render_model(deterministic_model, model_args=(data,), render_params=True)
prob_graph = render_model(probabilistic_model, model_args=(data,), render_params=True)

print("deterministic graph:")
print(det_graph.source)
print("probabilistic graph:")
print(prob_graph.source)
print("deterministic contains param:", "param" in det_graph.source)
print("probabilistic contains param:", "param" in prob_graph.source)

assert "param" in prob_graph.source, "control case should render the parameter"
assert (
    "param" in det_graph.source
), "render_model(render_params=True) omits a parameter that feeds only deterministic sites"
