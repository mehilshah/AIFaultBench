#!/usr/bin/env python3
"""Expose Temporal's cached argument type for the two model activities."""

from dataclasses import dataclass

from pydantic_ai import Agent
from pydantic_ai.durable_exec.temporal import TemporalAgent
from pydantic_ai.models.test import TestModel
from temporalio import activity


@dataclass
class MyDeps:
    tenant_id: str


agent = Agent(TestModel(), name='repro', deps_type=MyDeps)
model = TemporalAgent(agent).model

request_types = activity._Definition.from_callable(model.request_activity).arg_types
stream_types = activity._Definition.from_callable(model.request_stream_activity).arg_types
expected = MyDeps | None

if request_types[1] == expected:
    raise AssertionError(f'bug absent: request captured {request_types[1]!r}')
if stream_types[1] != expected:
    raise AssertionError(f'unexpected streaming type: {stream_types[1]!r}')

print(f'BUG REPRODUCED: request captured {request_types[1]!r}; stream captured {stream_types[1]!r}')
raise SystemExit(1)
