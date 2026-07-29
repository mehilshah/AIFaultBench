#!/usr/bin/env python3
"""Offline reproduction for Refine's missing structured-output error boundary."""

from unittest.mock import patch
from importlib.metadata import version

from pydantic import BaseModel

from llama_index.core.llms.mock import MockFunctionCallingLLM
from llama_index.core.program.function_program import FunctionCallingProgram
from llama_index.core.response_synthesizers import Refine


class Answer(BaseModel):
    response: str


refine = Refine(llm=MockFunctionCallingLLM(), output_cls=Answer)
assert version("llama-index-core") == "0.14.18"

# This stands in for the function-calling client detecting that the model response
# contains no tool call.  It ensures the reproduction makes no provider request.
with patch.object(
    FunctionCallingProgram,
    "__call__",
    side_effect=ValueError("LLM did not return any tool calls"),
):
    try:
        refine._give_response_single("What is the capital of France?", "Paris.")
    except ValueError as error:
        assert str(error) == "LLM did not return any tool calls"
        print(
            "OBSERVED: llama-index-core 0.14.18 Refine leaked ValueError: "
            "LLM did not return any tool calls"
        )
        raise AssertionError("BUG: Refine failed to catch ValueError") from error

raise AssertionError("BUG NOT OBSERVED: Refine caught the ValueError")
