#!/usr/bin/env python3
"""Offline reproduction for pydantic/pydantic-ai#6008."""

import asyncio
import sys
from importlib.metadata import version

from pydantic_graph import GraphBuilder, StepContext, reduce_list_append


emitted: list[list[int]] = []
graph_builder = GraphBuilder(output_type=list)


@graph_builder.step
async def produce(ctx: StepContext[None, None, None]) -> list[int]:
    return [1, 2, 3]


@graph_builder.step
async def identity(ctx: StepContext[None, None, int]) -> int:
    return ctx.inputs


collect = graph_builder.join(reduce_list_append, initial_factory=list)


@graph_builder.step
async def after_join(ctx: StepContext[None, None, list]) -> list:
    emitted.append(sorted(ctx.inputs))
    return ctx.inputs


graph_builder.add(graph_builder.edge_from(graph_builder.start_node).to(produce))
graph_builder.add_mapping_edge(produce, identity, downstream_join_id=collect.id)
graph_builder.add(
    graph_builder.edge_from(identity).to(collect),
    graph_builder.edge_from(collect).to(after_join),
    graph_builder.edge_from(after_join).to(graph_builder.end_node),
)
result = asyncio.run(graph_builder.build().run())

if result == [] and emitted == [[], [1, 2, 3]]:
    print(
        f"FAULT: pydantic-graph={version('pydantic-graph')}; "
        f"downstream_join_id returned {result}; join emitted {emitted}"
    )
    sys.exit(1)

raise AssertionError(f"Unexpected graph behavior: result={result}, emitted={emitted}")
