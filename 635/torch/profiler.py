"""Minimal torch.profiler compatibility shim for the repro."""

from __future__ import annotations

from contextlib import contextmanager


class ProfilerActivity:
    CPU = "CPU"
    CUDA = "CUDA"


@contextmanager
def record_function(name):
    yield
