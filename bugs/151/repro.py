#!/usr/bin/env python3
from __future__ import annotations

import os
import sys

import torch


ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "codebase", "src"))


from transformers import GPT2Config, GPT2LMHeadModel, GenerationConfig  # noqa: E402


def main() -> int:
    torch.manual_seed(0)

    model = GPT2LMHeadModel(
        GPT2Config(
            n_layer=1,
            n_head=1,
            n_embd=16,
            n_positions=8,
            n_ctx=8,
            vocab_size=32,
            bos_token_id=0,
            eos_token_id=1,
            pad_token_id=0,
        )
    )

    # Simulate a model whose bundled generation defaults prefer a very small temperature.
    model.generation_config.temperature = 1e-6
    model.generation_config.transformers_version = "4.50.0"

    custom_config = GenerationConfig(
        temperature=1.0,
        max_new_tokens=1,
        do_sample=True,
    )

    prepared_config, _ = model._prepare_generation_config(custom_config)

    print(f"model.generation_config.temperature={model.generation_config.temperature}")
    print(f"custom_config.temperature={custom_config.temperature}")
    print(f"prepared_config.temperature={prepared_config.temperature}")

    if prepared_config.temperature == 1.0:
        print("BUG NOT REPRODUCED: explicit temperature was preserved.")
        return 1

    if prepared_config.temperature == model.generation_config.temperature == 1e-6:
        print("BUG REPRODUCED: explicit temperature=1.0 was overwritten by the model default.")
        return 0

    print("Unexpected result.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
