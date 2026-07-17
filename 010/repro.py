#!/usr/bin/env python3
"""Minimal reproduction for validation loss staying at zero."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import tensorflow as tf


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
sys.path.insert(0, str(CODEBASE))

from official.vision.configs import maskrcnn as maskrcnn_cfg  # noqa: E402
from official.vision.configs import semantic_segmentation as seg_cfg  # noqa: E402
from official.vision.tasks.maskrcnn import MaskRCNNTask  # noqa: E402
from official.vision.tasks.semantic_segmentation import (  # noqa: E402
    SemanticSegmentationTask,
)


class DummyMaskRCNNModel(tf.keras.Model):

  def call(self, images, anchor_boxes=None, image_shape=None, training=False):
    batch = tf.shape(images)[0]
    return {
        "detection_boxes": tf.zeros([batch, 1, 4], tf.float32),
        "detection_scores": tf.zeros([batch, 1], tf.float32),
        "detection_classes": tf.zeros([batch, 1], tf.float32),
        "num_detections": tf.ones([batch], tf.float32),
    }


class DummySegmentationModel(tf.keras.Model):

  def call(self, inputs, training=False):
    batch = tf.shape(inputs)[0]
    height = tf.shape(inputs)[1]
    width = tf.shape(inputs)[2]
    return tf.zeros([batch, height, width, 2], tf.float32)


def _as_float(value):
  if hasattr(value, "numpy"):
    value = value.numpy()
  return float(value)


def reproduce_maskrcnn() -> float:
  task_config = maskrcnn_cfg.MaskRCNNTask()
  task_config.use_coco_metrics = False
  task_config.use_wod_metrics = False
  task_config.use_approx_instance_metrics = False

  task = MaskRCNNTask(task_config)
  task.instance_box_perclass_metrics = None
  task.instance_mask_perclass_metrics = None
  model = DummyMaskRCNNModel()
  images = tf.zeros([1, 8, 8, 3], tf.float32)
  labels = {
      "image_info": tf.zeros([1, 2, 4], tf.float32),
      "anchor_boxes": tf.zeros([1, 1, 4], tf.float32),
      "groundtruths": {
          "source_id": tf.constant([b"0"]),
          "boxes": tf.zeros([1, 1, 4], tf.float32),
          "classes": tf.zeros([1, 1], tf.float32),
          "is_crowds": tf.zeros([1, 1], tf.float32),
          "masks": tf.zeros([1, 1, 1, 1], tf.float32),
      },
  }

  logs = task.validation_step((images, labels), model=model)
  metric = tf.keras.metrics.Mean(name="validation_loss", dtype=tf.float32)
  metric.update_state(logs[task.loss])
  return _as_float(metric.result())


def reproduce_semantic_segmentation() -> float:
  task_config = seg_cfg.SemanticSegmentationTask()
  task_config.validation_data.resize_eval_groundtruth = False
  task_config.allow_image_summary = False

  task = SemanticSegmentationTask(task_config)
  task.iou_metric = None
  model = DummySegmentationModel()
  features = tf.zeros([1, 8, 8, 3], tf.float32)
  labels = tf.zeros([1, 8, 8, 1], tf.int32)

  logs = task.validation_step((features, labels), model=model)
  metric = tf.keras.metrics.Mean(name="validation_loss", dtype=tf.float32)
  metric.update_state(logs[task.loss])
  return _as_float(metric.result())


def main() -> int:
  mask_loss = reproduce_maskrcnn()
  sem_loss = reproduce_semantic_segmentation()

  result = {
      "maskrcnn_validation_loss": mask_loss,
      "semantic_segmentation_validation_loss": sem_loss,
  }
  print(json.dumps(result, sort_keys=True))
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
