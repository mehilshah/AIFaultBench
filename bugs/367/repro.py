#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
RESULT_PATH = ROOT / "reproduction.json"


def write_result(
    *,
    reproducible: bool,
    evidence: list[str],
    steps: list[str],
    blocking_reason: str | None,
    reproduction_command: str,
) -> None:
    payload: dict[str, Any] = {
        "reproducible": reproducible,
        "evidence": evidence,
        "steps": steps,
        "blocking_reason": blocking_reason,
        "reproduction_command": reproduction_command,
    }
    RESULT_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
    os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")

    # Import after setting env vars and after the venv has been activated.
    import torch
    from accelerate import dispatch_model
    from transformers import AutoModelForCausalLM
    from peft import LoraConfig, get_peft_model

    model_id = "sshleifer/tiny-gpt2"
    device_map = {
        "transformer.wte": "cpu",
        "transformer.wpe": "cpu",
        "transformer.drop": "cpu",
        "transformer.h.0": "cpu",
        "transformer.h.1": "disk",
        "transformer.ln_f": "cpu",
        "lm_head": "cpu",
    }

    print(f"torch={torch.__version__}")
    print(f"model_id={model_id}")

    evidence: list[str] = []
    steps = [
        "Load sshleifer/tiny-gpt2.",
        "Dispatch one transformer block to disk so the model contains meta tensors.",
        "Attach a LoRA adapter and call merge_and_unload().",
        "Call save_pretrained() on the merged model.",
    ]

    with tempfile.TemporaryDirectory(prefix="peft-offload-repro-") as tmpdir:
        tmp = Path(tmpdir)
        offload_dir = tmp / "offload"
        adapter_dir = tmp / "adapter"
        merged_dir = tmp / "merged"

        base = AutoModelForCausalLM.from_pretrained(model_id)
        base = dispatch_model(base, device_map=device_map, offload_dir=str(offload_dir))
        meta_before = sum(1 for _, param in base.named_parameters() if param.is_meta)
        print(f"meta_params_before_peft={meta_before}")

        config = LoraConfig(
            task_type="CAUSAL_LM",
            r=2,
            lora_alpha=4,
            lora_dropout=0.0,
            target_modules=["c_attn"],
        )
        model = get_peft_model(base, config)
        meta_after_peft = sum(1 for _, param in model.named_parameters() if param.is_meta)
        print(f"meta_params_after_peft={meta_after_peft}")

        model.save_pretrained(adapter_dir)

        merged = model.merge_and_unload()
        meta_after_merge = sum(1 for _, param in merged.named_parameters() if param.is_meta)
        print(f"meta_params_after_merge={meta_after_merge}")

        try:
            merged.save_pretrained(merged_dir)
        except Exception as exc:  # noqa: BLE001
            evidence.append(
                f"save_pretrained failed with {type(exc).__name__}: {exc}"
            )
            evidence.append(
                f"meta parameters stayed present after merge ({meta_after_merge} meta tensors)"
            )
            print(f"expected_failure={type(exc).__name__}: {exc}", file=sys.stderr)
            write_result(
                reproducible=True,
                evidence=evidence,
                steps=steps,
                blocking_reason=None,
                reproduction_command="./run_repro.sh",
            )
            return 0

        saved_files = sorted(p.name for p in merged_dir.iterdir())
        evidence.append(f"save_pretrained unexpectedly succeeded with files: {saved_files}")
        blocking_reason = "The offloaded merge/save failure did not reproduce in this run."
        write_result(
            reproducible=False,
            evidence=evidence,
            steps=steps,
            blocking_reason=blocking_reason,
            reproduction_command="./run_repro.sh",
        )
        print(blocking_reason, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
