#!/usr/bin/env python3
"""Offline reproducer for pydantic-ai issue #6081."""

import asyncio
import os

os.environ.setdefault('AWS_REGION', 'us-east-1')
os.environ.setdefault('AWS_DEFAULT_REGION', 'us-east-1')
# Constructing a boto client must not try the EC2 metadata service if the host has no credentials.
os.environ.setdefault('AWS_EC2_METADATA_DISABLED', 'true')

from pydantic_ai import DocumentUrl
from pydantic_ai._agent_graph import _clean_message_history
from pydantic_ai.messages import (
    ModelRequest,
    ModelResponse,
    ToolCallPart,
    ToolReturnPart,
    UserPromptPart,
)
from pydantic_ai.models import ModelRequestParameters
from pydantic_ai.models.bedrock import BedrockConverseModel


async def main() -> None:
    model = BedrockConverseModel('us.anthropic.claude-opus-4-6-v1')
    history = [
        ModelRequest(parts=[UserPromptPart(content='show me my expenses')]),
        ModelResponse(parts=[ToolCallPart(tool_name='get', args={}, tool_call_id='t1')]),
        ModelRequest(parts=[ToolReturnPart(tool_name='get', content='ok', tool_call_id='t1')]),
        ModelRequest(
            parts=[
                UserPromptPart(
                    content=[
                        'what accounts are in this?',
                        DocumentUrl(url='s3://bucket/file.csv', media_type='text/csv'),
                    ]
                )
            ]
        ),
    ]

    _system, messages = await model._map_messages(
        _clean_message_history(history), ModelRequestParameters(), None
    )
    final_content = messages[-1]['content']
    block_types = [next(iter(block)) for block in final_content]
    expected_fault = ['toolResult', 'text', 'document']
    print(f'BUG REPRODUCED: final Bedrock user content blocks = {block_types!r}')
    assert block_types == expected_fault, (
        'expected buggy co-location of toolResult and document, '
        f'got {block_types!r}'
    )
    raise RuntimeError(
        'BUG REPRODUCED: Bedrock would reject toolResult and document in one user message'
    )


asyncio.run(main())
