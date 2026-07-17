#!/usr/bin/env python3
"""Minimal reproducer for kornia.geometry.epipolar.projections_from_fundamental."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

import torch


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))

import kornia.geometry.epipolar as epi  # noqa: E402


def run_case(name: str, F: torch.Tensor) -> Dict[str, Any]:
    try:
        P = epi.projections_from_fundamental(F)
        return {
            "name": name,
            "status": "ok",
            "input_shape": list(F.shape),
            "output_shape": list(P.shape),
        }
    except Exception as exc:  # pragma: no cover - repro script
        return {
            "name": name,
            "status": "error",
            "input_shape": list(F.shape),
            "error_type": type(exc).__name__,
            "error_message": str(exc),
        }


def main() -> int:
    torch.manual_seed(0)

    cases: List[Dict[str, Any]] = [
        run_case("batch_1x3x3", torch.randn(1, 3, 3)),
        run_case("nested_batch_1x1x3x3", torch.randn(1, 1, 3, 3)),
        run_case("unbatched_3x3", torch.randn(3, 3)),
    ]

    for case in cases:
        if case["status"] == "ok":
            print(
                f'{case["name"]}: OK input={case["input_shape"]} output={case["output_shape"]}'
            )
        else:
            print(
                f'{case["name"]}: ERROR {case["error_type"]}: {case["error_message"]}'
            )

    print(json.dumps({"cases": cases}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
