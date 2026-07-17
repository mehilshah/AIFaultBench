#!/usr/bin/env python3
"""Minimal reproduction for vLLM issue 47418.

The bug is the unconditional attribute access in
`vllm/v1/worker/gpu/spec_decode/dspark/speculator.py`:

    if self.draft_logits is not None and model.draft_id_to_target_id is not None:

`DSparkDeepseekV4ForCausalLM` in
`vllm/models/deepseek_v4/nvidia/dspark.py` does not define
`draft_id_to_target_id`, so the check raises `AttributeError` as soon as DSpark
probabilistic sampling is enabled.
"""

from __future__ import annotations


class DSparkDeepseekV4ForCausalLM:
    """Stand-in for the DeepSeek-V4 DSpark draft model."""


def buggy_load_draft_model(model: DSparkDeepseekV4ForCausalLM) -> None:
    # This mirrors the buggy branch in DSparkSpeculator.load_draft_model().
    draft_logits = object()
    if draft_logits is not None and model.draft_id_to_target_id is not None:
        print("unreachable")


def main() -> None:
    model = DSparkDeepseekV4ForCausalLM()
    buggy_load_draft_model(model)


if __name__ == "__main__":
    main()
