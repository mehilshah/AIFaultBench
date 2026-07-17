#!/usr/bin/env python3
"""Minimal reproducer for verbose tensor reprs in TypeCheckError output."""

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
if str(CODEBASE) not in sys.path:
    sys.path.insert(0, str(CODEBASE))

import torch
import typeguard
from jaxtyping import Float, TypeCheckError, jaxtyped


@jaxtyped(typechecker=typeguard.typechecked)
def my_matmul(x: Float[torch.Tensor, "n k"], y: Float[torch.Tensor, "k p"]):
    return torch.matmul(x, y)


def main() -> int:
    torch.manual_seed(0)
    x = torch.randn((2, 16)).float()
    y = torch.randn((17, 8)).float()

    try:
        my_matmul(x, y)
    except TypeCheckError as exc:
        message = str(exc)
        if "tensor([[" not in message:
            print("reproducible=False")
            print("expected a verbose tensor repr in the error message")
            return 1

        print("reproducible=True")
        print("verbose_tensor_repr=True")
        print("first_line:", message.splitlines()[0])
        print("evidence_excerpt:")
        for line in message.splitlines()[:12]:
            print(line)
        return 0

    print("reproducible=False")
    print("expected a TypeCheckError but the call succeeded")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
