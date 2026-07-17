from __future__ import annotations

import sys
from pathlib import Path

import torch

ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR / "codebase"))

import pyro.distributions as dist  # noqa: E402


def main() -> int:
    torch.manual_seed(0)

    n = 1000
    rate = torch.tensor(100.0)
    p = torch.tensor(0.3)
    logit = torch.log(p / (1 - p))

    zip_from_logits = dist.ZeroInflatedPoisson(rate=rate, gate_logits=logit)
    zip_from_gate = dist.ZeroInflatedPoisson(rate=rate, gate=p)

    x1 = (zip_from_logits.sample((n,)) == 0).float().mean().item()
    x2 = (zip_from_gate.sample((n,)) == 0).float().mean().item()

    print(f"input_probability={p.item():.6f}")
    print(f"input_logit={logit.item():.6f}")
    print(f"zip_from_logits.gate={zip_from_logits.gate.item():.6f}")
    print(f"zip_from_gate.gate={zip_from_gate.gate.item():.6f}")
    print(f"zero_fraction_gate_logits={x1:.6f}")
    print(f"zero_fraction_gate={x2:.6f}")

    if not (x1 > 0.95 and abs(x2 - p.item()) < 0.1):
        raise SystemExit("unexpected: issue did not reproduce")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
