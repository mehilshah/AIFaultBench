#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import torch


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
if str(CODEBASE) not in sys.path:
    sys.path.insert(0, str(CODEBASE))

import x_transformers as xt  # noqa: E402


def main() -> int:
    torch.manual_seed(0)

    decoder = xt.TransformerWrapper(
        num_tokens=2049,
        max_seq_len=64,
        use_abs_pos_emb=True,
        scaled_sinu_pos_emb=True,
        attn_layers=xt.Decoder(
            dim=128,
            depth=2,
            heads=4,
            attn_dim_head=32,
            attn_flash=True,
            ff_no_bias=True,
            cross_attend=True,
        ),
    )

    tokens = torch.randint(0, 2048, (2, 12))
    context = torch.rand(2, 4, 128)
    context_mask = torch.zeros(2, 4, dtype=torch.bool)

    out = decoder(tokens, context=context, context_mask=context_mask)
    has_nan = torch.isnan(out).any().item()
    is_finite = torch.isfinite(out).all().item()

    payload = {
        "torch_version": torch.__version__,
        "output_shape": list(out.shape),
        "has_nan": bool(has_nan),
        "is_finite": bool(is_finite),
        "sample": out[0, 0, :8].detach().tolist(),
    }
    print(json.dumps(payload, indent=2))
    print("REPRODUCIBLE" if has_nan else "NOT_REPRODUCIBLE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
