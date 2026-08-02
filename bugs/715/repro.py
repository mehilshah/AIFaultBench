#!/usr/bin/env python3
"""Offline reproduction of Langflow's omitted LiteLLM proxy extra."""

from pathlib import Path
import sys


PYPROJECT = Path("codebase/src/backend/base/pyproject.toml")


def main() -> int:
    dependency_lines = [
        line.strip()
        for line in PYPROJECT.read_text(encoding="utf-8").splitlines()
        if line.strip().startswith("litellm")
    ]
    if not dependency_lines or any("[proxy]" in line for line in dependency_lines):
        print("NO BUG: pinned Langflow metadata includes the LiteLLM proxy extra")
        return 0

    try:
        # This is the proxy/logging import taken by LiteLLM.  It makes no model
        # request and requires no credentials.
        import litellm.proxy.proxy_server  # noqa: F401
    except ImportError as error:
        expected = "No module named 'apscheduler'"
        if expected in str(error):
            print(f"OBSERVED BUG: {error}")
            return 1
        print(f"UNEXPECTED IMPORT ERROR: {error}", file=sys.stderr)
        return 2

    print("NO BUG: LiteLLM proxy imported without the declared proxy extra")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
