#!/usr/bin/env python3
"""Reproduce the DeepCompile Qwen1.5-MoE embedding failure.

The real reproduction path requires a CUDA-capable DeepSpeed runtime.
When that stack is not available, this script falls back to a local
shape-only reproducer that shows the same low-level `weight must be 2-D`
exception once the embedding weight is flattened.
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class RunOutcome:
    reproducible: bool
    evidence: str
    steps: List[str]
    blocking_reason: str
    reproduction_command: str

    def to_json(self) -> Dict[str, Any]:
        return {
            "reproducible": self.reproducible,
            "evidence": self.evidence,
            "steps": self.steps,
            "blocking_reason": self.blocking_reason,
            "reproduction_command": self.reproduction_command,
        }


def _write_result(path: str, outcome: RunOutcome) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(outcome.to_json(), f, indent=2, sort_keys=True)
        f.write("\n")


def _have_cuda_and_deepspeed() -> bool:
    try:
        import torch  # type: ignore

        if not torch.cuda.is_available():
            return False
        import deepspeed  # noqa: F401  # type: ignore
        from transformers import Qwen2MoeConfig  # noqa: F401  # type: ignore
        return True
    except Exception:
        return False


def run_shape_only() -> RunOutcome:
    class TinyEmbedding:
        def __init__(self, num_embeddings: int, embedding_dim: int) -> None:
            self.weight_shape = (num_embeddings, embedding_dim)

        def forward(self, input_ids: List[List[int]]) -> List[List[float]]:
            if len(self.weight_shape) != 2:
                raise RuntimeError("'weight' must be 2-D")
            rows, cols = self.weight_shape
            return [[0.0 for _ in range(cols)] for _ in input_ids[0]]

    class TinyEmbeddingModel:
        def __init__(self) -> None:
            self.embed_tokens = TinyEmbedding(8, 4)

        def forward(self, input_ids: List[List[int]]) -> List[List[float]]:
            return self.embed_tokens.forward(input_ids)

        def __call__(self, input_ids: List[List[int]]) -> List[List[float]]:
            return self.forward(input_ids)

    model = TinyEmbeddingModel()
    input_ids = [[1, 2, 3]]

    before_shape = tuple(model.embed_tokens.weight_shape)
    model.embed_tokens.weight_shape = (before_shape[0] * before_shape[1],)
    after_shape = tuple(model.embed_tokens.weight_shape)

    steps = [
        f"Created a tiny embedding model with weight shape {before_shape}.",
        f"Flattened embed_tokens.weight to {after_shape} to simulate the bad DeepCompile shape.",
    ]

    try:
        _ = model(input_ids)
        return RunOutcome(
            reproducible=False,
            evidence="The synthetic fallback did not raise, which is unexpected.",
            steps=steps + ["Forward pass unexpectedly succeeded."],
            blocking_reason="The local fallback did not hit the expected embedding failure.",
            reproduction_command="bash run_repro.sh",
        )
    except Exception as exc:  # noqa: BLE001
        return RunOutcome(
            reproducible=False,
            evidence=f"Flattening the embedding weight to 1-D reproduces the same low-level failure here: {exc}",
            steps=steps + [f"Forward pass raised: {type(exc).__name__}: {exc}"],
            blocking_reason=(
                "The full DeepCompile/Qwen2Moe stack is not runnable in this machine; "
                "the bundled fallback only reproduces the embedding-shape failure mode."
            ),
            reproduction_command="bash run_repro.sh",
        )


def _build_tiny_qwen_config():
    from transformers import Qwen2MoeConfig

    return Qwen2MoeConfig(
        vocab_size=256,
        hidden_size=32,
        intermediate_size=64,
        num_hidden_layers=2,
        num_attention_heads=4,
        num_key_value_heads=4,
        moe_intermediate_size=16,
        shared_expert_intermediate_size=32,
        num_experts_per_tok=1,
        num_experts=4,
        max_position_embeddings=64,
        use_sliding_window=False,
        attention_dropout=0.0,
        tie_word_embeddings=False,
        output_router_logits=False,
        router_aux_loss_coef=0.0,
        qkv_bias=True,
        bos_token_id=1,
        eos_token_id=2,
        pad_token_id=0,
    )


def _build_tiny_llama_config():
    from transformers import LlamaConfig

    return LlamaConfig(
        vocab_size=256,
        hidden_size=32,
        intermediate_size=64,
        num_hidden_layers=2,
        num_attention_heads=4,
        num_key_value_heads=4,
        max_position_embeddings=64,
        tie_word_embeddings=False,
        bos_token_id=1,
        eos_token_id=2,
        pad_token_id=0,
    )


def _make_ds_config(zero_stage: int = 3) -> Dict[str, Any]:
    return {
        "train_micro_batch_size_per_gpu": 1,
        "steps_per_print": 1,
        "optimizer": {
            "type": "Adam",
            "params": {
                "lr": 1.5e-4,
            },
        },
        "zero_optimization": {
            "stage": zero_stage,
        },
        "compile": {
            "deepcompile": True,
        },
    }


def _run_single_model(name: str, model, input_ids, attention_mask, labels):
    import deepspeed

    engine, _, _, _ = deepspeed.initialize(config=_make_ds_config(), model=model, model_parameters=model.parameters())
    engine.compile()
    loss = engine(input_ids=input_ids, attention_mask=attention_mask, labels=labels, use_cache=False)
    return {
        "name": name,
        "loss": float(loss.loss.detach().cpu()),
        "weight_shape": tuple(engine.module.get_input_embeddings().weight.shape),
    }


def run_full() -> RunOutcome:
    import torch
    from transformers import LlamaForCausalLM, Qwen2MoeForCausalLM

    qwen_config = _build_tiny_qwen_config()
    llama_config = _build_tiny_llama_config()

    qwen_model = Qwen2MoeForCausalLM(qwen_config)
    llama_model = LlamaForCausalLM(llama_config)

    device = torch.device("cuda", int(os.environ.get("LOCAL_RANK", "0")))
    qwen_model.to(device)
    llama_model.to(device)

    input_ids = torch.randint(0, qwen_config.vocab_size, (1, 8), device=device)
    attention_mask = torch.ones_like(input_ids)

    steps = [
        "Built tiny Qwen2MoE and LLaMA models with random weights.",
        "Initialized DeepSpeed with compile.deepcompile=true and ZeRO stage 3.",
        "Ran a single forward pass on each model.",
    ]

    try:
        llama_out = _run_single_model("llama", llama_model, input_ids, attention_mask, input_ids)
        qwen_out = _run_single_model("qwen", qwen_model, input_ids, attention_mask, input_ids)
        evidence = (
            f"Full DeepCompile path completed in this machine. "
            f"LLaMA loss={llama_out['loss']:.6f}, Qwen loss={qwen_out['loss']:.6f}; "
            f"qwen embed weight shape={qwen_out['weight_shape']}."
        )
        return RunOutcome(
            reproducible=False,
            evidence=evidence,
            steps=steps + ["Both models completed without the reported exception."],
            blocking_reason="The reported Qwen failure did not manifest on this machine.",
            reproduction_command="bash run_repro.sh",
        )
    except Exception as exc:  # noqa: BLE001
        msg = f"{type(exc).__name__}: {exc}"
        evidence = (
            "The DeepCompile path failed while executing the Qwen model; "
            f"error={msg}"
        )
        return RunOutcome(
            reproducible="'weight' must be 2-D" in str(exc),
            evidence=evidence,
            steps=steps + [f"Forward pass raised: {msg}"],
            blocking_reason="",
            reproduction_command="bash run_repro.sh",
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["auto", "full", "shape-only"], default="auto")
    parser.add_argument("--result-file", required=True)
    args = parser.parse_args()

    if args.mode == "shape-only":
        outcome = run_shape_only()
    elif args.mode == "full":
        if not _have_cuda_and_deepspeed():
            outcome = RunOutcome(
                reproducible=False,
                evidence="CUDA/DeepSpeed/Transformers are not available here, so the full DeepCompile path could not be executed.",
                steps=["Checked runtime prerequisites and found the full stack unavailable."],
                blocking_reason="Missing CUDA-capable DeepSpeed runtime in this machine.",
                reproduction_command="bash run_repro.sh",
            )
        else:
            outcome = run_full()
    else:
        if _have_cuda_and_deepspeed():
            outcome = run_full()
        else:
            outcome = run_shape_only()

    _write_result(args.result_file, outcome)
    print(json.dumps(outcome.to_json(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
