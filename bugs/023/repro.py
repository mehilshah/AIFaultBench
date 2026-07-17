#!/usr/bin/env python3
"""Reproduce the notebook import cell from docs/vision/object_detection.ipynb.

The bug report claims this cell breaks while importing the TensorFlow Models
helpers. This script mirrors that cell closely and exits nonzero if any import
fails.
"""

from __future__ import annotations

import os
import pprint
import sys


def _prepend_local_deps() -> None:
    deps_dir = os.path.join(os.path.dirname(__file__), ".deps")
    if os.path.isdir(deps_dir) and deps_dir not in sys.path:
        sys.path.insert(0, deps_dir)


def main() -> int:
    _prepend_local_deps()

    import orbit  # noqa: F401
    import tensorflow as tf
    import tensorflow_models as tfm

    from official.core import config_definitions as cfg  # noqa: F401
    from official.core import exp_factory  # noqa: F401
    from official.vision.dataloaders.tf_example_decoder import TfExampleDecoder  # noqa: F401
    from official.vision.ops.preprocess_ops import normalize_image  # noqa: F401
    from official.vision.ops.preprocess_ops import resize_and_crop_image  # noqa: F401
    from official.vision.serving import export_saved_model_lib  # noqa: F401
    from official.vision.utils.object_detection import visualization_utils  # noqa: F401

    pp = pprint.PrettyPrinter(indent=4)
    print("tensorflow", tf.__version__)
    print("orbit", orbit.__file__)
    print("tfm.core", tfm.core.__file__)
    print("tfm.vision", tfm.vision.__file__)
    print("pretty_printer", pp.__class__.__name__)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
