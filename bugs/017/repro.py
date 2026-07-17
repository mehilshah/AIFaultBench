#!/usr/bin/env python3
"""Minimal repro for the object detection tutorial SavedModel inference path."""

from __future__ import annotations

import os
import pathlib
import sys

import numpy as np
from PIL import Image
import tensorflow as tf


REPO_ROOT = pathlib.Path(__file__).resolve().parent
CODEBASE_RESEARCH = REPO_ROOT / "codebase" / "research"
if str(CODEBASE_RESEARCH) not in sys.path:
    sys.path.insert(0, str(CODEBASE_RESEARCH))


def load_model(model_name: str):
    base_url = "http://download.tensorflow.org/models/object_detection/"
    model_file = model_name + ".tar.gz"
    model_dir = tf.keras.utils.get_file(
        fname=model_name,
        origin=base_url + model_file,
        untar=True,
    )
    model_dir = pathlib.Path(model_dir)
    candidates = [
        model_dir / "saved_model",
        model_dir / model_name / "saved_model",
        model_dir / model_name,
    ]
    for candidate in candidates:
        if (candidate / "saved_model.pb").is_file():
            model_dir = candidate
            break
    else:
        raise FileNotFoundError(
            "Could not locate saved_model.pb under any expected path: "
            + ", ".join(str(path) for path in candidates)
        )
    print(f"model_dir={model_dir}")
    return tf.saved_model.load(str(model_dir))


def run_inference_for_single_image(model, image):
    image = np.asarray(image)
    input_tensor = tf.convert_to_tensor(image)[tf.newaxis, ...]
    model_fn = model.signatures["serving_default"]
    output_dict = model_fn(input_tensor)
    num_detections_tensor = output_dict.pop("num_detections")
    num_detections = int(np.asarray(num_detections_tensor).reshape(-1)[0])
    output_dict = {
        key: value[0, :num_detections].numpy() for key, value in output_dict.items()
    }
    output_dict["num_detections"] = num_detections
    output_dict["detection_classes"] = output_dict["detection_classes"].astype(
        np.int64
    )
    return output_dict


def main() -> int:
    print(f"python={sys.version.split()[0]}")
    print(f"tensorflow={tf.__version__}")

    model_name = "ssd_mobilenet_v1_coco_2017_11_17"
    image_path = (
        REPO_ROOT / "codebase" / "research" / "object_detection" / "test_images" / "image1.jpg"
    )

    if not image_path.is_file():
        raise FileNotFoundError(image_path)

    model = load_model(model_name)
    image = Image.open(image_path).convert("RGB")
    output_dict = run_inference_for_single_image(model, image)

    scores = output_dict["detection_scores"]
    classes = output_dict["detection_classes"]
    boxes = output_dict["detection_boxes"]

    print(f"image={image_path}")
    print(f"num_detections={output_dict['num_detections']}")
    print(f"detection_scores[:5]={np.array2string(scores[:5], precision=4)}")
    print(f"detection_classes[:5]={classes[:5].tolist()}")
    print(f"detection_boxes[:2]={np.array2string(boxes[:2], precision=4)}")
    print(f"max_score={float(scores.max()) if scores.size else 0.0}")
    print(f"nonempty_scores={scores.size > 0}")

    if output_dict["num_detections"] == 0:
        raise RuntimeError("No detections were returned")
    if scores.size == 0:
        raise RuntimeError("Empty detection tensors were returned")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
