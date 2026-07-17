#!/usr/bin/env python3
"""Minimal reproduction for the missing `pyro.poutine.equalize` API."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))

import pyro  # noqa: E402
import torch  # noqa: E402


def per_category_model(category):
    shift = pyro.param(f"{category}_shift", torch.randn(1))
    mean = pyro.sample(f"{category}_mean", pyro.distributions.Normal(0, 1))
    std = pyro.sample(f"{category}_std", pyro.distributions.LogNormal(0, 1))
    with pyro.plate(f"{category}_num_samples", 5):
        return pyro.sample(f"{category}_values", pyro.distributions.Normal(mean + shift, std))


def model(categories):
    return {category: per_category_model(category) for category in categories}


def main():
    categories = ["dogs", "cats"]
    pyro.set_rng_seed(20240613)
    pyro.clear_param_store()

    print(f"pyro version: {pyro.__version__}")
    print(f"has pyro.poutine.equalize: {hasattr(pyro.poutine, 'equalize')}")
    print("attempting to call pyro.poutine.equalize(...)")

    # This line is expected to fail in the current checkout.
    equal_std_model = pyro.poutine.equalize(model, ["dogs_std", "cats_std"])
    equal_std_model(categories)


if __name__ == "__main__":
    main()
