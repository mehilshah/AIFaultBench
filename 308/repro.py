from __future__ import annotations

import sys
from pathlib import Path

import torch

SCRIPT_DIR = Path(__file__).resolve().parent
CODEBASE_DIR = SCRIPT_DIR / "codebase"
sys.path.insert(0, str(CODEBASE_DIR))

from torchrl.data import ListStorage, ReplayBuffer  # noqa: E402


def main() -> None:
    print(f"torch={torch.__version__}")

    rb = ReplayBuffer(
        storage=ListStorage(max_size=100),
        batch_size=2,
        prefetch=1,
    )
    rb.extend(torch.arange(100))

    _ = rb.sample()
    queue_length = len(rb._prefetch_queue)
    print(f"prefetch_queue_length={queue_length}")

    assert (
        queue_length == 1
    ), f"Bug present: Expected prefetch queue to have 1 item, but got {queue_length}."


if __name__ == "__main__":
    main()

