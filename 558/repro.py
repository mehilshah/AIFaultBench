from __future__ import annotations

import os
import tempfile
from pathlib import Path
from unittest import mock

import torch
from jsonargparse import lazy_instance
from lightning import LightningDataModule
from lightning.pytorch.cli import LightningCLI, LRSchedulerCallable, OptimizerCallable
from lightning.pytorch.demos.boring_classes import BoringDataModule, BoringModel


class TestDataSaveHparams(BoringDataModule):
    def __init__(self, batch_size: int = 32, num_workers: int = 4):
        super().__init__()
        self.save_hyperparameters()
        self.batch_size = batch_size
        self.num_workers = num_workers


class TestModelSaveHparams(BoringModel):
    def __init__(
        self,
        optimizer: OptimizerCallable = torch.optim.Adam,
        scheduler: LRSchedulerCallable = torch.optim.lr_scheduler.ConstantLR,
        activation: torch.nn.Module = lazy_instance(torch.nn.LeakyReLU, negative_slope=0.05),
    ):
        super().__init__()
        self.save_hyperparameters()
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.activation = activation

    def configure_optimizers(self):
        optimizer = self.optimizer(self.parameters())
        scheduler = self.scheduler(optimizer)
        return {"optimizer": optimizer, "lr_scheduler": scheduler}


def main() -> int:
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        with mock.patch(
            "sys.argv",
            [
                "any.py",
                "--trainer.max_epochs=1",
                "--trainer.limit_train_batches=1",
                "--trainer.limit_val_batches=0",
                "--trainer.enable_model_summary=False",
                "--model=TestModelSaveHparams",
                "--data=TestDataSaveHparams",
            ],
        ):
            cli = LightningCLI(
                run=False,
                auto_configure_optimizers=False,
            )

        cli.trainer.fit(cli.model, datamodule=cli.datamodule)

        checkpoint_path = next(Path(cli.trainer.log_dir, "checkpoints").glob("*.ckpt"), None)
        if checkpoint_path is None:
            print("checkpoint_path=None")
            return 1

        print(f"checkpoint_path={checkpoint_path}")
        loaded_checkpoint = torch.load(checkpoint_path, weights_only=True)
        dm_hparams = loaded_checkpoint[LightningDataModule.CHECKPOINT_HYPER_PARAMS_KEY]
        print(f"saved_datamodule_hparams={dm_hparams}")

        dm = LightningDataModule.load_from_checkpoint(checkpoint_path)
        print(f"loaded_type={type(dm).__module__}.{type(dm).__name__}")
        print(f"expected_type={TestDataSaveHparams.__module__}.{TestDataSaveHparams.__name__}")
        print(f"batch_size={getattr(dm, 'batch_size', None)}")
        print(f"num_workers={getattr(dm, 'num_workers', None)}")

        if isinstance(dm, TestDataSaveHparams):
            print("unexpectedly_restored_subclass=True")
            return 1

        print("unexpectedly_restored_subclass=False")
        print("reproducible=True")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
