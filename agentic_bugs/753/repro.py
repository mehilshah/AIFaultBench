#!/usr/bin/env python3
"""Reproduce loss of a signature-only Bedrock Converse stream delta."""

from llama_index.core.base.llms.types import ChatMessage, MessageRole, ThinkingBlock
from llama_index.llms.bedrock_converse import BedrockConverse
import llama_index.llms.bedrock_converse.base as bedrock_base


SIGNATURE = "signature-from-signature-only-delta"


def fake_converse_with_retry(**_kwargs):
    """A recorded local Bedrock stream; it performs no network I/O."""
    return {
        "stream": [
            {
                "contentBlockDelta": {
                    "contentBlockIndex": 0,
                    "delta": {"reasoningContent": {"text": "thinking text"}},
                }
            },
            {
                "contentBlockDelta": {
                    "contentBlockIndex": 0,
                    "delta": {"reasoningContent": {"signature": SIGNATURE}},
                }
            },
        ]
    }


def main():
    # Patch the imported call site before streaming.  The explicit fake client and
    # dummy credentials ensure construction itself cannot use AWS credentials.
    bedrock_base.converse_with_retry = fake_converse_with_retry
    llm = BedrockConverse(
        model="anthropic.claude-sonnet-4-5-20250929-v1:0",
        max_tokens=8,
        region_name="us-east-1",
        aws_access_key_id="unused",
        aws_secret_access_key="unused",
        client=object(),
        thinking={"type": "enabled", "budget_tokens": 1},
    )
    responses = list(
        llm.stream_chat([ChatMessage(role=MessageRole.USER, content="test")])
    )
    thinking_block = next(
        block
        for block in responses[-1].message.blocks
        if isinstance(block, ThinkingBlock)
    )
    observed = thinking_block.additional_information["signature"]

    if observed != SIGNATURE:
        print(
            "BUG OBSERVED: signature-only delta was dropped "
            f"(expected {SIGNATURE!r}, got {observed!r})"
        )
        raise AssertionError("Bedrock Converse lost a signature-only reasoning delta")
    raise RuntimeError("Bug absent: the signature-only delta was preserved")


if __name__ == "__main__":
    main()
