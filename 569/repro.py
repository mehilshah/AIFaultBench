#!/usr/bin/env python3
"""Minimal reproduction for the Minimax M3 attention head-collapsing bug.

The local Transformers implementation computes:

    block_scores = scores.amax(dim=-1).amax(dim=1)

That second reduction removes the head axis and produces one shared block ranking
for all heads. The reference behavior keeps the per-head block scores separate.

This script constructs a tiny synthetic score tensor where the two heads prefer
different blocks, then compares the collapsed ranking against the per-head
reference ranking.
"""

from __future__ import annotations

import json

import torch


def main() -> None:
    batch = 1
    heads = 2
    q_len = 1
    num_blocks = 2
    block_size = 2

    # Shape before pooling: [B, H, S_q, S_k]
    # Head 0 strongly prefers block 0.
    # Head 1 strongly prefers block 1.
    scores = torch.tensor(
        [[[[10.0, 9.0, 1.0, 0.0]], [[0.0, 1.0, 9.0, 10.0]]]],
        dtype=torch.float32,
    )

    pooled = scores.view(batch, heads, q_len, num_blocks, block_size).amax(dim=-1)
    current_block_scores = pooled.amax(dim=1)
    reference_block_scores = pooled

    current_top1 = current_block_scores.topk(1, dim=-1).indices
    reference_top1 = reference_block_scores.topk(1, dim=-1).indices

    evidence = {
        "scores_shape": list(scores.shape),
        "current_block_scores": current_block_scores.tolist(),
        "reference_block_scores": reference_block_scores.tolist(),
        "current_top1": current_top1.tolist(),
        "reference_top1": reference_top1.tolist(),
        "shared_ranking": current_top1[0, 0].item(),
        "head0_ranking": reference_top1[0, 0, 0].item(),
        "head1_ranking": reference_top1[0, 1, 0].item(),
    }

    print(json.dumps(evidence, indent=2, sort_keys=True))

    if current_top1[0, 0, 0].item() == reference_top1[0, 0, 0].item() and current_top1[0, 0, 0].item() == reference_top1[0, 1, 0].item():
        raise SystemExit("Unexpectedly no divergence was observed.")


if __name__ == "__main__":
    main()
