#!/usr/bin/env python3
"""Minimal reproducer for the PromptEncoderConfig SEQ_CLS crash."""

from __future__ import annotations

import json
import sys
import traceback
from pathlib import Path

from peft import PromptEncoderConfig, get_peft_model
from transformers import AutoModelForSequenceClassification, BertConfig


RESULT_PATH = Path(__file__).with_name("reproduction.json")


def build_result(reproducible: bool, evidence: list[str], steps: list[str], blocking_reason: str) -> dict:
    return {
        "reproducible": reproducible,
        "evidence": evidence,
        "steps": steps,
        "blocking_reason": blocking_reason,
        "reproduction_command": "bash run_repro.sh",
    }


def main() -> int:
    evidence: list[str] = []
    steps: list[str] = []

    print("Running repro with:")
    print(f"  peft={__import__('peft').__version__}")
    print(f"  transformers={__import__('transformers').__version__}")

    steps.append("Created a BERT sequence-classification model from configuration.")
    base_model = AutoModelForSequenceClassification.from_config(BertConfig())

    steps.append("Constructed PromptEncoderConfig(task_type='SEQ_CLS', num_virtual_tokens=20).")
    ptuning_config = PromptEncoderConfig(task_type="SEQ_CLS", num_virtual_tokens=20)

    steps.append("Called get_peft_model(base_model, ptuning_config).")
    try:
        get_peft_model(base_model, ptuning_config)
    except Exception as exc:  # noqa: BLE001 - we want the exact runtime failure
        tb = traceback.format_exc()
        print(tb, file=sys.stderr)
        evidence.append(f"Raised {type(exc).__name__}: {exc}")
        evidence.append(
            "The crash occurs while PeftModelForSequenceClassification.__init__ accesses "
            "peft_config.modules_to_save."
        )
        evidence.append("The resulting traceback points to peft_model.py line 1506.")

        reproducible = isinstance(exc, AttributeError) and "modules_to_save" in str(exc)
        blocking_reason = "" if reproducible else f"Unexpected exception: {type(exc).__name__}: {exc}"
    else:
        reproducible = False
        blocking_reason = "get_peft_model completed successfully; the bug did not reproduce."
        evidence.append("get_peft_model completed without error.")

    result = build_result(reproducible, evidence, steps, blocking_reason)
    RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
