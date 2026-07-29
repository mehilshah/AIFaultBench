#!/usr/bin/env python3
"""Reproduce ContextChatEngine's async postprocessor dispatch bug."""

import asyncio
from unittest.mock import MagicMock

from llama_index.core.base.base_retriever import BaseRetriever
from llama_index.core.chat_engine.context import ContextChatEngine
from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.core.schema import NodeWithScore, TextNode


class TrackingPostprocessor(BaseNodePostprocessor):
    called_sync: bool = False
    called_async: bool = False

    def _postprocess_nodes(self, nodes, query_bundle=None):
        self.called_sync = True
        return nodes

    async def _apostprocess_nodes(self, nodes, query_bundle=None):
        self.called_async = True
        return nodes


class DummyRetriever(BaseRetriever):
    def _retrieve(self, query_bundle):
        return [NodeWithScore(node=TextNode(text="dummy"))]

    async def _aretrieve(self, query_bundle):
        return self._retrieve(query_bundle)


async def main():
    postprocessor = TrackingPostprocessor()
    fake_llm = MagicMock()
    fake_llm.metadata.context_window = 4096
    fake_llm.metadata.system_role = "system"
    engine = ContextChatEngine.from_defaults(
        retriever=DummyRetriever(), llm=fake_llm, node_postprocessors=[postprocessor]
    )

    await engine._aget_nodes("test")
    print(
        "OBSERVED BUG: async path called_sync={} called_async={}".format(
            postprocessor.called_sync, postprocessor.called_async
        )
    )
    assert not postprocessor.called_sync, "sync postprocessor was called in async path"
    assert postprocessor.called_async, "async postprocessor was not called in async path"


asyncio.run(main())
