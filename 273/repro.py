from __future__ import annotations

import json
from pathlib import Path
import traceback

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, CompileConfig

from peft import VBLoRAConfig, get_peft_model


ROOT = Path(__file__).resolve().parent
RESULT_PATH = ROOT / "reproduction.json"


def main() -> int:
    model_id = "hf-internal-testing/tiny-random-Gemma3ForCausalLM"
    steps = [
        "Load hf-internal-testing/tiny-random-Gemma3ForCausalLM with attn_implementation='eager'.",
        "Wrap the model with VBLoRA using the same Gemma 3 target-module path as the reported issue.",
        "Switch the model to train mode so the VBLoRA logits check is active.",
        "Call generate() with cache_implementation='static' and a compile config that enables torch.compile on this CPU-only repro.",
    ]
    reproduction_command = "bash run_repro.sh"

    reproducible = False
    evidence = ""
    blocking_reason = None
    try:
        model = AutoModelForCausalLM.from_pretrained(model_id, attn_implementation="eager")
        config = VBLoRAConfig(
            task_type="CAUSAL_LM",
            target_modules=None,
            vblora_dropout=0.05,
            vector_length=1,
            num_vectors=2,
        )
        model = get_peft_model(model, config)
        model.train()

        tokenizer = AutoTokenizer.from_pretrained(model_id)
        inputs = tokenizer("hello", return_tensors="pt")
        compile_config = CompileConfig()
        compile_config._compile_all_devices = True
        model.generate(
            **inputs,
            max_new_tokens=3,
            cache_implementation="static",
            compile_config=compile_config,
        )
    except torch._dynamo.exc.Unsupported as exc:
        traceback.print_exc()
        message = str(exc)
        if "Data-dependent branching" in message:
            reproducible = True
            evidence = message
        else:
            blocking_reason = message
            evidence = message
    except Exception as exc:
        traceback.print_exc()
        blocking_reason = f"{type(exc).__name__}: {exc}"
        evidence = blocking_reason
    else:
        blocking_reason = "The compiled Gemma 3 + VB-LoRA generation path completed without raising."
        evidence = "No exception was raised."

    result = {
        "reproducible": reproducible,
        "evidence": evidence,
        "steps": steps,
        "blocking_reason": blocking_reason,
        "reproduction_command": reproduction_command,
    }

    RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
