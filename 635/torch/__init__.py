"""Minimal torch compatibility shim for the repro."""

from __future__ import annotations

from . import profiler


class _Cuda:
    def empty_cache(self):
        return None

    def reset_max_memory_allocated(self):
        return None

    def reset_peak_memory_stats(self):
        return None

    def synchronize(self):
        return None


cuda = _Cuda()
bfloat16 = "bfloat16"


__all__ = ["bfloat16", "cuda", "profiler"]
