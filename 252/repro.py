from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import tempfile

import torch

import torchrl.data.replay_buffers.samplers as samplers


class FakeSegmentTree:
    """Small pure-Python stand-in for the missing compiled segment trees."""

    def __init__(self, capacity: int):
        self.data = torch.zeros(capacity, dtype=torch.float64)

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        self.data[index] = torch.as_tensor(value, dtype=self.data.dtype)

    def query(self, start: int, end: int):
        return self.data[start:end].sum().item()

    def scan_lower_bound(self, mass):
        masses = torch.as_tensor(mass, dtype=torch.float64).reshape(-1)
        result = []
        for target in masses.tolist():
            total = 0.0
            chosen = len(self.data) - 1
            for idx, value in enumerate(self.data.tolist()):
                total += float(value)
                if total >= target:
                    chosen = idx
                    break
            result.append(chosen)
        return torch.tensor(result, dtype=torch.long)

    def __deepcopy__(self, memo):
        clone = type(self)(len(self.data))
        clone.data = self.data.clone()
        return clone


# Replace the missing C++ segment-tree symbols with the pure-Python shim above.
samplers.SumSegmentTreeFp32 = FakeSegmentTree
samplers.MinSegmentTreeFp32 = FakeSegmentTree
samplers.SumSegmentTreeFp64 = FakeSegmentTree
samplers.MinSegmentTreeFp64 = FakeSegmentTree


def main() -> None:
    size = 100
    sampler = samplers.PrioritizedSampler(max_capacity=size, alpha=0.6, beta=0.4)
    sampler.update_priority(torch.tensor([0, 1]), torch.tensor([1.0, 2.0]))

    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        sampler.dumps(path)
        print(f"dumped sampler state to {path}")

        loaded = samplers.PrioritizedSampler(max_capacity=size, alpha=0.6, beta=0.4)
        print(f"fresh sampler max priority before load: {loaded._max_priority}")
        loaded.loads(path)
        print("unexpected success: load completed without error")


if __name__ == "__main__":
    main()
