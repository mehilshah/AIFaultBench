from __future__ import annotations

import tempfile
from pathlib import Path

import torch
from torch import nn
from transformers import BertConfig, BertForSequenceClassification

from peft import LoraConfig, PeftModel, TaskType, get_peft_model


def build_model(classifier_seed: int) -> BertForSequenceClassification:
    """Create a deterministic backbone and vary only the classifier head."""
    torch.manual_seed(0)
    model = BertForSequenceClassification(
        BertConfig(
            vocab_size=97,
            hidden_size=32,
            num_hidden_layers=2,
            num_attention_heads=4,
            intermediate_size=64,
            num_labels=2,
        )
    )

    torch.manual_seed(classifier_seed)
    with torch.no_grad():
        nn.init.normal_(model.classifier.weight)
        nn.init.normal_(model.classifier.bias)

    return model


def main() -> None:
    torch.manual_seed(1234)
    inputs = {
        "input_ids": torch.randint(0, 97, (2, 8)),
        "attention_mask": torch.ones(2, 8, dtype=torch.long),
    }

    base_model = build_model(classifier_seed=111)
    peft_model = get_peft_model(
        base_model,
        LoraConfig(
            task_type=TaskType.SEQ_CLS,
            target_modules=["query", "value"],
            modules_to_save=["classifier"],
        ),
    )
    peft_model.eval()

    orig_on = peft_model(**inputs).logits
    with peft_model.disable_adapter():
        orig_disabled = peft_model(**inputs).logits

    print(f"original adapter-on == original disabled: {torch.allclose(orig_on, orig_disabled)}")

    with tempfile.TemporaryDirectory(prefix="peft-modules-to-save-") as tmpdir:
        peft_model.save_pretrained(tmpdir)

        loaded_base = build_model(classifier_seed=222)
        loaded_model = PeftModel.from_pretrained(loaded_base, Path(tmpdir))
        loaded_model.eval()

        loaded_on = loaded_model(**inputs).logits
        with loaded_model.disable_adapter():
            loaded_disabled = loaded_model(**inputs).logits

        print(f"loaded adapter-on == original adapter-on: {torch.allclose(loaded_on, orig_on)}")
        print(f"loaded disabled == original disabled: {torch.allclose(loaded_disabled, orig_disabled)}")
        print(f"max abs diff: {(loaded_disabled - orig_disabled).abs().max().item():.6f}")

        assert torch.allclose(
            loaded_disabled, orig_disabled
        ), "Loaded model loses the original classifier weights when adapters are disabled."


if __name__ == "__main__":
    main()
