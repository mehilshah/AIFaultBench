#!/usr/bin/env python3
"""Reproduce smolagents issue #1742 without contacting a model provider."""

from smolagents import CodeAgent, Model
from smolagents.memory import ActionStep
from smolagents.models import ChatMessage, MessageRole
from smolagents.monitoring import AgentLogger, LogLevel, Timing
from rich.console import Console


class FakeModel(Model):
    """An inert model: replay never calls it."""

    def generate(self, *args, **kwargs):
        raise AssertionError("replay must not invoke the model")


agent = CodeAgent(
    tools=[],
    model=FakeModel(model_id="offline-fake"),
    logger=AgentLogger(level=LogLevel.OFF, console=Console(log_time=False, log_path=False)),
)
agent.memory.steps.append(
    ActionStep(
        step_number=1,
        timing=Timing(start_time=0.0, end_time=0.0),
        model_input_messages=[ChatMessage(role=MessageRole.USER, content="what is 2*2?")],
    )
)

try:
    agent.replay(detailed=True)
except TypeError as error:
    assert str(error) == "'ChatMessage' object is not iterable", repr(error)
    print(f"OBSERVED BUG: {type(error).__name__}: {error}")
    raise
else:
    raise AssertionError("Expected replay(detailed=True) to reject ChatMessage as non-iterable")
