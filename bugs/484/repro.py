#!/usr/bin/env python3
"""Minimal reproduction for diffusers issue 13864.

The bug report's script assigns a pipeline instance to the `safety_checker`
argument. The Cosmos pipeline later does:

    self.safety_checker.check_text_safety(p)

so any pipeline object used as the checker raises AttributeError.
"""

from __future__ import annotations

import pathlib


SOURCE_PATH = pathlib.Path("codebase/src/diffusers/pipelines/cosmos/pipeline_cosmos2_5_predict.py")


class Cosmos2_5_PredictBasePipeline:
    def to(self, device):
        return self


def trigger_bug(pipe: Cosmos2_5_PredictBasePipeline, prompt: str) -> None:
    if pipe.safety_checker is not None:
        pipe.safety_checker.to("cpu")
        if prompt is not None:
            prompt_list = [prompt] if isinstance(prompt, str) else prompt
            for p in prompt_list:
                if not pipe.safety_checker.check_text_safety(p):
                    raise ValueError("unsafe prompt")


def main() -> None:
    source = SOURCE_PATH.read_text()
    marker = "self.safety_checker.check_text_safety(p)"
    if marker not in source:
        raise RuntimeError(f"Expected source marker not found: {marker}")

    line_number = next(
        idx for idx, line in enumerate(source.splitlines(), start=1) if marker in line
    )
    print(f"verified source marker: {SOURCE_PATH}:{line_number}")
    print("running with a pipeline object incorrectly assigned to safety_checker")

    pipe = Cosmos2_5_PredictBasePipeline()
    pipe.safety_checker = pipe
    trigger_bug(pipe, "hello world")


if __name__ == "__main__":
    main()
