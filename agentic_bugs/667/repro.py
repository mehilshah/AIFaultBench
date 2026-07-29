#!/usr/bin/env python3
"""Reproduce issue #1830 without constructing a real model client."""

from smolagents.local_python_executor import InterpreterError, LocalPythonExecutor


def main() -> None:
    # This is the CodeAgent local executor configuration created for
    # additional_authorized_imports=["*"].  No LLM or provider is involved.
    executor = LocalPythonExecutor(additional_authorized_imports=["*"])
    executor.send_tools({})

    try:
        executor("import os\nwith open('repro.py', 'rb') as file:\n    data = file.read()")
    except InterpreterError as error:
        expected = (
            "Forbidden function evaluation: 'open' is not among the explicitly "
            "allowed tools or defined/imported in the preceding code"
        )
        assert str(error).endswith(expected), f"unexpected InterpreterError: {error}"
        assert "Code execution failed at line 'with open('" in str(error), error
        # The import preceding the failing call proves wildcard import authorization
        # was active; only the built-in function allowlist rejected `open`.
        assert "os" in executor.state, "wildcard import authorization did not take effect"
        print(f"OBSERVED BUG: InterpreterError: {expected}")
        raise SystemExit(1)

    raise AssertionError("BUG NOT OBSERVED: open() unexpectedly ran with only wildcard import authorization")


if __name__ == "__main__":
    main()
