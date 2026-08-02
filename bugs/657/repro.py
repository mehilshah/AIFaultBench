#!/usr/bin/env python3
"""Offline reproduction for langchain-ai/langchain#39100."""

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.messages.content import create_text_block


class _RejectingMessages:
    """Local stand-in for Anthropic's API; it makes no network requests."""

    def create(self, **payload: object) -> object:
        system = payload["system"]
        assert isinstance(system, list), "expected a block-valued system payload"
        first_block = system[0]
        assert isinstance(first_block, dict), "expected a system content block"
        if "id" in first_block:
            print("BUG REPRODUCED: unsupported id leaked into system.0")
            raise AssertionError(
                "Anthropic would reject this payload: "
                "system.0.id: Extra inputs are not permitted"
            )
        print("BUG NOT PRESENT: system text block id was stripped")
        raise SystemExit(0)


class _OfflineClient:
    messages = _RejectingMessages()


def main() -> None:
    model = ChatAnthropic(
        model="claude-haiku-4-5",
        max_tokens=16,
        api_key="offline-test-key",
    )
    # Override the cached SDK client before invoke() reaches it. The stub records
    # the exact request payload and rejects it like Anthropic's schema validation.
    model.__dict__["_client"] = _OfflineClient()
    system_message = SystemMessage(
        content_blocks=[create_text_block("You are a helpful assistant.")]
    )
    model.invoke([system_message, HumanMessage("Say hi.")])


if __name__ == "__main__":
    main()
