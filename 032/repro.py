#!/usr/bin/env python3
"""Minimal reproduction for the BERT GELU type mismatch."""

from __future__ import annotations

import importlib.util
import pathlib
import sys
import traceback

import torch


ROOT = pathlib.Path(__file__).resolve().parent
BERT_MODELING = ROOT / "codebase" / "PyTorch" / "LanguageModeling" / "BERT" / "modeling.py"


def load_modeling_module():
    spec = importlib.util.spec_from_file_location("bert_modeling", BERT_MODELING)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module from {BERT_MODELING}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    x = torch.tensor([1.0])
    module = load_modeling_module()
    try:
        module.gelu(x)
    except Exception as exc:
        print(f"exception_type={type(exc).__name__}")
        print(f"exception_message={exc}")
        traceback.print_exc()
        return 1

    print("No exception raised.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
