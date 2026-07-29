#!/usr/bin/env python3
"""Reproduce pydantic-ai #6025 without a provider or network access."""

import asyncio

from pydantic_ai import Agent
from pydantic_ai.messages import ModelRequest, UserPromptPart
from pydantic_ai.models.test import TestModel
from pydantic_ai.run import AgentRunResultEvent
from pydantic_ai.ui.vercel_ai import VercelAIAdapter
from pydantic_ai.ui.vercel_ai.request_types import SubmitMessage, TextUIPart, UIMessage


def user_message(message_id: str, text: str) -> UIMessage:
    return UIMessage(id=message_id, role='user', parts=[TextUIPart(text=text)])


async def run_turn(agent: Agent, request: SubmitMessage, history: list | None):
    adapter = VercelAIAdapter(agent=agent, run_input=request)
    async for event in adapter.run_stream_native(message_history=history):
        if isinstance(event, AgentRunResultEvent):
            return event.result
    raise AssertionError('VercelAIAdapter did not emit an AgentRunResultEvent')


def has_user_request(messages: list) -> bool:
    return any(
        isinstance(message, ModelRequest) and any(isinstance(part, UserPromptPart) for part in message.parts)
        for message in messages
    )


async def main() -> None:
    agent = Agent(model=TestModel(custom_output_text='hi'), system_prompt='You are helpful.')

    first = await run_turn(
        agent,
        SubmitMessage(id='conversation', messages=[user_message('u1', 'hello')]),
        None,
    )
    second = await run_turn(
        agent,
        SubmitMessage(id='conversation', messages=[user_message('u2', 'thanks')]),
        first.all_messages(),
    )

    first_types = [type(message).__name__ for message in first.new_messages()]
    second_types = [type(message).__name__ for message in second.new_messages()]
    print(f'turn 1 new_messages: {first_types}')
    print(f'turn 2 new_messages: {second_types}')

    assert not has_user_request(second.new_messages()), 'control failed: turn 2 leaked its inbound user request'
    assert not has_user_request(first.new_messages()), (
        'BUG: turn 1 new_messages() includes the inbound user ModelRequest'
    )


asyncio.run(main())
