#!/usr/bin/env python3
"""Reproduce RedisKVStore's decode_responses=True key handling bug offline."""

import json

from llama_index.storage.kvstore.redis import RedisKVStore


class DecodeResponsesRedis:
    """Minimal Redis double: decode_responses=True makes hash keys str values."""

    def hscan_iter(self, *, name: str):
        assert name == "metadata"
        yield "document-hash", json.dumps({"source": "offline-double"})


def main() -> None:
    store = RedisKVStore(
        redis_client=DecodeResponsesRedis(),
        async_redis_client=object(),
    )
    try:
        store.get_all(collection="metadata")
    except AttributeError as exc:
        expected = "'str' object has no attribute 'decode'"
        assert str(exc) == expected, f"unexpected AttributeError: {exc!r}"
        print(f"OBSERVED BUG: RedisKVStore.get_all raised AttributeError: {exc}")
        raise
    raise AssertionError("BUG NOT OBSERVED: str Redis key was accepted")


if __name__ == "__main__":
    main()
