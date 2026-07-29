#!/usr/bin/env python3
"""Check whether Send-mapped nodes lose Runtime context in langgraph 1.0.2."""

import operator
import sys
from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.runtime import Runtime
from langgraph.types import Send


class OverallState(TypedDict):
    subjects: list[str]
    jokes: Annotated[list[str], operator.add]


class NestedState(TypedDict):
    subject: str


class ContextSchema(TypedDict):
    my_runtime_value: str


def generate_topics(state: OverallState) -> dict[str, list[str]]:
    return {"subjects": ["lions", "elephants", "penguins"]}


def generate_joke(
    state: NestedState, runtime: Runtime[ContextSchema]
) -> dict[str, list[str]]:
    if runtime.context is None:
        raise RuntimeError("Runtime context is not available")
    return {"jokes": [f"{runtime.context['my_runtime_value']}:{state['subject']}"]}


def continue_to_jokes(state: OverallState) -> list[Send]:
    return [Send("generate_joke", {"subject": subject}) for subject in state["subjects"]]


builder = StateGraph(OverallState, context_schema=ContextSchema)
builder.add_node("generate_topics", generate_topics)
builder.add_node("generate_joke", generate_joke)
builder.add_edge(START, "generate_topics")
builder.add_conditional_edges("generate_topics", continue_to_jokes, ["generate_joke"])
builder.add_edge("generate_joke", END)
graph = builder.compile()


def main() -> int:
    expected = {"ctx:lions", "ctx:elephants", "ctx:penguins"}
    try:
        result = graph.invoke({}, context={"my_runtime_value": "ctx"})
    except RuntimeError as exc:
        if str(exc) == "Runtime context is not available":
            print("BUG_REPRODUCED: Send-mapped node lost supplied Runtime context")
        raise

    assert set(result["jokes"]) == expected, result

    # This is the error reported by the issue, but it is expected when a run is
    # resumed/invoked without context (as the issue's closing comment explains).
    try:
        graph.invoke({})
    except RuntimeError as exc:
        assert str(exc) == "Runtime context is not available", repr(exc)
    else:
        raise AssertionError("missing context unexpectedly reached mapped node")

    print(
        "NOT_REPRODUCED: Send-mapped nodes received supplied Runtime context; "
        "the reported RuntimeError occurs only when context is omitted."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
