from __future__ import annotations

import traceback

import torch

from x_transformers import TransformerWrapper, Decoder


def main() -> None:
    print(f"torch={torch.__version__}")
    model = TransformerWrapper(
        num_tokens=100,
        max_seq_len=16,
        attn_layers=Decoder(
            dim=32,
            depth=1,
            heads=4,
            attn_kv_heads=2,
            attn_qk_norm=True,
            attn_qk_norm_dim_scale=True,
        ),
    )
    x = torch.randint(0, 100, (2, 16))

    try:
        model(x)
    except RuntimeError as exc:
        print("REPRODUCED: RuntimeError raised during forward pass")
        traceback.print_exc()
        if "The size of tensor a (2) must match the size of tensor b (4)" not in str(exc):
            raise SystemExit(1)
        return

    raise SystemExit("BUG NOT REPRODUCED: forward pass succeeded unexpectedly")


if __name__ == "__main__":
    main()
