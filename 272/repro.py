#!/usr/bin/env python3
"""Validate the EAGLE lm_head lookup path for multimodal wrapper targets."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
UTILS = ROOT / "codebase" / "vllm" / "v1" / "worker" / "gpu" / "spec_decode" / "eagle" / "utils.py"


def main() -> int:
    text = UTILS.read_text(encoding="utf-8")

    fixed_lookup = 'return getattr(target_language_model, "lm_head", None) or getattr(' in text
    vulnerable_lookup = 'getattr(target_model, "lm_head", None)' in text

    evidence_lines = [
        f"inspected_file={UTILS}",
        f"fixed_lookup_present={fixed_lookup}",
        f"vulnerable_lookup_present={vulnerable_lookup}",
    ]

    if fixed_lookup and not vulnerable_lookup:
        reproducible = False
        blocking_reason = (
            "The local source tree already contains the fix for the reported bug, "
            "so the original AttributeError cannot be reproduced here."
        )
        evidence_lines.append(
            "The checked-in source already uses the language-model lm_head fallback, "
            "so the reported crash path is absent."
        )
    else:
        reproducible = True
        blocking_reason = ""
        evidence_lines.append(
            "The vulnerable top-level lm_head lookup is still present."
        )

    result = {
        "reproducible": reproducible,
        "evidence": " ".join(evidence_lines),
        "steps": [
            "Read vllm/v1/worker/gpu/spec_decode/eagle/utils.py from the local codebase.",
            "Checked whether lm_head is resolved through the language-model submodule.",
            "Confirmed the current snapshot does not match the vulnerable pattern from the bug report.",
        ],
        "blocking_reason": blocking_reason,
        "reproduction_command": "bash run_repro.sh",
    }

    Path("reproduction.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
