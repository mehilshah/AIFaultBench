#!/usr/bin/env python3
"""Minimal reproduction for transformers issue 46829."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase" / "src"))


import torch
from transformers import VideoPrismVisionConfig
from transformers.models.videoprism.modeling_videoprism import VideoPrismForVideoClassification


def main() -> None:
    config = VideoPrismVisionConfig(num_labels=4, num_frames=2)
    model = VideoPrismForVideoClassification._from_config(config)
    model.eval()

    pixel_values = torch.randn(1, 2, 3, 288, 288)
    with torch.no_grad():
        outputs = model(pixel_values_videos=pixel_values)

    hidden_states = outputs.hidden_states
    print(f"hidden_states_type={type(hidden_states)}")
    print(f"hidden_states_is_none={hidden_states is None}")
    print(f"hidden_states_is_tuple={isinstance(hidden_states, tuple)}")
    if isinstance(hidden_states, torch.Tensor):
        print(f"hidden_states_shape={tuple(hidden_states.shape)}")

    assert hidden_states is None or isinstance(hidden_states, tuple), (
        f"FAIL: hidden_states is {type(hidden_states)}, expected None or tuple"
    )


if __name__ == "__main__":
    main()
