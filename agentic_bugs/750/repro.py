#!/usr/bin/env python3
"""Check the reported @task/runtime-checkpointer resume behavior offline."""

import warnings

warnings.simplefilter("ignore")

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import CONFIG_KEY_CHECKPOINTER
from langgraph.func import task
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt


task_calls = 0


@task
def completed_before_interrupt() -> str:
    """A non-idempotent stand-in whose call count exposes re-execution."""
    global task_calls
    task_calls += 1
    return "task-result"


def process(_: dict) -> dict:
    value = completed_before_interrupt().result()
    response = interrupt(f"Confirm {value}?")
    return {"value": value, "response": response}


builder = StateGraph(dict)
builder.add_node("process", process)
builder.add_edge(START, "process")
builder.add_edge("process", END)

# Deliberately compile without a saver, as an API deployment does.
graph = builder.compile()
runtime_config = {
    "configurable": {
        "thread_id": "runtime-injected-checkpointer",
        CONFIG_KEY_CHECKPOINTER: InMemorySaver(),
    }
}

first = graph.invoke({}, runtime_config)
assert "__interrupt__" in first, f"expected interrupt, got {first!r}"
resumed = graph.invoke(Command(resume="approved"), runtime_config)
assert resumed == {"value": "task-result", "response": "approved"}, resumed

if task_calls != 1:
    print(f"FAULT_OBSERVED: @task re-executed on resume (calls={task_calls})")
    raise AssertionError("runtime-injected checkpointer did not cache @task output")

print("NOT_REPRODUCED: runtime-injected checkpointer cached @task output (calls=1)")
