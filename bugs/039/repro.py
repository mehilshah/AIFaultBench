#!/usr/bin/env python3
"""Minimal reproduction for the RoPE shape mismatch bug."""

from __future__ import annotations

import importlib.util
import pathlib
import sys
import traceback
import types

import torch


ROOT = pathlib.Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"


def ensure_package(name: str, path: pathlib.Path | None = None) -> types.ModuleType:
    module = types.ModuleType(name)
    module.__path__ = [] if path is None else [str(path)]
    sys.modules[name] = module
    return module


def ensure_stub_labml() -> None:
    labml = ensure_package("labml")
    logger = types.ModuleType("labml.logger")
    tracker = types.ModuleType("labml.tracker")

    def inspect(*args, **kwargs):
        print(*args, **kwargs)

    def debug(*args, **kwargs):
        return None

    logger.inspect = inspect
    tracker.debug = debug
    labml.logger = logger
    labml.tracker = tracker
    sys.modules["labml.logger"] = logger
    sys.modules["labml.tracker"] = tracker


def load_module(module_name: str, file_path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {module_name} from {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    ensure_stub_labml()
    ensure_package("labml_nn", CODEBASE / "labml_nn")
    ensure_package("labml_nn.transformers", CODEBASE / "labml_nn" / "transformers")

    load_module("labml_nn.transformers.mha", CODEBASE / "labml_nn" / "transformers" / "mha.py")
    rope = load_module(
        "labml_nn.transformers.rope",
        CODEBASE / "labml_nn" / "transformers" / "rope" / "__init__.py",
    )

    RotaryPositionalEmbeddings = rope.RotaryPositionalEmbeddings
    x = torch.tensor([[1, 2, 3, 4], [4, 5, 6, 7], [7, 8, 9, 10]], dtype=torch.float32)
    x = x[:, None, None, :]

    print(f"input_shape={tuple(x.shape)}")
    print("rope_dim=3")

    try:
        RotaryPositionalEmbeddings(3)(x)
    except RuntimeError as exc:
        print(f"exception={exc}")
        print("reproduced: RuntimeError from RoPE cache broadcasting")
        traceback.print_exc()
        return 1

    print("no error raised")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
