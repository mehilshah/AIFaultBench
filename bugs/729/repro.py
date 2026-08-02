#!/usr/bin/env python3
"""Check the import claimed to fail in semantic-kernel issue #13298."""

try:
    from semantic_kernel.agents import CopilotStudioAgent
except ModuleNotFoundError as exc:
    if exc.name in {"microsoft", "microsoft.agents"}:
        print(f"BUG_REPRODUCED: {type(exc).__name__}: {exc}")
        raise AssertionError("CopilotStudioAgent used the invalid microsoft.agents import path") from exc
    raise

assert CopilotStudioAgent.__name__ == "CopilotStudioAgent"
print("NOT_REPRODUCED: CopilotStudioAgent imported via microsoft_agents dependencies")
