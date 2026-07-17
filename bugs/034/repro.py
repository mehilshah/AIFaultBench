#!/usr/bin/env python3
"""Minimal repro for the BERT GELU API mismatch."""

from __future__ import annotations

import sys
from pathlib import Path

import torch


def main() -> int:
    repo_root = Path(__file__).resolve().parent
    bert_dir = repo_root / "codebase" / "PyTorch" / "LanguageModeling" / "BERT"
    sys.path.insert(0, str(bert_dir))

    from modeling import gelu  # noqa: E402

    x = torch.tensor([0.25], dtype=torch.float32)
    print("Calling codebase/PyTorch/LanguageModeling/BERT/modeling.py:122 gelu()")
    print(f"Input tensor: {x!r}")
    gelu(x)
    print("Unexpected success: gelu() returned without error.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print(f"{type(exc).__name__}: {exc}", file=sys.stderr)
        raise
