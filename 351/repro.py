#!/usr/bin/env python3
"""Minimal reproducer for the parallel_tool_calls null validation crash.

This mirrors the schema mismatch in
`vllm/entrypoints/openai/responses/protocol.py`:

- request side accepts `parallel_tool_calls: bool | None = True`
- response side requires `parallel_tool_calls: bool`

The real bug happens when `from_request()` forwards `None` into the response
model and Pydantic raises a ValidationError instead of applying the default.
"""

from __future__ import annotations

import sys

from pydantic import BaseModel, ValidationError


class ResponsesRequest(BaseModel):
    parallel_tool_calls: bool | None = True


class ResponsesResponse(BaseModel):
    parallel_tool_calls: bool


def main() -> int:
    request = ResponsesRequest.model_validate({"parallel_tool_calls": None})
    print(f"request.parallel_tool_calls={request.parallel_tool_calls!r}")

    payload = {"parallel_tool_calls": request.parallel_tool_calls}
    try:
        ResponsesResponse.model_validate(payload)
    except ValidationError as exc:
        print("CRASH:", exc)
        return 0

    print("no error")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
