#!/usr/bin/env python3
"""Minimal reproduction for the inherited ignore bug in save_hyperparameters."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase" / "src"))

from lightning.pytorch import LightningModule  # noqa: E402


class BaseModel(LightningModule):
    def __init__(self, arg1, arg2):
        super().__init__()
        self.save_hyperparameters()


class ChildModel(BaseModel):
    def __init__(self, arg1, arg2):
        super().__init__(arg1, arg2)
        self.save_hyperparameters(ignore="arg2")


def main() -> None:
    model = ChildModel(arg1=1, arg2=2)
    hparams = dict(model.hparams)
    print(f"hparams={hparams}")
    if "arg2" in model.hparams:
        raise AssertionError("arg2 unexpectedly persisted in hparams")
    print("arg2 correctly removed")


if __name__ == "__main__":
    main()
