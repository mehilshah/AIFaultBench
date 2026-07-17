#!/usr/bin/env python3
"""Minimal reproduction for stale GradientState after an eval loop."""

from torch.utils.data import DataLoader, TensorDataset

import torch

from accelerate import Accelerator, debug_launcher


def repro_worker():
    accelerator = Accelerator()

    # A train loader that will continue after evaluation and an eval loader that
    # ends mid-run so it leaves the shared GradientState at end_of_dataloader=True.
    train_loader = DataLoader(TensorDataset(torch.arange(12)), batch_size=2, shuffle=False)
    eval_loader = DataLoader(TensorDataset(torch.arange(6)), batch_size=2, shuffle=False)

    train_loader, eval_loader = accelerator.prepare(train_loader, eval_loader)

    train_iter = iter(train_loader)
    first_train_batch = next(train_iter)[0]
    if accelerator.process_index == 0:
        print("first_train_batch", first_train_batch.tolist())
        print("state_before_eval", repr(accelerator.gradient_state))

    for batch in eval_loader:
        gathered = accelerator.gather_for_metrics(batch[0])
        if accelerator.process_index == 0:
            print("eval_gathered_shape", tuple(gathered.shape), "values", gathered.tolist())

    if accelerator.process_index == 0:
        print("state_after_eval", repr(accelerator.gradient_state))

    second_train_batch = next(train_iter)[0]
    gathered = accelerator.gather_for_metrics(second_train_batch)
    if accelerator.process_index == 0:
        print("train_after_eval_shape", tuple(gathered.shape), "values", gathered.tolist())

    # The bug reproduces when this non-final train batch is truncated down to the
    # eval remainder size instead of keeping the full gathered batch.
    expected_gathered_size = accelerator.num_processes * len(second_train_batch)
    if accelerator.process_index == 0:
        print("expected_train_after_eval_shape", expected_gathered_size)

    assert tuple(gathered.shape) == (
        expected_gathered_size,
    ), "gather_for_metrics truncated a non-final train batch after eval"


def main():
    debug_launcher(repro_worker)


if __name__ == "__main__":
    main()
