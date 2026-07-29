#!/usr/bin/env python3
"""Deterministically reproduce logging after Streamable HTTP termination."""

import sys

import anyio
import mcp.types as types
from mcp.server.models import InitializationOptions
from mcp.server.session import ServerSession
from mcp.server.streamable_http import StreamableHTTPServerTransport


async def reproduce() -> int:
    init_options = InitializationOptions(
        server_name="repro",
        server_version="1.0",
        capabilities=types.ServerCapabilities(),
    )
    transport = StreamableHTTPServerTransport("repro-session")

    # connect() creates the same memory write stream that terminate() closes when
    # a streamable-HTTP client sends DELETE.
    async with transport.connect() as (read_stream, write_stream):
        session = ServerSession(read_stream, write_stream, init_options, stateless=True)
        await transport.terminate()

        try:
            # This is the server's logging path from the issue stack trace.
            await session.send_log_message(
                level="error",
                data="handler completed during shutdown",
                logger="repro",
            )
        except anyio.ClosedResourceError:
            print("BUG REPRODUCED: send_log_message after terminate raised anyio.ClosedResourceError")
            return 1

    raise AssertionError("send_log_message unexpectedly succeeded after transport termination")


if __name__ == "__main__":
    sys.exit(anyio.run(reproduce))
