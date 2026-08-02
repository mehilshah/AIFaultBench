#!/usr/bin/env python3
"""Offline reproduction for CrewAI guardrail retry with output_pydantic."""

import os

os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"

from pydantic import BaseModel, ValidationError

from crewai import Task
from crewai.tasks.task_output import TaskOutput


class Answer(BaseModel):
    value: int


class OfflineAgent:
    """A deterministic agent double; it does not create an LLM client or make I/O."""

    role = "offline-double"
    verbose = False
    last_messages: list[object] = []

    def execute_task(self, task: Task, context: str, tools: list[object]) -> Answer:
        return Answer(value=2)


def reject_first_output(_: TaskOutput) -> tuple[bool, str]:
    """Force the retry path that reconstructs TaskOutput from the model result."""
    return False, "force one offline guardrail retry"


def main() -> None:
    task = Task(
        description="Return an Answer model.",
        expected_output="An Answer with an integer value.",
        output_pydantic=Answer,
        guardrail_max_retries=1,
    )
    initial = TaskOutput(
        description=task.description,
        expected_output=task.expected_output,
        raw='{"value": 1}',
        pydantic=Answer(value=1),
        agent=OfflineAgent.role,
        output_format=task._get_output_format(),
    )

    try:
        task._invoke_guardrail_function(
            initial, OfflineAgent(), [], reject_first_output
        )
    except ValidationError as error:
        errors = error.errors()
        assert len(errors) == 1, errors
        fault = errors[0]
        assert fault["loc"] == ("raw",), fault
        assert fault["type"] == "string_type", fault
        assert isinstance(fault["input"], Answer), fault
        print("OBSERVED BUG: guardrail retry passed Answer to TaskOutput.raw")
        raise

    raise AssertionError("Expected TaskOutput.raw validation failure was not raised")


if __name__ == "__main__":
    main()
