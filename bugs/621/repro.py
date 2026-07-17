#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import traceback
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent
SRC_DIR = ROOT / "codebase" / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import torch
from tokenizers import Tokenizer
from tokenizers.models import WordLevel
from tokenizers.pre_tokenizers import Whitespace
from transformers.generation import GenerationConfig
from transformers.models.diffusion_gemma.generation_diffusion_gemma import (
    DiffusionGemmaGenerationMixin,
    DiffusionGemmaGenerationOutput,
)
from transformers.pipelines.image_text_to_text import ImageTextToTextPipeline
from transformers.tokenization_utils_fast import PreTrainedTokenizerFast


def build_tokenizer() -> PreTrainedTokenizerFast:
    vocab = {
        "[PAD]": 0,
        "[UNK]": 1,
        "hello": 2,
        "world": 3,
    }
    backend = Tokenizer(WordLevel(vocab=vocab, unk_token="[UNK]"))
    backend.pre_tokenizer = Whitespace()
    tokenizer = PreTrainedTokenizerFast(tokenizer_object=backend, pad_token="[PAD]", unk_token="[UNK]")
    return tokenizer


class DummyProcessor:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def post_process_image_text_to_text(self, generated_outputs, skip_special_tokens=True, **kwargs):
        return self.tokenizer.decode(generated_outputs, skip_special_tokens=skip_special_tokens, **kwargs)


def main() -> int:
    steps: list[str] = []
    evidence: list[str] = []
    reproduction_command = "bash run_repro.sh"
    blocking_reason = ""

    print("Step 1: exercising DiffusionGemmaGenerationMixin._prepare_generation_config with a plain GenerationConfig")
    fake_model = SimpleNamespace(
        generation_config=None,
        config=SimpleNamespace(canvas_length=4, text_config=SimpleNamespace(vocab_size=8)),
    )
    try:
        prepared_generation_config, _ = DiffusionGemmaGenerationMixin._prepare_generation_config(
            fake_model, GenerationConfig()
        )
        DiffusionGemmaGenerationMixin._prepare_sampler(fake_model, prepared_generation_config)
    except Exception as exc:  # noqa: BLE001
        tb = traceback.format_exc()
        print(tb, end="")
        evidence.append(f"_prepare_sampler raised {type(exc).__name__}: {exc}")
        steps.append(
            "A plain GenerationConfig reaches DiffusionGemmaGenerationMixin._prepare_sampler and raises AttributeError on sampler_config."
        )
    else:
        blocking_reason = "The DiffusionGemma generation-config mismatch did not reproduce."

    print("Step 2: exercising ImageTextToTextPipeline.postprocess with DiffusionGemmaGenerationOutput")
    tokenizer = build_tokenizer()
    processor = DummyProcessor(tokenizer)
    fake_pipeline = SimpleNamespace(processor=processor, tokenizer=tokenizer)
    generated_outputs = DiffusionGemmaGenerationOutput(
        sequences=torch.tensor([[2, 3]], dtype=torch.long),
        tokens_per_forward=torch.tensor([1.0], dtype=torch.float32),
        past_key_values=None,
    )
    model_outputs = {
        "prompt_text": "hello",
        "generated_sequence": generated_outputs,
        "input_ids": torch.tensor([[2]], dtype=torch.long),
    }
    try:
        ImageTextToTextPipeline.postprocess(fake_pipeline, model_outputs)
    except Exception as exc:  # noqa: BLE001
        tb = traceback.format_exc()
        print(tb, end="")
        evidence.append(f"postprocess raised {type(exc).__name__}: {exc}")
        steps.append(
            "Passing DiffusionGemmaGenerationOutput into ImageTextToTextPipeline.postprocess raises KeyError on 'input_ids'."
        )
    else:
        blocking_reason = "The DiffusionGemma postprocess mismatch did not reproduce."

    reproducible = len(evidence) == 2
    result = {
        "reproducible": reproducible,
        "evidence": evidence,
        "steps": steps,
        "blocking_reason": blocking_reason,
        "reproduction_command": reproduction_command,
    }
    (ROOT / "reproduction.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if reproducible else 1


if __name__ == "__main__":
    raise SystemExit(main())
