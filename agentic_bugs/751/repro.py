#!/usr/bin/env python3
"""Offline reproduction attempt for langgraph issue #6456."""

import json
import operator
from contextlib import contextmanager
from typing import Annotated
from typing_extensions import TypedDict

from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Send
from psycopg.types.json import Jsonb


class OverallState(TypedDict):
    topics: list[str]
    jokes: Annotated[list[str], operator.add]
    all_jokes: str


class LocalCursor:
    """Validates JSONB values like psycopg, without opening a database connection."""

    def execute(self, query: str, params=None):
        if params:
            for value in params:
                if isinstance(value, Jsonb):
                    json.dumps(value.obj)
        return self

    def executemany(self, query: str, params):
        for row in params:
            self.execute(query, row)

    def fetchone(self):
        return None


class LocalPostgresSaver(PostgresSaver):
    """Runs the real PostgresSaver methods with a local JSONB adapter."""

    def __init__(self):
        # The overridden _cursor means this placeholder connection is never used.
        super().__init__(None)  # type: ignore[arg-type]

    @contextmanager
    def _cursor(self, *, pipeline: bool = False):
        yield LocalCursor()


def send_topics(state: OverallState):
    return [Send("create_joke", {"topic": topic}) for topic in state["topics"]]


def create_joke(state: dict[str, str]):
    return {"jokes": [f"Joke for topic {state['topic']}"]}


def reduce_jokes(state: OverallState):
    return {"all_jokes": "\n".join(state["jokes"])}


def main() -> None:
    workflow = StateGraph(OverallState)
    workflow.add_node("create_joke", create_joke)
    workflow.add_node("reduce_jokes", reduce_jokes)
    workflow.add_conditional_edges(START, send_topics, {"create_joke": "create_joke"})
    workflow.add_edge("create_joke", "reduce_jokes")
    workflow.add_edge("reduce_jokes", END)

    app = workflow.compile(checkpointer=LocalPostgresSaver())
    try:
        result = app.invoke(
            {"topics": ["fine arts", "firefighters", "maths"], "jokes": [], "all_jokes": ""},
            config={"configurable": {"thread_id": "1"}},
        )
    except TypeError as exc:
        if "Object of type Send is not JSON serializable" in str(exc):
            print(f"BUG REPRODUCED: {type(exc).__name__}: {exc}")
            raise
        raise

    expected = [
        "Joke for topic fine arts",
        "Joke for topic firefighters",
        "Joke for topic maths",
    ]
    assert result["jokes"] == expected, result
    print("NOT REPRODUCED: PostgresSaver serialized Send tasks and completed the graph")


if __name__ == "__main__":
    main()
