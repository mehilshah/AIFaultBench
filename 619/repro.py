#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import traceback
import warnings
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
if CODEBASE.exists() and str(CODEBASE) not in sys.path:
    sys.path.insert(0, str(CODEBASE))

RESULT_PATH = ROOT / "reproduction.json"
STDOUT_LOG = ROOT / "repro_stdout.log"
STDERR_LOG = ROOT / "repro_stderr.log"
REPRO_COMMAND = "bash run_repro.sh"


def write_result(
    *,
    reproducible: bool,
    evidence: str,
    steps: list[str],
    blocking_reason: str | None,
) -> None:
    payload = {
        "reproducible": reproducible,
        "evidence": evidence,
        "steps": steps,
        "blocking_reason": blocking_reason,
        "reproduction_command": REPRO_COMMAND,
    }
    RESULT_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def main() -> int:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    import pytorch_lightning as pl
    from torch_geometric.data import Data
    from torch_geometric.loader import DataLoader
    from torch_geometric.nn import global_mean_pool

    print(f"torch={torch.__version__}")
    print(f"pytorch_lightning={pl.__version__}")

    class Model(pl.LightningModule):
        def __init__(self) -> None:
            super().__init__()
            self.lin = nn.Linear(4, 1)

        def forward(self, x: torch.Tensor, batch: torch.Tensor) -> torch.Tensor:
            return self.lin(global_mean_pool(x, batch))

        def validation_step(self, batch: Data, batch_idx: int):
            y_pred = self(batch.x, batch.batch)
            loss = F.mse_loss(y_pred.view(-1), batch.y.view(-1))
            batch_size = batch.num_graphs

            # This is the trigger from the bug report: an unannotated scalar log
            # makes Lightning infer batch_size from the graph batch.
            self.log("val_loss", loss)
            self.log(
                "val_mae",
                torch.abs(y_pred.view(-1) - batch.y.view(-1)).mean(),
                batch_size=batch_size,
                on_step=True,
                on_epoch=True,
                prog_bar=True,
            )
            return loss

        def configure_optimizers(self):
            return torch.optim.SGD(self.parameters(), lr=0.1)

    data = Data(x=torch.randn(3161, 4), y=torch.tensor([1.0]))
    loader = DataLoader([data], batch_size=1)
    trainer = pl.Trainer(
        accelerator="cpu",
        devices=1,
        logger=False,
        enable_checkpointing=False,
        enable_model_summary=False,
        enable_progress_bar=False,
        limit_val_batches=1,
        max_epochs=1,
    )

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        warnings.filterwarnings(
            "ignore",
            message=".*does not have many workers.*",
        )
        trainer.validate(Model(), dataloaders=loader, verbose=False)

    warning_messages = [str(item.message) for item in caught]
    relevant = [
        message for message in warning_messages
        if "Trying to infer the `batch_size` from an ambiguous collection" in message
    ]

    for message in warning_messages:
        print(f"warning: {message}")

    reproducible = bool(relevant)
    evidence = (
        "Lightning emitted the ambiguous batch-size warning during validation. "
        f"Captured warning(s): {relevant or warning_messages}"
    )
    steps = [
        "Create a single-graph PyG `Data` object with 3161 nodes.",
        "Run `pytorch_lightning.Trainer.validate` on a module whose `validation_step` calls `self.log('val_loss', loss)` without `batch_size`.",
        "Observe Lightning warn that it inferred batch size 3161 from an ambiguous collection, even though the other metric log passes `batch_size=batch.num_graphs`.",
    ]

    if reproducible:
        write_result(
            reproducible=True,
            evidence=evidence,
            steps=steps,
            blocking_reason=None,
        )
        return 0

    write_result(
        reproducible=False,
        evidence=evidence,
        steps=steps,
        blocking_reason="Lightning did not emit the ambiguous batch-size warning in this environment.",
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover - defensive fallback
        traceback.print_exc()
        write_result(
            reproducible=False,
            evidence=f"Repro script failed before reaching the validation step: {exc!r}",
            steps=[
                "Create the Lightning validation script.",
                "Install the pinned Torch and PyTorch Lightning dependencies.",
                "Run the validation step and capture any failure.",
            ],
            blocking_reason=f"{type(exc).__name__}: {exc}",
        )
        raise
