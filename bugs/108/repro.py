#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase" / "src"))

import torch
import transformers
from transformers import DataCollatorWithFlattening


def batch_to_jsonable(batch):
    output = {}
    for key, value in batch.items():
        output[key] = value.tolist() if hasattr(value, "tolist") else value
    return output


def main() -> int:
    print(f"transformers_version={transformers.__version__}")
    print(f"torch_version={torch.__version__}")

    collator = DataCollatorWithFlattening(return_tensors="pt")

    tensor_features = [
        {"input_ids": torch.tensor([1, 2, 3, 4]), "labels": torch.tensor([10, 11, 12, 13])},
        {"input_ids": torch.tensor([5, 6, 7]), "labels": torch.tensor([14, 15, 16])},
    ]

    print("tensor_labels_case=")
    try:
        batch = collator(tensor_features)
    except Exception as exc:  # noqa: BLE001 - we want the exact runtime failure in the log
        print(f"tensor_labels_status=error")
        print(f"tensor_labels_error={type(exc).__name__}: {exc}")
    else:
        print("tensor_labels_status=unexpected_success")
        print(json.dumps(batch_to_jsonable(batch), indent=2, sort_keys=True))

    list_features = [
        {"input_ids": torch.tensor([1, 2, 3, 4]), "labels": [10, 11, 12, 13]},
        {"input_ids": torch.tensor([5, 6, 7]), "labels": [14, 15, 16]},
    ]

    print("list_labels_case=")
    batch = collator(list_features)
    print(json.dumps(batch_to_jsonable(batch), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
