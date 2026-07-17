#!/usr/bin/env python3
"""Minimal reproduction for the Flux2-Klein image-id batching bug.

The training script in:
  codebase/examples/dreambooth/train_dreambooth_lora_flux2_klein_img2img.py
builds image IDs for the whole conditioning batch at once and only splits them
back into batch-sized chunks afterwards.

This script reproduces that logic with the same coordinate-generation algorithm
and shows that two identical conditioning images in the same batch receive
different time coordinates.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class LatentShape:
    batch: int
    channels: int
    height: int
    width: int


def prepare_image_ids(image_latents: list[LatentShape], scale: int = 10) -> list[tuple[int, int, int, int]]:
    """Pure-Python equivalent of Flux2KleinPipeline._prepare_image_ids."""

    if not isinstance(image_latents, list):
        raise ValueError(f"Expected `image_latents` to be a list, got {type(image_latents)}.")

    image_latent_ids: list[tuple[int, int, int, int]] = []
    for idx, latent in enumerate(image_latents):
        t = scale + scale * idx
        for h in range(latent.height):
            for w in range(latent.width):
                image_latent_ids.append((t, h, w, 0))

    return image_latent_ids


def split_into_batch_chunks(flat_ids: list[tuple[int, int, int, int]], batch_size: int) -> list[list[tuple[int, int, int, int]]]:
    if len(flat_ids) % batch_size != 0:
        raise ValueError("The flattened ID count must be divisible by batch_size.")
    chunk_size = len(flat_ids) // batch_size
    return [flat_ids[i * chunk_size : (i + 1) * chunk_size] for i in range(batch_size)]


def main() -> None:
    # Two identical conditioning images in the same batch.
    batch_size = 2
    cond_model_input = [LatentShape(batch=1, channels=4, height=2, width=2) for _ in range(batch_size)]

    # This mirrors the buggy training code:
    #   cond_model_input_list = [cond_model_input[i].unsqueeze(0) for i in range(cond_model_input.shape[0])]
    #   cond_model_input_ids = Flux2KleinPipeline._prepare_image_ids(cond_model_input_list)
    #   cond_model_input_ids = cond_model_input_ids.view(cond_model_input.shape[0], -1, model_input_ids.shape[-1])
    flat_ids = prepare_image_ids(cond_model_input)
    actual_batch_ids = split_into_batch_chunks(flat_ids, batch_size)

    # What the issue report expects: compute one image-id block and repeat it.
    reference_ids = prepare_image_ids([cond_model_input[0]])
    expected_batch_ids = [reference_ids for _ in range(batch_size)]

    payload = {
        "actual_batch_ids": actual_batch_ids,
        "expected_batch_ids": expected_batch_ids,
        "batch0_equals_reference": actual_batch_ids[0] == reference_ids,
        "batch1_equals_reference": actual_batch_ids[1] == reference_ids,
        "batch0_equals_batch1": actual_batch_ids[0] == actual_batch_ids[1],
    }
    print(json.dumps(payload, indent=2))

    # Reproduces the logic bug: batch element 1 is not independent of batch element 0.
    assert actual_batch_ids[0] == reference_ids
    assert actual_batch_ids[1] != reference_ids
    assert actual_batch_ids[0] != actual_batch_ids[1]


if __name__ == "__main__":
    main()
