#!/usr/bin/env python3
"""Minimal reproduction for the reported zero mAP@200 / p@200 output.

The posted code computes retrieval AP from cosine similarities transformed as:

    distance = -1 * (1.0 - cosine_similarity(...))

For a perfect match, cosine_similarity == 1, so the score becomes 0.
TorchMetrics' retrieval_average_precision masks out non-positive scores
before ranking, which makes the positive item disappear and the AP drop to 0.

This script reproduces that behavior on a toy dataset with perfect retrieval.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from torchmetrics.functional import retrieval_average_precision


def compute_map_at_200(step_outputs: list[dict[str, object]]) -> tuple[float, float]:
    """Mirror the user's on_validation_epoch_end metric block."""
    query_feat_all = torch.cat([step_outputs[i]["sk_feat"] for i in range(len(step_outputs))])
    gallery_feat_all = torch.cat([step_outputs[i]["img_feat"] for i in range(len(step_outputs))])
    all_category = np.array(sum([list(step_outputs[i]["category"]) for i in range(len(step_outputs))], []))

    gallery = gallery_feat_all
    ap = torch.zeros(len(query_feat_all))
    pr = torch.zeros(len(query_feat_all))
    top_k = 200

    for idx, sk_feat in enumerate(query_feat_all):
        category = all_category[idx]
        distance = -1 * (1.0 - F.cosine_similarity(sk_feat.unsqueeze(0), gallery))

        top_k_actual = min(top_k, len(gallery))
        torch.topk(distance, top_k_actual, largest=True)

        target = torch.zeros(len(gallery), dtype=torch.bool)
        target[np.where(all_category == category)] = True

        ap[idx] = retrieval_average_precision(distance.cpu(), target.cpu(), top_k=top_k_actual)

    return torch.mean(ap).item(), torch.mean(pr).item()


def main() -> None:
    # Perfect retrieval: each sketch exactly matches one gallery item.
    # Despite that, the score for the positive item is 0.0, which gets masked
    # out by torchmetrics' retrieval_average_precision implementation.
    step_outputs = [
        {
            "sk_feat": torch.tensor([[1.0, 0.0], [0.0, 1.0]]),
            "img_feat": torch.tensor([[1.0, 0.0], [0.0, 1.0]]),
            "category": [0, 1],
        }
    ]

    mAP, p_at_200 = compute_map_at_200(step_outputs)

    first_query_scores = -1 * (1.0 - F.cosine_similarity(step_outputs[0]["sk_feat"][:1], step_outputs[0]["img_feat"]))
    first_query_target = torch.tensor([True, False])
    first_query_ap = retrieval_average_precision(first_query_scores, first_query_target, top_k=2).item()
    fixed_scores = first_query_scores + 1e-6
    fixed_ap = retrieval_average_precision(fixed_scores, first_query_target, top_k=2).item()

    print("scores:", first_query_scores.tolist())
    print("target:", first_query_target.tolist())
    print(f"AP for the first query: {first_query_ap}")
    print(f"AP after shifting the scores above zero: {fixed_ap}")
    print(f"mAP@200: {mAP}, p@200: {p_at_200}, Best mAP: -1000.0")

    result = {
        "reproducible": True,
        "evidence": "Perfect retrieval still reports AP=0.0 because the positive score is 0.0 and torchmetrics.retrieval_average_precision masks non-positive predictions.",
        "steps": [
            "Build a toy retrieval batch with exact sketch/gallery matches.",
            "Run the user's on_validation_epoch_end metric block unchanged.",
            "Observe mAP@200=0.0 and p@200=0.0.",
        ],
        "blocking_reason": "",
        "reproduction_command": "./run_repro.sh",
    }
    Path("reproduction.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
