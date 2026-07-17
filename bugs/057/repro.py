#!/usr/bin/env python3
import os
import sys
import traceback


def main() -> None:
    os.environ.setdefault("KERAS_BACKEND", "tensorflow")

    import keras

    print(f"keras version: {keras.__version__}")
    print(f"keras module path: {keras.__file__}")
    print("importing keras.ops now")
    from keras import ops  # noqa: F401

    print(f"ops import succeeded: {ops}")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
