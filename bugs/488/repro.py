#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


GLM52_FREQ = 4
GLM52_OFFSET = 2
MAX_LAYER_TO_CHECK = 12
EXPECTED_CARRY_LAYERS = [0, 1, 2, 6, 10]


def actual_carry_layers(
    *, max_layer: int, freq: int, offset: int
) -> list[int]:
    """Mirror the current sparse-indexer formula from the source tree."""

    carry_layers: list[int] = []
    for layer_id in range(max_layer):
        skip_topk = max(layer_id - offset + 1, 0) % freq != 0
        if not skip_topk:
            carry_layers.append(layer_id)
    return carry_layers


def main() -> int:
    source_path = Path("codebase/vllm/models/deepseek_v32/nvidia/attention.py")
    source = source_path.read_text(encoding="utf-8")

    if "GLM-5.2 uses index_topk_freq=4" not in source:
        raise RuntimeError(f"missing expected GLM-5.2 comment in {source_path}")

    actual = actual_carry_layers(
        max_layer=MAX_LAYER_TO_CHECK, freq=GLM52_FREQ, offset=GLM52_OFFSET
    )

    print("GLM-5.2 sparse indexer schedule check")
    print(f"source: {source_path}")
    print(
        "documented carry layers (from comment): "
        f"{EXPECTED_CARRY_LAYERS}"
    )
    print(
        "current formula carry layers: "
        f"{actual}"
    )

    if actual != EXPECTED_CARRY_LAYERS:
        raise AssertionError(
            "GLM-5.2 sparse-indexer layer selection does not match the "
            "documented schedule"
        )

    print("schedule matches")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
