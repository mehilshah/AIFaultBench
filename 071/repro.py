#!/usr/bin/env python3
"""Minimal reproducer for the missing `transformers.deepspeed` module.

This script mirrors the import site in
`codebase/applications/DeepSpeed-Chat/dschat/utils/model/model_utils.py`.
"""

from __future__ import annotations

import traceback
from pathlib import Path

import transformers


TARGET_FILE = Path(
    "codebase/applications/DeepSpeed-Chat/dschat/utils/model/model_utils.py"
)


def main() -> int:
    print(f"Using transformers=={transformers.__version__}")
    print(f"Relevant source file: {TARGET_FILE}")
    print("Attempting: from transformers.deepspeed import HfDeepSpeedConfig")

    try:
        from transformers.deepspeed import HfDeepSpeedConfig  # noqa: F401
    except Exception:
        traceback.print_exc()
        return 1

    print("Import unexpectedly succeeded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
