#!/usr/bin/env python3
"""Minimal reproduction for Detectron2 MapDataset __new__ bug."""

from __future__ import annotations

import os
import sys
import types
from pathlib import Path


def _install_namespace_package(name: str, path: Path) -> None:
    module = sys.modules.get(name)
    if module is None:
        module = types.ModuleType(name)
        module.__path__ = [str(path)]
        sys.modules[name] = module


def main() -> None:
    root = Path(__file__).resolve().parent
    codebase = root / "codebase"

    # Avoid importing detectron2/__init__.py, which is unrelated to this bug.
    _install_namespace_package("detectron2", codebase / "detectron2")
    _install_namespace_package("detectron2.data", codebase / "detectron2" / "data")
    _install_namespace_package("detectron2.utils", codebase / "detectron2" / "utils")

    sys.path.insert(0, str(codebase))

    from detectron2.data.common import MapDataset

    dataset = [{"x": 1}]
    map_func = lambda x: x

    print("Constructing MapDataset over a list-backed dataset...")
    MapDataset(dataset, map_func)


if __name__ == "__main__":
    main()
