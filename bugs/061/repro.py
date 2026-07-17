from __future__ import annotations

import importlib.util
import site
import sys
import traceback
from pathlib import Path


def find_weights_file() -> Path:
    candidates = []
    for base in site.getsitepackages():
        candidates.append(Path(base) / "keras_cv" / "models" / "weights.py")

    usersite = site.getusersitepackages()
    if isinstance(usersite, str):
        candidates.append(Path(usersite) / "keras_cv" / "models" / "weights.py")

    for candidate in candidates:
        if candidate.exists():
            return candidate

    raise FileNotFoundError("Could not locate keras_cv/models/weights.py")


def main() -> int:
    weights_path = find_weights_file()
    print(f"loading {weights_path}")

    spec = importlib.util.spec_from_file_location("keras_cv_weights_repro", weights_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to create import spec for {weights_path}")

    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        print("LOADED_OK")
        return 0
    except Exception:
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
