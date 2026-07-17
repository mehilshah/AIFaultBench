from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import torch


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase" / "src"
sys.path.insert(0, str(CODEBASE))

from liger_kernel.ops import fused_linear_cross_entropy as flce


def load_module(module_name: str, relative_path: str):
    module_path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DummyKernel:
    def __getitem__(self, grid):
        def launch(**kwargs):
            loss_ptr = kwargs["loss_ptr"]
            x_ptr = kwargs["X_ptr"]
            loss_ptr.copy_(
                torch.arange(
                    loss_ptr.numel(), device=loss_ptr.device, dtype=loss_ptr.dtype
                )
                + 1
            )
            x_ptr.zero_()

        return launch


def main() -> None:
    flce.liger_cross_entropy_kernel = DummyKernel()

    transformers_mod = load_module(
        "repro_liger_kernel_transformers_fused_linear_cross_entropy",
        "codebase/src/liger_kernel/transformers/fused_linear_cross_entropy.py",
    )
    loss_cls = transformers_mod.LigerFusedLinearCrossEntropyLoss

    weight = torch.randn(4, 3)
    hidden = torch.randn(2, 3)
    target = torch.tensor([1, 2], dtype=torch.long)

    loss = loss_cls(reduction="none")(weight, hidden, target)

    print("reduction=none output:", loss)
    print("output.shape:", tuple(loss.shape))
    print("output.ndim:", loss.ndim)
    print("expected shape for unreduced loss: (batch_tokens,)")


if __name__ == "__main__":
    main()
