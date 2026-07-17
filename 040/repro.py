#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import torch


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
UNET_PATH = CODEBASE / "labml_nn" / "diffusion" / "ddpm" / "unet.py"
RESULT_PATH = ROOT / "reproduction.json"


def load_attention_block():
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(CODEBASE))

    spec = importlib.util.spec_from_file_location("ddpm_unet", UNET_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.AttentionBlock


def main() -> int:
    torch.manual_seed(7)
    AttentionBlock = load_attention_block()

    block = AttentionBlock(n_channels=4, n_heads=1, d_k=4, n_groups=1)
    block.eval()

    x = torch.arange(1, 1 + 4 * 2 * 3, dtype=torch.float32).view(1, 4, 2, 3)

    with torch.no_grad():
        batch_size, n_channels, height, width = x.shape
        tokens = x.view(batch_size, n_channels, -1).permute(0, 2, 1)
        qkv = block.projection(tokens).view(batch_size, -1, block.n_heads, 3 * block.d_k)
        q, k, v = torch.chunk(qkv, 3, dim=-1)
        logits = torch.einsum("bihd,bjhd->bijh", q, k) * block.scale

        attn_buggy = logits.softmax(dim=1)
        attn_correct = logits.softmax(dim=2)

        buggy_sum_over_queries = attn_buggy.sum(dim=1)
        buggy_sum_over_keys = attn_buggy.sum(dim=2)
        correct_sum_over_keys = attn_correct.sum(dim=2)

        buggy_query_deviation = (buggy_sum_over_queries - 1.0).abs().max().item()
        buggy_key_deviation = (buggy_sum_over_keys - 1.0).abs().max().item()
        correct_key_deviation = (correct_sum_over_keys - 1.0).abs().max().item()
        attn_gap = (attn_buggy - attn_correct).abs().max().item()

    reproducible = buggy_query_deviation < 1e-6 and buggy_key_deviation > 1e-4 and correct_key_deviation < 1e-6

    evidence = [
        f"{UNET_PATH}:188 uses attn.softmax(dim=1) after einsum('bihd,bjhd->bijh', ...).",
        f"Buggy attention sum over query axis max deviation: {buggy_query_deviation:.3e}.",
        f"Buggy attention sum over key axis max deviation: {buggy_key_deviation:.3e}.",
        f"Correct attention sum over key axis max deviation: {correct_key_deviation:.3e}.",
        f"Max absolute difference between buggy and corrected attention weights: {attn_gap:.3e}.",
    ]

    result = {
        "reproducible": reproducible,
        "evidence": evidence,
        "steps": [
            "Load the actual DDPM AttentionBlock implementation from the bundled codebase.",
            "Construct deterministic q, k, v tensors from the module's projection layer.",
            "Compare softmax(dim=1) against the expected softmax(dim=2) normalization axis.",
        ],
        "blocking_reason": "" if reproducible else "The expected normalization mismatch did not reproduce on the deterministic check.",
        "reproduction_command": "bash run_repro.sh",
    }

    RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0 if reproducible else 1


if __name__ == "__main__":
    raise SystemExit(main())
