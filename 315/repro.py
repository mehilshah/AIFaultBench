#!/usr/bin/env python3
from __future__ import annotations

import io
import logging
import pathlib
import sys
from unittest.mock import patch


ROOT = pathlib.Path(__file__).resolve().parent
CODEBASE_SRC = ROOT / "codebase" / "src"
sys.path.insert(0, str(CODEBASE_SRC))

import huggingface_hub  # noqa: E402


if not hasattr(huggingface_hub, "is_offline_mode"):
    huggingface_hub.is_offline_mode = lambda: False  # type: ignore[attr-defined]

import transformers  # noqa: E402
import transformers.utils as transformers_utils  # noqa: E402
import transformers.utils.import_utils as import_utils  # noqa: E402


for module in (transformers_utils, import_utils):
    module.is_vision_available = lambda: False
    module.is_torchvision_available = lambda: False

from transformers import AutoModelForCausalLM, GPT2Config  # noqa: E402
import torch  # noqa: E402


def main() -> int:
    config = GPT2Config(
        n_embd=16,
        n_layer=1,
        n_head=2,
        n_positions=16,
        n_ctx=16,
        vocab_size=32,
        bos_token_id=1,
        eos_token_id=0,
        pad_token_id=0,
    )
    model = AutoModelForCausalLM.from_config(config)
    input_ids = torch.tensor([[1, 2, 3]], dtype=torch.long)

    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setLevel(logging.WARNING)
    logger = logging.getLogger("transformers.generation.utils")
    logger.addHandler(handler)
    logger.setLevel(logging.WARNING)
    logger.propagate = False

    with patch.object(model, "generate_batch", return_value={}):
        output = model.generate(input_ids, synced_gpus=True, cache_implementation="paged")

    handler.flush()
    warning_lines = [line for line in stream.getvalue().splitlines() if line.strip()]
    reproduced = any("synced_gpus is not ignored for continuous batching" in line for line in warning_lines)

    print(f"output_shape={tuple(output.shape)}")
    print("captured_warnings:")
    for line in warning_lines:
        print(line)
    print(f"reproduced={reproduced}")
    return 0 if reproduced else 1


if __name__ == "__main__":
    raise SystemExit(main())
