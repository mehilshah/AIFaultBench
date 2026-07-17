#!/usr/bin/env python3
"""Reproduce the empty-shard behavior in accelerate's batch dispatcher.

This script avoids GPU and distributed runtime requirements by:
1. Building a one-element iterable dataset.
2. Instantiating accelerate's DataLoaderDispatcher directly.
3. Running the same batch-size arithmetic used by the dispatcher for a 4-process setup.

The bug is that a single sample becomes a batch of size 2 after fallback duplication,
which is then split into four process slices. Ranks 2 and 3 receive empty tensors.
"""

from __future__ import annotations

import torch
from torch.utils.data import DataLoader, IterableDataset

import accelerate.data_loader as dlmod
from accelerate.utils import concatenate, find_batch_size, slice_tensors


NUM_PROCESSES = 4


class FakeState:
    def __init__(self):
        self.process_index = 0
        self.num_processes = NUM_PROCESSES
        self.device = torch.device("cpu")
        self.distributed_type = dlmod.DistributedType.MULTI_CPU


class FakeGradientState:
    def _add_dataloader(self, *args, **kwargs):
        return None

    def _remove_dataloader(self, *args, **kwargs):
        return None

    def _set_remainder(self, *args, **kwargs):
        return None


class OneSampleDataset(IterableDataset):
    def __iter__(self):
        yield {
            "input_ids": torch.tensor([101, 102, 103], dtype=torch.long),
            "attention_mask": torch.tensor([1, 1, 1], dtype=torch.long),
        }


def main() -> int:
    original_accelerator_state = dlmod.AcceleratorState
    original_gradient_state = dlmod.GradientState
    original_broadcast_object_list = dlmod.broadcast_object_list

    try:
        # The dispatcher only needs a process-0 state to build the first batch.
        dlmod.AcceleratorState = lambda: FakeState()
        dlmod.GradientState = FakeGradientState
        dlmod.broadcast_object_list = lambda object_list, from_process=0: object_list

        dataloader = DataLoader(OneSampleDataset(), batch_size=1)
        dispatcher = dlmod.DataLoaderDispatcher(
            dataloader.dataset,
            split_batches=False,
            batch_size=dataloader.batch_size,
            _drop_last=dataloader.drop_last,
        )

        batch, batch_info = dispatcher._fetch_batches(iter(dataloader))
        observed_batch_size = find_batch_size(batch)
        batch_size_per_rank = observed_batch_size // NUM_PROCESSES
        first_batch = slice_tensors(batch, slice(0, NUM_PROCESSES))

        if observed_batch_size % NUM_PROCESSES != 0:
            batch = concatenate([batch, first_batch], dim=0)
            batch_size_per_rank += 1

        print(f"batch_info_stop={batch_info[1]}")
        print(f"observed_batch_size={observed_batch_size}")
        print(f"batch_size_per_rank={batch_size_per_rank}")

        results = []
        for rank in range(NUM_PROCESSES):
            data_slice = slice(rank * batch_size_per_rank, (rank + 1) * batch_size_per_rank)
            sliced = slice_tensors(batch, data_slice)
            shape = tuple(sliced["input_ids"].shape)
            attn_shape = tuple(sliced["attention_mask"].shape)
            results.append((shape, attn_shape))
            print(f"rank={rank} input_ids_shape={shape} attention_mask_shape={attn_shape}")

        expected = [((1, 3), (1, 3)), ((1, 3), (1, 3)), ((0, 3), (0, 3)), ((0, 3), (0, 3))]
        if results != expected:
            print(f"unexpected_results={results}")
            return 1

        print("BUG_REPRODUCED: ranks 2 and 3 receive empty tensors")
        return 0
    finally:
        dlmod.AcceleratorState = original_accelerator_state
        dlmod.GradientState = original_gradient_state
        dlmod.broadcast_object_list = original_broadcast_object_list


if __name__ == "__main__":
    raise SystemExit(main())
