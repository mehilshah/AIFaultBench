#!/usr/bin/env python3
"""Minimal reproduction for the RoPE shape mismatch bug."""

from __future__ import annotations

import importlib.util
import sys
import traceback
import types
from pathlib import Path

import torch


ROOT = Path(__file__).resolve().parent
ROPE_PATH = ROOT / "codebase" / "labml_nn" / "transformers" / "rope" / "__init__.py"


def _install_import_stubs() -> None:
    """Stub unrelated imports so we can load the target module directly."""

    labml = types.ModuleType("labml")
    logger = types.ModuleType("labml.logger")
    logger.inspect = lambda *args, **kwargs: None
    labml.logger = logger

    labml_nn = types.ModuleType("labml_nn")
    transformers = types.ModuleType("labml_nn.transformers")
    mha = types.ModuleType("labml_nn.transformers.mha")

    class MultiHeadAttention(torch.nn.Module):
        pass

    mha.MultiHeadAttention = MultiHeadAttention
    transformers.mha = mha
    labml_nn.transformers = transformers

    sys.modules["labml"] = labml
    sys.modules["labml.logger"] = logger
    sys.modules["labml_nn"] = labml_nn
    sys.modules["labml_nn.transformers"] = transformers
    sys.modules["labml_nn.transformers.mha"] = mha


def load_rope_module():
    _install_import_stubs()
    spec = importlib.util.spec_from_file_location("rope_module", ROPE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {ROPE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    module = load_rope_module()

    x = torch.tensor(
        [[1, 2, 3, 4], [4, 5, 6, 7], [7, 8, 9, 10]],
        dtype=torch.float,
    )[:, None, None, :]

    rope = module.RotaryPositionalEmbeddings(3)

    print(f"module_path={ROPE_PATH}")
    print(f"input_shape={tuple(x.shape)}")
    print(f"rope_features={rope.d}")

    try:
        rope(x)
    except Exception as exc:  # noqa: BLE001 - we want the exact runtime failure
        print(f"reproduced_exception={type(exc).__name__}")
        print(f"reproduced_message={exc}")
        traceback.print_exc()
        return 0

    print("BUG_NOT_REPRODUCED")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
