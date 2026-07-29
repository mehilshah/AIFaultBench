#!/usr/bin/env python3
"""Verify the reported Send/checkpointer serialization behavior offline."""

from __future__ import annotations

import operator
import warnings
from typing import Annotated

import ormsgpack
from langchain_core._api.deprecation import LangChainPendingDeprecationWarning
from typing_extensions import TypedDict

# This warning is unrelated to Send serialization and would obscure the evidence.
warnings.simplefilter("ignore", LangChainPendingDeprecationWarning)

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
from langgraph.errors import InvalidUpdateError
from langgraph.graph import END, START, StateGraph
from langgraph.types import Send


class State(TypedDict):
    tasks: list[str]
    results: Annotated[list[str], operator.add]


class ReportedState(TypedDict):
    messages: list[str]
    results: list[str]


def route(state: State) -> list[Send]:
    """Supported Send usage: dynamic routing from a conditional edge."""
    return [Send("worker", {"task": task}) for task in state["tasks"]]


def worker(state: State) -> dict[str, list[str]]:
    return {"results": [state["task"]]}


def reported_router(state: ReportedState) -> list[Send]:
    """The unsupported node return from the issue report."""
    return [Send("worker", {"task": f"task_{index}"}) for index in range(3)]


def reported_worker(state: ReportedState) -> dict[str, list[str]]:
    return {"results": [state.get("task", "done")]}


def reported_aggregator(state: ReportedState) -> dict[str, list[str]]:
    return {"messages": ["All tasks completed"]}


def main() -> None:
    send = Send("worker", {"task": "alpha"})

    try:
        ormsgpack.packb(send)
    except TypeError as exc:
        raw_error = str(exc)
    else:
        raise AssertionError("raw ormsgpack unexpectedly serialized Send")
    assert "not msgpack serializable: Send" in raw_error, raw_error
    print(f"RAW_ORMSGPACK_REJECTS_SEND: {raw_error}")

    serde = JsonPlusSerializer()
    packed = serde.dumps_typed(send)
    restored = serde.loads_typed(packed)
    assert packed[0] == "msgpack", packed[0]
    assert restored == send, (restored, send)
    print(f"JSONPLUS_SEND_ROUND_TRIP_OK: type={packed[0]}, value={restored!r}")

    reported_graph = StateGraph(ReportedState)
    reported_graph.add_node("router", reported_router)
    reported_graph.add_node("worker", reported_worker)
    reported_graph.add_node("aggregator", reported_aggregator)
    reported_graph.add_edge(START, "router")
    reported_graph.add_edge("worker", "aggregator")
    reported_app = reported_graph.compile(checkpointer=InMemorySaver())
    try:
        reported_app.invoke(
            {"messages": ["start"]},
            config={"configurable": {"thread_id": "reported-example"}},
        )
    except InvalidUpdateError as exc:
        assert str(exc).startswith("Expected dict, got [Send("), str(exc)
        print("REPORTED_GRAPH_REJECTED_AS_NODE_UPDATE: InvalidUpdateError")
    else:
        raise AssertionError("the issue's unsupported node return unexpectedly succeeded")

    graph = StateGraph(State)
    graph.add_node("worker", worker)
    graph.add_conditional_edges(START, route)
    graph.add_edge("worker", END)
    saver = InMemorySaver()
    app = graph.compile(checkpointer=saver)
    config = {"configurable": {"thread_id": "send-serde-repro"}}
    result = app.invoke({"tasks": ["alpha", "beta"]}, config=config)
    assert result["results"] == ["alpha", "beta"], result
    assert saver.get_tuple(config) is not None
    print(f"CHECKPOINTED_SEND_GRAPH_OK: results={result['results']!r}")
    print("NOT_REPRODUCED: JsonPlusSerializer and supported checkpointed Send routing succeed")


if __name__ == "__main__":
    main()
