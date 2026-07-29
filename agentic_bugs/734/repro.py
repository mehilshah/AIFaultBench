#!/usr/bin/env python3
"""Offline reproduction for mem0 issue #5911."""

from mem0.memory.main import Memory


def main() -> None:
    try:
        # Calling the method on an uninitialised instance is sufficient: Python
        # rejects the missing public keyword before Memory.add's body can run.
        Memory.add(
            object(),
            [{"role": "user", "content": "Always verify inputs before processing."}],
            agent_id="agent-1",
            memory_type="procedural_memory",
            llm=object(),
        )
    except TypeError as error:
        expected = "Memory.add() got an unexpected keyword argument 'llm'"
        assert str(error) == expected, repr(error)
        print(f"BUG REPRODUCED: {error}")
        raise SystemExit(1)

    raise AssertionError("Memory.add unexpectedly accepted the llm keyword")


if __name__ == "__main__":
    main()
