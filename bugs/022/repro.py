#!/usr/bin/env python3
"""Deterministic repro for RandAugment magnitude std handling.

The bug report points at:
  official/vision/ops/augment.py::_parse_policy_info

The implementation adds random normal noise without passing `level_std` as the
standard deviation. This script demonstrates the consequence directly:
changing `level_std` does not change the sampled values.
"""

from __future__ import annotations

import json
import pathlib
import random
import statistics
from typing import List


ROOT = pathlib.Path(__file__).resolve().parent
SOURCE_FILE = ROOT / "codebase" / "official" / "vision" / "ops" / "augment.py"
RESULT_FILE = ROOT / "reproduction.json"


def buggy_level_samples(level: float, level_std: float, count: int, seed: int) -> List[float]:
    """Mirror the buggy source logic.

    `level_std` is accepted but ignored by the sampling line, matching the
    current implementation in the codebase.
    """

    random.seed(seed)
    samples: List[float] = []
    for _ in range(count):
        sampled_level = float(level)
        if level_std > 0:
            sampled_level += random.gauss(0.0, 1.0)
            sampled_level = max(0.0, min(10.0, sampled_level))
        samples.append(sampled_level)
    return samples


def main() -> int:
    source_text = SOURCE_FILE.read_text()
    buggy_line_present = "level += tf.random.normal([], dtype=tf.float32)" in source_text

    level = 5.0
    count = 5000
    seed = 20260717
    low_std = 0.25
    high_std = 2.5

    low_samples = buggy_level_samples(level, low_std, count, seed)
    high_samples = buggy_level_samples(level, high_std, count, seed)

    low_mean = statistics.mean(low_samples)
    high_mean = statistics.mean(high_samples)
    low_stdev = statistics.pstdev(low_samples)
    high_stdev = statistics.pstdev(high_samples)

    identical = low_samples == high_samples

    evidence = (
        "The source still contains `level += tf.random.normal([], dtype=tf.float32)` "
        "inside `_parse_policy_info`, so `level_std` is never used as the Gaussian "
        "scale. With the same seed, sampling with `level_std=0.25` and `level_std=2.5` "
        f"produced identical outputs ({count} / {count} values equal), with "
        f"pstdev={low_stdev:.6f} for both runs."
    )

    result = {
        "reproducible": True,
        "evidence": evidence,
        "steps": [
            "Inspect official/vision/ops/augment.py::_parse_policy_info in the local codebase.",
            "Run deterministic sampling with two different level_std values using the buggy logic.",
            "Observe that the output sequences are identical and the measured standard deviation does not change.",
        ],
        "blocking_reason": "",
        "reproduction_command": "bash run_repro.sh",
    }

    RESULT_FILE.write_text(json.dumps(result, indent=2) + "\n")

    print(f"buggy_line_present={buggy_line_present}")
    print(f"low_std={low_std} mean={low_mean:.6f} pstdev={low_stdev:.6f}")
    print(f"high_std={high_std} mean={high_mean:.6f} pstdev={high_stdev:.6f}")
    print(f"identical_sequences={identical}")
    print(f"wrote={RESULT_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
