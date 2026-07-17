#!/usr/bin/env python3
"""Load local POT modules from codebase/ without importing the package root.

This avoids the compiled extension import path in ``ot.__init__`` and keeps the
repro focused on ``ot.unbalanced.sinkhorn_knopp_unbalanced``.
"""

from __future__ import annotations

import importlib.util
import os
import sys
import types
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OT_ROOT = ROOT / "codebase" / "ot"


def _load_module(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {module_name} from {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def load_local_sinkhorn_knopp_unbalanced():
    """Return the local ``sinkhorn_knopp_unbalanced`` function."""

    ot_pkg = types.ModuleType("ot")
    ot_pkg.__path__ = [str(OT_ROOT)]
    sys.modules["ot"] = ot_pkg

    unbalanced_pkg = types.ModuleType("ot.unbalanced")
    unbalanced_pkg.__path__ = [str(OT_ROOT / "unbalanced")]
    sys.modules["ot.unbalanced"] = unbalanced_pkg

    _load_module("ot.backend", OT_ROOT / "backend.py")
    _load_module("ot.utils", OT_ROOT / "utils.py")
    sinkhorn_mod = _load_module("ot.unbalanced._sinkhorn", OT_ROOT / "unbalanced" / "_sinkhorn.py")
    return sinkhorn_mod.sinkhorn_knopp_unbalanced
