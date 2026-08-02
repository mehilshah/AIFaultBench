#!/usr/bin/env python3
"""Reproduce the async EnsembleRetriever non-string normalization bug."""

import asyncio

from langchain_classic.retrievers import EnsembleRetriever
from langchain_core.retrievers import BaseRetriever
from pydantic import ValidationError


class WeirdRetriever(BaseRetriever):
    """A local, deterministic retriever that violates the Document output type."""

    def _get_relevant_documents(self, query: str, *, run_manager=None):
        return [42]

    async def _aget_relevant_documents(self, query: str, *, run_manager=None):
        return [42]


async def main() -> None:
    ensemble = EnsembleRetriever(retrievers=[WeirdRetriever()], weights=[1.0])
    try:
        await ensemble.ainvoke("test")
    except ValidationError as exc:
        error = exc.errors()[0]
        assert error["loc"] == ("page_content",), error
        assert error["input"] == 42, error
        assert error["type"] == "string_type", error
        print("BUG OBSERVED: async arank_fusion rejected integer 42 as Document.page_content")
        raise
    raise AssertionError("BUG NOT OBSERVED: async EnsembleRetriever accepted integer output")


asyncio.run(main())
