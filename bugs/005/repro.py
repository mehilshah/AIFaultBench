#!/usr/bin/env python3
"""Minimal import probe for the reported tf_keras failure.

The bug report says the failure happens during:
    import tensorflow as tf, tf_keras
    from tensorflow.python.framework import tensor

This script exercises that exact import chain and reports whether it fails on
the current host.
"""

from __future__ import annotations

import sys


def main() -> int:
  try:
    import tensorflow as tf
    import tf_keras
    from tensorflow.python.framework import tensor
  except Exception as exc:  # pragma: no cover - used for repro logging.
    print(f"REPRO_FAIL: {type(exc).__name__}: {exc}")
    return 1

  print(f"tensorflow={tf.__version__}")
  print(f"tf_keras={tf_keras.__version__}")
  print(f"tensor_module={tensor.__file__}")
  print("repro_status=import_succeeded")
  return 0


if __name__ == "__main__":
  sys.exit(main())
