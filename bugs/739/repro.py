#!/usr/bin/env python3
"""Reproduce ATIF metrics validation accepting a non-mapping."""

from phoenix.client.helpers.atif._convert import _convert_atif_trajectory_to_spans
from phoenix.client.helpers.atif._validate import _validate_atif_trajectory


trajectory = {
    "schema_version": "ATIF-v1.4",
    "session_id": "deterministic-session",
    "agent": {"name": "agent", "version": "1"},
    "steps": [
        {
            "step_id": 1,
            "timestamp": "2025-01-01T00:00:00Z",
            "source": "user",
            "message": "hello",
        },
        {
            "step_id": 2,
            "timestamp": "2025-01-01T00:00:01Z",
            "source": "agent",
            "message": "hi",
            "metrics": "oops",
        },
    ],
}

_validate_atif_trajectory(trajectory)
print("VALIDATION_ACCEPTED_NON_OBJECT_METRICS")

try:
    _convert_atif_trajectory_to_spans(trajectory)
except AttributeError as error:
    expected = "'str' object has no attribute 'get'"
    if str(error) != expected:
        raise AssertionError(f"unexpected converter AttributeError: {error!s}") from error
    print(f"BUG_REPRODUCED: converter raised AttributeError: {error}")
    raise SystemExit(1)
else:
    raise AssertionError("converter unexpectedly accepted string metrics")
