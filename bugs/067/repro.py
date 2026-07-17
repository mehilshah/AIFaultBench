#!/usr/bin/env python3
"""Minimal reproduction for keras-io issue 1147.

The issue report claims that the Oxford Pets segmentation tutorial applies
`sparse_categorical_crossentropy` to labels with an extra singleton channel
dimension. This script checks the smallest possible version of that setup and
compares the loss for `(batch, h, w)` versus `(batch, h, w, 1)` targets.
"""

from __future__ import annotations

import json
import sys

import numpy as np
import tensorflow as tf


def main() -> int:
    print(f"tensorflow_version={tf.__version__}")

    # Tiny per-pixel classification example with 3 classes.
    y_pred = np.array(
        [[[[0.70, 0.20, 0.10], [0.10, 0.80, 0.10]], [[0.10, 0.20, 0.70], [0.20, 0.50, 0.30]]]],
        dtype="float32",
    )
    y_true_3d = np.array([[[0, 1], [2, 1]]], dtype="int32")
    y_true_4d = np.expand_dims(y_true_3d, axis=-1)

    loss_3d = tf.keras.losses.sparse_categorical_crossentropy(y_true_3d, y_pred)
    loss_4d = tf.keras.losses.sparse_categorical_crossentropy(y_true_4d, y_pred)

    diff = np.max(np.abs(loss_3d.numpy() - loss_4d.numpy()))
    print("y_true_3d_shape=", y_true_3d.shape)
    print("y_true_4d_shape=", y_true_4d.shape)
    print("loss_3d=", loss_3d.numpy().tolist())
    print("loss_4d=", loss_4d.numpy().tolist())
    print(f"max_abs_diff={diff:.10f}")

    summary = {
        "tensorflow_version": tf.__version__,
        "loss_3d": loss_3d.numpy().tolist(),
        "loss_4d": loss_4d.numpy().tolist(),
        "max_abs_diff": float(diff),
    }
    print("summary=", json.dumps(summary, sort_keys=True))

    if diff == 0.0:
        print(
            "result=no_runtime_bug_detected: the singleton label dimension is accepted and produces identical loss"
        )
        return 0

    print("result=runtime_bug_detected: the two label shapes produce different losses")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
