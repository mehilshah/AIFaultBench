from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))


def main() -> None:
    import torch
    from torchrl.data import LazyMemmapStorage, ReplayBuffer, TED2Flat

    print(f"torch={torch.__version__}")
    rb = ReplayBuffer(storage=LazyMemmapStorage(10))
    print(f"storage={type(rb._storage).__name__}")
    rb.register_save_hook(TED2Flat())


if __name__ == "__main__":
    main()
