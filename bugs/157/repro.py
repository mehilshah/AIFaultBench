#!/usr/bin/env python3
"""Minimal reproduction for OPT safetensors loading.

This script mirrors the bug report's load call and then inspects the tied
embedding/output weights to see whether either one remains on `meta`.
"""

from __future__ import annotations

import json
import os


os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")

try:
    import huggingface_hub
except Exception as exc:  # pragma: no cover - environment-specific failure
    raise SystemExit(f"failed to import huggingface_hub: {exc}") from exc

if not hasattr(huggingface_hub, "is_offline_mode"):
    huggingface_hub.is_offline_mode = lambda: False

import torch
import transformers


def main() -> int:
    model = transformers.AutoModelForCausalLM.from_pretrained(
        "facebook/opt-125m",
        torch_dtype=torch.float16,
        use_safetensors=True,
    )

    lm_head = model.lm_head.weight
    embed = model.model.decoder.embed_tokens.weight
    result = {
        "transformers_version": transformers.__version__,
        "torch_version": torch.__version__,
        "model_id": "facebook/opt-125m",
        "lm_head_is_meta": lm_head.is_meta,
        "embed_tokens_is_meta": embed.is_meta,
        "lm_head_device": str(lm_head.device),
        "embed_tokens_device": str(embed.device),
        "lm_head_dtype": str(lm_head.dtype),
        "embed_tokens_dtype": str(embed.dtype),
        "shared_storage": lm_head.data_ptr() == embed.data_ptr(),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
