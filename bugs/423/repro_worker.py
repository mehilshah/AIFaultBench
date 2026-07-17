#!/usr/bin/env python3
"""Tiny entrypoint used by the Accelerate launcher during the repro."""

from __future__ import annotations

import json
import os
import sys


def main() -> None:
    payload = {
        "argv": sys.argv,
        "rank": os.environ.get("RANK"),
        "local_rank": os.environ.get("LOCAL_RANK"),
        "world_size": os.environ.get("WORLD_SIZE"),
    }
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
