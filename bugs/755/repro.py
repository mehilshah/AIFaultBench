#!/usr/bin/env python3
"""Reproduce smolagents' E2B 2.0.0 sandbox-construction incompatibility."""

from smolagents.monitoring import AgentLogger, LogLevel
from smolagents.remote_executors import E2BExecutor


def main() -> None:
    try:
        # This is the exact constructor call CodeAgent reaches for executor_type="e2b".
        E2BExecutor([], AgentLogger(level=LogLevel.OFF))
    except TypeError as error:
        required = "SandboxBase.__init__() missing 5 required positional arguments"
        assert required in str(error), f"unexpected TypeError: {error}"
        print(f"OBSERVED BUG: {required}")
        raise SystemExit(1)
    raise AssertionError("BUG NOT REPRODUCED: E2BExecutor constructed a Sandbox")


if __name__ == "__main__":
    main()
