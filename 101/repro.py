#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

import torch


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))

from rotary_embedding_torch import RotaryEmbedding  # noqa: E402


def summarize(seq_len: int) -> dict[str, object]:
    rotary_emb = RotaryEmbedding(dim=32, use_xpos=True)
    q = torch.ones(1, 1, seq_len, 64)
    k = torch.ones(1, 1, seq_len, 64)
    rq, rk = rotary_emb.rotate_queries_and_keys(q, k)
    return {
        "seq_len": seq_len,
        "q_finite": bool(torch.isfinite(rq).all().item()),
        "k_finite": bool(torch.isfinite(rk).all().item()),
        "q_nan": bool(torch.isnan(rq).any().item()),
        "k_nan": bool(torch.isnan(rk).any().item()),
        "q_inf": bool(torch.isinf(rq).any().item()),
        "k_inf": bool(torch.isinf(rk).any().item()),
        "k_non_finite_count": int((~torch.isfinite(rk)).sum().item()),
    }


def main() -> int:
    print(f"torch={torch.__version__}")
    print("trigger=RotaryEmbedding(dim=32, use_xpos=True)")

    checks = [summarize(seq_len) for seq_len in (64, 96)]
    for result in checks:
        print(result)

    broken = checks[-1]
    if broken["k_finite"]:
        raise AssertionError("Expected k to contain non-finite values at seq_len=96")

    if broken["k_non_finite_count"] == 0:
        raise AssertionError("Expected at least one non-finite value in k at seq_len=96")

    print("reproduced=True")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
