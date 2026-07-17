#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))

from vector_quantize_pytorch.residual_vq import ResidualVQ  # noqa: E402


def main() -> None:
    rvq = ResidualVQ(
        dim=8,
        num_quantizers=4,
        codebook_size=16,
        implicit_neural_codebook=False,
    )

    num_mlps = len(rvq.mlps)
    print(f"implicit_neural_codebook={rvq.implicit_neural_codebook}")
    print(f"num_quantizers={rvq.num_quantizers}")
    print(f"initialized_mlps={num_mlps}")
    print("expected_initialized_mlps=0")

    if num_mlps != 0:
        raise AssertionError(
            "ResidualVQ initialized MLP modules even though "
            "implicit_neural_codebook=False"
        )


if __name__ == "__main__":
    main()
