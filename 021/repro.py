#!/usr/bin/env python3
"""Minimal reproduction for the ConcatV2 empty-list failure in detection_generator."""

from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path

import tensorflow as tf


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"


def _ensure_package(name: str, path: Path) -> None:
  module = sys.modules.get(name)
  if module is None:
    module = types.ModuleType(name)
    module.__path__ = [str(path)]
    sys.modules[name] = module


def _load_module(module_name: str, file_path: Path):
  if module_name in sys.modules:
    return sys.modules[module_name]
  spec = importlib.util.spec_from_file_location(module_name, file_path)
  if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot load {module_name} from {file_path}")
  module = importlib.util.module_from_spec(spec)
  sys.modules[module_name] = module
  spec.loader.exec_module(module)
  return module


def _install_lightweight_official_packages() -> None:
  _ensure_package("official", CODEBASE / "official")
  _ensure_package("official.vision", CODEBASE / "official" / "vision")
  _ensure_package("official.vision.ops", CODEBASE / "official" / "vision" / "ops")
  _ensure_package(
      "official.vision.modeling", CODEBASE / "official" / "vision" / "modeling"
  )
  _ensure_package(
      "official.vision.modeling.layers",
      CODEBASE / "official" / "vision" / "modeling" / "layers",
  )

  preprocess_ops = types.ModuleType("official.vision.ops.preprocess_ops")

  def clip_or_pad_to_fixed_size(input_tensor, size, constant_values=0):
    """Minimal helper used by the repro path."""
    clipped = input_tensor[: tf.minimum(tf.shape(input_tensor)[0], size)]
    pad = tf.maximum(0, size - tf.shape(clipped)[0])
    rank = clipped.shape.rank
    if rank is None:
      raise ValueError("Expected a statically known tensor rank.")
    paddings = [[0, 0] for _ in range(rank)]
    paddings[0][1] = pad
    return tf.pad(clipped, paddings, constant_values=constant_values)

  preprocess_ops.clip_or_pad_to_fixed_size = clip_or_pad_to_fixed_size
  sys.modules["official.vision.ops.preprocess_ops"] = preprocess_ops

  _load_module("official.vision.ops.box_ops", CODEBASE / "official/vision/ops/box_ops.py")
  _load_module("official.vision.ops.nms", CODEBASE / "official/vision/ops/nms.py")
  _load_module(
      "official.vision.modeling.layers.edgetpu",
      CODEBASE / "official/vision/modeling/layers/edgetpu.py",
  )


def _load_detection_generator():
  _install_lightweight_official_packages()
  return _load_module(
      "official.vision.modeling.layers.detection_generator",
      CODEBASE / "official/vision/modeling/layers/detection_generator.py",
  )


def main() -> int:
  detection_generator = _load_detection_generator()

  # This raw score tensor contains only the implicit background channel.
  # After the background slice in _decode_multilevel_outputs, the class count
  # becomes zero, which leads to tf.concat([]) in _generate_detections_v2_class_aware.
  raw_boxes = {"1": tf.zeros([1, 1, 1, 4], dtype=tf.float32)}
  raw_scores = {"1": tf.zeros([1, 1, 1, 1], dtype=tf.float32)}
  anchor_boxes = {"1": tf.zeros([1, 1, 4], dtype=tf.float32)}
  image_shape = tf.constant([[100.0, 100.0]], dtype=tf.float32)

  generator = detection_generator.MultilevelDetectionGenerator(
      apply_nms=True,
      pre_nms_top_k=10,
      pre_nms_score_threshold=0.05,
      nms_iou_threshold=0.5,
      max_num_detections=5,
      nms_version="v2",
      use_cpu_nms=False,
      soft_nms_sigma=None,
      use_class_agnostic_nms=False,
  )

  print("Running MultilevelDetectionGenerator on a zero-class input.")
  print(f"raw_boxes shape: {raw_boxes['1'].shape}")
  print(f"raw_scores shape: {raw_scores['1'].shape}")
  print(f"anchor_boxes shape: {anchor_boxes['1'].shape}")

  try:
    generator(raw_boxes, raw_scores, anchor_boxes, image_shape)
  except Exception as exc:  # pylint: disable=broad-except
    message = str(exc)
    print(f"Observed exception: {type(exc).__name__}", file=sys.stderr)
    print(message, file=sys.stderr)
    if "ConcatV2" not in message:
      raise SystemExit(
          f"Unexpected exception type/message: {type(exc).__name__}: {message}"
      )
    print("Reproduced the empty-list ConcatV2 failure.", file=sys.stdout)
    return 0

  raise SystemExit("Bug not reproduced: the generator call unexpectedly succeeded.")


if __name__ == "__main__":
  raise SystemExit(main())
