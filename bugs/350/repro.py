#!/usr/bin/env python3
"""Reproduce the functorch incompatibility in DeepSpeed ZeRO-3 linear."""

from __future__ import annotations

import importlib.util
import json
import sys
import types
from pathlib import Path

import torch


ROOT = Path(__file__).resolve().parent
LINEAR_PATH = ROOT / "codebase" / "deepspeed" / "runtime" / "zero" / "linear.py"


def install_minimal_deepspeed_shims() -> None:
    ds_pkg = types.ModuleType("deepspeed")
    ds_pkg.__path__ = []  # mark as package

    comm_mod = types.ModuleType("deepspeed.comm")
    comm_mod.get_rank = lambda: 0

    accel_mod = types.ModuleType("deepspeed.accelerator")

    class DummyAccelerator:
        def device_name(self) -> str:
            return "cpu"

    accel_mod.get_accelerator = lambda: DummyAccelerator()

    ds_pkg.comm = comm_mod
    sys.modules["deepspeed"] = ds_pkg
    sys.modules["deepspeed.comm"] = comm_mod
    sys.modules["deepspeed.accelerator"] = accel_mod


def load_linear_module():
    install_minimal_deepspeed_shims()
    spec = importlib.util.spec_from_file_location("ds_zero_linear", LINEAR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {LINEAR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    module = load_linear_module()
    x = torch.randn(2, 3)
    w = torch.randn(4, 3)
    b = torch.randn(4)

    def loss_fn(input_tensor, weight, bias):
        return module.zero3_linear_wrap(input_tensor, weight, bias).sum()

    payload = {
        "torch_version": torch.__version__,
        "linear_module": str(LINEAR_PATH),
        "target": "LinearFunctionForZeroStage3.apply under torch.func.grad_and_value",
    }

    try:
        grad_fn = torch.func.grad_and_value(loss_fn)
        grad_fn(x, w, b)
    except RuntimeError as exc:
        payload["reproducible"] = "setup_context staticmethod" in str(exc)
        payload["exception_type"] = type(exc).__name__
        payload["exception"] = str(exc)
        print(json.dumps(payload, indent=2, sort_keys=True))
        if payload["reproducible"]:
            print("BUG REPRODUCED")
            return 1
        print("Unexpected RuntimeError that does not match the reported bug.")
        return 2

    payload["reproducible"] = False
    payload["exception_type"] = None
    payload["exception"] = None
    print(json.dumps(payload, indent=2, sort_keys=True))
    print("BUG NOT REPRODUCED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
