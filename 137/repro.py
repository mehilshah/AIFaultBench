#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import evaluate


def _to_builtin(value):
    if isinstance(value, dict):
        return {key: _to_builtin(val) for key, val in value.items()}
    if isinstance(value, list):
        return [_to_builtin(item) for item in value]
    if hasattr(value, "item"):
        return value.item()
    return value


def main() -> None:
    root = Path(__file__).resolve().parent
    metric_path = root / "codebase" / "metrics" / "rouge"

    summary = "मलेसियन एयरलाइन्सको विमानमा दुई सय ९८"
    reference = "मलेसियन एयरलाइन्सको विमानमा दुई सय ९८"

    rouge = evaluate.load(str(metric_path))

    default_scores = rouge.compute(predictions=[summary], references=[reference])
    split_scores = rouge.compute(
        predictions=[summary],
        references=[reference],
        tokenizer=str.split,
    )

    payload = {
        "evaluate_version": evaluate.__version__,
        "metric_path": str(metric_path),
        "default_scores": _to_builtin(default_scores),
        "split_scores": _to_builtin(split_scores),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
