#!/usr/bin/env python3
"""Reproduce ModelRequest's missing NativeToolReturnPart union member."""

from pydantic import ValidationError
from pydantic_ai.messages import ModelMessagesTypeAdapter, ModelRequest, NativeToolReturnPart


messages = [
    ModelRequest(
        parts=[
            NativeToolReturnPart(
                tool_name='my_tool',
                content='ok',
                tool_call_id='c1',
                provider_name='anthropic',
            )
        ]
    )
]
payload = ModelMessagesTypeAdapter.dump_json(messages)

try:
    ModelMessagesTypeAdapter.validate_json(payload)
except ValidationError as error:
    detail = str(error)
    if 'union_tag_invalid' not in detail or "Input tag 'builtin-tool-return'" not in detail:
        raise AssertionError(f'Unexpected validation error: {detail}') from error
    print('OBSERVED: ModelRequest NativeToolReturnPart round-trip raised union_tag_invalid')
    raise
else:
    raise AssertionError('BUG ABSENT: NativeToolReturnPart unexpectedly round-tripped in ModelRequest')
