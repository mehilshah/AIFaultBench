#!/usr/bin/env python3
"""Minimal reproduction for DataCollatorWithFlattening tensor-label failure."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import torch


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase" / "src"))

from transformers import DataCollatorWithFlattening  # noqa: E402


def repro_tensor_labels():
    features = [
        {
            "input_ids": torch.tensor([1, 2, 3, 4]),
            "labels": torch.tensor([10, 11, 12, 13]),
        },
        {
            "input_ids": torch.tensor([5, 6, 7]),
            "labels": torch.tensor([14, 15, 16]),
        },
    ]
    collator = DataCollatorWithFlattening(return_tensors="pt")
    return collator(features)


def repro_list_labels():
    features = [
        {
            "input_ids": torch.tensor([1, 2, 3, 4]),
            "labels": [10, 11, 12, 13],
        },
        {
            "input_ids": torch.tensor([5, 6, 7]),
            "labels": [14, 15, 16],
        },
    ]
    collator = DataCollatorWithFlattening(return_tensors="pt")
    return collator(features)


def main() -> int:
    print(json.dumps({"python": sys.version.split()[0], "torch": torch.__version__}))

    print("labels as tensors")
    tensor_error = None
    try:
        batch = repro_tensor_labels()
        print("unexpected success:", batch)
    except Exception as exc:  # noqa: BLE001
        tensor_error = exc
        print("got error:", repr(exc))

    print("\nlabels as list")
    batch = repro_list_labels()
    for key, value in batch.items():
        print(key, value)

    expected = 'TypeError(\'can only concatenate list (not "Tensor") to list\')'
    reproduced = repr(tensor_error) == expected
    print("\nreproduced:", reproduced)
    return 0 if reproduced else 1


if __name__ == "__main__":
    raise SystemExit(main())
