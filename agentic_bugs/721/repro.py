#!/usr/bin/env python3
"""Reproduce CodeAgent's unstarted-Browser CDP failure with a recorded model reply."""

import asyncio
import logging
import os

# Must be set before importing browser_use: the reproduction must not emit
# telemetry or make a provider request.
os.environ['ANONYMIZED_TELEMETRY'] = 'false'
os.environ['BROWSER_USE_SETUP_LOGGING'] = 'false'

from browser_use import Browser
from browser_use.code_use.service import CodeAgent
from browser_use.llm.views import ChatInvokeCompletion

# Keep the captured result stable; the assertions below are the evidence.
browser_use_logger = logging.getLogger('browser_use')
browser_use_logger.addHandler(logging.NullHandler())
browser_use_logger.propagate = False


class ChatBrowserUse:
	"""A no-network recorded replacement accepted by CodeAgent's 0.12.1 guard."""

	model = 'recorded-no-network-model'
	provider = 'recorded'

	async def ainvoke(self, _messages, output_format=None, **_kwargs):
		return ChatInvokeCompletion(
			completion="```python\nawait evaluate('window.location.href')\n```",
			usage=None,
			stop_reason='end_turn',
		)


async def main() -> None:
	# This is the Browser construction in the report, intentionally without
	# `await browser.start()`. CodeAgent accepts it but does not initialize CDP.
	# No Chromium process, LLM request, or browser/network request is made.
	browser = Browser(headless=True, window_size={'width': 1280, 'height': 720})
	try:
		await browser.get_browser_state_summary()
	except Exception as exc:
		state_message = str(exc)
		assert state_message.startswith('Expected at least one handler to return a non-None result'), state_message
	else:
		raise AssertionError('Expected an unstarted BrowserStateRequestEvent to have no handler result')

	agent = CodeAgent(
		task='local task',
		llm=ChatBrowserUse(),
		browser=browser,
		max_steps=1,
		use_vision=False,
	)
	session = await agent.run()

	assert len(session.cells) == 1, session.cells
	cell = session.cells[0]
	assert cell.error == 'AssertionError: Root CDP client not initialized', cell.error
	print(f'OBSERVED BUG: BrowserStateRequestEvent had no result; {cell.error}')
	raise SystemExit(1)


if __name__ == '__main__':
	asyncio.run(main())
