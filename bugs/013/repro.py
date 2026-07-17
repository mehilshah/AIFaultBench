#!/usr/bin/env python3
"""Minimal reproduction for the Matplotlib backend flip on import.

The actual bug in the source tree is that
`official/vision/utils/object_detection/visualization_utils.py` calls
`matplotlib.use('Agg')` at module import time. Importing the full
`tensorflow_models` package reaches that module transitively, but the current
Python 3.12 environment cannot import the historical TensorFlow wheel stack
cleanly. This harness executes the real source file with tiny import stubs so we
can reproduce the backend change without mutating application code.
"""

from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path

import matplotlib


def _install_stub(name: str) -> None:
  """Registers an empty module for an import that is irrelevant to the bug."""
  sys.modules.setdefault(name, types.ModuleType(name))


def main() -> int:
  matplotlib.use("svg")
  before = matplotlib.get_backend()
  print(f"before={before}")

  # The module under test changes the backend before it imports TensorFlow and
  # the rest of the object-detection stack. Stubbing those imports keeps the
  # repro focused on the import-time side effect.
  for name in [
      "tensorflow",
      "official",
      "official.vision",
      "official.vision.ops",
      "official.vision.ops.box_ops",
      "official.vision.ops.preprocess_ops",
      "official.vision.utils",
      "official.vision.utils.object_detection",
      "official.vision.utils.object_detection.shape_utils",
  ]:
    _install_stub(name)

  module_path = (
      Path(__file__).resolve().parent /
      "codebase/official/vision/utils/object_detection/visualization_utils.py")
  spec = importlib.util.spec_from_file_location("viz_under_test", module_path)
  if spec is None or spec.loader is None:
    print("failed to load visualization_utils.py", file=sys.stderr)
    return 1

  module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module)

  after = matplotlib.get_backend()
  print(f"after={after}")
  if after.lower() != "agg":
    print("expected backend to switch to Agg", file=sys.stderr)
    return 1
  return 0


if __name__ == "__main__":
  raise SystemExit(main())

