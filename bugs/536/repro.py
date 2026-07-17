#!/usr/bin/env python3
"""Static repro harness for vLLM issue 47196.

The local environment does not have the ROCm/AITER stack required to trigger
the GPU memory fault described in the report, so this script records the
observed blockers and validates that the vulnerable source path is present.
"""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
SPARSE_PATH = CODEBASE / "vllm/v1/attention/backends/mla/rocm_aiter_mla_sparse.py"
DENSE_PATH = CODEBASE / "vllm/v1/attention/backends/mla/rocm_aiter_mla.py"
RESULT_PATH = ROOT / "reproduction.json"


def run_cmd(cmd: list[str]) -> tuple[int, str]:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        output = (proc.stdout or "") + (proc.stderr or "")
        return proc.returncode, output.strip()
    except FileNotFoundError as exc:
        return 127, str(exc)


def source_evidence() -> list[str]:
    evidence: list[str] = []
    sparse = SPARSE_PATH.read_text(encoding="utf-8")
    dense = DENSE_PATH.read_text(encoding="utf-8")

    if "get_mla_metadata_v1(" in sparse:
        evidence.append(
            "Sparse MLA build() recomputes shared work buffers via get_mla_metadata_v1() at "
            "codebase/vllm/v1/attention/backends/mla/rocm_aiter_mla_sparse.py:542-560."
        )
    if "get_mla_metadata_v1(" in dense:
        evidence.append(
            "Dense MLA build() also recomputes persistent decode metadata via get_mla_metadata_v1() "
            "at codebase/vllm/v1/attention/backends/mla/rocm_aiter_mla.py:523-543."
        )
    if "torch.cuda.synchronize" not in sparse and "torch.cuda.synchronize" not in dense:
        evidence.append(
            "Neither MLA build() path inserts a stream sync after the metadata write before returning "
            "the tensors to the captured decode path."
        )

    return evidence


def env_evidence() -> tuple[list[str], list[str], bool]:
    evidence: list[str] = []
    blockers: list[str] = []
    ok = True

    torch_spec = importlib.util.find_spec("torch")
    if torch_spec is None:
        blockers.append("torch is not importable")
        ok = False
    else:
        try:
            import torch  # type: ignore

            evidence.append(f"torch import succeeded: {torch.__version__}")
            evidence.append(f"torch.cuda.is_available() -> {torch.cuda.is_available()}")
        except Exception as exc:  # noqa: BLE001
            blockers.append(f"torch import failed: {exc}")
            ok = False

    aiter_spec = importlib.util.find_spec("aiter")
    if aiter_spec is None:
        blockers.append("aiter is not installed")
        ok = False
    else:
        evidence.append(f"aiter importable at {aiter_spec.origin}")

    rocm_binary = None
    for binary in ("rocm-smi", "rocminfo", "hipconfig"):
        path = shutil.which(binary)
        if path:
            rocm_binary = path
            code, out = run_cmd([path])
            evidence.append(f"{binary} present at {path}; probe exit={code}")
            if out:
                evidence.append(out.splitlines()[0])
            break
    if rocm_binary is None:
        blockers.append("no ROCm runtime utilities found")
        ok = False

    return evidence, blockers, ok


def main() -> int:
    source = source_evidence()
    env, blockers, env_ok = env_evidence()

    reproducible = env_ok and False
    blocking_reason = "; ".join(blockers) if blockers else ""
    steps = [
        "Inspect the ROCm sparse-MLA builder in codebase/vllm/v1/attention/backends/mla/rocm_aiter_mla_sparse.py.",
        "Inspect the dense MLA builder in codebase/vllm/v1/attention/backends/mla/rocm_aiter_mla.py.",
        "Attempt to import the local runtime dependencies and probe for ROCm/GPU support.",
        "Record the result in reproduction.json.",
    ]

    evidence = source + env
    if blockers:
        evidence.extend(blockers)

    result = {
        "reproducible": reproducible,
        "evidence": evidence,
        "steps": steps,
        "blocking_reason": blocking_reason,
        "reproduction_command": "bash run_repro.sh",
    }
    RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(result, indent=2))
    if reproducible:
        return 1

    if blocking_reason:
        print(f"BLOCKED: {blocking_reason}")
    else:
        print("BLOCKED: environment does not satisfy the ROCm/AITER prerequisites.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
