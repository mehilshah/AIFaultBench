#!/usr/bin/env python3
"""Minimal reproduction for the EfficientNet gradient warning."""

from __future__ import annotations

import logging
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
RESEARCH = CODEBASE / "research"
sys.path.insert(0, str(RESEARCH))
sys.path.insert(0, str(CODEBASE))


def main() -> int:
  import tensorflow as tf
  import tf_keras
  from official.legacy.image_classification.efficientnet import efficientnet_model
  from official.modeling import grad_utils

  logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
  tf.get_logger().setLevel("INFO")
  tf_keras.backend.clear_session()
  tf.random.set_seed(7)

  # Build the EfficientNet-B1 backbone used by EfficientDet-style feature
  # extractors and tap it before the final backbone stages.
  backbone = efficientnet_model.EfficientNet.from_name(
      "efficientnet-b1",
      overrides={"rescale_input": False},
  )
  feature_model = tf_keras.Model(
      inputs=backbone.inputs,
      outputs=backbone.get_layer("stack_6/block_0/project_bn").output,
      name="efficientnet_b1_feature_slice",
  )

  inputs = tf.zeros((1, 240, 240, 3), dtype=tf.float32)

  with tf.GradientTape() as tape:
    features = feature_model(inputs, training=True)
    loss = tf.reduce_sum(features)

  # Keep the classifier weights out of the repro so the warning focuses on the
  # unused EfficientNet backbone stages, matching the reported issue.
  trainable_variables = [
      var for var in backbone.trainable_variables
      if not var.name.startswith("logits/")
  ]

  print("trainable_variables:", len(trainable_variables))
  print("loss:", float(loss.numpy()))
  grad_utils.minimize_using_explicit_allreduce(
      tape,
      tf_keras.optimizers.SGD(0.1),
      loss,
      trainable_variables,
  )
  print("completed")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())

