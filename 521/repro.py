#!/usr/bin/env python3
from __future__ import annotations

import traceback

import torch

from transformers.models.qwen3_5.configuration_qwen3_5 import Qwen3_5TextConfig
from transformers.models.qwen3_5.modeling_qwen3_5 import Qwen3_5TextModel


EXPECTED_MISSING_TP_KEYS = [
    "layers.*.linear_attn.in_proj_qkv",
    "layers.*.linear_attn.in_proj_z",
    "layers.*.linear_attn.in_proj_b",
    "layers.*.linear_attn.in_proj_a",
    "layers.*.linear_attn.out_proj",
]


def main() -> int:
    print("transformers base_model_tp_plan linear_attn entries:")
    present = [key for key in EXPECTED_MISSING_TP_KEYS if key in Qwen3_5TextConfig.base_model_tp_plan]
    missing = [key for key in EXPECTED_MISSING_TP_KEYS if key not in Qwen3_5TextConfig.base_model_tp_plan]
    print(f"  present: {present}")
    print(f"  missing: {missing}")

    config = Qwen3_5TextConfig(
        num_hidden_layers=1,
        hidden_size=16,
        num_attention_heads=2,
        num_key_value_heads=1,
        intermediate_size=32,
        linear_conv_kernel_dim=4,
        linear_key_head_dim=2,
        linear_value_head_dim=2,
        linear_num_key_heads=2,
        linear_num_value_heads=2,
        layer_types=["linear_attention"],
        vocab_size=64,
        max_position_embeddings=16,
        rope_parameters={"rope_type": "default", "rope_theta": 10000.0},
    )
    model = Qwen3_5TextModel(config).eval()
    layer = model.layers[0].linear_attn

    print(f"full in_proj_qkv weight shape: {tuple(layer.in_proj_qkv.weight.shape)}")
    print(f"expected conv_dim: {layer.conv_dim}")

    # Simulate the local shard created by a naive colwise TP plan.
    with torch.no_grad():
        sharded_weight = layer.in_proj_qkv.weight.chunk(2, dim=0)[0].contiguous()
        layer.in_proj_qkv.weight = torch.nn.Parameter(sharded_weight)

    print(f"simulated colwise shard shape: {tuple(layer.in_proj_qkv.weight.shape)}")

    hidden_states = torch.randn(1, 3, config.hidden_size)
    try:
        layer(hidden_states)
    except Exception as exc:  # noqa: BLE001
        print(f"{type(exc).__name__}: {exc}")
        traceback.print_exc()
        return 1

    print("unexpected success")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
