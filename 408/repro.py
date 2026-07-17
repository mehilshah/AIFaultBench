#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path
from types import ModuleType
from importlib import metadata


ROOT = Path(__file__).resolve().parent
CODEBASE_SRC = ROOT / "codebase" / "src"
sys.path.insert(0, str(CODEBASE_SRC))

if "pkg_resources" not in sys.modules:
    pkg_resources = ModuleType("pkg_resources")

    def get_distribution(name: str):
        class _Distribution:
            def __init__(self, version: str):
                self.version = version

        return _Distribution(metadata.version(name))

    pkg_resources.get_distribution = get_distribution  # type: ignore[attr-defined]
    sys.modules["pkg_resources"] = pkg_resources

import torch
from accelerate import Accelerator
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator


def run_case(value, label: str):
    with tempfile.TemporaryDirectory(prefix=f"accelerate-bug-408-{label}-") as tmpdir:
        project_dir = Path(tmpdir)
        accelerator = Accelerator(log_with="tensorboard", project_dir=project_dir)
        accelerator.init_trackers("train")
        accelerator.log({"loss": value}, step=1)
        accelerator.end_training()

        logdir = project_dir / "train"
        event_files = sorted(p.name for p in logdir.glob("events.out.tfevents.*"))

        accumulator = EventAccumulator(str(logdir))
        accumulator.Reload()
        scalar_events = []
        if "loss" in accumulator.Tags().get("scalars", []):
            scalar_events = [(event.step, event.value) for event in accumulator.Scalars("loss")]

        return {
            "logdir": str(logdir),
            "event_files": event_files,
            "tags": accumulator.Tags(),
            "scalar_events": scalar_events,
        }


def main() -> int:
    tensor_result = run_case(torch.tensor(1.0), "tensor")
    float_result = run_case(1.0, "float")

    print(f"torch_version={torch.__version__}")
    print("tensor_case_event_files=", tensor_result["event_files"])
    print("tensor_case_tags=", tensor_result["tags"])
    print("tensor_case_scalar_events=", tensor_result["scalar_events"])
    print("float_case_event_files=", float_result["event_files"])
    print("float_case_tags=", float_result["tags"])
    print("float_case_scalar_events=", float_result["scalar_events"])

    tensor_bug = len(tensor_result["scalar_events"]) == 0
    float_control = float_result["scalar_events"] == [(1, 1.0)]

    if tensor_bug and float_control:
        print("BUG_REPRODUCED: tensor input is silently ignored while float input is logged.")
        return 0

    print("BUG_NOT_REPRODUCED: tensor and float behavior matched expectations.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
