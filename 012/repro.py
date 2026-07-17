from __future__ import annotations

import importlib.util
import sys
import traceback
from pathlib import Path

import tensorflow as tf
import tf_keras


def main() -> int:
    root = Path(__file__).resolve().parent
    module_path = root / "codebase" / "official" / "modeling" / "optimization" / "ema_optimizer.py"

    print(f"tensorflow={tf.__version__}")
    print(f"tf_keras={tf_keras.__version__}")
    print(
        "tf_keras.optimizers.legacy.Optimizer present:",
        hasattr(tf_keras.optimizers.legacy, "Optimizer"),
    )
    print(f"loading={module_path}")

    spec = importlib.util.spec_from_file_location("ema_optimizer_repro", module_path)
    if spec is None or spec.loader is None:
        print("failed_to_create_import_spec")
        return 2

    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception:
        traceback.print_exc()
        return 1

    print("ema_optimizer_imported_successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
