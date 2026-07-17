#!/usr/bin/env python3
"""Minimal reproduction for mixed-import callback validation in Lightning."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODEBASE_SRC = ROOT / "codebase" / "src"
sys.path.insert(0, str(CODEBASE_SRC))

from lightning.pytorch import Trainer  # noqa: E402
from lightning.pytorch.callbacks import Callback as NewCallback  # noqa: E402
from pytorch_lightning.callbacks import Callback as OldCallback  # noqa: E402


class MyCallback(OldCallback):
    pass


def main() -> None:
    print(f"new_callback_module={NewCallback.__module__}", flush=True)
    print(f"old_callback_module={OldCallback.__module__}", flush=True)
    print(f"my_callback_module={MyCallback.__module__}", flush=True)
    print(f"isinstance(MyCallback, NewCallback)={isinstance(MyCallback, NewCallback)}", flush=True)
    print("creating Trainer(callbacks=[MyCallback])", flush=True)
    Trainer(
        callbacks=[MyCallback],
        logger=False,
        enable_checkpointing=False,
        enable_progress_bar=False,
        enable_model_summary=False,
    )


if __name__ == "__main__":
    main()
