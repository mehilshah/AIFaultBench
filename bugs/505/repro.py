#!/usr/bin/env python3
from __future__ import annotations

import sys

import torch


class CpuGpuBuffer:
    """Small helper that matches the relevant vLLM buffer behavior."""

    def __init__(self, size: int, *, dtype: torch.dtype, device: torch.device):
        with torch.inference_mode(False):
            self.cpu = torch.zeros(size, dtype=dtype, device="cpu", pin_memory=True)
            self.gpu = torch.zeros_like(self.cpu, device=device)

    def copy_to_gpu(self, n: int | None = None) -> torch.Tensor:
        if n is None:
            return self.gpu.copy_(self.cpu, non_blocking=True)
        return self.gpu[:n].copy_(self.cpu[:n], non_blocking=True)


def sigmoid_score(value: torch.Tensor) -> float:
    return torch.sigmoid((value.float() - 50.0) / 5.0).item()


def main() -> int:
    if not torch.cuda.is_available():
        print("CUDA is not available in this environment.", file=sys.stderr)
        return 2

    device = torch.device("cuda:0")
    copy_stream = torch.cuda.Stream(device=device)
    read_stream = torch.cuda.Stream(device=device)

    # Large enough to make the async copy visibly race the consumer.
    # 256 MiB of int32 values.
    buf = CpuGpuBuffer(64 * 1024 * 1024, dtype=torch.int32, device=device)

    buf.cpu.zero_()
    buf.cpu[-1] = 100

    with torch.cuda.stream(copy_stream):
        buf.copy_to_gpu()

    with torch.cuda.stream(read_stream):
        stale_value = buf.gpu[-1].clone()

    read_stream.synchronize()
    observed = int(stale_value.item())
    async_score = sigmoid_score(stale_value)

    torch.cuda.synchronize()
    synced_value = int(buf.gpu[-1].item())
    synced_score = sigmoid_score(buf.gpu[-1])

    print(f"async_read_value={observed}")
    print(f"async_read_score={async_score:.8f}")
    print(f"sync_read_value={synced_value}")
    print(f"sync_read_score={synced_score:.8f}")

    if observed != 100:
        print(
            "REPRODUCED: the unsynchronized consumer observed stale data "
            "from the async GPU copy."
        )
        return 0

    print(
        "No mismatch observed in this run; rerun if you need another sample."
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
