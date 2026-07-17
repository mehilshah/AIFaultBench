#!/usr/bin/env python3

"""Minimal reproduction for Point equality behavior."""

import sys
from datetime import datetime, timezone

from influxdb_client import Point


def main() -> int:
    point_a = (
        Point("asd")
        .tag("foo", "bar")
        .field("value", 123.45)
        .time(datetime(2023, 12, 19, 13, 27, 42, 215000, tzinfo=timezone.utc))
    )

    point_b = (
        Point("asd")
        .tag("foo", "bar")
        .field("value", 123.45)
        .time(datetime(2023, 12, 19, 13, 27, 42, 215000, tzinfo=timezone.utc))
    )

    line_protocol_a = point_a.to_line_protocol()
    line_protocol_b = point_b.to_line_protocol()
    equality = point_a == point_b

    print(f"point_a.to_line_protocol(): {line_protocol_a}")
    print(f"point_b.to_line_protocol(): {line_protocol_b}")
    print(f"line_protocol_equal: {line_protocol_a == line_protocol_b}")
    print(f"point_equality: {equality}")

    if equality:
        print("unexpected: Point objects compare equal")
        return 0

    print("bug reproduced: structurally identical Point objects compare unequal")
    return 1


if __name__ == "__main__":
    sys.exit(main())
