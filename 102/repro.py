from __future__ import annotations

import pathlib
import sys
import traceback

import torch


ROOT = pathlib.Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
sys.path.insert(0, str(CODEBASE))

from vector_quantize_pytorch import ResidualSimVQ  # noqa: E402


def main() -> int:
    torch.manual_seed(0)

    model = ResidualSimVQ(
        dim=512,
        num_quantizers=4,
        codebook_size=1024,
        quantize_dropout=True,
        channel_first=True,
    )

    x = torch.randn(1, 512, 32, 32)

    try:
        model(x)
    except Exception as exc:
        print(f"type={type(exc).__name__}")
        print(f"message={exc}")
        traceback.print_exc()
        return 1

    print("ResidualSimVQ.forward completed without error")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
