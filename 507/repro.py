#!/usr/bin/env python3
"""Source-level repro probe for vLLM issue #48493.

The reported crash is triggered when the MiniMax-M3 Marlin MoE path reaches
`SWIGLUOAI_UNINTERLEAVE` without a clamp limit. In this checkout the code
already threads `swiglu_limit` into `clamp_limit`, so the missing-parameter
failure is not reproducible here.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
ACTIVATION = CODEBASE / "vllm/model_executor/layers/fused_moe/activation.py"
MARLIN = CODEBASE / "vllm/model_executor/layers/fused_moe/experts/marlin_moe.py"
UNQUANT = CODEBASE / "vllm/model_executor/layers/fused_moe/unquantized_fused_moe_method.py"
RESULT = ROOT / "reproduction.json"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    activation_text = read_text(ACTIVATION)
    marlin_text = read_text(MARLIN)
    unquant_text = read_text(UNQUANT)

    assert_line = (
        'assert clamp_limit is not None, "SWIGLUOAI_UNINTERLEAVE requires clamp_limit"'
    )
    clamp_threaded = "clamp_limit=self.gemm1_clamp_limit" in marlin_text
    clamp_plumbed = (
        'gemm1_clamp_limit = getattr(layer, "swiglu_limit", None)' in unquant_text
    )
    low_level_assert = assert_line in activation_text

    evidence = []
    evidence.append(
        "Low-level activation guard still exists: "
        + ("yes" if low_level_assert else "no")
    )
    evidence.append(
        "Marlin MoE path threads clamp_limit: "
        + ("yes" if clamp_threaded else "no")
    )
    evidence.append(
        "Unquantized MoE config plumbs swiglu_limit into gemm1_clamp_limit: "
        + ("yes" if clamp_plumbed else "no")
    )

    reproducible = not (clamp_threaded and clamp_plumbed)
    blocking_reason = (
        "Current checkout already carries the clamp-limit plumbing for "
        "MiniMax-M3 MoE, so the reported Marlin warmup failure is not "
        "reproducible here."
        if not reproducible
        else ""
    )
    steps = [
        "Inspect the MiniMax-M3 MoE path in `marlin_moe.py` and verify that `quant_config.gemm1_clamp_limit` is stored and passed into the fused Marlin kernel.",
        "Inspect `unquantized_fused_moe_method.py` and verify that `layer.swiglu_limit` is copied into `FusedMoEQuantConfig` as `gemm1_clamp_limit`.",
        "Confirm the low-level activation helper still asserts when called without a clamp limit, which is expected and not the reported caller bug.",
    ]

    result = {
        "reproducible": reproducible,
        "evidence": evidence,
        "steps": steps,
        "blocking_reason": blocking_reason,
        "reproduction_command": "bash run_repro.sh",
    }
    RESULT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("Reproduction command:", result["reproduction_command"])
    for line in evidence:
        print(line)
    print("Conclusion:", "reproducible" if reproducible else "not reproducible")
    print("Result written to:", RESULT.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
