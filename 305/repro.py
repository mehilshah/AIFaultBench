#!/usr/bin/env python3
from __future__ import annotations

import os
import sys


ROOT = os.path.dirname(os.path.abspath(__file__))
CODEBASE_SRC = os.path.join(ROOT, "codebase", "src")
if CODEBASE_SRC not in sys.path:
    sys.path.insert(0, CODEBASE_SRC)

from transformers import BertConfig, BertForSequenceClassification

from peft import LoraConfig, TaskType, get_peft_model


def main() -> None:
    base_model = BertForSequenceClassification(
        BertConfig(
            vocab_size=100,
            hidden_size=32,
            num_hidden_layers=2,
            num_attention_heads=4,
            intermediate_size=64,
            num_labels=2,
        )
    )

    config = LoraConfig(task_type=TaskType.SEQ_CLS)
    model = get_peft_model(base_model, config)

    adapter_to_delete = "delete_me"
    model.add_adapter(adapter_to_delete, config)

    before = list(model.base_model.classifier.modules_to_save.keys())
    print(f"before_delete={before}")
    assert adapter_to_delete in model.base_model.classifier.modules_to_save

    model.delete_adapter(adapter_to_delete)

    after = list(model.base_model.classifier.modules_to_save.keys())
    print(f"after_delete={after}")
    print(f"remaining_peft_config={list(model.peft_config.keys())}")
    assert adapter_to_delete not in model.base_model.classifier.modules_to_save


if __name__ == "__main__":
    main()
