#!/usr/bin/env python3
"""Reproduce LLMChatEndEvent serialization corrupting ChatResponse.raw."""

from pydantic import BaseModel

from llama_index.core.base.llms.types import ChatMessage, ChatResponse
from llama_index.core.instrumentation.events.llm import LLMChatEndEvent


class StructuredReply(BaseModel):
    answer: str


response = ChatResponse(
    message=ChatMessage.from_str("hello"), raw=StructuredReply(answer="world")
)
LLMChatEndEvent(messages=[], response=response).model_dump()

if isinstance(response.raw, dict):
    print("BUG REPRODUCED: LLMChatEndEvent.model_dump changed ChatResponse.raw to dict")
    raise RuntimeError("ChatResponse.raw was mutated in place during event serialization")

raise AssertionError(
    f"Bug not reproduced: ChatResponse.raw remained {type(response.raw).__name__}"
)
