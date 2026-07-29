#!/usr/bin/env python3
"""Offline reproduction for pydantic-ai issue #6611.

The fake SDK represents OpenAI's persisted-response endpoint.  It never makes
a network request: it rejects exactly the unsupported retrieval parameter.
"""

import asyncio

import httpx
from openai import BadRequestError
from pydantic_ai.exceptions import ModelHTTPError
from pydantic_ai.models.openai import OpenAIResponsesModel
from pydantic_ai.providers.openai import OpenAIProvider


class FakeResponses:
    async def retrieve(self, **kwargs):
        include = kwargs["include"]
        if "reasoning.encrypted_content" not in include:
            raise AssertionError(f"expected buggy include parameter, got {include!r}")

        message = "Encrypted content cannot be requested for persisted responses."
        response = httpx.Response(
            400,
            request=httpx.Request("GET", "https://offline.invalid/v1/responses/resp_persisted"),
            json={"message": message, "type": "invalid_request_error", "param": "include"},
        )
        raise BadRequestError(message, response=response, body=response.json())


class FakeClient:
    base_url = "https://offline.invalid/v1/"
    responses = FakeResponses()


async def main() -> None:
    model = OpenAIResponsesModel(
        "gpt-5.6-sol",
        provider=OpenAIProvider(openai_client=FakeClient()),  # type: ignore[arg-type]
    )
    try:
        await model._responses_retrieve("resp_persisted", {})
    except ModelHTTPError as error:
        expected = "Encrypted content cannot be requested for persisted responses."
        assert error.status_code == 400, error
        assert error.body["message"] == expected, error.body
        print(f"BUG REPRODUCED: persisted polling sent reasoning.encrypted_content; {expected}")
        raise
    raise AssertionError("retrieve unexpectedly succeeded")


asyncio.run(main())
