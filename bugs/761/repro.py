#!/usr/bin/env python3
"""Reproduce RetryPromptPart partial ErrorDetails JSON round-trip failure."""

from datetime import datetime, timezone

from pydantic import ValidationError
from pydantic_ai.messages import ModelMessagesTypeAdapter, ModelRequest, RetryPromptPart


content: list[dict[str, object]] = [
    {'type': 'missing', 'loc': ('x',), 'msg': 'Field required'},
]
part = RetryPromptPart(
    content=content,  # type: ignore[arg-type]
    tool_name='foo',
    tool_call_id='call_1',
    timestamp=datetime(2025, 1, 1, tzinfo=timezone.utc),
)
messages = [ModelRequest(parts=[part])]
serialized = ModelMessagesTypeAdapter.dump_json(messages)

try:
    ModelMessagesTypeAdapter.validate_json(serialized)
except ValidationError as exc:
    errors = exc.errors()
    if not any(error['loc'][-1] == 'input' and error['type'] == 'missing' for error in errors):
        raise AssertionError(f'Unexpected validation errors: {errors}') from exc
    print('BUG REPRODUCED: partial ErrorDetails JSON cannot be reloaded (input is required).')
    raise SystemExit(1)
else:
    raise AssertionError('Bug not reproduced: partial ErrorDetails unexpectedly round-tripped.')
