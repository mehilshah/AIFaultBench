from __future__ import annotations

import sys
from pathlib import Path
import traceback


ROOT = Path(__file__).resolve().parent
SOURCE_DIR = ROOT / "codebase" / "src"
sys.path.insert(0, str(SOURCE_DIR))


def main() -> int:
    try:
        from transformers.configuration_utils import ALLOWED_LAYER_TYPES  # noqa: F401
    except Exception:
        traceback.print_exc()
        return 1

    print("Unexpected success: ALLOWED_LAYER_TYPES imported")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
