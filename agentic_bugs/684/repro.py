#!/usr/bin/env python3
"""Reproduce mem0ai 2.0.12 failing at import on a read-only filesystem."""

import errno
import os
import sys


# This is a read-only snap mount on the reference host.  It is used in place
# of the read-only application directory in the Kubernetes report.
READ_ONLY_HOME = "/snap/bare/5"
EXPECTED_PATH = f"{READ_ONLY_HOME}/.mem0"


def main() -> int:
    os.environ["HOME"] = READ_ONLY_HOME
    os.environ.pop("MEM0_DIR", None)

    try:
        import mem0  # noqa: F401  # Performs os.makedirs(~/.mem0) at import time.
    except OSError as exc:
        if exc.errno != errno.EROFS or exc.filename != EXPECTED_PATH:
            raise AssertionError(f"unexpected import failure: {exc!r}") from exc
        print(f"OBSERVED BUG: importing mem0 raised {exc.__class__.__name__}: {exc}")
        return 1

    raise AssertionError("mem0 import unexpectedly succeeded on a read-only HOME")


if __name__ == "__main__":
    sys.exit(main())
