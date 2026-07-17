#!/usr/bin/env python3
"""Minimal checkpoint saver probe for bug 627.

This exercises the code path reported in the issue with a tiny model and a
temporary local output directory. The reported FileNotFoundError does not
occur in this environment.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
import traceback
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"


def _build_model():
    import torch.nn as nn

    class TinyModel(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.fc = nn.Linear(2, 2)

    return TinyModel()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--max-history", type=int, default=3)
    args = parser.parse_args()

    sys.path.insert(0, str(CODEBASE))

    import torch
    from timm.utils.checkpoint_saver import CheckpointSaver

    workdir = Path(tempfile.mkdtemp(prefix="timm-checkpoint-probe-"))
    print(f"workdir={workdir}")
    try:
        model = _build_model()
        optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
        saver = CheckpointSaver(
            model=model,
            optimizer=optimizer,
            checkpoint_dir=str(workdir),
            recovery_dir=str(workdir),
            max_history=args.max_history,
        )

        for epoch in range(args.epochs):
            best_metric, best_epoch = saver.save_checkpoint(epoch, metric=float(epoch))
            files = sorted(p.name for p in workdir.iterdir())
            print(
                f"epoch={epoch} best_metric={best_metric} "
                f"best_epoch={best_epoch} files={files}"
            )

        print("completed_without_error=true")
        return 0
    except Exception:
        traceback.print_exc()
        return 1
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
