#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FLASH_UTILS = ROOT / "codebase" / "src" / "transformers" / "modeling_flash_attention_utils.py"


def extract_function_block(source: str, func_name: str) -> str:
    lines = source.splitlines()
    start = None
    for idx, line in enumerate(lines):
        if line.startswith(f"def {func_name}("):
            start = idx
            break
    if start is None:
        return ""
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("def ") or lines[j].startswith("class "):
            return "\n".join(lines[start:j])
    return "\n".join(lines[start:])


def source_regression_evidence() -> dict[str, object]:
    source = FLASH_UTILS.read_text(encoding="utf-8")
    unpad_block = extract_function_block(source, "_unpad_input")
    get_unpad_block = extract_function_block(source, "_get_unpad_data")

    buggy_line = "max_seqlen_in_batch = seqlens_in_batch.max()"
    fixed_line = "max_seqlen_in_batch = seqlens_in_batch.max().item()"

    return {
        "source_path": str(FLASH_UTILS),
        "unpad_has_buggy_line": buggy_line in unpad_block,
        "unpad_has_fixed_line": fixed_line in unpad_block,
        "get_unpad_has_buggy_line": buggy_line in get_unpad_block,
        "get_unpad_has_fixed_line": fixed_line in get_unpad_block,
    }


def try_import_torch():
    try:
        import torch
        import torch.nn.functional as F
    except Exception as exc:  # pragma: no cover - runtime dependent
        return None, None, f"{type(exc).__name__}: {exc}"
    return torch, F, None


def _buggy_get_unpad_data(attention_mask, torch_mod, F_mod):
    seqlens_in_batch = attention_mask.sum(dim=-1, dtype=torch_mod.int32)
    indices = torch_mod.nonzero(attention_mask.flatten(), as_tuple=False).flatten()
    max_seqlen_in_batch = seqlens_in_batch.max()
    cu_seqlens = F_mod.pad(torch_mod.cumsum(seqlens_in_batch, dim=0, dtype=torch_mod.int32), (1, 0))
    return indices, cu_seqlens, max_seqlen_in_batch


def _fixed_get_unpad_data(attention_mask, torch_mod, F_mod):
    seqlens_in_batch = attention_mask.sum(dim=-1, dtype=torch_mod.int32)
    indices = torch_mod.nonzero(attention_mask.flatten(), as_tuple=False).flatten()
    max_seqlen_in_batch = seqlens_in_batch.max().item()
    cu_seqlens = F_mod.pad(torch_mod.cumsum(seqlens_in_batch, dim=0, dtype=torch_mod.int32), (1, 0))
    return indices, cu_seqlens, max_seqlen_in_batch


def benchmark_hot_path(max_seqlen, rounds: int = 250_000) -> float:
    start = time.perf_counter()
    checksum = 0
    for _ in range(rounds):
        checksum += int(max_seqlen)
    elapsed = time.perf_counter() - start
    # Keep the checksum live so the loop cannot be optimized away.
    if checksum < 0:  # pragma: no cover - defensive
        print(checksum)
    return elapsed


def main() -> int:
    evidence = source_regression_evidence()
    print(json.dumps({"source_evidence": evidence}, indent=2))

    torch_mod, F_mod, import_error = try_import_torch()
    if import_error:
        print(
            json.dumps(
                {
                    "status": "blocked",
                    "reason": "torch import failed in the local environment",
                    "detail": import_error,
                },
                indent=2,
            ),
            file=sys.stderr,
        )
        return 2

    if not torch_mod.cuda.is_available():
        print(
            json.dumps(
                {
                    "status": "blocked",
                    "reason": "CUDA is unavailable in this environment",
                    "detail": "The upstream reproducer requires a GPU and FlashAttention 2.",
                },
                indent=2,
            )
        )

    try:
        import importlib.util

        flash_attn_available = importlib.util.find_spec("flash_attn") is not None
    except Exception:
        flash_attn_available = False

    if not flash_attn_available:
        print(
            json.dumps(
                {
                    "status": "blocked",
                    "reason": "flash_attn is unavailable in this environment",
                    "detail": "This folder can only run a CPU-side proxy benchmark here.",
                },
                indent=2,
            )
        )

    # CPU proxy benchmark that mirrors the root cause: a tensor-valued max sequence
    # length forces downstream int coercion every iteration, while the fixed path
    # does the conversion once in the helper.
    attention_mask = torch_mod.ones((2, 8192), dtype=torch_mod.int32)
    attention_mask[1, 4096:] = 0

    _, _, buggy_max = _buggy_get_unpad_data(attention_mask, torch_mod, F_mod)
    _, _, fixed_max = _fixed_get_unpad_data(attention_mask, torch_mod, F_mod)

    benchmark_rounds = 250_000
    buggy_elapsed = benchmark_hot_path(buggy_max, benchmark_rounds)
    fixed_elapsed = benchmark_hot_path(fixed_max, benchmark_rounds)
    slowdown = (buggy_elapsed / fixed_elapsed) if fixed_elapsed else float("inf")

    result = {
        "status": "cpu_proxy_complete",
        "buggy_max_type": type(buggy_max).__name__,
        "fixed_max_type": type(fixed_max).__name__,
        "benchmark_rounds": benchmark_rounds,
        "buggy_elapsed_s": buggy_elapsed,
        "fixed_elapsed_s": fixed_elapsed,
        "slowdown_ratio": slowdown,
        "interpretation": (
            "The local snapshot still propagates a tensor-valued max sequence length. "
            "That is the regression mechanism called out in the upstream fix for #46693."
        ),
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
