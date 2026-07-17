#!/usr/bin/env python3
"""Reproduce the SAM3 bf16 torch.compile dtype mismatch."""

from __future__ import annotations

import sys
import traceback

import torch

from transformers import (
    CLIPTextConfig,
    Sam3Config,
    Sam3DETRDecoderConfig,
    Sam3DETREncoderConfig,
    Sam3GeometryEncoderConfig,
    Sam3MaskDecoderConfig,
    Sam3Model,
    Sam3ViTConfig,
    Sam3VisionConfig,
)


def build_tiny_model() -> Sam3Model:
    vit = Sam3ViTConfig(
        hidden_size=32,
        intermediate_size=64,
        num_hidden_layers=2,
        num_attention_heads=4,
        image_size=64,
        patch_size=16,
        window_size=4,
        global_attn_indexes=[0, 1],
    )
    vision = Sam3VisionConfig(
        backbone_config=vit,
        fpn_hidden_size=16,
        backbone_feature_sizes=[[16, 16], [8, 8], [4, 4]],
        scale_factors=[4.0, 2.0, 1.0, 0.5],
    )
    text = CLIPTextConfig(
        vocab_size=100,
        hidden_size=32,
        intermediate_size=64,
        projection_dim=32,
        num_hidden_layers=2,
        num_attention_heads=4,
        max_position_embeddings=32,
        bos_token_id=0,
        eos_token_id=1,
        pad_token_id=2,
    )
    geometry = Sam3GeometryEncoderConfig(hidden_size=16, num_layers=1, num_attention_heads=4, intermediate_size=32, roi_size=2)
    detr_encoder = Sam3DETREncoderConfig(hidden_size=16, num_layers=1, num_attention_heads=4, intermediate_size=32)
    detr_decoder = Sam3DETRDecoderConfig(
        hidden_size=16, num_layers=1, num_queries=4, num_attention_heads=4, intermediate_size=32
    )
    mask_decoder = Sam3MaskDecoderConfig(hidden_size=16, num_upsampling_stages=2, num_attention_heads=4)

    config = Sam3Config(
        vision_config=vision,
        text_config=text,
        geometry_encoder_config=geometry,
        detr_encoder_config=detr_encoder,
        detr_decoder_config=detr_decoder,
        mask_decoder_config=mask_decoder,
    )
    return Sam3Model(config).eval().to(dtype=torch.bfloat16)


def main() -> int:
    print(f"torch={torch.__version__}")
    print(f"cuda_available={torch.cuda.is_available()}")
    print(f"cuda_device_count={torch.cuda.device_count()}")

    model = build_tiny_model()
    print(f"model_dtype={next(model.parameters()).dtype}")

    pixel_values = torch.randn(1, 3, 64, 64, dtype=torch.bfloat16)
    input_ids = torch.randint(0, 100, (1, 8))
    attention_mask = torch.ones_like(input_ids)

    with torch.inference_mode():
        eager_outputs = model(pixel_values=pixel_values, input_ids=input_ids, attention_mask=attention_mask)
    print(f"eager_ok pred_logits={tuple(eager_outputs.pred_logits.shape)} pred_masks={tuple(eager_outputs.pred_masks.shape)}")

    compiled = torch.compile(model)
    try:
        with torch.inference_mode():
            compiled_outputs = compiled(
                pixel_values=pixel_values, input_ids=input_ids, attention_mask=attention_mask
            )
        print(
            "compiled_ok "
            f"pred_logits={tuple(compiled_outputs.pred_logits.shape)} "
            f"pred_masks={tuple(compiled_outputs.pred_masks.shape)}"
        )
        return 0
    except Exception as exc:  # pragma: no cover - script is meant to surface the failure
        print(f"compiled_failed {type(exc).__name__}: {exc}", file=sys.stderr)
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
