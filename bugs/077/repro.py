#!/usr/bin/env python3
"""Minimal reproducer for the reported graph-execution failure.

The GitHub issue's traceback points to a missing JPEG path being consumed by
TensorFlow's input pipeline during `model.fit()`. TensorBoard is present in the
callback list, but the failure itself is the missing file.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import tensorflow as tf


ROOT = Path(__file__).resolve().parent
VALID_IMAGE = ROOT / "codebase" / "images" / "2516944023_d00345997d_z.jpg"
MISSING_IMAGE = ROOT / "codebase" / "images" / "definitely_missing.jpg"


def build_dataset(batch_size: int = 1) -> tf.data.Dataset:
    paths = tf.constant([str(VALID_IMAGE), str(MISSING_IMAGE)])
    labels = tf.constant([0, 0], dtype=tf.int32)

    def _load_image(path: tf.Tensor, label: tf.Tensor):
        image = tf.io.read_file(path)
        image = tf.io.decode_jpeg(image, channels=3)
        image = tf.image.resize(image, [32, 32])
        image = tf.cast(image, tf.float32) / 255.0
        return image, label

    dataset = tf.data.Dataset.from_tensor_slices((paths, labels))
    dataset = dataset.map(_load_image, num_parallel_calls=tf.data.AUTOTUNE)
    dataset = dataset.batch(batch_size)
    return dataset


def build_model() -> tf.keras.Model:
    inputs = tf.keras.Input(shape=(32, 32, 3))
    x = tf.keras.layers.Flatten()(inputs)
    x = tf.keras.layers.Dense(8, activation="relu")(x)
    outputs = tf.keras.layers.Dense(1, activation="sigmoid")(x)
    model = tf.keras.Model(inputs, outputs)
    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"],
    )
    return model


def main() -> int:
    if not VALID_IMAGE.exists():
        raise FileNotFoundError(f"Expected bundled sample image at {VALID_IMAGE}")

    log_dir = Path(tempfile.mkdtemp(prefix="tensorboard_logs_"))
    print(f"Using TensorBoard log_dir: {log_dir}")
    print(f"Valid image: {VALID_IMAGE}")
    print(f"Missing image: {MISSING_IMAGE}")

    model = build_model()
    dataset = build_dataset()

    callbacks = [
        tf.keras.callbacks.TensorBoard(log_dir=str(log_dir)),
    ]

    # The second sample in the dataset points at a nonexistent path, so the
    # first epoch fails when the input pipeline reaches ReadFile.
    model.fit(dataset, epochs=1, callbacks=callbacks, shuffle=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
