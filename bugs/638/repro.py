#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import pathlib
import sys
import types

import torch


ROOT = pathlib.Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
MODULE_PATH = CODEBASE / "deepspeed" / "ops" / "adam" / "zenflow_torch_adam.py"


def load_zenflow_module():
    """Load the optimizer module without importing the full DeepSpeed package."""
    deepspeed_mod = types.ModuleType("deepspeed")
    utils_mod = types.ModuleType("deepspeed.utils")
    torch_utils_mod = types.ModuleType("deepspeed.utils.torch")
    torch_utils_mod.required_torch_version = lambda min_version=None, max_version=None: True
    utils_mod.torch = torch_utils_mod
    deepspeed_mod.utils = utils_mod

    sys.modules["deepspeed"] = deepspeed_mod
    sys.modules["deepspeed.utils"] = utils_mod
    sys.modules["deepspeed.utils.torch"] = torch_utils_mod

    spec = importlib.util.spec_from_file_location("zenflow_torch_adam", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec from {MODULE_PATH}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def build_corrupted_param():
    """Create a parameter with the corrupted internal state from the report."""
    param = torch.nn.Parameter(torch.randn(2, 4))
    param.ds_shape = (3072, 1024)
    param.ds_tensor = torch.tensor(0.0)
    param.complete_column_offset = 0
    param.complete_numel = param.numel()
    param.group_id = 0
    param.selected_indices = torch.tensor([0, 1], dtype=torch.long)
    param.selected_grad = torch.randn(2, 2)
    return param


def main() -> None:
    module = load_zenflow_module()
    param = build_corrupted_param()

    print(f"param.ds_shape={param.ds_shape}")
    print(f"param.ds_tensor.shape={tuple(param.ds_tensor.shape)}")

    optimizer = module.ZenFlowSelectiveAdamW_stage3([param], lr=1e-3, offload=False)
    optimizer.group_step([param])


if __name__ == "__main__":
    main()
