#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import torch
import torch.nn.functional as F
from torch.nn import CrossEntropyLoss


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase" / "src"))

from transformers import BartConfig, Florence2Config, Florence2ForConditionalGeneration  # noqa: E402


def build_model() -> Florence2ForConditionalGeneration:
    text_config = BartConfig(
        vocab_size=11,
        d_model=16,
        encoder_layers=1,
        decoder_layers=1,
        encoder_attention_heads=2,
        decoder_attention_heads=2,
        encoder_ffn_dim=32,
        decoder_ffn_dim=32,
        max_position_embeddings=16,
        pad_token_id=1,
        decoder_start_token_id=2,
        bos_token_id=0,
        eos_token_id=3,
    )
    vision_config = {
        "embed_dim": (8, 8, 8, 8),
        "num_heads": (1, 1, 1, 1),
        "num_groups": (1, 1, 1, 1),
        "depths": (1, 1, 1, 1),
        "patch_size": (2, 2, 2, 2),
        "patch_stride": (2, 2, 2, 2),
        "patch_padding": (0, 0, 0, 0),
        "projection_dim": 16,
        "max_position_embeddings": 8,
        "max_temporal_embeddings": 8,
    }
    config = Florence2Config(text_config=text_config, vision_config=vision_config)
    model = Florence2ForConditionalGeneration(config)
    model.eval()
    return model


def main() -> None:
    torch.manual_seed(0)
    torch.set_num_threads(1)

    model = build_model()
    vocab_size = model.config.text_config.vocab_size

    input_ids = torch.tensor([[4, 5, 6]], dtype=torch.long)
    labels = torch.tensor([[7, 8, 9]], dtype=torch.long)

    with torch.no_grad():
        outputs = model(input_ids=input_ids, labels=labels)

    logits = outputs.logits
    correct_loss = CrossEntropyLoss()(logits.reshape(-1, vocab_size), labels.reshape(-1))
    shifted_labels = F.pad(labels, (0, 1), value=-100)[..., 1:]
    shifted_loss = CrossEntropyLoss(ignore_index=-100)(
        logits.reshape(-1, vocab_size), shifted_labels.reshape(-1)
    )

    reproducible = bool(
        torch.allclose(outputs.loss, shifted_loss) and not torch.allclose(outputs.loss, correct_loss)
    )

    result = {
        "reproducible": reproducible,
        "evidence": (
            f"Florence2ForConditionalGeneration.loss_function is {model.loss_function.__name__}; "
            f"model loss={outputs.loss.item():.9f}, direct CE on labels={correct_loss.item():.9f}, "
            f"shifted-label CE={shifted_loss.item():.9f}."
        ),
        "steps": [
            "Build a tiny random Florence2ForConditionalGeneration model from the local transformers checkout.",
            "Run a forward pass with synthetic input_ids and labels.",
            "Compare the returned loss against direct cross-entropy on labels and against shifted-label cross-entropy.",
        ],
        "blocking_reason": "",
        "reproduction_command": "bash setup_env.sh && bash run_repro.sh",
    }

    (ROOT / "reproduction.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

