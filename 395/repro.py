#!/usr/bin/env python3
"""Minimal reproducer for the routed-experts empty-expert indexing crash.

This script mirrors the failing branch reported in
`vllm/model_executor/layers/fused_moe/routed_experts.py`:

    expert_data = param.data if full_load else param.data[expert_id]

When `param.data` has zero expert rows and `expert_id == 0`, the access
raises `IndexError`, matching the bug report.
"""

from __future__ import annotations


class ZeroSizedExpertTensor:
    def __getitem__(self, idx: int):
        raise IndexError("index 0 is out of bounds for dimension 0 with size 0")


class DummyParam:
    def __init__(self) -> None:
        self.data = ZeroSizedExpertTensor()


def weight_loader(param: DummyParam, loaded_weight, weight_name: str, shard_id: str, expert_id: int, return_success: bool = False):
    full_load = False
    # This is the exact access pattern that fails in the bug report.
    expert_data = param.data if full_load else param.data[expert_id]
    return expert_data


def main() -> int:
    param = DummyParam()
    loaded_weight = [[1, 2], [3, 4]]
    weight_loader(
        param=param,
        loaded_weight=loaded_weight,
        weight_name="w13_weight",
        shard_id="w1",
        expert_id=0,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
