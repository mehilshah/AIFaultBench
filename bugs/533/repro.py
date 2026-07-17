import os

import torch
import torch.nn.functional as F
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

import lightning.pytorch as L


class SimpleModel(L.LightningModule):
    def __init__(self) -> None:
        super().__init__()
        self.layer = nn.Linear(10, 10)
        self.automatic_optimization = False

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.layer(x)

    def training_step(self, batch, batch_idx):
        # This is the path reported in the issue: compiled training_step + toggle_optimizer.
        self.toggle_optimizer(self.optimizers())
        x, y = batch
        y_hat = self(x)
        loss = F.mse_loss(y_hat, y)
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=0.02)


def main() -> None:
    torch.manual_seed(1234)

    x = torch.randn(4, 10)
    y = torch.randn(4, 10)
    loader = DataLoader(TensorDataset(x, y), batch_size=2)

    model = SimpleModel()
    model = torch.compile(model)

    trainer = L.Trainer(
        max_epochs=1,
        limit_train_batches=1,
        limit_val_batches=0,
        logger=False,
        enable_checkpointing=False,
    )
    trainer.fit(model, loader)


if __name__ == "__main__":
    os.environ.setdefault("PYTHONWARNINGS", "ignore")
    main()
