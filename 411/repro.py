#!/usr/bin/env python3
import os
import sys
import tempfile
import traceback

import torch
from peft import LoraConfig, TaskType, get_peft_model
from transformers import AutoModelForSequenceClassification, set_seed


MODEL_ID = os.environ.get("MODEL_ID", "bigscience/bloomz-560m")
OFFLOAD_BUDGET = os.environ.get("OFFLOAD_BUDGET", "1600MB")


def build_peft_model(device_map=None, max_memory=None, offload_folder=None):
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_ID,
        device_map=device_map,
        max_memory=max_memory,
        offload_folder=offload_folder,
        torch_dtype=torch.float32,
    )
    config = LoraConfig(
        r=4,
        lora_alpha=4,
        lora_dropout=0.0,
        bias="none",
        task_type=TaskType.SEQ_CLS,
    )
    return get_peft_model(model, config)


def run_control_case():
    peft_model = build_peft_model()
    head = peft_model.base_model.model.score
    inputs = torch.randn((1, head.original_module.in_features), dtype=torch.float32)
    out = head(inputs)
    out.mean().backward()
    original_has_grad = head.original_module.weight.grad is not None
    modules_has_grad = head.modules_to_save["default"].weight.grad is not None
    print(
        "control",
        f"hf_device_map={getattr(peft_model.base_model.model, 'hf_device_map', None)}",
        f"original_module_has_grad={original_has_grad}",
        f"modules_to_save_has_grad={modules_has_grad}",
    )
    if original_has_grad or not modules_has_grad:
        raise AssertionError("control case did not route gradients to modules_to_save.default")


def run_offload_case():
    with tempfile.TemporaryDirectory(prefix="peft-offload-") as offload_dir:
        peft_model = build_peft_model(
            device_map="auto",
            max_memory={"cpu": OFFLOAD_BUDGET},
            offload_folder=offload_dir,
        )
        head = peft_model.base_model.model.score
        print(
            "offload",
            f"hf_device_map={getattr(peft_model.base_model.model, 'hf_device_map', None)}",
            f"head_device={head.original_module.weight.device}",
            f"wrapper_device={head.modules_to_save['default'].weight.device}",
        )
        inputs = torch.randn((1, head.original_module.in_features), dtype=torch.float32)
        try:
            out = head(inputs)
            out.mean().backward()
        except Exception as exc:  # pragma: no cover - exercised by repro run
            print(f"bug_reproduced={type(exc).__name__}: {exc}")
            traceback.print_exc()
            return 1

        original_has_grad = head.original_module.weight.grad is not None
        modules_has_grad = head.modules_to_save["default"].weight.grad is not None
        print(
            "offload_backward",
            f"original_module_has_grad={original_has_grad}",
            f"modules_to_save_has_grad={modules_has_grad}",
        )
        if original_has_grad and not modules_has_grad:
            print("bug_reproduced=gradient_routed_to_original_module")
            return 1

        raise AssertionError("offloaded device_map case did not reproduce the bug")


def main():
    set_seed(123)
    print(f"model_id={MODEL_ID}")
    print(f"offload_budget={OFFLOAD_BUDGET}")
    run_control_case()
    return run_offload_case()


if __name__ == "__main__":
    sys.exit(main())
