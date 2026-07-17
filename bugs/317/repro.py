#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
import traceback
from pathlib import Path

import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

import lightning.pytorch as pl
from lightning.pytorch.tuner.tuning import Tuner


class TorchCoder(nn.Module):
    def __init__(self, in_features: int, out_features: int) -> None:
        super().__init__()
        self.net = nn.Linear(in_features, out_features)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class SimpleModel(pl.LightningModule):
    def __init__(self, coder: TorchCoder, loss: nn.Module, lr: float = 1e-3) -> None:
        super().__init__()
        self.save_hyperparameters()
        self.layer = nn.Linear(4, 2)
        self.loss = loss
        self.lr = lr

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self.layer(x)
        return nn.functional.mse_loss(y_hat, y)

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.lr)


def build_loader() -> DataLoader:
    x = torch.randn(8, 4)
    y = torch.randn(8, 2)
    return DataLoader(TensorDataset(x, y), batch_size=4)


def main() -> int:
    root = Path(__file__).resolve().parent
    result_path = root / "reproduction.json"

    steps = [
        "Install torch 2.6.0+cpu and the Lightning runtime deps in an isolated venv.",
        "Fit a simple LightningModule that stores a custom nn.Module in hyperparameters and save a checkpoint.",
        "Verify the checkpoint loads with `torch.load(..., weights_only=False)`.",
        "Call `Tuner(trainer).lr_find(...)` on a fresh trainer and observe the restore-time UnpicklingError.",
    ]

    evidence_lines: list[str] = []
    reproducible = False
    blocking_reason = ""

    with tempfile.TemporaryDirectory(prefix="lrfinder_bug_") as tmp:
        workdir = Path(tmp)
        loader = build_loader()

        model = SimpleModel(TorchCoder(4, 2), loss=nn.MSELoss())
        trainer = pl.Trainer(
            default_root_dir=workdir / "fit",
            max_epochs=1,
            logger=False,
            enable_checkpointing=False,
            enable_model_summary=False,
            accelerator="cpu",
            devices=1,
            limit_train_batches=1,
        )
        trainer.fit(model, train_dataloaders=loader)

        manual_ckpt = workdir / "manual.ckpt"
        trainer.save_checkpoint(manual_ckpt)
        manual_loaded = torch.load(manual_ckpt, weights_only=False)
        evidence_lines.append(f"Manual checkpoint load with weights_only=False succeeded: {sorted(manual_loaded.keys())[:5]}")

        trainer2 = pl.Trainer(
            default_root_dir=workdir / "lr_find",
            max_epochs=1,
            logger=False,
            enable_checkpointing=True,
            enable_model_summary=False,
            accelerator="cpu",
            devices=1,
            limit_train_batches=1,
        )

        try:
            Tuner(trainer2).lr_find(
                SimpleModel(TorchCoder(4, 2), loss=nn.MSELoss()),
                train_dataloaders=loader,
                num_training=1,
            )
            evidence_lines.append("lr_find completed without error.")
        except Exception as exc:  # noqa: BLE001
            reproducible = True
            blocking_reason = ""
            evidence_lines.append(f"lr_find raised {exc.__class__.__name__}: {exc}")
            evidence_lines.append(traceback.format_exc())

    result = {
        "reproducible": reproducible,
        "evidence": "\n".join(evidence_lines),
        "steps": steps,
        "blocking_reason": blocking_reason,
        "reproduction_command": "bash run_repro.sh",
    }
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(json.dumps(result, indent=2))
    return 0 if reproducible else 1


if __name__ == "__main__":
    raise SystemExit(main())
