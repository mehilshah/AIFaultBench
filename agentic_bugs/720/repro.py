#!/usr/bin/env python3
"""Offline reproduction for browser-use issue #4510."""

import asyncio

from pydantic import BaseModel

from anthropic.types import Message, ToolUseBlock
from browser_use.llm.anthropic.chat import ChatAnthropic
from browser_use.llm.exceptions import ModelProviderError
from browser_use.llm.messages import UserMessage


class DoneAction(BaseModel):
	text: str


class Action(BaseModel):
	done: DoneAction


class AgentOutput(BaseModel):
	action: list[Action]


MALFORMED_ACTION = '[{"done":{"text":"first line\nsecond line"}}]'


class FakeMessages:
	async def create(self, **_kwargs):
		return Message(
			id='offline-response',
			content=[
				ToolUseBlock(
					id='offline-tool',
					# This is the malformed Claude tool input reported in #4510:
					# action is a JSON string with literal newlines in its done text.
					input={'action': MALFORMED_ACTION},
					name='AgentOutput',
					type='tool_use',
				)
			],
			model='claude-sonnet-4-0',
			role='assistant',
			stop_reason='tool_use',
			stop_sequence=None,
			type='message',
			usage={'input_tokens': 1, 'output_tokens': 1},
		)


class FakeClient:
	messages = FakeMessages()


class OfflineChatAnthropic(ChatAnthropic):
	def get_client(self):
		return FakeClient()


async def reproduce() -> None:
	assert '\n' in MALFORMED_ACTION
	chat = OfflineChatAnthropic(model='offline-stub')
	try:
		await chat.ainvoke([UserMessage(content='return a done action')], output_format=AgentOutput)
	except ModelProviderError as error:
		message = str(error)
		assert 'action' in message and 'Input should be a valid list' in message, message
		print('BUG REPRODUCED: nested newline action string was rejected as not a list')
		raise AssertionError('buggy parser rejected the newline-containing action string')
	raise AssertionError('expected the malformed action to be rejected')


if __name__ == '__main__':
	asyncio.run(reproduce())
