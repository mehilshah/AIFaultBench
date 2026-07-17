#!/usr/bin/env python3
"""Reproducer for the reported GBM/Hummingbird CUDA device mismatch.

The issue report describes a failure during GBM regression on GPU. In this
checkout, the closest code path is GBM TorchScript conversion on CUDA. The
script below exercises that path directly:

1. Load the Auto MPG dataset used in the bug report.
2. Train a tiny LightGBM regressor on the seven GBM inputs.
3. Attach the fitted model to Ludwig's GBM wrapper.
4. Convert the GBM model to TorchScript on CUDA.

If the reported bug is present, the TorchScript conversion should fail with a
CPU/CUDA tensor mismatch inside Hummingbird. In this environment, the
conversion completes successfully.
"""

from __future__ import annotations

import importlib.machinery
import sys
import types


def _stub_optional_torchtext() -> None:
    """Stub `torchtext` so Ludwig imports do not hit the broken wheel in this env."""
    torchtext = types.ModuleType("torchtext")
    torchtext.__spec__ = importlib.machinery.ModuleSpec("torchtext", loader=None)
    torchtext.__path__ = []
    torchtext.__version__ = "0.0"
    sys.modules["torchtext"] = torchtext

    for submodule in ["datasets", "data", "utils", "vocab"]:
        module_name = f"torchtext.{submodule}"
        module = types.ModuleType(module_name)
        module.__spec__ = importlib.machinery.ModuleSpec(module_name, loader=None)
        module.__path__ = []
        sys.modules[module_name] = module


def main() -> None:
    _stub_optional_torchtext()

    import pandas as pd
    import lightgbm as lgb
    import torch

    from ludwig.models.gbm import GBM
    from ludwig.schema.model_config import ModelConfig

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required for this repro.")

    url = "http://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data"
    column_names = [
        "MPG",
        "Cylinders",
        "Displacement",
        "Horsepower",
        "Weight",
        "Acceleration",
        "Model Year",
        "Origin",
    ]

    df = pd.read_csv(
        url,
        names=column_names,
        na_values="?",
        comment="\t",
        sep=" ",
        skipinitialspace=True,
    ).dropna()

    inputs = df[[
        "Cylinders",
        "Displacement",
        "Horsepower",
        "Weight",
        "Acceleration",
        "Model Year",
        "Origin",
    ]].copy()
    inputs["Origin"] = inputs["Origin"].astype("category").cat.codes.astype("float32")
    targets = df["MPG"].astype("float32")

    config = ModelConfig.from_dict(
        {
            "model_type": "gbm",
            "input_features": [
                {"name": "Cylinders", "type": "number"},
                {"name": "Displacement", "type": "number"},
                {"name": "Horsepower", "type": "number"},
                {"name": "Weight", "type": "number"},
                {"name": "Acceleration", "type": "number"},
                {"name": "Model Year", "type": "number"},
                {"name": "Origin", "type": "category"},
            ],
            "output_features": [
                {
                    "name": "MPG",
                    "type": "number",
                    "optimizer": {"type": "mean_squared_error"},
                }
            ],
        }
    )

    model = GBM(config)
    booster = lgb.LGBMRegressor(n_estimators=2, learning_rate=0.1, random_state=0)
    booster.fit(inputs, targets)
    model.lgbm_model = booster

    print("CUDA available:", torch.cuda.is_available())
    with model.compile():
        torchscript_model = model.to_torchscript(device="cuda")

    print("TorchScript conversion succeeded:", type(torchscript_model).__name__)


if __name__ == "__main__":
    main()
