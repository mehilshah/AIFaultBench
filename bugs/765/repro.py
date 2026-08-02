#!/usr/bin/env python3
"""Reproduce LangGraph issue #6439 without a model or network access."""

import warnings

from typing_extensions import TypedDict

# A dependency emits this unrelated warning during import on the reference host.
warnings.filterwarnings(
    "ignore", message=r"The default value of `allowed_objects` will change.*"
)

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    done_d: bool


def node_a(_: State) -> dict[str, object]:
    return {}


def node_b(_: State) -> dict[str, object]:
    return {}


def node_c(_: State) -> dict[str, object]:
    return {}


def node_d(_: State) -> dict[str, bool]:
    return {"done_d": True}


def node_f(state: State) -> dict[str, object]:
    if not state["done_d"]:
        raise RuntimeError("node_f ran before node_d completed")
    return {}


def main() -> None:
    graph = StateGraph(State)
    graph.add_node("a", node_a)
    graph.add_node("b", node_b)
    graph.add_node("c", node_c)
    graph.add_node("d", node_d)
    graph.add_node("f", node_f)
    graph.add_edge(START, "a")
    graph.add_edge(START, "b")
    # Separate add_edge calls do not form a join: f is scheduled by a alone.
    graph.add_edge("a", "f")
    graph.add_edge("b", "c")
    graph.add_edge("c", "d")
    graph.add_edge("d", "f")
    graph.add_edge("f", END)

    try:
        graph.compile().invoke({"done_d": False})
    except RuntimeError as exc:
        assert str(exc) == "node_f ran before node_d completed"
        print(f"OBSERVED EARLY EXECUTION: {exc}")
        raise
    raise AssertionError("node_f unexpectedly waited for node_d")


if __name__ == "__main__":
    main()
