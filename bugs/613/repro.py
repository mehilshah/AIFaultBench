#!/usr/bin/env python3
"""Minimal repro for the Gemma 4 expert_weights AttributeError.

The failure described in bug_report.txt comes from the unified Gemma 4
wrapper dereferencing `self.language_model.expert_weights` while the
text-only Gemma4ForCausalLM class in the local codebase does not assign
that attribute during initialization.
"""

from __future__ import annotations

import json
import traceback
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
GEMMA4 = CODEBASE / "vllm/model_executor/models/gemma4.py"
GEMMA4_UNIFIED = CODEBASE / "vllm/model_executor/models/gemma4_unified.py"


class Gemma4ForCausalLM:
    """Proxy that matches the broken protocol surface in the report.

    It intentionally defines the MoE metadata that Gemma4ForCausalLM
    already populates in the source tree, but omits `expert_weights`.
    """

    def __init__(self) -> None:
        self.moe_layers = []
        self.num_moe_layers = 0
        self.num_logical_experts = 0
        self.num_physical_experts = 0
        self.num_local_physical_experts = 0
        self.num_routed_experts = 0
        self.num_expert_groups = 1
        self.num_shared_experts = 0
        self.num_redundant_experts = 0


class Gemma4ForConditionalGeneration:
    """Stand-in for the unified wrapper's MoE delegation line."""

    def __init__(self, language_model: Gemma4ForCausalLM) -> None:
        self.language_model = language_model
        self.expert_weights = self.language_model.expert_weights


def _extract_evidence() -> dict[str, object]:
    gemma4_src = GEMMA4.read_text()
    unified_src = GEMMA4_UNIFIED.read_text()

    return {
        "gemma4_has_expert_weights_assignment": "self.expert_weights = []" in gemma4_src,
        "gemma4_unified_accesses_expert_weights": (
            "self.expert_weights = self.language_model.expert_weights" in unified_src
        ),
        "gemma4_proxy_source_hint": "Gemma4ForCausalLM" in gemma4_src,
    }


def main() -> int:
    evidence = _extract_evidence()
    print(json.dumps({"source_evidence": evidence}, indent=2, sort_keys=True))

    try:
        # This mirrors the failing line in gemma4_unified.py:
        # self.expert_weights = self.language_model.expert_weights
        language_model = Gemma4ForCausalLM()
        _ = Gemma4ForConditionalGeneration(language_model)
    except AttributeError as exc:
        print("Observed failure:")
        traceback.print_exc()
        print(f"\nException text: {exc}")
        return 1

    print("Unexpectedly no AttributeError was raised.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
