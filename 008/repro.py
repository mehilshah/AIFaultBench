#!/usr/bin/env python3
"""Minimal reproducer for TF2 object detection TFLite export guard.

The TF2 exporter in TensorFlow Models only supports SSD and CenterNet models.
Passing a Faster R-CNN pipeline config raises ValueError immediately.
"""

from __future__ import annotations

from pathlib import Path
import re
import sys


CONFIG_PATH = Path(
    "codebase/research/object_detection/configs/tf2/"
    "faster_rcnn_resnet50_v1_640x640_coco17_tpu-8.config"
)


def infer_model_type(config_text: str) -> str:
    """Extract the top-level model type from a pipeline config."""
    for line in config_text.splitlines():
        match = re.match(r"^\s*(ssd|center_net|faster_rcnn)\s*\{", line)
        if match:
            return match.group(1)
    raise RuntimeError("Could not determine model type from pipeline config")


def main() -> int:
    config_text = CONFIG_PATH.read_text(encoding="utf-8")
    model_type = infer_model_type(config_text)
    print(f"Loaded pipeline config: {CONFIG_PATH}")
    print(f"Detected model type: {model_type}")
    print("Calling the TF2 TFLite export guard...")
    if model_type not in {"ssd", "center_net"}:
        raise ValueError(
            f"Only ssd or center_net models are supported in tflite. "
            f"Found {model_type} in config"
        )
    print("Unexpectedly reached a supported model type.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
