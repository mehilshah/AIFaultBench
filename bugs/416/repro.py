#!/usr/bin/env python3

from __future__ import annotations

import subprocess
import sys
import textwrap

import torch
from pyro import __version__ as pyro_version
from pyro.ops.provenance import ProvenanceTensor


def main() -> None:
    print(f"torch={torch.__version__}")
    print(f"pyro={pyro_version}")
    print(f"cuda_available={torch.cuda.is_available()}")
    print(f"default_device_before={torch.get_default_device()}")

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required to reproduce this bug.")

    baseline = textwrap.dedent(
        """
        import torch
        from pyro.ops.provenance import ProvenanceTensor

        x = torch.tensor([1., 2., 3.])
        y = ProvenanceTensor(x, frozenset(["x"]))
        result = torch.as_tensor(y.cuda())
        print(f"baseline_result={result!r} device={result.device} shape={tuple(result.shape)}")
        """
    ).strip()

    print("baseline_without_default_device:")
    subprocess.run([sys.executable, "-c", baseline], check=True)

    torch.set_default_device(torch.device("cuda"))
    print(f"default_device_after={torch.get_default_device()}")

    x = torch.tensor([1.0, 2.0, 3.0])
    y = ProvenanceTensor(x, frozenset({"x"}))
    result = torch.as_tensor(y)
    print(f"bug_result={result!r} device={result.device} shape={tuple(result.shape)}")

    expected_shape = (3,)
    if tuple(result.shape) != expected_shape:
        raise AssertionError(
            f"bug reproduced: expected shape {expected_shape}, got {tuple(result.shape)}"
        )


if __name__ == "__main__":
    main()
