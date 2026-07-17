from __future__ import annotations

import torch

from x_transformers.x_transformers import Decoder


def main() -> None:
    model = Decoder(
        dim=512,
        depth=2,
        heads=8,
        alibi_pos_bias=True,
        attn_flash=True,
    )

    x = torch.randn(2, 4, 512)
    pos = torch.tensor([[0, 1, 2, 4], [1, 3, 5, 7]])

    print("Running Decoder with flash attention and custom ALiBi positions")
    print(f"x.shape={tuple(x.shape)} pos.shape={tuple(pos.shape)}")

    # This should fail in Attend.flash_attn when it tries to reshape a 4D bias
    # with a 3D-only rearrange pattern.
    model(x, pos=pos)


if __name__ == "__main__":
    main()
