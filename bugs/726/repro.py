#!/usr/bin/env python3
"""Reproduce generic dict output types being incorrectly wrapped."""

import sys

from agents.agent_output import AgentOutputSchema
from agents.exceptions import ModelBehaviorError


plain = AgentOutputSchema(dict, strict_json_schema=False)
generic = AgentOutputSchema(dict[str, int], strict_json_schema=False)

assert plain._is_wrapped is False, "bare dict unexpectedly wrapped"
assert generic._is_wrapped is True, "generic dict was not incorrectly wrapped"
assert "response" in generic.json_schema()["properties"], "wrapper schema missing response"

try:
    generic.validate_json('{"a": 1}')
except ModelBehaviorError as exc:
    assert "response" in str(exc) and "Field required" in str(exc), str(exc)
else:
    raise AssertionError("natural generic-dict payload was accepted")

assert generic.validate_json('{"response": {"a": 1}}') == {"a": 1}
print("BUG REPRODUCED: dict[str, int] requires an unwanted response wrapper")
sys.exit(1)
