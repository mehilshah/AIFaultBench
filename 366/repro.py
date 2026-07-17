#!/usr/bin/env python3
"""Minimal repro for Qwen3-VL multi-label sequence-classification configs.

The bug report describes a checkpoint whose top-level config advertises
`num_labels=20` and `problem_type=multi_label_classification`, but the vLLM
Qwen3-VL sequence-classification path still builds a 2-class head because the
nested text config keeps its default `num_labels=2`.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from transformers import AutoConfig


def main() -> None:
    config_dict = {
        "architectures": ["Qwen3VLForConditionalGeneration"],
        "model_type": "qwen3_vl",
        "problem_type": "multi_label_classification",
        "id2label": {str(i): f"LABEL_{i}" for i in range(20)},
        "label2id": {f"LABEL_{i}": i for i in range(20)},
    }

    tmp_dir = Path(tempfile.mkdtemp(prefix="qwen3_vl_seq_cls_"))
    (tmp_dir / "config.json").write_text(json.dumps(config_dict), encoding="utf-8")

    cfg = AutoConfig.from_pretrained(tmp_dir)
    text_cfg = cfg.get_text_config()

    top_num_labels = cfg.num_labels
    text_num_labels = text_cfg.num_labels
    expected_num_labels = len(config_dict["id2label"])

    print("Loaded config:", type(cfg).__name__)
    print("Top-level problem_type:", getattr(cfg, "problem_type", None))
    print("Top-level num_labels:", top_num_labels)
    print("Nested text num_labels:", text_num_labels)
    print("Nested text problem_type:", getattr(text_cfg, "problem_type", None))
    print("Expected labels from checkpoint metadata:", expected_num_labels)
    print(
        "Checkpoint score.weight shape:",
        f"({expected_num_labels}, 4096)",
    )
    print(
        "vLLM-side head shape if derived from nested text config:",
        f"({text_num_labels}, 4096)",
    )

    assert top_num_labels == expected_num_labels, (
        "Top-level config should preserve the checkpoint's 20 labels"
    )
    assert text_num_labels == 2, (
        "Nested Qwen3-VL text config still defaults to 2 labels"
    )
    assert text_num_labels != expected_num_labels, (
        "This mismatch is the reproduction: the serving path sees 2 labels "
        "where the checkpoint has 20"
    )


if __name__ == "__main__":
    main()
