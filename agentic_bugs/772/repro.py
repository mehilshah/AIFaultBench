#!/usr/bin/env python3
"""Reproduce GH-1518 without a network request or provider credentials."""

from smolagents.models import ChatMessage, MessageRole, OpenAIServerModel


class DeepInfra422(RuntimeError):
    """The relevant part of DeepInfra's documented/observed validation failure."""


class FlattenedRequestAccepted(RuntimeError):
    pass


class DeepInfraCompatibleCompletions:
    def __init__(self):
        self.last_request = None

    def create(self, **request):
        self.last_request = request
        content = request["messages"][0]["content"]
        if not isinstance(content, str):
            raise DeepInfra422(
                "Error code: 422 - message content must be a string; "
                f"got {type(content).__name__}"
            )
        raise FlattenedRequestAccepted


class FakeClient:
    def __init__(self):
        self.chat = type("Chat", (), {"completions": DeepInfraCompatibleCompletions()})()


def main() -> int:
    fake_client = FakeClient()
    original_create_client = OpenAIServerModel.create_client
    OpenAIServerModel.create_client = lambda _self: fake_client
    try:
        model = OpenAIServerModel(
            model_id="google/gemini-2.5-flash",
            api_base="https://api.deepinfra.com/v1/openai",
            api_key="not-used",
        )
        message = ChatMessage(
            role=MessageRole.USER,
            content=[{"type": "text", "text": "Return a short answer."}],
        )
        try:
            model.generate([message])
        except DeepInfra422 as error:
            sent_content = fake_client.chat.completions.last_request["messages"][0]["content"]
            assert sent_content == [{"type": "text", "text": "Return a short answer."}]
            assert isinstance(sent_content, list)
            workaround = OpenAIServerModel(
                model_id="google/gemini-2.5-flash",
                api_base="https://api.deepinfra.com/v1/openai",
                api_key="not-used",
                flatten_messages_as_text=True,
            )
            try:
                workaround.generate([message])
            except FlattenedRequestAccepted:
                assert isinstance(fake_client.chat.completions.last_request["messages"][0]["content"], str)
            else:
                raise AssertionError("fake provider did not receive the flattened workaround request")
            print(f"OBSERVED BUG: {error}")
            return 1
        raise AssertionError("bug absent: the fake DeepInfra validator accepted the default request")
    finally:
        OpenAIServerModel.create_client = original_create_client


if __name__ == "__main__":
    raise SystemExit(main())
