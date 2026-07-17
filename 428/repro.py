#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import pathlib
import sys
import types

import numpy as np


ROOT = pathlib.Path(__file__).resolve().parent / "codebase"


def install_stubs() -> None:
    """Stub out runtime pieces that are irrelevant to the bug."""

    fake_torch = types.ModuleType("torch")

    class Tensor:  # Minimal placeholder for isinstance checks and annotations.
        pass

    class device:
        def __init__(self, name: str):
            self.type = str(name)

        def __repr__(self) -> str:
            return f"device({self.type!r})"

    fake_torch.Tensor = Tensor
    fake_torch.BoolTensor = Tensor
    fake_torch.device = device
    fake_torch.int32 = "int32"
    fake_torch.int64 = "int64"
    fake_torch.float32 = "float32"
    fake_torch.float64 = "float64"
    sys.modules["torch"] = fake_torch

    pycocotools = types.ModuleType("pycocotools")
    mask = types.ModuleType("pycocotools.mask")
    mask.frPyObjects = lambda *args, **kwargs: None
    mask.merge = lambda *args, **kwargs: None
    mask.decode = lambda *args, **kwargs: np.zeros((1, 1), dtype=np.uint8)
    pycocotools.mask = mask
    sys.modules["pycocotools"] = pycocotools
    sys.modules["pycocotools.mask"] = mask

    detectron2 = types.ModuleType("detectron2")
    detectron2.__path__ = [str(ROOT / "detectron2")]
    sys.modules["detectron2"] = detectron2

    layers = types.ModuleType("detectron2.layers")
    layers.cat = lambda tensors, dim=0: tensors
    sys.modules["detectron2.layers"] = layers

    roi_align = types.ModuleType("detectron2.layers.roi_align")

    class ROIAlign:
        pass

    roi_align.ROIAlign = ROIAlign
    sys.modules["detectron2.layers.roi_align"] = roi_align

    structures = types.ModuleType("detectron2.structures")
    structures.__path__ = [str(ROOT / "detectron2" / "structures")]
    sys.modules["detectron2.structures"] = structures

    boxes = types.ModuleType("detectron2.structures.boxes")

    class Boxes:
        pass

    boxes.Boxes = Boxes
    sys.modules["detectron2.structures.boxes"] = boxes


def load_masks_module():
    spec = importlib.util.spec_from_file_location(
        "detectron2.structures.masks", ROOT / "detectron2" / "structures" / "masks.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main() -> None:
    install_stubs()
    masks = load_masks_module()

    polygon_masks = masks.PolygonMasks([[[0, 0, 1, 0, 1, 1]]])
    print("Constructed PolygonMasks")
    print("Accessing PolygonMasks.device now")
    print(polygon_masks.device)


if __name__ == "__main__":
    main()
