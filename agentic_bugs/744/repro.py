#!/usr/bin/env python3
"""Reproduce AutoGen GraphFlow issue #6551 without a model provider."""

import asyncio
from collections.abc import Sequence

from autogen_agentchat.agents import BaseChatAgent
from autogen_agentchat.base import Response
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.messages import BaseChatMessage, TextMessage
from autogen_agentchat.teams import DiGraphBuilder, GraphFlow
from autogen_core import CancellationToken


class ScriptedAgent(BaseChatAgent):
    """A local deterministic replacement for an LLM-backed AssistantAgent."""

    def __init__(self, name: str, replies: list[str]) -> None:
        super().__init__(name, "deterministic test agent")
        self._replies = replies

    @property
    def produced_message_types(self) -> Sequence[type[BaseChatMessage]]:
        return (TextMessage,)

    async def on_messages(
        self, messages: Sequence[BaseChatMessage], cancellation_token: CancellationToken
    ) -> Response:
        if not self._replies:
            raise AssertionError(f"{self.name} was scheduled unexpectedly")
        return Response(chat_message=TextMessage(content=self._replies.pop(0), source=self.name))

    async def on_reset(self, cancellation_token: CancellationToken) -> None:
        pass


async def main() -> None:
    # The B responses take the loop once, then select the D branch.
    agent_a = ScriptedAgent("A", ["search", "search"])
    agent_b = ScriptedAgent("B", ["SEARCH_AGAIN", "NOT_FOUND"])
    agent_c = ScriptedAgent("C", ["unused"])
    agent_d = ScriptedAgent("D", ["not found"])
    agent_e = ScriptedAgent("E", ["unused"])

    builder = DiGraphBuilder()
    for agent in (agent_a, agent_b, agent_c, agent_d, agent_e):
        builder.add_node(agent)
    builder.add_edge(agent_a, agent_b)
    builder.add_edge(agent_b, agent_a, condition="SEARCH_AGAIN")
    builder.add_edge(agent_b, agent_c, condition="APPROVE")
    builder.add_edge(agent_b, agent_d, condition="NOT_FOUND")
    builder.add_edge(agent_c, agent_e)  # Adding this edge triggers the bug.
    builder.add_edge(agent_d, agent_e)
    builder.set_entry_point(agent_a)

    team = GraphFlow(
        participants=builder.get_participants(),
        graph=builder.build(),
        termination_condition=MaxMessageTermination(10),
    )
    try:
        await team.run(task="test")
    except RuntimeError as error:
        if "No available speakers found." not in str(error):
            raise AssertionError(f"Unexpected RuntimeError: {error}") from error
        print("OBSERVED: RuntimeError: No available speakers found.")
        raise
    raise AssertionError("Expected RuntimeError: No available speakers found.")


if __name__ == "__main__":
    asyncio.run(main())
