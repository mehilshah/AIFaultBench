from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase" / "src"))

import torch
from torch import nn

import lightning
from lightning.pytorch.plugins import MixedPrecision


def main() -> None:
    model = nn.Linear(10, 1)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, fused=True)
    precision = MixedPrecision(precision="bf16-mixed", device="cpu")

    print(f"lightning_version={lightning.__version__}")
    print(f"precision={precision.precision}")
    print(f"scaler_is_none={precision.scaler is None}")
    print(f"optimizer_type={type(optimizer).__name__}")
    print(f"step_supports_amp_scaling={getattr(optimizer, '_step_supports_amp_scaling', None)}")

    try:
        precision.clip_gradients(optimizer, clip_val=1.0)
    except Exception as exc:  # pragma: no cover - runtime evidence only
        print(f"unexpected_exception={type(exc).__name__}: {exc}")
        raise

    print("clip_gradients_completed_without_runtimeerror=True")


if __name__ == "__main__":
    main()
