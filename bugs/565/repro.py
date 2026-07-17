#!/usr/bin/env python3
"""Minimal GPU repro for the TraceEnum_ELBO memory leak.

This script mirrors the issue report's one-site discrete model, but marks the
site for model-side parallel enumeration so the TraceEnum_ELBO code path is
actually exercised.
"""

from __future__ import annotations

import gc
import sys

import torch


def main() -> int:
    if not torch.cuda.is_available():
        print("CUDA is not available on this machine.")
        return 2

    # The local Pyro snapshot expects a Torch 1.x version string, but the GPU
    # in this environment requires a much newer CUDA wheel. Patch the reported
    # version before importing pyro so the source stays unchanged.
    real_torch_version = torch.__version__
    torch.__version__ = "1.10.0"

    import pyro
    import pyro.distributions as dist
    from pyro.infer import SVI, TraceEnum_ELBO
    from pyro.optim import Adam

    print(f"torch_real={real_torch_version}")
    print(f"torch_reported={torch.__version__}")
    print(f"cuda_capability={torch.cuda.get_device_capability(0)}")

    pyro.clear_param_store()
    pyro.set_rng_seed(0)

    accept_ratio = 0.5
    ones = torch.ones((), device="cuda")
    ratio = 1 / (accept_ratio + 1)
    alpha_prior = torch.stack(
        (ones - ratio, ones - accept_ratio * ratio)
    )

    def model():
        pyro.sample(
            "y",
            dist.OneHotCategorical(alpha_prior),
            infer={"enumerate": "parallel"},
        )

    def guide():
        pass

    svi = SVI(
        model,
        guide,
        Adam({"lr": 1e-4}),
        loss=TraceEnum_ELBO(
            max_plate_nesting=0,
            strict_enumeration_warning=False,
        ),
    )

    torch.cuda.empty_cache()
    allocations = []
    for step in range(200):
        loss = svi.step()
        gc.collect()
        torch.cuda.synchronize()
        allocated = torch.cuda.memory_allocated()
        reserved = torch.cuda.memory_reserved()
        allocations.append(allocated)
        if step % 20 == 0:
            print(
                f"step={step} loss={loss} allocated={allocated} reserved={reserved}"
            )

    delta = allocations[-1] - allocations[0]
    ups = sum(b > a for a, b in zip(allocations, allocations[1:]))
    print(f"start={allocations[0]} end={allocations[-1]} delta={delta} ups={ups}")

    if delta <= 0:
        print("Expected GPU memory to grow, but it stayed flat.", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
