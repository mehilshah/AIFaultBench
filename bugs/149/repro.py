from __future__ import annotations

import importlib.util
import sys
import traceback
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MODULE_PATH = ROOT / "codebase" / "sentence_transformers" / "util" / "file_io.py"


def main() -> int:
    print(f"python={sys.version.split()[0]}")
    print(f"module_path={MODULE_PATH}")
    print(f"requests_available={importlib.util.find_spec('requests') is not None}")

    spec = importlib.util.spec_from_file_location("sentence_transformers.util.file_io", MODULE_PATH)
    if spec is None or spec.loader is None:
        print("Could not construct import spec for file_io.py", file=sys.stderr)
        return 2

    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception:
        traceback.print_exc()
        return 1

    print("Import succeeded unexpectedly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
