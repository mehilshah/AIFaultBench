#!/usr/bin/env python3
"""Reduced reproduction for the Gemma4 unified multimodal dtype bug.

The real issue happens when a quantized projection exposes `weight.dtype == torch.uint8`.
The multimodal embedder casts its inputs to that dtype before normalization, which then
propagates a byte tensor into downstream masked_scatter logic.
"""

from __future__ import annotations

import sys
from pathlib import Path

import torch
from torch import nn


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase" / "src"))

from transformers.models.gemma4_unified.modular_gemma4_unified import (  # noqa: E402
    Gemma4UnifiedAudioConfig,
    Gemma4UnifiedMultimodalEmbedder,
    Gemma4UnifiedTextConfig,
)


class FakeQuantLinear(nn.Module):
    """Minimal stand-in for a 4-bit quantized linear layer."""

    def __init__(self) -> None:
        super().__init__()
        self.register_buffer("weight", torch.zeros(1, dtype=torch.uint8))

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        return inputs


def main() -> None:
    audio_config = Gemma4UnifiedAudioConfig()
    text_config = Gemma4UnifiedTextConfig()

    embedder = Gemma4UnifiedMultimodalEmbedder(audio_config, text_config)

    # Replace the norm/projection with minimal stand-ins so the buggy cast can be
    # observed without loading the full model or bitsandbytes.
    embedder.embedding_pre_projection_norm = nn.Identity()
    embedder.embedding_projection = FakeQuantLinear()

    inputs = torch.randn(2, 3, embedder.multimodal_hidden_size, dtype=torch.float32)
    features = embedder(inputs)
    print(f"feature_dtype={features.dtype}")
    print(f"feature_shape={tuple(features.shape)}")

    target = torch.zeros_like(features, dtype=torch.bfloat16)
    mask = torch.ones_like(features, dtype=torch.bool)
    target.masked_scatter(mask, features)


if __name__ == "__main__":
    main()
