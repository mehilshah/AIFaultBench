#!/usr/bin/env python3
from __future__ import annotations

import traceback


cdb = None


def all_reduce(tensor, op="SUM", group=None, async_op=False):
    # Mirrors deepspeed/comm/comm.py: all_reduce() without the guard.
    return cdb.all_reduce(tensor, op, group, async_op)


def main() -> int:
    tensor = [1, 2, 3]
    try:
        all_reduce(tensor)
    except Exception:
        traceback.print_exc()
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
