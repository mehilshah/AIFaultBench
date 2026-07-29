#!/usr/bin/env python3
"""Reproduce CrewAI 1.14.3 checkpoint serialization of callable guardrails."""

import socket

# This repro never starts a crew, but hard-disable outbound connections as an
# additional guard against a provider or telemetry call being introduced.
def no_network(*_args, **_kwargs):
    raise AssertionError("network access is forbidden in this reproduction")


socket.socket.connect = no_network

from crewai import Agent, Crew, Task
from pydantic_core import PydanticSerializationError
from crewai.state.runtime import RuntimeState


def local_guardrail(output):
    return True, output


agent = Agent(role="local role", goal="local goal", backstory="local backstory")
task = Task(
    description="Return a fixed value.",
    expected_output="A fixed value.",
    agent=agent,
    guardrails=[local_guardrail],
)
crew = Crew(tasks=[task], agents=[agent])
runtime_state = RuntimeState(root=[crew])

try:
    # CheckpointListener performs this exact JSON-mode serialization.
    runtime_state.model_dump(mode="json")
except PydanticSerializationError as error:
    message = str(error)
    expected = "Unable to serialize unknown type: <class 'function'>"
    assert expected in message, message
    print(f"OBSERVED: RuntimeState JSON serialization: {message}")
    raise

raise AssertionError("BUG NOT OBSERVED: callable guardrail serialized to JSON")
