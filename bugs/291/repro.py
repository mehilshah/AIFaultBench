#!/usr/bin/env python3
"""Minimal reproducer for the BitMasks single-index shape assertion."""

import os
import sys
import types
import importlib.util

import torch


ROOT = os.path.dirname(os.path.abspath(__file__))
CODEBASE = os.path.join(ROOT, "codebase")
if CODEBASE not in sys.path:
    sys.path.insert(0, CODEBASE)


def _install_stub_modules() -> None:
    """Provide the small import surface this repro needs."""
    if "fvcore" not in sys.modules:
        fvcore = types.ModuleType("fvcore")
        fvcore.__version__ = "0.1.5"
        sys.modules["fvcore"] = fvcore

    if "yaml" not in sys.modules:
        yaml = types.ModuleType("yaml")
        yaml.__version__ = "6.0"
        sys.modules["yaml"] = yaml

    if "pycocotools" not in sys.modules:
        pycocotools = types.ModuleType("pycocotools")
        sys.modules["pycocotools"] = pycocotools
    else:
        pycocotools = sys.modules["pycocotools"]

    if "pycocotools.mask" not in sys.modules:
        mask = types.ModuleType("pycocotools.mask")

        def _unused(*args, **kwargs):
            raise RuntimeError("pycocotools.mask stub should not be called")

        mask.frPyObjects = _unused
        mask.merge = _unused
        mask.decode = _unused
        sys.modules["pycocotools.mask"] = mask
        pycocotools.mask = mask

    if "torchvision" not in sys.modules:
        torchvision = types.ModuleType("torchvision")
        torchvision.__version__ = "0.8.0"
        sys.modules["torchvision"] = torchvision
    else:
        torchvision = sys.modules["torchvision"]

    if "torchvision.ops" not in sys.modules:
        ops = types.ModuleType("torchvision.ops")

        def roi_align(*args, **kwargs):
            raise RuntimeError("torchvision.ops.roi_align stub should not be called")

        ops.roi_align = roi_align
        sys.modules["torchvision.ops"] = ops
        torchvision.ops = ops


def _install_detectron2_packages() -> None:
    """Create lightweight package shells so we can load the target modules directly."""
    package_roots = {
        "detectron2": os.path.join(CODEBASE, "detectron2"),
        "detectron2.structures": os.path.join(CODEBASE, "detectron2", "structures"),
        "detectron2.layers": os.path.join(CODEBASE, "detectron2", "layers"),
        "detectron2.utils": os.path.join(CODEBASE, "detectron2", "utils"),
    }

    for name, path in package_roots.items():
        package = sys.modules.get(name)
        if package is None:
            package = types.ModuleType(name)
            sys.modules[name] = package
        package.__path__ = [path]

    sys.modules["detectron2"].structures = sys.modules["detectron2.structures"]
    sys.modules["detectron2"].layers = sys.modules["detectron2.layers"]
    sys.modules["detectron2"].utils = sys.modules["detectron2.utils"]


def _load_module(module_name: str, file_path: str):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main() -> None:
    _install_stub_modules()
    _install_detectron2_packages()

    _load_module(
        "detectron2.utils.memory",
        os.path.join(CODEBASE, "detectron2", "utils", "memory.py"),
    )
    _load_module(
        "detectron2.layers.roi_align",
        os.path.join(CODEBASE, "detectron2", "layers", "roi_align.py"),
    )
    _load_module(
        "detectron2.structures.boxes",
        os.path.join(CODEBASE, "detectron2", "structures", "boxes.py"),
    )
    masks_module = _load_module(
        "detectron2.structures.masks",
        os.path.join(CODEBASE, "detectron2", "structures", "masks.py"),
    )
    BitMasks = masks_module.BitMasks

    masks = BitMasks(torch.ones(10, 256, 256))
    print(f"Created BitMasks with tensor shape: {tuple(masks.tensor.shape)}")
    print("Indexing masks[4] now triggers the bug...")
    masks[4]


if __name__ == "__main__":
    main()
