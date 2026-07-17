#!/usr/bin/env python3
"""Minimal reproduction for DeepSpeed SuperOffload subgroup indexing bug.

The bug report says `sub_group_to_param_num` is populated with local subgroup
indices per optimizer group, but later the code looks up the dictionary with the
global subgroup index (`_cur_bucket_index` / `grad_position[i][0]`).

This harness mirrors that bookkeeping with a tiny pure-Python model of the
relevant control flow and triggers the same `KeyError: 2` when a third global
subgroup is processed.
"""

from __future__ import annotations

import json
import traceback
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class DummyParam:
    name: str
    numel_value: int = 1

    def partition_numel(self) -> int:
        return self.numel_value


@dataclass
class DummyBucket:
    params: List[DummyParam]


def create_fp16_sub_groups(params_group: List[DummyParam], sub_group_size: int, sub_group_to_param_num: Dict[int, int]):
    params_group_numel = sum(param.partition_numel() for param in params_group)
    if sub_group_size is None or sub_group_size >= params_group_numel:
        return [params_group]

    sub_groups = []
    sub_group = []
    local_sub_group_size = 0

    for param in params_group:
        sub_group.append(param)
        local_sub_group_size += param.partition_numel()

        if local_sub_group_size >= sub_group_size or param is params_group[-1]:
            sub_groups.append(sub_group)
            # This mirrors the buggy code in
            # `deepspeed/runtime/superoffload/superoffload_stage3.py`.
            sub_group_to_param_num[len(sub_groups) - 1] = len(sub_group)
            sub_group = []
            local_sub_group_size = 0

    return sub_groups


def main() -> int:
    # Two optimizer parameter groups, each split into two subgroups.
    # The resulting global subgroup layout is:
    #   group 0 -> global indices 0, 1
    #   group 1 -> global indices 2, 3
    # but the buggy dictionary is keyed only by local subgroup indices 0 and 1.
    sub_group_to_param_num: Dict[int, int] = {}
    fp16_groups: List[List[DummyParam]] = []

    group_0 = [DummyParam("g0.p0"), DummyParam("g0.p1")]
    group_1 = [DummyParam("g1.p0"), DummyParam("g1.p1")]
    fp16_groups.extend(create_fp16_sub_groups(group_0, sub_group_size=1, sub_group_to_param_num=sub_group_to_param_num))
    fp16_groups.extend(create_fp16_sub_groups(group_1, sub_group_size=1, sub_group_to_param_num=sub_group_to_param_num))

    grad_position = {}
    for i, group in enumerate(fp16_groups):
        current_offset = 0
        for param in group:
            grad_position[id(param)] = [i, current_offset, param.partition_numel()]
            current_offset += param.partition_numel()

    target_param = fp16_groups[2][0]
    bucket = DummyBucket(params=[])
    current_bucket_index = -1

    print("fp16_groups:", [[p.name for p in group] for group in fp16_groups])
    print("sub_group_to_param_num:", sub_group_to_param_num)
    print("grad_position[target]:", grad_position[id(target_param)])
    print("selected target:", target_param.name)

    try:
        # Mirrors `reduce_independent_p_g_buckets_and_remove_grads` in
        # `superoffload_stage3.py`.
        i, _, _ = grad_position[id(target_param)]
        if len(bucket.params) == 0:
            current_bucket_index = i
            bucket.params.append(target_param)
            if sub_group_to_param_num[current_bucket_index] == 1:
                pass
        print("unexpected success", current_bucket_index)
        return 0
    except Exception as exc:
        print("EXPECTED FAILURE")
        print(f"{type(exc).__name__}: {exc}")
        print(traceback.format_exc())
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
