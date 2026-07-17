#!/usr/bin/env python3
"""Minimal repro for Detectron2 `ColorMode.IMAGE_BW` rendering mismatch.

This script loads the local `detectron2/utils/visualizer.py` directly and
stubs the unrelated imports that are not needed for the visualizer-only path.
That keeps the repro focused on the bug in `VisImage.get_image()` vs the
updated `self.output.img` buffer.
"""

from __future__ import annotations

import importlib.util
import json
import pathlib
import sys
import types

import numpy as np
from PIL import Image


ROOT = pathlib.Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
RESULT_PATH = ROOT / "reproduction.json"


def _patch_compat() -> None:
    # Detectron2's older code expects these symbols.
    if not hasattr(Image, "LINEAR"):
        Image.LINEAR = Image.BILINEAR
    if not hasattr(np, "bool"):
        np.bool = np.bool_


def _install_stubs() -> None:
    detectron2 = types.ModuleType("detectron2")
    detectron2.__path__ = [str(CODEBASE / "detectron2")]

    utils = types.ModuleType("detectron2.utils")
    utils.__path__ = [str(CODEBASE / "detectron2" / "utils")]

    data = types.ModuleType("detectron2.data")

    class _MetadataCatalog:
        @staticmethod
        def get(name):
            return {}

    data.MetadataCatalog = _MetadataCatalog

    structures = types.ModuleType("detectron2.structures")
    for name in ["BitMasks", "Boxes", "BoxMode", "Keypoints", "PolygonMasks", "RotatedBoxes"]:
        setattr(structures, name, type(name, (), {}))

    file_io = types.ModuleType("detectron2.utils.file_io")

    class _PathManager:
        @staticmethod
        def open(path, mode="r"):
            return open(path, mode)

    file_io.PathManager = _PathManager

    colormap = types.ModuleType("detectron2.utils.colormap")
    colormap.random_color = lambda rgb=True, maximum=1: (1.0, 0.0, 0.0)

    # The visualizer imports torch, but this repro never executes tensor ops.
    torch = types.ModuleType("torch")
    torch.device = lambda name: name

    sys.modules.update(
        {
            "detectron2": detectron2,
            "detectron2.utils": utils,
            "detectron2.data": data,
            "detectron2.structures": structures,
            "detectron2.utils.file_io": file_io,
            "detectron2.utils.colormap": colormap,
            "torch": torch,
        }
    )


def _load_visualizer_module():
    spec = importlib.util.spec_from_file_location(
        "detectron2.utils.visualizer", CODEBASE / "detectron2" / "utils" / "visualizer.py"
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load detectron2.utils.visualizer from local codebase")

    module = importlib.util.module_from_spec(spec)
    sys.modules["detectron2.utils.visualizer"] = module
    spec.loader.exec_module(module)
    return module


class _FakeMaskBool:
    def __init__(self, arr):
        self.arr = np.asarray(arr)

    def __gt__(self, other):
        return _FakeMaskBool(self.arr > other)

    def numpy(self):
        return self.arr


class _FakeMasks:
    def __init__(self, arr):
        self.arr = np.asarray(arr)

    def any(self, dim=0):
        return _FakeMaskBool(self.arr.any(axis=dim))

    def __array__(self, dtype=None):
        return np.asarray(self.arr, dtype=dtype)


class _FakePredictions:
    def __init__(self, mask):
        self.pred_masks = _FakeMasks(mask)

    def has(self, name):
        return name == "pred_masks"


def _make_input():
    height = width = 64
    image = np.zeros((height, width, 3), dtype=np.uint8)
    image[:, :, 0] = 255

    mask = np.zeros((1, height, width), dtype=bool)
    mask[0, 16:48, 16:48] = True
    return image, mask


def main() -> int:
    _patch_compat()
    _install_stubs()
    visualizer = _load_visualizer_module()

    image, mask = _make_input()
    predictions = _FakePredictions(mask)

    # We only want to exercise the grayscale branch, not the overlay drawing.
    v = visualizer.Visualizer(image, {"get": lambda key, default=None: default}, instance_mode=visualizer.ColorMode.IMAGE_BW)
    v.overlay_instances = lambda **kwargs: None
    result = v.draw_instance_predictions(predictions)

    buffer_pixel = result.img[8, 8].astype("uint8").tolist()
    rendered_pixel = result.get_image()[8, 8].tolist()
    original_pixel = image[8, 8].tolist()

    reproducible = (
        buffer_pixel[0] == buffer_pixel[1] == buffer_pixel[2]
        and rendered_pixel == original_pixel
        and rendered_pixel != buffer_pixel
    )

    payload = {
        "reproducible": reproducible,
        "evidence": (
            "v.output.img[8,8] becomes {} but v.output.get_image()[8,8] stays {}. "
            "That means IMAGE_BW updates the buffer, but the rendered canvas still uses the original image."
        ).format(buffer_pixel, rendered_pixel),
        "steps": [
            "Load detectron2/utils/visualizer.py with local stubs for unrelated imports",
            "Call draw_instance_predictions with instance_mode=ColorMode.IMAGE_BW on a synthetic mask",
            "Compare the updated image buffer to VisImage.get_image()",
        ],
        "blocking_reason": "",
        "reproduction_command": "bash run_repro.sh",
    }

    RESULT_PATH.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))
    return 0 if reproducible else 1


if __name__ == "__main__":
    raise SystemExit(main())
