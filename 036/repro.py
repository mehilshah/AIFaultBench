#!/usr/bin/env python3
"""Reproduce the GAE formula typo reported in bug_report.txt.

This is a documentation/source-level repro: the code in
`labml_nn/rl/ppo/gae.py` still contains the incorrect infinite-horizon
example and the unnormalized weighting formula from the report.
"""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "codebase" / "labml_nn" / "rl" / "ppo" / "gae.py"

EXPECTED_CORRECT_INFINITE_HORIZON = (
    r"\hat{A_t^{(\infty)}} &= r_t + \gamma r_{t+1} +\gamma^2 r_{t+2} + ... - V(s)"
)
EXPECTED_CORRECT_WEIGHTS = r"We set $w_k = (1-\lambda) \lambda^{k-1}$"


def main() -> int:
    text = SOURCE.read_text()
    lines = text.splitlines()

    print(f"Inspecting {SOURCE.relative_to(ROOT)}")
    print()
    print("Relevant source excerpt:")
    for line_no in range(29, 46):
        print(f"{line_no:03d}: {lines[line_no - 1]}")
    print()

    has_infinite_horizon_typo = "gamma^2 r_{t+1}" in text
    has_weight_typo = r"We set $w_k = \lambda^{k-1}$" in text

    if has_infinite_horizon_typo and has_weight_typo:
        print("Reproduced: the docstring still contains both reported formula bugs.")
        print(f"Expected correction for the infinite-horizon term: {EXPECTED_CORRECT_INFINITE_HORIZON}")
        print(f"Expected correction for the weights: {EXPECTED_CORRECT_WEIGHTS}")
        raise AssertionError(
            "GAE docstring is still incorrect: the infinite-horizon term uses r_{t+1} "
            "instead of r_{t+2}, and the weights omit the (1-lambda) factor."
        )

    print("Reported typo not present in the current source.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
