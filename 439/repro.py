#!/usr/bin/env python3
"""Minimal repro for the WSL2 UVA gate in vLLM's V2 GPU request state init."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR / "codebase"))

import torch
import vllm.utils.platform_utils as platform_utils


def main() -> None:
    # Emulate the WSL2 pin-memory-off branch that triggers the bug report.
    platform_utils.is_pin_memory_available = lambda: False  # type: ignore[assignment]
    platform_utils.is_uva_available.cache_clear()

    print(f"is_uva_available={platform_utils.is_uva_available()}")

    from vllm.v1.worker.gpu.states import RequestState

    # This matches the bug report's failing initialization path:
    # RequestState -> StagedWriteTensor(uva_instead_of_gpu=True) -> UvaBuffer.
    RequestState(
        max_num_reqs=1,
        max_model_len=8,
        max_num_batched_tokens=8,
        num_speculative_steps=1,
        vocab_size=100,
        device=torch.device("cpu"),
    )


if __name__ == "__main__":
    main()
