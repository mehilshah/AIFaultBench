#!/usr/bin/env python3
"""Reproduce #8211 without contacting an LLM provider."""

import asyncio
import json

import httpx
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field, ValidationError


class SomeStructuredResp(BaseModel):
    response: str = Field("default reasoning")


async def responses_api_stub(request: httpx.Request) -> httpx.Response:
    """Return the local-server plain text that the issue reports."""
    assert request.method == "POST"
    assert request.url.path == "/v1/responses"
    payload = json.loads(request.content)
    assert payload["reasoning"] == {"effort": "low"}
    assert payload["text"]["format"]["type"] == "json_schema"
    assert payload["text"]["format"]["name"] == "SomeStructuredResp"
    return httpx.Response(
        200,
        json={
            "id": "resp_8211",
            "object": "response",
            "created_at": 0,
            "model": "local-test-model",
            "status": "completed",
            "parallel_tool_calls": True,
            "tool_choice": "auto",
            "tools": [],
            "output": [
                {
                    "id": "msg_8211",
                    "type": "message",
                    "status": "completed",
                    "role": "assistant",
                    "content": [
                        {
                            "type": "output_text",
                            "text": "Hello! How can I help you today?",
                            "annotations": [],
                        }
                    ],
                }
            ],
        },
    )


async def reproduce() -> int:
    transport = httpx.MockTransport(responses_api_stub)
    async with httpx.AsyncClient(transport=transport) as mock_client:
        llm = ChatOpenAI(
            model="local-test-model",
            api_key="not-used",
            base_url="https://unit.test/v1",
            reasoning={"effort": "low"},
            http_async_client=mock_client,
        )
        structured_llm = llm.with_structured_output(SomeStructuredResp)
        try:
            await structured_llm.ainvoke("hi there")
        except ValidationError as error:
            message = str(error)
            expected = (
                "Invalid JSON: expected value at line 1 column 1"
                " [type=json_invalid, input_value='Hello! How can I help you today?'"
            )
            assert expected in message, message
            print("OBSERVED ValidationError: reasoning + structured output parsed plain text as JSON")
            return 1
    raise AssertionError("Expected structured-output parsing to reject the plain-text reply")


if __name__ == "__main__":
    raise SystemExit(asyncio.run(reproduce()))
