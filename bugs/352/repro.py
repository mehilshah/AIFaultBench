#!/usr/bin/env python3
"""Minimal reproduction for PEFT prefix-tuning passing duplicate past_key_values."""

from __future__ import annotations

import json
from pathlib import Path

import torch
from transformers import GPT2Config, GPT2LMHeadModel

from peft import PrefixTuningConfig, TaskType, get_peft_model


ROOT = Path(__file__).resolve().parent
RESULT_PATH = ROOT / "reproduction.json"


def run_repro() -> dict:
    torch.manual_seed(0)

    base_model = GPT2LMHeadModel(
        GPT2Config(
            vocab_size=64,
            n_positions=16,
            n_ctx=16,
            n_embd=32,
            n_layer=2,
            n_head=4,
            bos_token_id=0,
            eos_token_id=1,
        )
    )
    peft_config = PrefixTuningConfig(
        task_type=TaskType.CAUSAL_LM,
        num_virtual_tokens=4,
        token_dim=32,
        num_transformer_submodules=1,
        num_attention_heads=4,
        num_layers=2,
    )
    model = get_peft_model(base_model, peft_config).eval()

    input_ids = torch.tensor([[1, 2, 3, 4]], dtype=torch.long)
    attention_mask = torch.ones_like(input_ids)
    caller_past_key_values = ("caller-supplied-cache",)

    try:
        _ = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            past_key_values=caller_past_key_values,
        )
    except TypeError as exc:
        import traceback

        traceback.print_exc()
        message = str(exc)
        reproduced = "multiple values for keyword argument 'past_key_values'" in message
        return {
            "reproducible": reproduced,
            "evidence": f"{type(exc).__name__}: {message}",
            "steps": [
                "Created a tiny GPT-2 causal LM and wrapped it with PrefixTuningConfig.",
                "Called PeftModelForCausalLM.forward() with a caller-supplied past_key_values kwarg.",
                "Python raised TypeError about multiple values for keyword argument 'past_key_values'.",
            ]
            if reproduced
            else [
                "Created a tiny GPT-2 causal LM and wrapped it with PrefixTuningConfig.",
                "Called PeftModelForCausalLM.forward() with a caller-supplied past_key_values kwarg.",
                "A TypeError was raised, but it did not match the reported duplicate-keyword failure.",
            ],
            "blocking_reason": "" if reproduced else "Unexpected TypeError shape; the observed failure is not the reported bug.",
            "reproduction_command": "bash run_repro.sh",
        }
    except Exception as exc:
        import traceback

        traceback.print_exc()
        return {
            "reproducible": False,
            "evidence": f"{type(exc).__name__}: {exc}",
            "steps": [
                "Created a tiny GPT-2 causal LM and wrapped it with PrefixTuningConfig.",
                "Called PeftModelForCausalLM.forward() with a caller-supplied past_key_values kwarg.",
                "Execution failed before reaching the expected duplicate-keyword path.",
            ],
            "blocking_reason": f"Unexpected exception type prevented the intended reproduction: {type(exc).__name__}",
            "reproduction_command": "bash run_repro.sh",
        }

    return {
        "reproducible": False,
        "evidence": "No TypeError was raised when passing past_key_values through prefix tuning.",
        "steps": [
            "Created a tiny GPT-2 causal LM and wrapped it with PrefixTuningConfig.",
            "Called PeftModelForCausalLM.forward() with a caller-supplied past_key_values kwarg.",
            "The call completed successfully, so the historical duplicate-keyword bug was not reproduced.",
        ],
        "blocking_reason": "The current PEFT snapshot appears to already handle the prefix-tuning past_key_values path.",
        "reproduction_command": "bash run_repro.sh",
    }


def main() -> int:
    result = run_repro()
    RESULT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
