#!/usr/bin/env python3
"""Minimal reproduction for the NaN loss in the transformer MNIST example.

The legacy training code in `codebase/transformer/cluttered_mnist.py` uses:

    cross_entropy = -tf.reduce_sum(y * tf.log(y_pred))

That expression is numerically unstable when `y_pred` contains exact zeros,
because `0 * log(0)` becomes `nan` in floating point arithmetic.
This script reproduces that failure mode deterministically with TensorFlow.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import tensorflow as tf


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase" / "transformer"))

from tf_utils import dense_to_one_hot  # noqa: E402


def main() -> int:
    tf.compat.v1.disable_eager_execution()

    labels = dense_to_one_hot(np.array([0], dtype=np.int32), n_classes=4)
    y = tf.constant(labels, dtype=tf.float32)

    # A softmax with exact zeros in the non-target classes triggers the legacy
    # cross-entropy formulation to become NaN.
    logits = tf.constant([[1000.0, -1000.0, -1000.0, -1000.0]], dtype=tf.float32)
    y_pred = tf.nn.softmax(logits)
    unstable_loss = -tf.reduce_sum(y * tf.math.log(y_pred))
    stable_loss = tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=logits)

    with tf.compat.v1.Session() as sess:
        y_pred_v, unstable_v, stable_v = sess.run(
            [y_pred, unstable_loss, stable_loss]
        )

    print("softmax =", y_pred_v.tolist())
    print("unstable_loss =", unstable_v)
    print("stable_loss =", stable_v.tolist())
    print("unstable_is_nan =", bool(np.isnan(unstable_v)))

    if not np.isnan(unstable_v):
        raise SystemExit(
            "Expected the legacy cross-entropy expression to produce NaN."
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
