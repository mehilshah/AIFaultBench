#!/usr/bin/env python3
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
CODEBASE = os.path.join(ROOT, "codebase")
if CODEBASE not in sys.path:
    sys.path.insert(0, CODEBASE)

import coremltools as ct
import torch
import torch.nn as nn

from timm.layers.pos_embed_sincos import apply_rot_embed_cat


class ReproModule(nn.Module):
    def forward(self, x, emb):
        return apply_rot_embed_cat(x, emb)


def main():
    print(f"torch={torch.__version__}")
    print(f"coremltools={ct.__version__}")
    print(f"timm={CODEBASE}")

    module = ReproModule().eval()
    x = torch.randn(1, 2, 4)
    emb = torch.randn(1, 2, 8)

    with torch.no_grad():
        traced = torch.jit.trace(module, (x, emb))

    print("traced")
    ct.convert(
        traced,
        inputs=[
            ct.TensorType(shape=x.shape),
            ct.TensorType(shape=emb.shape),
        ],
        convert_to="mlprogram",
    )
    print("conversion succeeded")


if __name__ == "__main__":
    main()
