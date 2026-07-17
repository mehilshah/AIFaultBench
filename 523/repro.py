#!/usr/bin/env python3
"""Minimal reproducer for accelerate issue 1174.

Expected outcome in the affected source snapshot:
Accelerator(cpu=True).prepare(optimizer) raises an AssertionError from
AcceleratorState() inside AcceleratedOptimizer.__init__.
"""

import torch

from accelerate import Accelerator


def main():
    print(f"torch={torch.__version__}")
    try:
        import accelerate

        print(f"accelerate={accelerate.__version__}")
    except Exception:
        print("accelerate=<unknown>")

    model = torch.nn.Linear(10, 10)
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
    accelerator = Accelerator(cpu=True)

    print(f"accelerator.device={accelerator.device}")
    print(f"partial_state_cpu={accelerator.state._cpu}")

    # This call is the reported failure point.
    accelerator.prepare(optimizer)
    print("prepare completed without error")


if __name__ == "__main__":
    main()
