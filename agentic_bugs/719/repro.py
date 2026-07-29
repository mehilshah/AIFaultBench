#!/usr/bin/env python3
"""Reproduce browser-use 0.12.6's raw-LangChain token-tracker crash offline."""

import asyncio

from browser_use.tokens.service import TokenCost
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, ConfigDict


class CustomDeepSeek(ChatOpenAI):
	model_config = ConfigDict(extra='allow', arbitrary_types_allowed=True)

	@property
	def provider(self):
		return 'openai'


class ExpectedOutput(BaseModel):
	answer: str


async def main() -> None:
	# The invalid URL and inert key ensure that an unexpected network call fails locally.
	llm = CustomDeepSeek(model='deepseek-chat', api_key='not-a-real-key', base_url='http://127.0.0.1:9/v1')
	TokenCost().register_llm(llm)

	try:
		await llm.ainvoke('hello', output_format=ExpectedOutput)
	except AttributeError as error:
		assert str(error) == 'items', f'expected AttributeError("items"), got {error!r}'
		print('OBSERVED BUG: AttributeError: items')
		raise

	raise AssertionError('expected browser-use token tracking to pass the Pydantic output model as LangChain config')


if __name__ == '__main__':
	asyncio.run(main())
