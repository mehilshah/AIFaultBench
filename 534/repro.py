from __future__ import annotations

import shutil
import sys
from pathlib import Path

import torch
from accelerate import Accelerator
from accelerate.utils import ProjectConfiguration


def main() -> int:
    root = Path(__file__).resolve().parent
    project_dir = root / "total_limit_test"

    if project_dir.exists():
        shutil.rmtree(project_dir)

    config = ProjectConfiguration(
        project_dir=str(project_dir),
        total_limit=3,
        automatic_checkpoint_naming=True,
    )
    accelerator = Accelerator(project_dir=str(project_dir), project_config=config)

    model = torch.nn.Linear(1, 1)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    scheduler = torch.optim.lr_scheduler.ConstantLR(optimizer, factor=1.0, total_iters=1)

    model, optimizer, scheduler = accelerator.prepare(model, optimizer, scheduler)

    for _ in range(20):
        accelerator.save_state()

    checkpoint_root = project_dir / "checkpoints"
    actual = sorted(p.name for p in checkpoint_root.iterdir() if p.is_dir())
    expected = [f"checkpoint_{i}" for i in range(17, 20)]

    print(f"project_dir={project_dir}")
    print(f"checkpoint_root={checkpoint_root}")
    print(f"expected_latest={expected}")
    print(f"actual_retained={actual}")

    if actual != expected:
        print("BUG_REPRODUCED: save_state pruned the wrong checkpoint folders.")
        return 0

    print("BUG_NOT_REPRODUCED: checkpoint pruning kept the latest three folders.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
