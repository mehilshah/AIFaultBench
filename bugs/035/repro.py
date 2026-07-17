#!/usr/bin/env python3
"""Reproduce the RoPE shape mismatch from labml_nn.transformers.rope."""

from pathlib import Path
import sys

import torch


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))

from labml_nn.transformers.rope import RotaryPositionalEmbeddings


def main() -> None:
    x = torch.tensor(
        [[1, 2, 3, 4], [4, 5, 6, 7], [7, 8, 9, 10]],
        dtype=torch.float,
    )[:, None, None, :]
    print(f"input_shape={tuple(x.shape)}")

    rotary_pe = RotaryPositionalEmbeddings(3)
    print(f"rotary_d={rotary_pe.d}")
    print("calling_forward")
    y = rotary_pe(x)
    print(f"output_shape={tuple(y.shape)}")


if __name__ == "__main__":
    main()
