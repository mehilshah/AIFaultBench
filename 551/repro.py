#!/usr/bin/env python3
"""Source-level reproduction for NumPyro issue 2026.

The bug report claims the MatrixNormal docstring says the scale_tril parameters
are lower Cholesky factors of correlation matrices, but the implementation and
parameter constraints treat them as lower Cholesky factors of covariance-scale
matrices.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "codebase" / "numpyro" / "distributions" / "continuous.py"
RESULT = ROOT / "reproduction.json"


def extract_matrix_normal_block(text: str) -> str:
    start = text.index("class MatrixNormal(Distribution):")
    end = text.index("def _batch_mahalanobis", start)
    return text[start:end]


def numbered_lines(block: str, base_lineno: int) -> list[str]:
    return [
        f"{base_lineno + offset}: {line}"
        for offset, line in enumerate(block.splitlines())
        if line.strip()
    ]


def main() -> int:
    text = SOURCE.read_text(encoding="utf-8")
    block = extract_matrix_normal_block(text)
    base_lineno = text[: text.index("class MatrixNormal(Distribution):")].count("\n") + 1

    source_lines = numbered_lines(block, base_lineno)
    docstring_hits = [
        line
        for line in source_lines
        if "correlation matrix" in line or "lower_triangular parametrization" in line
    ]
    implementation_hits = [
        line
        for line in source_lines
        if "constraints.lower_cholesky" in line
        or "scale_tril_row @ eps @" in line
        or "U=scale_tril_row @ scale_tril_row" in line
        or "V=scale_tril_column @ scale_tril_column" in line
    ]

    reproducible = any("correlation matrix" in line for line in docstring_hits) and any(
        "constraints.lower_cholesky" in line for line in implementation_hits
    )

    evidence = {
        "docstring_lines": docstring_hits,
        "implementation_lines": implementation_hits,
        "interpretation": (
            "The docstring says 'correlation matrix' while the class enforces "
            "lower Cholesky factors and samples via matrix multiplication, which "
            "matches covariance factors."
        ),
    }

    payload = {
        "reproducible": reproducible,
        "evidence": evidence,
        "steps": [
            "Open codebase/numpyro/distributions/continuous.py.",
            "Inspect the MatrixNormal docstring at lines 1444-1452.",
            "Inspect arg_constraints and sample() at lines 1459-1500.",
            "Confirm the docstring says 'lower cholesky of rows/columns correlation matrix' while the implementation uses lower_cholesky factors and covariance-style sampling.",
        ],
        "blocking_reason": "" if reproducible else "Could not verify the docstring/implementation mismatch from the local source.",
        "reproduction_command": "bash run_repro.sh",
    }

    RESULT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
