from __future__ import annotations

import torch
from torch import nn


class Linformer(nn.Module):
    """
    Minimal local compatibility shim for the example notebook.

    The original issue report imports `Linformer` from the external package
    `linformer`.  For the repro bundle we only need a transformer-shaped module
    with the same constructor signature so the example can run in a clean
    environment without adding another network dependency.
    """

    def __init__(self, dim, seq_len, depth, heads, k):  # noqa: D401
        super().__init__()
        self.layers = nn.ModuleList([])
        for _ in range(depth):
            self.layers.append(
                nn.ModuleDict(
                    {
                        "norm1": nn.LayerNorm(dim),
                        "attn": nn.MultiheadAttention(dim, heads, batch_first=True),
                        "norm2": nn.LayerNorm(dim),
                        "ff": nn.Sequential(
                            nn.Linear(dim, dim * 4),
                            nn.GELU(),
                            nn.Linear(dim * 4, dim),
                        ),
                    }
                )
            )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        for layer in self.layers:
            attn_input = layer["norm1"](x)
            attn_out, _ = layer["attn"](attn_input, attn_input, attn_input, need_weights=False)
            x = x + attn_out
            x = x + layer["ff"](layer["norm2"](x))
        return x
