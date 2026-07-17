#!/usr/bin/env python3
"""Minimal reproduction for AdaLoRA dropout=0 TypeError."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase" / "src"))

from peft import AdaLoraConfig, get_peft_model
from transformers import BertConfig, BertForSequenceClassification


def main() -> None:
    # Tiny in-memory model; the bug happens while PEFT wraps the target modules.
    model = BertForSequenceClassification(
        BertConfig(
            vocab_size=100,
            hidden_size=32,
            num_hidden_layers=1,
            num_attention_heads=4,
            intermediate_size=64,
            num_labels=2,
        )
    )

    config = AdaLoraConfig(
        peft_type="ADALORA",
        task_type="SEQ_CLS",
        r=4,
        lora_alpha=16,
        init_r=6,
        target_modules=["query", "value"],
        bias="lora_only",
        orth_reg_weight=0.5,
        lora_dropout=0,
        tinit=0,
        modules_to_save=["classifier"],
    )

    print("Wrapping model with AdaLoRA (lora_dropout=0)...")
    get_peft_model(model, config)
    print("Unexpected success: bug did not reproduce.")


if __name__ == "__main__":
    main()
