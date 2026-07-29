#!/usr/bin/env python3
"""Reproduce LocalPythonExecutor rejecting a documented base built-in before send_tools()."""

from smolagents.local_python_executor import InterpreterError, LocalPythonExecutor


def main() -> None:
    executor = LocalPythonExecutor([])
    try:
        executor("range(1)")
    except InterpreterError as error:
        expected = "Forbidden function evaluation: 'range' is not among the explicitly allowed tools"
        if expected not in str(error):
            raise AssertionError(f"unexpected InterpreterError: {error}")
        print(f"OBSERVED BUG: LocalPythonExecutor rejects range before send_tools: {error}")
        raise SystemExit(1)
    raise AssertionError("BUG NOT OBSERVED: range executed without send_tools()")


if __name__ == "__main__":
    main()
