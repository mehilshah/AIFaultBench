#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase" / "src"))

import torch
from transformers.pipelines.base import Pipeline


EVENTS: list[str] = []


class DummyModel(torch.nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.param = torch.nn.Parameter(torch.zeros(1))
        self.device = torch.device("cpu")
        self.config = type("Cfg", (), {"prefix": None, "task_specific_params": {}})()
        self.generation_config = type("GenCfg", (), {"pad_token_id": None})()

    def to(self, device):
        self.device = torch.device(device)
        return self

    def can_generate(self) -> bool:
        return False


class DummyPipeline(Pipeline):
    def _sanitize_parameters(self, **kwargs):
        return {}, {}, {}

    def preprocess(self, inputs, **kwargs):
        EVENTS.append(f"preprocess:{inputs}")
        return inputs

    def _forward(self, model_inputs, **kwargs):
        EVENTS.append(f"forward:{model_inputs}")
        return model_inputs

    def postprocess(self, model_outputs, **kwargs):
        EVENTS.append(f"postprocess:{model_outputs}")
        return model_outputs


def stream_items():
    for index in range(3):
        EVENTS.append(f"yield:{index}")
        yield f"item-{index}"


def main() -> int:
    pipe = DummyPipeline(DummyModel(), device=-1)
    result = pipe(stream_items())

    print("RESULT", result)
    print("EVENTS", EVENTS)

    expected_prefix = ["yield:0", "yield:1", "yield:2"]
    if EVENTS[:3] != expected_prefix:
        raise AssertionError(f"unexpected event prefix: {EVENTS[:3]!r}")
    if EVENTS[3] != "preprocess:item-0":
        raise AssertionError(f"generator was not eagerly materialized: {EVENTS!r}")

    print("BUG_REPRODUCED=True")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
