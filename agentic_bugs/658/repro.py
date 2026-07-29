#!/usr/bin/env python3
"""Offline reproducer for Fireworks._acall's un-awaited aiohttp response body."""

import asyncio
from unittest.mock import patch

from langchain_fireworks import Fireworks


class _Resp:
    status = 400

    def __repr__(self) -> str:
        return "<fake Fireworks 400 response>"

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return False

    async def text(self) -> str:
        return '{"error":"invalid model"}'


class _Session:
    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return False

    def post(self, *args, **kwargs):
        return _Resp()


async def main() -> None:
    llm = Fireworks(model="foo", api_key="dummy")
    with patch("langchain_fireworks.llms.ClientSession", return_value=_Session()):
        try:
            await llm._acall("hi")
        except ValueError as exc:
            message = str(exc)
            assert "<bound method _Resp.text" in message, message
            assert '{"error":"invalid model"}' not in message, message
            print("OBSERVED BUG: async error contains bound method, not response body")
            raise AssertionError("buggy missing-await behavior reproduced") from exc
        raise AssertionError("expected Fireworks to reject the fake HTTP 400 response")


asyncio.run(main())
