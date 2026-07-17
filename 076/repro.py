#!/usr/bin/env python3
"""Minimal reproduction for Mask R-CNN issue 3050.

This script uses the repository's own `MaskRCNN.load_weights()` method and a
legacy-style HDF5 file to trigger the HDF5 loader failure reported in the bug.
"""

from __future__ import annotations

import os
import sys
import tempfile
import traceback
import types

import h5py
import numpy as np


def install_keras_engine_shim() -> None:
    """Expose the legacy `keras.engine` namespace expected by the repo."""

    import keras
    from tensorflow.python.keras.saving import hdf5_format

    engine = types.ModuleType("keras.engine")
    engine.saving = hdf5_format
    engine.Layer = keras.layers.Layer
    sys.modules["keras.engine"] = engine
    sys.modules["keras.engine.saving"] = hdf5_format


def build_legacy_hdf5(path: str) -> None:
    """Create a tiny legacy-format HDF5 weight file.

    The file only needs a matching layer name to reach the loader code path
    where the failure occurs.
    """

    with h5py.File(path, "w") as f:
        f.attrs["layer_names"] = np.array([b"conv1"])
        group = f.create_group("conv1")
        group.attrs["weight_names"] = np.array([b"conv1/kernel:0", b"conv1/bias:0"])
        group.create_dataset(
            "conv1/kernel:0",
            data=np.zeros((7, 7, 3, 64), dtype=np.float32),
        )
        group.create_dataset(
            "conv1/bias:0",
            data=np.zeros((64,), dtype=np.float32),
        )


def main() -> int:
    repo_root = os.path.dirname(os.path.abspath(__file__))
    codebase_dir = os.path.join(repo_root, "codebase")
    sys.path.insert(0, codebase_dir)

    install_keras_engine_shim()

    import keras
    from mrcnn.config import Config
    from mrcnn.model import MaskRCNN

    class MiniConfig(Config):
        NAME = "mini"
        GPU_COUNT = 1
        IMAGES_PER_GPU = 1
        NUM_CLASSES = 2
        BACKBONE = "resnet50"
        IMAGE_MIN_DIM = 128
        IMAGE_MAX_DIM = 128

    config = MiniConfig()

    keras_model = keras.Sequential(
        [
            keras.layers.Input((8, 8, 3), name="input_image"),
            keras.layers.Conv2D(64, 7, name="conv1"),
        ]
    )

    weight_fd, weight_path = tempfile.mkstemp(suffix=".h5")
    os.close(weight_fd)
    build_legacy_hdf5(weight_path)

    class DummyMaskRCNN:
        def __init__(self) -> None:
            self.keras_model = keras_model
            self.config = config
            self.model_dir = tempfile.mkdtemp(prefix="mask_rcnn_repro_")

        def set_log_dir(self, *args, **kwargs) -> None:
            return None

    dummy = DummyMaskRCNN()

    try:
        MaskRCNN.load_weights(dummy, weight_path, by_name=True)
    except NotImplementedError as exc:
        print("REPRODUCED: MaskRCNN.load_weights() raised NotImplementedError")
        print(str(exc).split(" Got a model or layer")[0])
        return 0
    except Exception:
        print("UNEXPECTED_EXCEPTION: load_weights raised a different error")
        traceback.print_exc()
        return 1

    print("NO_BUG: load_weights completed successfully")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
