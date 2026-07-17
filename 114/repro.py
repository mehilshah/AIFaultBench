#!/usr/bin/env python3
"""Minimal repro for the missing transformers.modeling_utils.shard_checkpoint import."""

from __future__ import annotations

import sys
import traceback


def main() -> int:
    print("Attempting: from transformers.modeling_utils import shard_checkpoint")
    try:
        from transformers.modeling_utils import shard_checkpoint  # noqa: F401
    except Exception as exc:  # pylint: disable=broad-exception-caught
        print(f"IMPORT_FAILED: {type(exc).__name__}: {exc}")
        traceback.print_exc()
        return 1

    print("IMPORT_OK: shard_checkpoint imported successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
