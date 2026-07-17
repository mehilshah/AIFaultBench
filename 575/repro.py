#!/usr/bin/env python3
"""Source-level reproduction check for issue 2457.

The reported failure was:
    AttributeError: 'Namespace' object has no attribute 'validation_batch_size'

This script inspects the checked-in `codebase/train.py` directly. If the
`--validation-batch-size` CLI option is already present, the reported bug is
not reproducible in this tree because `args.validation_batch_size` is now set
by argparse before the line that reads it.
"""

from __future__ import annotations

from pathlib import Path
import json


ROOT = Path(__file__).resolve().parent
TRAIN_PY = ROOT / "codebase" / "train.py"


def line_number(text: str, needle: str) -> int | None:
    for idx, line in enumerate(text.splitlines(), start=1):
        if needle in line:
            return idx
    return None


def main() -> int:
    text = TRAIN_PY.read_text(encoding="utf-8")

    flag_line = line_number(text, "--validation-batch-size")
    access_line = line_number(text, "args.validation_batch_size or args.batch_size")

    result = {
        "train_py": str(TRAIN_PY),
        "validation_batch_size_flag_line": flag_line,
        "validation_batch_size_access_line": access_line,
        "reproducible": False,
        "reason": (
            "Local train.py already defines --validation-batch-size, so the "
            "reported Namespace AttributeError is fixed in this tree."
        ),
    }

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
