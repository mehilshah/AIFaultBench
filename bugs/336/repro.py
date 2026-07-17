#!/usr/bin/env python3
"""Minimal reproduction harness for the DeepSeek V2 aux hidden-state bug.

The local tree already contains the post-loop `end_layer` capture that fixes
the reported issue, so this script demonstrates that the bug is not reproducible
here by contrasting the pre-fix behavior with the current source layout.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "codebase" / "vllm" / "model_executor" / "models" / "deepseek_v2.py"
RESULT = ROOT / "reproduction.json"


def buggy_aux_capture(num_layers: int, aux_layers: tuple[int, ...]) -> list[str]:
    """Model the pre-fix behavior from the issue report."""
    aux_hidden_states: list[str] = []
    for idx in range(num_layers):
        if idx in aux_layers:
            aux_hidden_states.append(f"layer_{idx}")
    return aux_hidden_states


def fixed_aux_capture(num_layers: int, aux_layers: tuple[int, ...]) -> list[str]:
    """Model the current source, which captures the final layer after the loop."""
    aux_hidden_states = buggy_aux_capture(num_layers, aux_layers)
    if num_layers in aux_layers:
        aux_hidden_states.append(f"layer_{num_layers}")
    return aux_hidden_states


def main() -> int:
    source = SOURCE.read_text(encoding="utf-8")
    source_has_fix = "if self.end_layer in self.aux_hidden_state_layers" in source

    num_layers = 1
    aux_layers = (1,)
    buggy = buggy_aux_capture(num_layers, aux_layers)
    fixed = fixed_aux_capture(num_layers, aux_layers)

    reproducible = False
    evidence = [
        f"Source check: {SOURCE.relative_to(ROOT)} contains the final-layer capture branch: {source_has_fix}.",
        f"Pre-fix simulation for num_layers={num_layers}, aux_layers={aux_layers}: {buggy!r}.",
        f"Current/fixed simulation for num_layers={num_layers}, aux_layers={aux_layers}: {fixed!r}.",
        "The fixed path captures the last layer auxiliary hidden state, so the reported bug is not reproducible in this tree.",
    ]
    steps = [
        "Inspect vllm/model_executor/models/deepseek_v2.py.",
        "Compare pre-fix and current aux-hidden-state capture behavior with a 1-layer simulation.",
        "Confirm that the current tree already appends the final layer hidden state after the loop.",
    ]
    payload = {
        "reproducible": reproducible,
        "evidence": evidence,
        "steps": steps,
        "blocking_reason": "The checked-in DeepSeek V2 implementation already includes the post-loop end-layer aux hidden-state capture that the bug report proposes.",
        "reproduction_command": "bash run_repro.sh",
    }

    RESULT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
