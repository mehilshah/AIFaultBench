#!/usr/bin/env python3
"""Minimal repro for the TimesFM 2.5 window_size AttributeError."""

from __future__ import annotations

import sys
from pathlib import Path

import torch


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase" / "src"))

from transformers import TimesFm2_5Config, TimesFm2_5ModelForPrediction  # noqa: E402


def main() -> None:
    config = TimesFm2_5Config(
        context_length=64,
        horizon_length=8,
        patch_length=8,
        hidden_size=32,
        intermediate_size=32,
        num_hidden_layers=1,
        num_attention_heads=4,
        num_key_value_heads=4,
        head_dim=8,
        output_quantile_len=16,
        quantiles=(0.1, 0.5, 0.9),
        max_position_embeddings=64,
    )
    model = TimesFm2_5ModelForPrediction(config)

    past_values = [
        torch.sin(torch.linspace(0, 20, 100, dtype=torch.float32)),
        torch.sin(torch.linspace(0, 20, 200, dtype=torch.float32)),
        torch.sin(torch.linspace(0, 20, 400, dtype=torch.float32)),
    ]

    print("Instantiated TimesFm2_5ModelForPrediction")
    print("Calling forward with window_size=5")
    with torch.no_grad():
        model(past_values=past_values, window_size=5)


if __name__ == "__main__":
    main()
