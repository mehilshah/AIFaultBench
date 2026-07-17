from __future__ import annotations

import pathlib
import sys
import traceback


ROOT_DIR = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR / "codebase"))

import torch
from x_transformers.x_transformers import RotaryEmbedding


def main() -> None:
    torch.manual_seed(0)

    rotary = RotaryEmbedding(32, use_xpos=True)
    print("running RotaryEmbedding.forward_from_seq_len with use_xpos=True")
    print("seq_len=32")

    try:
        rotary.forward_from_seq_len(32)
    except Exception:
        print("forward_failed")
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
