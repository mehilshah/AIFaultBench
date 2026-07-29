#!/usr/bin/env python3
"""Reproduce MCP's legacy SSE read-timeout propagation after initialization."""

import asyncio
import json

import anyio
import httpx

from mcp import ClientSession
from mcp.client.sse import sse_client


class State:
    def __init__(self) -> None:
        self.initialize_id: int | str | None = None
        self.initialize_received = anyio.Event()
        self.release_timeout = anyio.Event()


class ScriptedSSEStream(httpx.AsyncByteStream):
    """An SSE stream that becomes silent only after MCP initialization."""

    def __init__(self, state: State) -> None:
        self.state = state

    async def __aiter__(self):
        yield b"event: endpoint\ndata: /messages\n\n"
        await self.state.initialize_received.wait()
        response = {
            "jsonrpc": "2.0",
            "id": self.state.initialize_id,
            "result": {
                "protocolVersion": "2025-06-18",
                "capabilities": {},
                "serverInfo": {"name": "local-stub", "version": "1.0"},
            },
        }
        yield f"event: message\ndata: {json.dumps(response)}\n\n".encode()
        await self.state.release_timeout.wait()
        raise httpx.ReadTimeout("scripted silent SSE stream")

    async def aclose(self) -> None:
        pass


class ScriptedTransport(httpx.AsyncBaseTransport):
    def __init__(self, state: State) -> None:
        self.state = state

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        if request.method == "GET":
            return httpx.Response(
                200,
                headers={"content-type": "text/event-stream"},
                stream=ScriptedSSEStream(self.state),
                request=request,
            )

        payload = json.loads(request.content)
        if payload.get("method") == "initialize":
            self.state.initialize_id = payload["id"]
            self.state.initialize_received.set()
        return httpx.Response(202, request=request)


def client_factory(state: State):
    def create_client(**kwargs):
        return httpx.AsyncClient(transport=ScriptedTransport(state), **kwargs)

    return create_client


async def main() -> None:
    state = State()
    received: list[Exception] = []
    timeout_seen = anyio.Event()

    async def message_handler(message: object) -> None:
        if isinstance(message, Exception):
            received.append(message)
            timeout_seen.set()

    async with sse_client(
        "http://mcp.invalid/sse",
        httpx_client_factory=client_factory(state),
    ) as streams:
        async with ClientSession(*streams, message_handler=message_handler) as session:
            await session.initialize()
            print("MCP session initialized using local stub")
            state.release_timeout.set()
            await timeout_seen.wait()

    observed = received[0] if received else None
    if not isinstance(observed, httpx.ReadTimeout):
        raise AssertionError(f"expected httpx.ReadTimeout after initialization, got {observed!r}")

    print(f"OBSERVED BUG: {type(observed).__name__}: {observed}")
    raise AssertionError("buggy SSE transport forwards httpx.ReadTimeout after initialization")


if __name__ == "__main__":
    asyncio.run(main())
