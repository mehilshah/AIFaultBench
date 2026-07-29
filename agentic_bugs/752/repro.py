#!/usr/bin/env python3
"""Offline reproduction for SubQuestionQueryEngine partial-failure handling."""

from llama_index.core.base.base_query_engine import BaseQueryEngine
from llama_index.core.base.response.schema import RESPONSE_TYPE
from llama_index.core.callbacks import CallbackManager
from llama_index.core.question_gen.types import SubQuestion
from llama_index.core.query_engine.sub_question_query_engine import (
    SubQuestionQueryEngine,
)
from llama_index.core.schema import QueryBundle
from llama_index.core.tools import QueryEngineTool, ToolMetadata


class SuccessfulQueryEngine(BaseQueryEngine):
    def __init__(self) -> None:
        super().__init__(callback_manager=CallbackManager([]))

    def _query(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
        return "Paris"

    async def _aquery(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
        return "Paris"

    def _get_prompt_modules(self):
        return {}


class RateLimitedQueryEngine(BaseQueryEngine):
    def __init__(self) -> None:
        super().__init__(callback_manager=CallbackManager([]))

    def _query(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
        raise RuntimeError("API rate limit exceeded")

    async def _aquery(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
        raise RuntimeError("API rate limit exceeded")

    def _get_prompt_modules(self):
        return {}


class FixedQuestionGenerator:
    def generate(self, tools, query_bundle):
        return [
            SubQuestion(sub_question="capital of France", tool_name="france_docs"),
            SubQuestion(sub_question="capital of Germany", tool_name="germany_docs"),
        ]


class OfflineSynthesizer:
    def synthesize(self, query, nodes, additional_source_nodes):
        # Reaching here would mean the failed Germany sub-question was skipped.
        return "synthesized from surviving answers"


engine = SubQuestionQueryEngine(
    question_gen=FixedQuestionGenerator(),
    response_synthesizer=OfflineSynthesizer(),
    query_engine_tools=[
        QueryEngineTool(
            query_engine=SuccessfulQueryEngine(),
            metadata=ToolMetadata(name="france_docs", description="offline success"),
        ),
        QueryEngineTool(
            query_engine=RateLimitedQueryEngine(),
            metadata=ToolMetadata(name="germany_docs", description="offline failure"),
        ),
    ],
    verbose=False,
    use_async=False,
)

try:
    engine.query("Compare France and Germany")
except RuntimeError as exc:
    assert str(exc) == "API rate limit exceeded", repr(exc)
    print("BUG REPRODUCED: RuntimeError escaped failed sub-question")
    raise
else:
    raise AssertionError("Expected RuntimeError to escape the failed sub-question")
