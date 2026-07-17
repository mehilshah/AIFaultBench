#!/usr/bin/env python3
"""Minimal hook-order check for Lightning issue 21428.

The bug report claims that `on_validation_epoch_end` can run before the optimizer
step. This script records the actual hook order for a tiny train/validation run
and exits non-zero only if that ordering is observed.
"""

from __future__ import annotations

import json

import torch
import lightning.pytorch as pl
from torch.utils.data import DataLoader, TensorDataset

EVENTS: list[str] = []


class HookOrderModel(pl.LightningModule):
    def __init__(self) -> None:
        super().__init__()
        self.layer = torch.nn.Linear(4, 2)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.layer(x)

    def training_step(self, batch, batch_idx):
        EVENTS.append(f"training_step:{self.current_epoch}:{batch_idx}")
        x, y = batch
        loss = torch.nn.functional.cross_entropy(self(x), y)
        return loss

    def validation_step(self, batch, batch_idx):
        EVENTS.append(f"validation_step:{self.current_epoch}:{batch_idx}")
        x, y = batch
        loss = torch.nn.functional.cross_entropy(self(x), y)
        self.log("val_loss", loss)

    def on_validation_epoch_end(self) -> None:
        EVENTS.append(f"on_validation_epoch_end:{self.current_epoch}")

    def optimizer_step(self, epoch, batch_idx, optimizer, optimizer_closure, **kwargs):
        EVENTS.append(f"optimizer_step:{epoch}:{batch_idx}")
        return super().optimizer_step(epoch, batch_idx, optimizer, optimizer_closure, **kwargs)

    def configure_optimizers(self):
        return torch.optim.SGD(self.parameters(), lr=0.1)


def main() -> int:
    x = torch.randn(4, 4)
    y = torch.randint(0, 2, (4,))
    loader = DataLoader(TensorDataset(x, y), batch_size=2)

    trainer = pl.Trainer(
        max_epochs=1,
        limit_train_batches=1,
        limit_val_batches=1,
        num_sanity_val_steps=0,
        enable_model_summary=False,
        logger=False,
        enable_checkpointing=False,
        accelerator="cpu",
        devices=1,
    )
    trainer.fit(HookOrderModel(), train_dataloaders=loader, val_dataloaders=loader)

    optimizer_idx = next(i for i, event in enumerate(EVENTS) if event.startswith("optimizer_step"))
    val_end_idx = next(i for i, event in enumerate(EVENTS) if event.startswith("on_validation_epoch_end"))
    order_ok = optimizer_idx < val_end_idx

    print("EVENTS:", json.dumps(EVENTS))
    print("optimizer_step_before_validation_epoch_end:", order_ok)
    return 0 if order_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
