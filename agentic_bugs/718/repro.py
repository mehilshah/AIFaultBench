#!/usr/bin/env python3
"""Offline reproduction for browser-use issue #4769."""

import asyncio
from types import SimpleNamespace

from pydantic import BaseModel

from browser_use.llm.exceptions import ModelProviderError
from browser_use.llm.messages import UserMessage
from browser_use.llm.openai.chat import ChatOpenAI


class ExpectedOutput(BaseModel):
	answer: str


class RecordedCompletions:
	async def create(self, **kwargs):
		# This mirrors the LM Studio response in the report: JSON is put in
		# reasoning_content while content is an empty string.
		assert kwargs['response_format']['type'] == 'json_schema'
		message = SimpleNamespace(content='', reasoning_content='{"answer":"from reasoning_content"}')
		return SimpleNamespace(choices=[SimpleNamespace(message=message, finish_reason='stop')], usage=None)


class RecordedClient:
	chat = SimpleNamespace(completions=RecordedCompletions())


class OfflineChatOpenAI(ChatOpenAI):
	def get_client(self):
		return RecordedClient()


async def main():
	llm = OfflineChatOpenAI(model='nvidia/nemotron-3-nano-4b')
	try:
		await llm.ainvoke([UserMessage(content='Return structured output')], ExpectedOutput)
	except ModelProviderError as error:
		assert 'Invalid JSON: EOF while parsing a value at line 1 column 0' in error.message
		print(f'BUG REPRODUCED: {error.message}')
		raise
	raise AssertionError('Expected structured JSON in reasoning_content to be rejected')


asyncio.run(main())
