#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass

import torch


@dataclass
class DummyBatch:
    logits_indices: torch.Tensor


class DummySpeculator:
    def __init__(self) -> None:
        # Mirrors the MTPSpeculator contract in vLLM: the speculator assumes the
        # draft model returns a single tensor.
        self.model_returns_tuple = False

    def _run_model(self):
        # The regression is triggered when the draft model returns a tuple
        # anyway. The second element is the aux-hidden-state payload used by
        # several GLM-family models.
        return torch.zeros(4, 8), [torch.zeros(4, 8)]

    def prefill(self) -> None:
        ret_hidden_states = self._run_model()
        if self.model_returns_tuple:
            last_hidden_states, hidden_states = ret_hidden_states
        else:
            last_hidden_states = ret_hidden_states
            hidden_states = ret_hidden_states

        last_token_indices = torch.tensor([0, 2], dtype=torch.int64)
        # This is the same shape of bug as the upstream traceback:
        # tuple indexing with a tensor.
        _ = last_hidden_states[last_token_indices]


def main() -> None:
    batch = DummyBatch(logits_indices=torch.tensor([0, 1], dtype=torch.int64))
    speculator = DummySpeculator()

    print("batch.logits_indices =", batch.logits_indices.tolist())
    print("running DummySpeculator.prefill() ...")
    speculator.prefill()


if __name__ == "__main__":
    main()
