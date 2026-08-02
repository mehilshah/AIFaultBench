#!/usr/bin/env python3
from __future__ import annotations

import json
import traceback
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Tuple


@dataclass
class Bucket:
    params: List[object] = field(default_factory=list)
    elements: int = 0


class DummyParam:
    def __init__(self, numel: int, ds_grad_is_ready: bool = True):
        self._numel = numel
        self.ds_numel = numel
        self.ds_grad_is_ready = ds_grad_is_ready
        self.grad = object()

    def partition_numel(self) -> int:
        return self._numel


class ReproHarness:
    def __init__(self, sub_group_size: int):
        self.sub_group_size = sub_group_size
        self.max_grad_numel = 0
        self.sub_group_to_param_num: Dict[int, int] = {}
        self.params_in_ipg_bucket_buffer = deque()
        self._cur_bucket_index = -1
        self.reduce_bucket_size = 1024
        self.ipg_buckets = {"fp16": Bucket()}
        self.grad_position: Dict[int, Tuple[int, int, int]] = {}

    def get_param_id(self, param: DummyParam) -> int:
        return id(param)

    def get_param_comm_dtype(self, param: DummyParam) -> str:
        return "fp16"

    def __add_grad_to_ipg_bucket(self, param: DummyParam) -> None:
        bucket = self.ipg_buckets[self.get_param_comm_dtype(param)]
        bucket.params.append(param)
        bucket.elements += param.ds_numel

    def __reduce_and_partition_ipg_grads(self, comm_dtype: str) -> None:
        # Unused in this reproducer because the KeyError fires before it matters.
        raise AssertionError(f"unexpected reduction for {comm_dtype}")

    def _create_fp16_sub_groups(self, params_group: List[DummyParam]):
        params_group_numel = sum([param.partition_numel() for param in params_group])
        sub_group_size = self.sub_group_size

        if sub_group_size is None or sub_group_size >= params_group_numel:
            return [params_group]

        sub_groups = []
        sub_group = []
        local_sub_group_size = 0

        for param in params_group:
            sub_group.append(param)
            local_sub_group_size += param.partition_numel()

            if local_sub_group_size >= sub_group_size or id(param) == id(params_group[-1]):
                self.max_grad_numel = max(self.max_grad_numel, local_sub_group_size)
                sub_groups.append(sub_group)
                self.sub_group_to_param_num[len(sub_groups) - 1] = len(sub_group)

                sub_group = []
                local_sub_group_size = 0

        return sub_groups

    def reduce_independent_p_g_buckets_and_remove_grads(self, param: DummyParam):
        comm_dtype = self.get_param_comm_dtype(param)
        bucket = self.ipg_buckets[comm_dtype]
        i, _, _ = self.grad_position[self.get_param_id(param)]

        if len(bucket.params) == 0:
            self._cur_bucket_index = i
            if getattr(param, "ds_grad_is_ready", True):
                self.__add_grad_to_ipg_bucket(param)

            # This is the bug: `sub_group_to_param_num` is empty for a single subgroup.
            if self.sub_group_to_param_num[self._cur_bucket_index] == 1:
                self.__reduce_and_partition_ipg_grads(comm_dtype)

        elif i != self._cur_bucket_index:
            self.params_in_ipg_bucket_buffer.append(param)
        else:
            if getattr(param, "ds_grad_is_ready", True):
                self.__add_grad_to_ipg_bucket(param)

            if self.sub_group_to_param_num[self._cur_bucket_index] == len(bucket.params):
                self.__reduce_and_partition_ipg_grads(comm_dtype)

                while self.params_in_ipg_bucket_buffer:
                    buffered_param = self.params_in_ipg_bucket_buffer.popleft()
                    ci, _, _ = self.grad_position[self.get_param_id(buffered_param)]
                    self._cur_bucket_index = ci
                    if getattr(buffered_param, "ds_grad_is_ready", True):
                        self.__add_grad_to_ipg_bucket(buffered_param)


def read_source_context() -> str:
    stage3 = Path("codebase/deepspeed/runtime/superoffload/superoffload_stage3.py").read_text()
    zero3 = Path("codebase/deepspeed/runtime/zero/stage3.py").read_text()

    snippets = [
        "Relevant source context:",
        "1) superoffload_stage3.py: `_create_fp16_sub_groups` returns early for a single subgroup.",
        "2) superoffload_stage3.py: `reduce_independent_p_g_buckets_and_remove_grads` immediately indexes `sub_group_to_param_num`.",
        "3) stage3.py: offload bookkeeping is based on the subgroup count, so a single subgroup keeps the mapping empty.",
        "",
        "--- superoffload excerpt ---",
        "\n".join(stage3.splitlines()[30:110]),
        "",
        "--- stage3 excerpt ---",
        "\n".join(zero3.splitlines()[962:1040]),
    ]
    return "\n".join(snippets)


def main() -> int:
    print(read_source_context())

    harness = ReproHarness(sub_group_size=16)
    param = DummyParam(numel=4)

    created = harness._create_fp16_sub_groups([param])
    harness.grad_position[harness.get_param_id(param)] = (0, 0, 0)

    outcome = {
        "reproducible": False,
        "evidence": "",
        "steps": [],
        "blocking_reason": "",
        "reproduction_command": "bash run_repro.sh",
    }

    try:
        harness.reduce_independent_p_g_buckets_and_remove_grads(param)
        outcome["evidence"] = "No exception was raised when the empty mapping path was exercised."
        outcome["steps"] = [
            "Create a single dummy parameter whose total numel is smaller than the subgroup threshold.",
            "Call the subgroup splitter, which returns one subgroup and leaves `sub_group_to_param_num` empty.",
            "Trigger the first bucket reduction path with a matching grad position.",
        ]
        outcome["blocking_reason"] = "The bug did not reproduce in this run."
    except KeyError as exc:
        outcome["reproducible"] = True
        outcome["evidence"] = (
            f"KeyError reproduced as expected: {exc!r}. "
            f"After `_create_fp16_sub_groups`, sub_group_to_param_num={harness.sub_group_to_param_num}; "
            f"the first bucket reduction set _cur_bucket_index={harness._cur_bucket_index} and then indexed the empty map."
        )
        outcome["steps"] = [
            f"Create a single dummy parameter and split it with `_create_fp16_sub_groups`; it returns {len(created)} subgroup(s).",
            f"Observe that `sub_group_to_param_num` stays empty: {harness.sub_group_to_param_num}.",
            "Call `reduce_independent_p_g_buckets_and_remove_grads` for that parameter and hit `KeyError: 0`.",
        ]
        outcome["blocking_reason"] = ""
    except Exception as exc:
        outcome["reproducible"] = False
        outcome["evidence"] = f"Unexpected exception type: {type(exc).__name__}: {exc}"
        outcome["steps"] = [
            "Create a single dummy parameter whose total numel is smaller than the subgroup threshold.",
            "Trigger the first bucket reduction path.",
        ]
        outcome["blocking_reason"] = f"Unexpected failure while reproducing: {type(exc).__name__}: {exc}"
        traceback.print_exc()

    Path("reproduction.json").write_text(json.dumps(outcome, indent=2) + "\n")
    print(json.dumps(outcome, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
