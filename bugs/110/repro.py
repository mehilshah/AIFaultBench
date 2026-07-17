#!/usr/bin/env python3
"""Minimal reproduction for safetensors error pickling in a multi-worker DataLoader."""

from __future__ import annotations

import safetensors
import safetensors.torch
import torch
import torch.utils.data

NUM_ITEMS = 5
CATCH_EXCEPTION = False
DATA_FILE = "my_tensor.safetensors"


class SafeTensorDataset(torch.utils.data.Dataset):
    def __init__(self) -> None:
        super().__init__()
        # Create a small safetensors file so the worker failure comes from lookup time.
        data = {str(i): torch.ones((1,)) for i in range(NUM_ITEMS)}
        safetensors.torch.save_file(data, DATA_FILE)

    def __getitem__(self, idx: int):
        with safetensors.safe_open(DATA_FILE, framework="pt", device="cpu") as f:
            if CATCH_EXCEPTION:
                try:
                    return f.get_tensor(str(idx))
                except Exception as e:
                    raise Exception(str(e))
            return f.get_tensor(str(idx))

    def __len__(self) -> int:
        return NUM_ITEMS + 1


def main() -> None:
    print(f"safetensors={safetensors.__version__}")
    print(f"torch={torch.__version__}")
    print(f"CATCH_EXCEPTION={CATCH_EXCEPTION}")
    dataset = SafeTensorDataset()
    dataloader = torch.utils.data.DataLoader(dataset, num_workers=2)

    for i, batch in enumerate(dataloader):
        print(f"Retrieved batch {i}: {batch}")

    print("Completed without error")


if __name__ == "__main__":
    torch.multiprocessing.set_start_method("fork", force=True)
    main()
