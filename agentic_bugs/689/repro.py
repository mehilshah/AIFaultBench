#!/usr/bin/env python3
"""Reproduce LangGraph's unvalidated non-mapping config failure."""

import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    messages: Annotated[list[str], operator.add]


def node(state: State) -> dict[str, list[str]]:
    return {"messages": ["entered node"]}


builder = StateGraph(State)
builder.add_node("node", node)
builder.add_edge(START, "node")
builder.add_edge("node", END)
graph = builder.compile()

try:
    graph.invoke(None, config="invalid_config")
except AttributeError as error:
    expected = "'str' object has no attribute 'items'"
    if str(error) != expected:
        raise AssertionError(f"unexpected AttributeError: {error!s}") from error
    print(f"OBSERVED: AttributeError: {error}", flush=True)
    raise
else:
    raise AssertionError("expected invalid string config to raise AttributeError")
