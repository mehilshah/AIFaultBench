#!/usr/bin/env python3
"""Run the reported TRL SFT training path and emit a compact JSON summary."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from datasets import load_dataset
from transformers import AutoTokenizer
from trl import SFTConfig, SFTTrainer


MODEL_NAME = "trl-internal-testing/tiny-Qwen2ForCausalLM-2.5"
DATASET_NAME = "trl-internal-testing/zen"
DATASET_CONFIG = "standard_prompt_completion"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-size", type=int, required=True)
    parser.add_argument("--gradient-accumulation-steps", type=int, required=True)
    parser.add_argument("--max-steps", type=int, default=8)
    parser.add_argument("--learning-rate", type=float, default=1e-3)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--summary-file", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Avoid any external tracker side effects while still exercising the same
    # training code path reported in the issue.
    os.environ.setdefault("WANDB_DISABLED", "true")
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    output_dir = args.output_dir or Path(
        f"SFT-bsz{args.batch_size}-grad_acc{args.gradient_accumulation_steps}-zero2"
    )

    training_args = SFTConfig(
        output_dir=str(output_dir),
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        max_steps=args.max_steps,
        logging_steps=1,
        logging_strategy="steps",
        report_to="none",
        run_name=output_dir.name,
        completion_only_loss=True,
        learning_rate=args.learning_rate,
        bf16=True,
        disable_tqdm=True,
        seed=args.seed,
    )

    dummy_dataset = load_dataset(DATASET_NAME, DATASET_CONFIG)
    trainer = SFTTrainer(
        model=MODEL_NAME,
        args=training_args,
        processing_class=tokenizer,
        train_dataset=dummy_dataset["train"],
    )

    output = trainer.train()
    logs = [entry for entry in trainer.state.log_history if "loss" in entry]
    summary = {
        "batch_size": args.batch_size,
        "gradient_accumulation_steps": args.gradient_accumulation_steps,
        "max_steps": args.max_steps,
        "train_loss": output.training_loss,
        "logs": logs,
    }

    text = json.dumps(summary, indent=2, sort_keys=True)
    print(text)
    if args.summary_file is not None:
        args.summary_file.write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
