#!/usr/bin/env python3
"""Reproduce ATIF's missing timestamp-format validation."""

from phoenix.client.helpers.atif._convert import _convert_atif_trajectory_to_spans
from phoenix.client.helpers.atif._validate import _validate_atif_trajectory


trajectory = {
    "schema_version": "ATIF-v1.4",
    "session_id": "session-1",
    "agent": {"name": "agent", "version": "1"},
    "steps": [
        {
            "step_id": 1,
            "source": "user",
            "message": "hello",
            "timestamp": "not-a-date",
        }
    ],
}

_validate_atif_trajectory(trajectory)

try:
    _convert_atif_trajectory_to_spans(trajectory)
except ValueError as error:
    assert str(error) == "Invalid isoformat string: 'not-a-date'", str(error)
    print(
        "BUG REPRODUCED: validation accepted an invalid timestamp; "
        "conversion raised ValueError: Invalid isoformat string: 'not-a-date'"
    )
    raise SystemExit(1)

raise AssertionError("conversion unexpectedly accepted an invalid ATIF timestamp")
