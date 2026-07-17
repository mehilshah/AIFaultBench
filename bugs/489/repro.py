#!/usr/bin/env python3
"""Minimal reproduction for the reported lsnet_t failure.

This script demonstrates two states:
1. Before the custom `lsnet` package is imported, `timm.create_model('lsnet_t')`
   raises `RuntimeError: Unknown model (lsnet_t)`.
2. After importing a package that registers the model, creation succeeds.

That matches the behavior in the local `timm` codebase: model names are only
available after their entrypoint has been registered.
"""

from __future__ import annotations

import sys
import traceback
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))
sys.path.insert(0, str(ROOT / "helper"))


def main() -> int:
    import timm

    print(f"timm_version={timm.__version__}")
    print(f"registered_before_import={'lsnet_t' in timm.list_models()}")

    try:
        timm.create_model("lsnet_t")
    except Exception as exc:  # noqa: BLE001
        print(f"before_import_error={type(exc).__name__}: {exc}")
        traceback.print_exc()
    else:
        print("before_import_error=None")

    import lsnet  # noqa: F401  # registers lsnet_t as a side effect

    print(f"registered_after_import={'lsnet_t' in timm.list_models()}")
    model = timm.create_model("lsnet_t")
    print(f"after_import_model={model.__class__.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
