"""Helpers for loading the target module with minimal local stubs.

The system PyTorch install is broken in this environment, but the bug we need to
reproduce lives in a pure string repr method. We therefore stub only the pieces
of torch/torchvision that are required to import `timm/data/transforms.py`.
"""

from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path


def _install_stub_modules() -> None:
    if "torch" not in sys.modules:
        torch = types.ModuleType("torch")
        torch.float32 = "float32"
        torch.Tensor = type("Tensor", (), {})

        class _Module:
            def __init__(self, *args, **kwargs):
                pass

        nn = types.ModuleType("torch.nn")
        nn.Module = _Module
        torch.nn = nn
        torch.tensor = lambda *args, **kwargs: ("tensor", args, kwargs)
        sys.modules["torch"] = torch
        sys.modules["torch.nn"] = nn

    if "torchvision" not in sys.modules:
        torchvision = types.ModuleType("torchvision")
        torchvision.__path__ = []  # mark as package

        transforms = types.ModuleType("torchvision.transforms")

        class _ToTensor:
            pass

        transforms.ToTensor = _ToTensor

        functional = types.ModuleType("torchvision.transforms.functional")

        class _InterpolationMode:
            NEAREST = object()
            BILINEAR = object()
            BICUBIC = object()
            BOX = object()
            HAMMING = object()
            LANCZOS = object()

        functional.InterpolationMode = _InterpolationMode

        torchvision.transforms = transforms
        sys.modules["torchvision"] = torchvision
        sys.modules["torchvision.transforms"] = transforms
        sys.modules["torchvision.transforms.functional"] = functional


def load_transforms_module():
    """Load the local `timm.data.transforms` file under a private module name."""

    _install_stub_modules()
    repo_root = Path(__file__).resolve().parent
    transforms_path = repo_root / "codebase" / "timm" / "data" / "transforms.py"
    spec = importlib.util.spec_from_file_location("repro_timm_data_transforms", transforms_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {transforms_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module
