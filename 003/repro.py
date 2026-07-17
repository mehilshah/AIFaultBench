import traceback

import tensorflow as tf


def main():
  print(f"tensorflow_version={tf.__version__}")
  print(
      "has_tf_keras_layers_experimental="
      f"{hasattr(tf.keras.layers, 'experimental')}"
  )
  try:
    from object_detection.core import freezable_sync_batch_norm  # noqa: F401
    print("imported object_detection.core.freezable_sync_batch_norm")
    return 0
  except Exception as exc:  # pragma: no cover - exercised in repro
    print(f"import_failed={type(exc).__name__}: {exc}")
    traceback.print_exc()
    return 1


if __name__ == "__main__":
  raise SystemExit(main())
