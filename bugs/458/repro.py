import sys
import traceback
from pathlib import Path

import torch

ROOT_DIR = Path(__file__).resolve().parent
CODEBASE_DIR = ROOT_DIR / "codebase"
if CODEBASE_DIR.exists():
    sys.path.insert(0, str(CODEBASE_DIR))

from torchrl.data import LazyTensorStorage, PrioritizedSampler, TensorDictReplayBuffer


def main() -> int:
    print(f"torch={torch.__version__}")
    print(f"cuda_available={torch.cuda.is_available()}")

    device = torch.device("cuda:0")
    print(f"device={device}")

    try:
        TensorDictReplayBuffer(
            storage=LazyTensorStorage(max_size=100, device=device),
            batch_size=4,
            sampler=PrioritizedSampler(
                max_capacity=100,
                alpha=0.7,
                beta=0.5,
                dtype=torch.float,
            ),
            priority_key="priority",
        )
    except Exception:
        traceback.print_exc()
        return 1

    print("PrioritizedSampler initialized successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main())
