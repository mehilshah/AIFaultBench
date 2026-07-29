#!/usr/bin/env python3
"""Deterministically reproduce #3970 without an LLM or browser connection."""

from pydantic import BaseModel

from browser_use.agent.message_manager.service import MessageManager
from browser_use.tools.registry.service import Registry


class InputAction(BaseModel):
	text: str


SECRETS = {
	'user_name': 'learner@gmail.com',
	'pass_word': 'learner',
}


def main() -> None:
	# Use the pinned MessageManager implementation to build the exact instruction
	# supplied to an LLM.  Avoiding __init__ also avoids files, browser setup, and
	# all provider calls; this method depends only on sensitive_data.
	message_manager = object.__new__(MessageManager)
	message_manager.sensitive_data = SECRETS
	prompt = message_manager._get_sensitive_data_description('https://example.test/login')

	# This is the action emitted in the issue report: the model used the raw
	# placeholder name, rather than the tag required by the replacement layer.
	fake_model_action = InputAction(text='user_name')
	registry = object.__new__(Registry)
	executed_action = registry._replace_sensitive_data(fake_model_action, SECRETS)

	missing_concrete_example = '<secret>user_name</secret>' not in prompt
	raw_placeholder_was_typed = executed_action.text == 'user_name'
	if missing_concrete_example and raw_placeholder_was_typed:
		print('BUG REPRODUCED: raw placeholder user_name was not replaced; literal user_name would be typed.')
		raise AssertionError(
			'buggy prompt lacks a concrete <secret>user_name</secret> example and the action executor leaves raw user_name unchanged'
		)

	print('FIXED: sensitive-data instruction contains a concrete tag example or raw placeholders are replaced.')


if __name__ == '__main__':
	main()
