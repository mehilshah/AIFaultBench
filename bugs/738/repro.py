#!/usr/bin/env python3
"""Reproduce Phoenix issue #13934 without contacting AWS."""

import boto3
from botocore.exceptions import ParamValidationError

from phoenix.db.types.prompts import PromptToolRaw, PromptTools
from phoenix.server.api.helpers.playground_clients import BedrockStreamingClient
from phoenix.server.api.types.ChatCompletionMessageRole import ChatCompletionMessageRole


class _Span:
    def set_attribute(self, *_: object) -> None:
        pass


def _forbid_transport(*_: object, **__: object) -> object:
    raise AssertionError("unexpected transport attempt; validation should happen locally")


def main() -> None:
    raw_tool = {
        "name": "weather",
        "description": "reports weather",
        "inputSchema": {"json": {"type": "object"}},
    }
    tools = PromptTools(type="tools", tools=[PromptToolRaw(type="raw", raw=raw_tool)])
    phoenix_client = BedrockStreamingClient(
        client_factory=None,
        model_name="anthropic.claude-3-haiku-20240307-v1:0",
    )
    request = phoenix_client._converse_build_request(
        messages=[{"role": ChatCompletionMessageRole.USER, "content": "What is the weather?"}],
        tools=tools,
        response_format=None,
        span=_Span(),
    )
    emitted_tool = request["toolConfig"]["tools"][0]
    if emitted_tool != raw_tool:
        print("BUG NOT OBSERVED: Phoenix wrapped the raw Bedrock tool")
        return
    print("EMITTED_TOOL_KEYS: name,description,inputSchema")

    # botocore validates before invoking its endpoint. This callback makes a
    # transport attempt an error, so this reproduction cannot call AWS.
    bedrock = boto3.client(
        "bedrock-runtime",
        region_name="us-east-1",
        aws_access_key_id="offline",
        aws_secret_access_key="offline",
    )
    bedrock._endpoint.make_request = _forbid_transport  # type: ignore[method-assign]
    try:
        bedrock.converse_stream(**request)
    except ParamValidationError as error:
        message = str(error)
        assert "toolConfig.tools[0]" in message
        assert 'Unknown parameter in toolConfig.tools[0]: "name"' in message
        print(
            "OBSERVED ParamValidationError: invalid tagged union "
            "toolConfig.tools[0] (raw Bedrock tool lacks toolSpec wrapper)"
        )
        raise SystemExit(1)

    print("BUG NOT OBSERVED: botocore accepted the malformed Bedrock tool")


if __name__ == "__main__":
    main()
