#!/usr/bin/env python3
"""Offline reproduction for smolagents issue #1814 at the pinned commit."""

from smolagents.local_python_executor import InterpreterError, LocalPythonExecutor


CODE = '''
structure = {"group": [1]}
result = {(group, e): e for group, values in structure.items() for e in values}
'''


def main() -> None:
    try:
        LocalPythonExecutor([])(CODE)
    except InterpreterError as error:
        expected = "The variable `e` is not defined."
        if expected not in str(error):
            raise AssertionError(f"unexpected InterpreterError: {error}") from error
        print(f"BUG REPRODUCED: {expected}")
        raise SystemExit(1)
    raise AssertionError("expected nested dictionary comprehension to raise InterpreterError")


if __name__ == "__main__":
    main()
