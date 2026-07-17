#!/usr/bin/env python3
"""Minimal reproduction for freezegun issue 344."""

from __future__ import annotations

import datetime
import sys


ROOT = __file__.rsplit("/", 1)[0]
CODEBASE = ROOT + "/codebase"
if CODEBASE not in sys.path:
    sys.path.insert(0, CODEBASE)

from freezegun import freeze_time  # noqa: E402


def baseline_round_trip() -> None:
    t = datetime.datetime.now().timestamp()
    t2 = datetime.datetime.fromtimestamp(t).timestamp()
    print("baseline_equal=", t == t2)


@freeze_time(datetime.datetime.fromtimestamp(100_000), tz_offset=-1)
def frozen_round_trip() -> None:
    now = datetime.datetime.now()
    t = now.timestamp()
    round_tripped = datetime.datetime.fromtimestamp(t)
    t2 = round_tripped.timestamp()

    print("frozen_now=", now)
    print("timestamp=", t)
    print("round_tripped=", round_tripped)
    print("round_trip_timestamp=", t2)
    print("equal=", t == t2)

    assert t == t2, (
        "Expected t == datetime.fromtimestamp(t).timestamp() under tz_offset=-1, "
        f"but got t={t!r} and t2={t2!r}"
    )


def main() -> None:
    baseline_round_trip()
    frozen_round_trip()


if __name__ == "__main__":
    main()
