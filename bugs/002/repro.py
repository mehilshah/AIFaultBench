#!/usr/bin/env python3
"""Minimal reproduction for the TensorFlow 2.x contrib import failure."""

from pathlib import Path

import tensorflow as tf


def main():
    exporter_path = (
        Path(__file__).resolve().parent
        / "codebase"
        / "research"
        / "object_detection"
        / "exporter.py"
    )
    for lineno, line in enumerate(exporter_path.read_text().splitlines(), 1):
        if "tensorflow.contrib.quantize.python" in line or "graph_matcher" in line:
            print(f"{exporter_path}:{lineno}: {line}")

    print(f"TensorFlow version: {tf.__version__}")
    print(f"Executing eagerly: {tf.executing_eagerly()}")

    # This is the legacy dependency referenced by exporter.py. Under TF2,
    # tensorflow.contrib is absent and the import fails.
    from tensorflow.contrib.quantize.python import graph_matcher  # noqa: F401


if __name__ == "__main__":
    main()
