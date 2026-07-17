from __future__ import annotations

import os
import sys
from pathlib import Path
from unittest import mock

import torch

ROOT = Path(__file__).resolve().parent
CODEBASE_SRC = ROOT / "codebase" / "src"
if str(CODEBASE_SRC) not in sys.path:
    sys.path.insert(0, str(CODEBASE_SRC))

import lightning.pytorch as pl  # noqa: E402
from lightning.pytorch.accelerators.cuda import CUDAAccelerator  # noqa: E402
from torch.utils.data import DataLoader, TensorDataset  # noqa: E402


class TinyModule(pl.LightningModule):
    def __init__(self) -> None:
        super().__init__()
        self.layer = torch.nn.Linear(4, 2)
        self.loss_fn = torch.nn.CrossEntropyLoss()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.layer(x)

    def training_step(self, batch: tuple[torch.Tensor, torch.Tensor], batch_idx: int) -> torch.Tensor:
        x, y = batch
        logits = self(x)
        loss = self.loss_fn(logits, y)
        self.log("train_loss", loss, prog_bar=False)
        return loss

    def configure_optimizers(self) -> torch.optim.Optimizer:
        return torch.optim.SGD(self.parameters(), lr=0.1)


def main() -> int:
    x = torch.zeros(8, 4)
    y = torch.zeros(8, dtype=torch.long)
    loader = DataLoader(TensorDataset(x, y), batch_size=4)

    print(f"python={sys.version.split()[0]}")
    print(f"lightning={pl.__version__}")
    print(f"cwd={os.getcwd()}")

    with (
        mock.patch.object(CUDAAccelerator, "is_available", return_value=True),
        mock.patch.object(CUDAAccelerator, "parse_devices", return_value=[0, 1]),
        mock.patch("torch.cuda.is_initialized", return_value=True),
        mock.patch("torch.cuda._is_in_bad_fork", None, create=True),
    ):
        trainer = pl.Trainer(
            accelerator="gpu",
            devices=2,
            strategy="ddp_notebook",
            max_epochs=1,
            logger=False,
            enable_checkpointing=False,
            enable_progress_bar=False,
            limit_train_batches=1,
        )

        try:
            trainer.fit(TinyModule(), train_dataloaders=loader)
        except RuntimeError as exc:
            message = str(exc)
            print("caught_runtime_error=1")
            print(message)
            if "Lightning can't create new processes if CUDA is already initialized" not in message:
                print("unexpected_runtime_error_message=1")
                return 1
            return 0

    print("caught_runtime_error=0")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
