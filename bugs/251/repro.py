#!/usr/bin/env python3
"""Benchmark the SliceSampler slowdown described in bug_report.txt."""

from __future__ import annotations

import json
import os
import timeit


def _install_tensordict_compat() -> None:
    """Bridge the old TorchRL import path to current tensordict names."""
    import tensordict.nn.probabilistic as probabilistic

    if not hasattr(probabilistic, "interaction_mode"):
        probabilistic.interaction_mode = probabilistic.interaction_type
    if not hasattr(probabilistic, "set_interaction_mode"):
        probabilistic.set_interaction_mode = probabilistic.set_interaction_type


def make_rb(*, use_slice_sampler: bool):
    import torch
    from tensordict import TensorDict
    from torchrl.data.replay_buffers import LazyTensorStorage, ReplayBuffer
    from torchrl.data.replay_buffers.samplers import SliceSampler

    torch.manual_seed(0)
    sampler = SliceSampler(num_slices=32) if use_slice_sampler else None
    rb = ReplayBuffer(
        sampler=sampler,
        storage=LazyTensorStorage(100),
        generator=torch.Generator(),
    )
    done = torch.zeros(100, 1, dtype=torch.bool)
    done[49] = 1
    done[-1] = 1
    data = TensorDict({("next", "done"): done}, batch_size=[100])
    rb.extend(data)
    return rb


def sample(rb, num_samples: int, sample_size: int) -> None:
    for _ in range(num_samples):
        rb.sample(sample_size)


def measure_time(num_samples: int, sample_size: int, *, use_slice_sampler: bool) -> float:
    rb = make_rb(use_slice_sampler=use_slice_sampler)
    timer = timeit.Timer(stmt=lambda: sample(rb, num_samples, sample_size))
    num_iters = 30
    return timer.timeit(num_iters) / num_iters


def main() -> int:
    _install_tensordict_compat()

    import torch
    import tensordict

    from torchrl.data.replay_buffers.samplers import SliceSampler  # noqa: F401

    num_samples = 10
    sample_size = 32

    t0 = measure_time(num_samples, sample_size, use_slice_sampler=False)
    t1 = measure_time(num_samples, sample_size, use_slice_sampler=True)
    factor = t1 / t0

    print(f"torch: {torch.__version__}")
    print(f"tensordict: {tensordict.__version__}")
    print(f"working_dir: {os.getcwd()}")
    print(f"Without SliceSampler: {t0} s")
    print(f"With SliceSampler: {t1} s")
    print(f"Slowdown factor: {factor}x")
    print(json.dumps({"reproducible": factor >= 10.0, "factor": factor}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
