import os

import torch
from lightning import LightningModule, Trainer
from torch.utils.data import DataLoader, Dataset


class LargeTensorDataset(Dataset):
    def __init__(self, size: int = 50) -> None:
        self.size = size

    def __len__(self) -> int:
        return self.size

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor | int]:
        # Large tensors increase the chance of hitting the worker-shutdown race from the issue report.
        images = torch.randn(8, 640, 640, 3, dtype=torch.float64)
        return {"images": images, "index": idx}


class TestModel(LightningModule):
    def predict_step(self, batch, batch_idx, dataloader_idx=0):
        return batch


def main() -> None:
    num_workers = min(4, os.cpu_count() or 1)
    print(f"torch={torch.__version__}")
    print(f"workers={num_workers}")

    dataloader = DataLoader(
        LargeTensorDataset(),
        batch_size=8,
        num_workers=num_workers,
        multiprocessing_context="spawn",
        persistent_workers=True,
    )

    trainer = Trainer(max_epochs=1, limit_predict_batches=1, enable_progress_bar=False, logger=False)
    trainer.predict(model=TestModel(), dataloaders=dataloader)
    print("predict completed")


if __name__ == "__main__":
    main()
