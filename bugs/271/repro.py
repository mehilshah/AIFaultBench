# SPDX-License-Identifier: Apache-2.0
# DeepSpeed Team
from __future__ import annotations

import sys
from dataclasses import dataclass

import torch


@dataclass
class FakeParam:
    name: str
    ds_tensor: torch.Tensor


class FakeGatherBackend:
    """Stand-in for the collective check that PyTorch performs at runtime."""

    @staticmethod
    def all_gather_into_tensor(output_tensor: torch.Tensor, input_tensor: torch.Tensor) -> None:
        if output_tensor.dtype != input_tensor.dtype:
            raise TypeError("output tensor must have the same type as input tensor")
        output_tensor.view(-1)[: input_tensor.numel()].copy_(input_tensor.view(-1))


class FakeZeroContext:
    def __init__(self, num_partitions: int = 2):
        self.num_partitions = num_partitions
        self.local_device = "cpu"
        self.use_all_gather_into_tensor = True

    def _allgather_params_coalesced(self, param_list, hierarchy=0, quantize=False):
        if len(param_list) == 0:
            return

        partition_sizes = []
        local_tensors = []
        for param in param_list:
            partition_sizes.append(param.ds_tensor.numel())
            local_tensors.append(param.ds_tensor.to(self.local_device))

        allgather_params = []
        for psize in partition_sizes:
            tensor_size = psize * self.num_partitions
            flat_tensor = torch.empty(tensor_size, dtype=param_list[0].ds_tensor.dtype, device=self.local_device)
            allgather_params.append(flat_tensor)

        for param_idx, param in enumerate(param_list):
            input_tensor = local_tensors[param_idx].view(-1)
            FakeGatherBackend.all_gather_into_tensor(allgather_params[param_idx], input_tensor)


def main() -> int:
    ctx = FakeZeroContext(num_partitions=2)

    params = [
        FakeParam("base_weight", torch.tensor([1.0], dtype=torch.bfloat16)),
        FakeParam("lora_adapter", torch.tensor([2.0], dtype=torch.float32)),
    ]

    print("DeepSpeed ZeRO-3 mixed-dtype repro")
    print(f"  persistent params: {[p.name for p in params]}")
    print(f"  input dtypes     : {[p.ds_tensor.dtype for p in params]}")
    print(f"  output dtype     : {params[0].ds_tensor.dtype} (taken from param[0])")

    try:
        ctx._allgather_params_coalesced(params)
    except TypeError as exc:
        print(f"  raised           : {exc}")
        return 1

    print("  result           : unexpectedly succeeded")
    return 0


if __name__ == "__main__":
    sys.exit(main())
