#!/usr/bin/env python3
"""Reproduce RedisCache leaking dill's TypeError for an SSLContext."""

import asyncio
import ssl
import sys
from unittest.mock import AsyncMock, patch

from langflow.services.cache.service import RedisCache


async def main() -> None:
    # Redis is entirely local to this script: no server or network operation occurs.
    with patch("redis.asyncio.StrictRedis") as strict_redis:
        strict_redis.return_value = AsyncMock()
        cache = RedisCache(expiration_time=60)
        cache._signing_key = b"r" * 32

        try:
            await cache.set("vertex", {"model_client_context": ssl.create_default_context()})
        except TypeError as exc:
            message = str(exc)
            assert "cannot pickle 'SSLContext' object" in message, message
            print(f"BUG OBSERVED: RedisCache.set leaked raw TypeError: {message}")
            return

    raise AssertionError("RedisCache.set unexpectedly handled the unpicklable SSLContext")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as exc:
        print(f"REPRO ASSERTION FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise
    raise SystemExit(1)  # Non-zero means the buggy behavior was observed.
