#!/usr/bin/env python3
"""Offline reproduction for smolagents issue #1706."""

from smolagents.local_python_executor import InterpreterError, LocalPythonExecutor


def main() -> None:
    executor = LocalPythonExecutor([])
    executor.send_tools({})

    try:
        executor("print(f'{type(bytes)=}')\nprint(f\"{isinstance(b'123', bytes)=}\")")
    except InterpreterError as error:
        message = str(error)
        expected = "The variable `bytes` is not defined."
        if expected not in message:
            raise AssertionError(f"Unexpected interpreter failure: {message}") from error
        print(f"BUG OBSERVED: InterpreterError: {message}")
        raise SystemExit(1)

    raise AssertionError("Bug not observed: LocalPythonExecutor accepted bytes.")


if __name__ == "__main__":
    main()
