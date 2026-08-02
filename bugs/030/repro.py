#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pytorch_lightning as pl
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


class SchedulerBugModule(pl.LightningModule):
    def __init__(self):
        super().__init__()
        self.weight = nn.Parameter(torch.tensor(1.0))

    def training_step(self, batch, batch_idx):
        return self.weight * batch[0].sum()

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        scheduler = torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(
            optimizer, 4096, eta_min=8e-5
        )
        return {"optimizer": optimizer, "monitor": "val_loss", "lr_scheduler": scheduler}

    def train_dataloader(self):
        data = TensorDataset(torch.ones(2, 1))
        return DataLoader(data, batch_size=1)


def main():
    print(f"torch={torch.__version__}")
    print(f"pytorch_lightning={pl.__version__}")
    trainer = pl.Trainer(
        max_epochs=1,
        accelerator="cpu",
        devices=1,
        logger=False,
        enable_checkpointing=False,
    )
    trainer.fit(SchedulerBugModule())


if __name__ == "__main__":
    main()
