#!/usr/bin/env python3
"""Minimal reproduction for the bound-method profiling bug.

This uses the real profiling helper from the local codebase, but avoids any
model downloads or GPU requirements.
"""

from __future__ import annotations

import copy
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
PROFILING_DIR = CODEBASE / "examples" / "profiling"
sys.path.insert(0, str(PROFILING_DIR))

from profiling_utils import annotate_pipeline  # noqa: E402


class DummyScheduler:
    def __init__(self) -> None:
        self._step_index = 0

    def step(self, value=None, *args, **kwargs):
        self._step_index += 1
        return {
            "value": value,
            "step_index": self._step_index,
            "self_id": id(self),
        }


class DummyPipe:
    def __init__(self) -> None:
        self.scheduler = DummyScheduler()


def _captured_self(func):
    for cell in getattr(func, "__closure__", ()) or ():
        contents = cell.cell_contents
        if hasattr(contents, "__self__"):
            return contents.__self__
    return None


def main() -> None:
    pipe = DummyPipe()
    annotate_pipeline(pipe)

    audio_scheduler = copy.deepcopy(pipe.scheduler)

    wrapped_step = audio_scheduler.step
    captured_self = _captured_self(wrapped_step)

    print(f"original_scheduler_id={id(pipe.scheduler)}")
    print(f"copied_scheduler_id={id(audio_scheduler)}")
    print(f"captured_self_id={id(captured_self) if captured_self is not None else 'None'}")
    print(f"wrapped_step_is_plain_function={type(wrapped_step).__name__ == 'function'}")

    if captured_self is not pipe.scheduler:
        raise AssertionError("expected wrapper to capture the original scheduler instance")

    result = audio_scheduler.step("audio")
    print(f"audio_step_result={result}")
    print(f"original_step_index={pipe.scheduler._step_index}")
    print(f"copied_step_index={audio_scheduler._step_index}")

    if pipe.scheduler._step_index != 1:
        raise AssertionError("expected copied scheduler step() to mutate the original scheduler")
    if audio_scheduler._step_index != 0:
        raise AssertionError("expected copied scheduler to keep its own step_index unchanged")

    original_result = pipe.scheduler.step("video")
    print(f"original_step_result={original_result}")
    print("BUG_REPRODUCED=1")


if __name__ == "__main__":
    main()
