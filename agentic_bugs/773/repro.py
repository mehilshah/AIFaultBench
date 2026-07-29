#!/usr/bin/env python3
"""Offline reproduction for browser-use issue #4267."""

import os

# Disable optional telemetry even when this file is invoked directly.
os.environ.setdefault('ANONYMIZED_TELEMETRY', 'false')
os.environ.setdefault('BROWSER_USE_SETUP_LOGGING', 'false')
os.environ.setdefault('BROWSER_USE_DISABLE_EXTENSIONS', '1')

from browser_use import Agent
from browser_use.code_use.notebook_export import session_to_python_script


class OfflineEchoModel:
	"""A model double: Agent construction must not make an API request."""

	model = 'offline-echo'
	_verified_api_keys = True

	@property
	def provider(self) -> str:
		return 'offline'

	@property
	def name(self) -> str:
		return self.model

	async def ainvoke(self, *args, **kwargs):
		raise AssertionError('The reproduction must not invoke an LLM.')


agent = Agent(
	task='Extract product data from https://example.com',
	llm=OfflineEchoModel(),
	directly_open_url=False,
	use_vision=False,
)

try:
	session_to_python_script(agent)
except AttributeError as error:
	message = str(error)
	assert "'Agent' object has no attribute 'session'" in message, message
	print(f'OBSERVED_BUG: {type(error).__name__}: {message}')
	raise SystemExit(1)

raise AssertionError('Expected session_to_python_script(Agent) to raise AttributeError')
