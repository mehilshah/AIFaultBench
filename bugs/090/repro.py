#!/usr/bin/env python3
from __future__ import annotations

import os
import sys

import torch


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CODEBASE_DIR = os.path.join(ROOT_DIR, "codebase")
sys.path.insert(0, CODEBASE_DIR)

from x_transformers.x_transformers import XTransformer  # noqa: E402


def main() -> int:
    torch.manual_seed(0)

    model = XTransformer(
        dim=32,
        enc_num_tokens=16,
        enc_max_seq_len=8,
        enc_depth=2,
        enc_heads=4,
        dec_num_tokens=16,
        dec_max_seq_len=8,
        dec_depth=2,
        dec_heads=4,
    )

    src = torch.randint(0, 16, (2, 8))
    tgt = torch.randint(0, 16, (2, 8))

    loss = model(src, tgt)
    loss.backward()

    enc_to_logits_weight = model.encoder.to_logits.weight
    enc_to_logits_grad_none = enc_to_logits_weight.grad is None

    print(f"torch_version={torch.__version__}")
    print(f"loss={loss.detach().item():.6f}")
    print(f"encoder.to_logits.weight.requires_grad={enc_to_logits_weight.requires_grad}")
    print(f"encoder.to_logits.weight.grad_is_none={enc_to_logits_grad_none}")
    if enc_to_logits_weight.grad is not None:
        print(f"encoder.to_logits.weight.grad_norm={float(enc_to_logits_weight.grad.norm()):.6f}")

    # This is the bug: the encoder output head exists as a parameter but is never used.
    if enc_to_logits_grad_none:
        print("REPRODUCED: encoder.to_logits.weight is unused in the forward pass")
    else:
        print("NOT REPRODUCED: encoder.to_logits.weight received a gradient")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
