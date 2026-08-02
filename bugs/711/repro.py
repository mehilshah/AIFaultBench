#!/usr/bin/env python3
"""Offline reproducer for CAMEL issue #3339."""

import asyncio
import logging

from camel.agents import ChatAgent
from camel.models.stub_model import StubModel
from camel.types import ModelType


async def fail_offline_tool(query: str) -> str:
    """Always fail locally, without contacting a provider or service."""
    raise RuntimeError("deterministic offline tool failure")


def main() -> None:
    logging.getLogger("camel.camel.agents.chat_agent").setLevel(
        logging.CRITICAL
    )
    agent = ChatAgent(
        model=StubModel(ModelType.STUB),
        tools=[fail_offline_tool],
    )
    tool_call_id = "call_offline_failure"
    asyncio.run(
        agent._aexecute_tool_from_stream_data(
            {
                "id": tool_call_id,
                "function": {
                    "name": "fail_offline_tool",
                    "arguments": '{"query": "offline"}',
                },
            }
        )
    )

    messages, _ = agent.memory.get_context()
    orphaned_tool = (
        len(messages) == 1
        and messages[0].get("role") == "tool"
        and messages[0].get("tool_call_id") == tool_call_id
        and "deterministic offline tool failure"
        in str(messages[0].get("content"))
    )
    if orphaned_tool:
        print(
            "OBSERVED BUG: failed async tool left an unpaired tool message "
            f"(tool_call_id={tool_call_id})"
        )
        raise AssertionError(
            "tool result was recorded without its preceding assistant tool_call"
        )

    raise AssertionError(
        "bug not observed: expected exactly one orphaned tool message, "
        f"got {messages!r}"
    )


if __name__ == "__main__":
    main()
