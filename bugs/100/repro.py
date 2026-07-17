#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

import torch

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'codebase'))

from rotary_embedding_torch import RotaryEmbedding  # noqa: E402


def run() -> None:
    rotary = RotaryEmbedding(dim=8)

    for step in range(2):
        q = torch.randn(1, 2, 4, 8, requires_grad=True)
        rotated = rotary.rotate_queries_or_keys(q)
        loss = rotated.square().mean()
        loss.backward()

        print(f'step={step} loss={loss.item():.6f}')
        if step == 0:
            cached = rotary.cached_freqs
            print(f'cached_freqs_exists={cached is not None}')
            print(f'cached_freqs_grad_fn={getattr(cached, "grad_fn", None)}')

    print('result=not_reproduced')


if __name__ == '__main__':
    run()
