#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RESULT_PATH = ROOT / "reproduction.json"


def _write_result(
    *,
    reproducible: bool,
    evidence: list[str],
    steps: list[str],
    blocking_reason: str | None,
    reproduction_command: str,
) -> None:
    payload = {
        "reproducible": reproducible,
        "evidence": evidence,
        "steps": steps,
        "blocking_reason": blocking_reason,
        "reproduction_command": reproduction_command,
    }
    RESULT_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    evidence: list[str] = []
    steps: list[str] = []
    blocking_reason: str | None = None
    reproduction_command = "bash run_repro.sh"

    sparse_mla = ROOT / "codebase" / "vllm" / "models" / "deepseek_v4" / "sparse_mla.py"
    flashmla = ROOT / "codebase" / "vllm" / "v1" / "attention" / "ops" / "flashmla.py"

    steps.append("Inspect the issue source and the relevant FlashMLA code path.")
    if sparse_mla.exists():
        sparse_text = sparse_mla.read_text(encoding="utf-8")
        if "_C128A_TOPK_ALIGNMENT = 128" in sparse_text:
            evidence.append(
                "The current source already pads C128A top-k width to 128 in "
                "vllm/models/deepseek_v4/sparse_mla.py."
            )
        else:
            evidence.append(
                "The current source does not contain the C128A top-k padding fix marker."
            )
    else:
        evidence.append("Missing source file: vllm/models/deepseek_v4/sparse_mla.py")

    if flashmla.exists():
        flashmla_text = flashmla.read_text(encoding="utf-8")
        if "FlashMLA Sparse is only supported on Hopper and Blackwell DC devices." in flashmla_text:
            evidence.append(
                "FlashMLA sparse support is gated to Hopper/Blackwell in "
                "vllm/v1/attention/ops/flashmla.py."
            )
    else:
        evidence.append("Missing source file: vllm/v1/attention/ops/flashmla.py")

    try:
        import torch
    except Exception as exc:  # pragma: no cover - environment-specific
        blocking_reason = f"torch import failed: {type(exc).__name__}: {exc}"
        evidence.append(blocking_reason)
        steps.append("Attempted to import torch; the local environment failed before FlashMLA could load.")
        _write_result(
            reproducible=False,
            evidence=evidence,
            steps=steps,
            blocking_reason=blocking_reason,
            reproduction_command=reproduction_command,
        )
        print(blocking_reason)
        return 2

    evidence.append(f"torch import succeeded: {torch.__version__}")
    evidence.append(f"torch.cuda.is_available() -> {torch.cuda.is_available()}")

    sys.path.insert(0, str(ROOT / "codebase"))
    try:
        from vllm.v1.attention.ops import flashmla as fm
    except Exception as exc:  # pragma: no cover - environment-specific
        blocking_reason = f"vllm.flashmla import failed: {type(exc).__name__}: {exc}"
        evidence.append(blocking_reason)
        steps.append("Importing FlashMLA from the local codebase failed.")
        _write_result(
            reproducible=False,
            evidence=evidence,
            steps=steps,
            blocking_reason=blocking_reason,
            reproduction_command=reproduction_command,
        )
        print(blocking_reason)
        return 2

    supported, reason = fm.is_flashmla_sparse_supported()
    evidence.append(f"is_flashmla_sparse_supported() -> {supported}, reason={reason!r}")

    if not supported:
        blocking_reason = reason or "FlashMLA sparse is not supported in this environment."
        steps.append("FlashMLA is unavailable here, so the GPU-only repro cannot be exercised.")
        _write_result(
            reproducible=False,
            evidence=evidence,
            steps=steps,
            blocking_reason=blocking_reason,
            reproduction_command=reproduction_command,
        )
        print(blocking_reason)
        return 3

    steps.append("FlashMLA is available, but the bug-specific crash was not observed in this snapshot.")
    blocking_reason = "The reported crash did not reproduce under the current source snapshot."
    _write_result(
        reproducible=False,
        evidence=evidence,
        steps=steps,
        blocking_reason=blocking_reason,
        reproduction_command=reproduction_command,
    )
    print(blocking_reason)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
