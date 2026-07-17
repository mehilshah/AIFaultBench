#!/usr/bin/env python3
from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))

import torch
from tensordict import TensorDict
from torchrl.data import LazyMemmapStorage


def format_tensor(tensor: torch.Tensor) -> str:
    return repr(tensor.cpu())


def main() -> int:
    workdir = Path(tempfile.mkdtemp(prefix="bug210_"))
    storage_path = workdir / "storage"
    storage_path.mkdir(parents=True, exist_ok=True)

    try:
        # First run: matches the issue report's working example.
        storage = LazyMemmapStorage(1000, scratch_dir=str(storage_path))
        data1 = TensorDict({"a": torch.zeros(5, 3) + 1, "d": torch.zeros(5, 1) + 1}, [5])
        storage.set(range(5), data1)
        data2 = TensorDict({"a": torch.zeros(1, 3) + 2}, [1])
        storage.set(range(5, 6), data2)
        first_run = storage["d"].clone()
        print("first_run_d =", format_tensor(first_run))

        # Second run: reuse the same scratch dir and write a partial tensordict.
        storage = LazyMemmapStorage(1000, scratch_dir=str(storage_path))
        data1 = TensorDict({"a": torch.zeros(1, 3) + 1, "d": torch.zeros(1, 1) + 1}, [1])
        storage.set(range(1), data1)
        data2 = TensorDict({"a": torch.zeros(5, 3) + 2}, [5])
        storage.set(range(1, 6), data2)
        second_run = storage["d"].clone()
        expected = torch.tensor([[1.0], [0.0], [0.0], [0.0], [0.0], [0.0]])

        print("second_run_d =", format_tensor(second_run))
        print("expected_d   =", format_tensor(expected))

        if torch.equal(second_run, expected):
            print("BUG_NOT_REPRODUCED")
            return 1

        print("BUG_REPRODUCED")
        return 0
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
