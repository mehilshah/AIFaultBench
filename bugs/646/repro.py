#!/usr/bin/env python3
"""Offline regression reproduction for LangChain issue #38639."""

from anthropic.types import (
    RawContentBlockDeltaEvent,
    RawContentBlockStartEvent,
    SignatureDelta,
    ThinkingBlock,
)
from langchain_anthropic.chat_models import ChatAnthropic
from langchain_core.messages import AIMessage, HumanMessage


llm = ChatAnthropic(model="claude-opus-4-6", api_key="offline-test-key")
events = [
    RawContentBlockStartEvent(
        type="content_block_start",
        index=0,
        content_block=ThinkingBlock(type="thinking", thinking="", signature=""),
    ),
    RawContentBlockDeltaEvent(
        type="content_block_delta",
        index=0,
        delta=SignatureDelta(type="signature_delta", signature="offline-signature"),
    ),
]

aggregated = None
block_start_event = None
for event in events:
    chunk, block_start_event = llm._make_message_chunk_from_anthropic_event(
        event,
        stream_usage=True,
        coerce_content_to_string=False,
        block_start_event=block_start_event,
    )
    if chunk is not None:
        aggregated = chunk if aggregated is None else aggregated + chunk

assert aggregated is not None
block = aggregated.content[0]
payload = llm._get_request_payload(
    [HumanMessage("hi"), AIMessage(content=aggregated.content), HumanMessage("continue")]
)
replayed_block = payload["messages"][1]["content"][0]

if "thinking" not in block and "thinking" not in replayed_block:
    print(f"BUG OBSERVED: streamed block and replay payload omit thinking: {replayed_block}")
    raise AssertionError("empty thinking block loses required 'thinking' field")

print(f"BUG NOT OBSERVED: streamed={block!r}, replayed={replayed_block!r}")
