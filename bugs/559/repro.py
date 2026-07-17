#!/usr/bin/env python3
from pathlib import Path
import sys

import torch


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase" / "src"))

from accelerate.state import PartialState
from accelerate.utils import DistributedType
from accelerate.utils.operations import reduce as accelerate_reduce


def install_mock_distributed_state():
    # This keeps the repro focused on the reducer logic itself.
    PartialState._shared_state = {
        "_cpu": False,
        "backend": "gloo",
        "device": torch.device("cpu"),
        "distributed_type": DistributedType.MULTI_CPU,
        "num_processes": 4,
        "process_index": 0,
        "local_process_index": 0,
    }


def main():
    install_mock_distributed_state()
    state = PartialState()

    expected_sum = torch.tensor([16, 20, 24, 28])

    def fake_all_reduce(tensor, op):
        tensor.copy_(expected_sum)

    original_all_reduce = torch.distributed.all_reduce
    try:
        torch.distributed.all_reduce = fake_all_reduce

        process_tensor = torch.arange(state.num_processes) + 1 + (4 * state.process_index)
        sum_reduced_tensor = accelerate_reduce(process_tensor, reduction="sum")
        mean_reduced_tensor = accelerate_reduce(process_tensor, reduction="mean")

        print(f"distributed_type={state.distributed_type}")
        print(f"input={process_tensor}")
        print(f"sum={sum_reduced_tensor}")
        print(f"mean={mean_reduced_tensor}")
        print(f"expected_mean={expected_sum // state.num_processes}")

        if torch.equal(sum_reduced_tensor, mean_reduced_tensor):
            raise AssertionError("BUG: reduction='mean' returned the same tensor as reduction='sum'")

        raise AssertionError("Expected reduction='mean' to differ from reduction='sum', but it did not")
    finally:
        torch.distributed.all_reduce = original_all_reduce


if __name__ == "__main__":
    main()
