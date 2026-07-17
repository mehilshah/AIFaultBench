#!/usr/bin/env python3
"""Reproduce the YOLOV8 SavedModel box-shape export issue."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import tensorflow as tf
import keras

from keras_cv.models import YOLOV8Backbone
from keras_cv.models import YOLOV8Detector


ROOT = Path(__file__).resolve().parent


def run_saved_model_cli(export_dir: str) -> str:
    """Return the relevant SavedModel CLI signature block."""
    cmd = [
        sys.executable,
        "-m",
        "tensorflow.python.tools.saved_model_cli",
        "show",
        "--dir",
        export_dir,
        "--tag_set",
        "serve",
        "--all",
    ]
    completed = subprocess.run(
        cmd,
        check=True,
        capture_output=True,
        text=True,
    )
    lines = completed.stdout.splitlines()
    capture = []
    in_signature = False
    for line in lines:
        if "outputs['boxes'] tensor_info:" in line:
            in_signature = True
        if in_signature:
            capture.append(line)
            if "Method name is:" in line:
                break
    return "\n".join(capture) if capture else completed.stdout


def main() -> int:
    image = np.ones((1, 512, 512, 3), dtype=np.float32)
    model = YOLOV8Detector(
        num_classes=20,
        bounding_box_format="xywh",
        fpn_depth=1,
        backbone=YOLOV8Backbone.from_preset("yolo_v8_xs_backbone"),
    )

    raw_outputs = model(image)
    raw_boxes_shape = tuple(raw_outputs["boxes"].shape)
    raw_classes_shape = tuple(raw_outputs["classes"].shape)

    print(f"tensorflow_version={tf.__version__}")
    print(f"keras_version={keras.__version__}")
    print(f"raw_boxes_shape={raw_boxes_shape}")
    print(f"raw_classes_shape={raw_classes_shape}")

    with tempfile.TemporaryDirectory(prefix="yolo8_export_", dir=str(ROOT)) as export_dir:
        tf.saved_model.save(model, export_dir)
        print(f"saved_model_dir={export_dir}")
        print(run_saved_model_cli(export_dir))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
