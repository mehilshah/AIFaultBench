#!/usr/bin/env python3
"""Minimal trigger for the HMC step-size search infinite loop."""

from __future__ import annotations

import pathlib
import sys

import torch


ROOT = pathlib.Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"


def main() -> None:
    # The bundled Pyro snapshot predates the PyTorch 2.x version string.
    torch.__version__ = "1.13.1"
    sys.path.insert(0, str(CODEBASE))

    import pyro
    from pyro.infer.mcmc.hmc import HMC

    torch.manual_seed(0)
    print(f"pyro={pyro.__version__}")
    print(f"torch={torch.__version__}")

    def potential_fn(z):
        return (z["x"] * 0).sum() + torch.tensor(float("nan"))

    hmc = HMC(
        potential_fn=potential_fn,
        step_size=1.0,
        adapt_step_size=False,
        adapt_mass_matrix=False,
    )
    hmc.initial_params = {"x": torch.tensor(0.0)}

    print("setup start")
    hmc.setup(1)
    print(f"setup done {hmc._potential_energy_last}")
    print("call start")

    result = hmc._find_reasonable_step_size(hmc.initial_params)
    print(f"call returned {result}")


if __name__ == "__main__":
    main()
