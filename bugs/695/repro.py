#!/usr/bin/env python3
"""Offline reproduction for llama-index Ollama custom-client loss."""

from llama_index.llms.ollama import Ollama
from llama_index.llms.ollama import base as ollama_base


class SuppliedAsyncClient:
    """A stand-in for the caller's authenticated AsyncClient."""

    headers = {"Authorization": "Bearer test-token"}


class UnauthenticatedSyncClient:
    """Records the client LlamaIndex creates instead of using the supplied one."""

    instances = []

    def __init__(self, host, timeout):
        self.host = host
        self.timeout = timeout
        self.headers = {}
        self.instances.append(self)

    def show(self, model):
        raise RuntimeError("Unauthorized (status code: 401)")


def main():
    # Prevent all network I/O while preserving the buggy client-property path.
    ollama_base.Client = UnauthenticatedSyncClient
    supplied = SuppliedAsyncClient()
    llm = Ollama(
        async_client=supplied,
        base_url="http://authenticated-ollama.invalid",
        model="test-model",
    )

    try:
        llm.complete("hi")
    except RuntimeError as exc:
        assert str(exc) == "Unauthorized (status code: 401)", exc
    else:
        raise AssertionError("expected the unauthenticated synchronous client to be used")

    assert llm._async_client is supplied
    assert len(UnauthenticatedSyncClient.instances) == 1
    created = UnauthenticatedSyncClient.instances[0]
    assert created.host == "http://authenticated-ollama.invalid"
    assert created.headers == {}, created.headers
    print("BUG OBSERVED: sync complete ignored supplied async-client Authorization headers")
    raise SystemExit(1)


if __name__ == "__main__":
    main()
