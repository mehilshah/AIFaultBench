#!/usr/bin/env python3
"""Offline reproduction for smolagents issue #1532."""

from smolagents import ToolCallingAgent
from smolagents.models import ChatMessage, ChatMessageToolCall, ChatMessageToolCallFunction, MessageRole, Model
from smolagents.monitoring import LogLevel


class OfflineFinalAnswerModel(Model):
    """A deterministic model double: it never makes provider or network calls."""

    def __init__(self):
        super().__init__(model_id="offline-final-answer-model")

    def generate(self, messages, **kwargs):
        return ChatMessage(
            role=MessageRole.ASSISTANT,
            tool_calls=[
                ChatMessageToolCall(
                    id="offline-final-answer",
                    type="function",
                    function=ChatMessageToolCallFunction(name="final_answer", arguments={"answer": "done"}),
                )
            ],
        )


agent = ToolCallingAgent(
    tools=[],
    model=OfflineFinalAnswerModel(),
    name="offline_agent",
    description="A deterministic managed agent for reproducing the summary path.",
    max_steps=1,
    provide_run_summary=True,
    verbosity_level=LogLevel.ERROR,
)

try:
    agent("Return the deterministic final answer.", additional_args={})
except TypeError as error:
    assert str(error) == "'ChatMessage' object is not subscriptable", repr(error)
    print(f"OBSERVED BUG: {type(error).__name__}: {error}")
    raise SystemExit(1)
else:
    raise AssertionError("Expected the ChatMessage subscripting TypeError was not raised")
