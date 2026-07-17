#!/usr/bin/env python3
"""Minimal reproduction for the LayoutLM bbox range validation bug."""

from __future__ import annotations

import sys
import types

import torch

# The bundled codebase expects a newer torch distributed API than the minimal
# CPU wheel available in this environment. Stub the missing symbols so we can
# reach the actual bbox validation path under test.
try:
    import torch.distributed.tensor as torch_distributed_tensor
except Exception:  # pragma: no cover - import-time compatibility shim
    torch_distributed_tensor = None
else:
    if not hasattr(torch_distributed_tensor, "DTensor"):
        class DTensor:  # noqa: N801 - mimic the upstream symbol name
            pass

        torch_distributed_tensor.DTensor = DTensor

    if "torch.distributed.tensor._utils" not in sys.modules:
        tensor_utils = types.ModuleType("torch.distributed.tensor._utils")

        def compute_local_shape_and_global_offset(shape, device_mesh, placements):
            return tuple(shape), tuple(0 for _ in shape)

        tensor_utils.compute_local_shape_and_global_offset = compute_local_shape_and_global_offset
        sys.modules["torch.distributed.tensor._utils"] = tensor_utils

    if "torch.distributed.tensor.placement_types" not in sys.modules:
        placement_types = types.ModuleType("torch.distributed.tensor.placement_types")

        class Shard:  # pragma: no cover - import-time compatibility shim
            def __init__(self, dim=0):
                self.dim = dim

            def is_shard(self):
                return True

            @staticmethod
            def local_shard_size_and_offset(length, world_size, rank):
                base = length // world_size
                remainder = length % world_size
                local_shard_size = base + (1 if rank < remainder else 0)
                local_shard_offset = rank * base + min(rank, remainder)
                return local_shard_size, local_shard_offset

        placement_types.Shard = Shard
        sys.modules["torch.distributed.tensor.placement_types"] = placement_types

from transformers import LayoutLMConfig, LayoutLMModel


def main() -> None:
    # Tiny config keeps the repro fast and avoids any need for pretrained weights.
    config = LayoutLMConfig(
        vocab_size=100,
        hidden_size=32,
        num_hidden_layers=1,
        num_attention_heads=4,
        intermediate_size=64,
        max_position_embeddings=64,
        max_2d_position_embeddings=1001,
        type_vocab_size=2,
    )

    model = LayoutLMModel(config)
    model.eval()

    input_ids = torch.zeros((1, 4), dtype=torch.long)
    bbox = torch.tensor(
        [[[0, 0, 0, 0], [1, 1, 1001, 1], [0, 0, 0, 0], [0, 0, 0, 0]]],
        dtype=torch.long,
    )

    print("Calling LayoutLMModel with an invalid bbox value of 1001.")
    model(input_ids=input_ids, bbox=bbox)


if __name__ == "__main__":
    main()
