#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys
import tempfile

import torch
from tensordict import TensorDict


ROOT_DIR = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR / "codebase"))

from torchrl.data import LazyMemmapStorage, TensorDictReplayBuffer


class CustomTransform:
    def __call__(self, tensordict: TensorDict) -> TensorDict:
        # Match the issue report: construct a new TensorDict without an explicit device.
        return TensorDict({"observation": tensordict["observation"]}, batch_size=10)


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="torchrl-repro-") as scratch_dir:
        rb = TensorDictReplayBuffer(
            storage=LazyMemmapStorage(1000, scratch_dir=scratch_dir),
            pin_memory=True,
            transform=CustomTransform(),
        )

        for _ in range(100):
            td = TensorDict({"observation": torch.randn(10, 4)}, batch_size=[10])
            rb.add(td)

        sample = rb.sample(10)
        print(f"torch={torch.__version__}")
        print(f"sample.device={sample.device}")
        print(f"observation.device={sample['observation'].device}")
        print(f"observation.is_pinned={sample['observation'].is_pinned()}")

        assert sample.device is None
        assert sample["observation"].device.type == "cpu"
        assert not sample["observation"].is_pinned()
        print("reproducible=True")


if __name__ == "__main__":
    main()
