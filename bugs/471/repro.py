#!/usr/bin/env python3
"""Reproduce the RandomCrop __repr__ failure from detectron2."""

from __future__ import annotations

import importlib.util
import sys
import traceback
import types
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
SOURCE_ROOT = ROOT / "codebase" / "detectron2" / "data" / "transforms"
SUPPORT_ROOT = ROOT / "support"


def ensure_compatibility_shims() -> None:
    # Old detectron2 code expects Image.LINEAR, which modern Pillow removed.
    if not hasattr(Image, "LINEAR"):
        Image.LINEAR = Image.BILINEAR

    # The buggy code imports fvcore.transforms.transform; the local stub avoids
    # pulling in torch and other heavyweight dependencies that are irrelevant
    # to the repr bug.
    sys.path.insert(0, str(SUPPORT_ROOT))


def ensure_detectron2_package_stubs() -> None:
    for name in ["detectron2", "detectron2.data", "detectron2.data.transforms"]:
        module = sys.modules.get(name)
        if module is None:
            module = types.ModuleType(name)
            module.__path__ = []
            sys.modules[name] = module


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main() -> int:
    ensure_compatibility_shims()
    ensure_detectron2_package_stubs()

    print(f"python={sys.version.split()[0]}")
    print(f"source={SOURCE_ROOT}")

    load_module("detectron2.data.transforms.transform", SOURCE_ROOT / "transform.py")
    transform_gen = load_module(
        "detectron2.data.transforms.transform_gen", SOURCE_ROOT / "transform_gen.py"
    )

    crop = transform_gen.RandomCrop("relative", (100, 100))
    print(f"constructed={crop.__class__.__name__}")
    print("repr_attempt=begin")
    try:
        print(str(crop))
    except Exception:
        traceback.print_exc()
        return 1

    print("repr_attempt=unexpected-success")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
