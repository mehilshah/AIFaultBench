#!/usr/bin/env python3
"""Reproduce SWE-agent #1048 without starting a model or remote service."""

from pathlib import PureWindowsPath

import sweagent.tools.tools as tools_module


class PosixContainer:
    """A fake container runtime that contains the state file at its POSIX path."""

    def __init__(self) -> None:
        self.requested_path = ""

    def read_file(self, path, **_kwargs: object) -> str:
        self.requested_path = str(path)
        if self.requested_path != "/root/state.json":
            raise FileNotFoundError(2, "No such file or directory", self.requested_path)
        return '{"cwd": "/root"}'


def main() -> None:
    # On Windows, pathlib.Path('/root/state.json') serializes this way.  Substituting
    # PureWindowsPath lets this Linux host execute the same client-side code path.
    tools_module.Path = PureWindowsPath
    handler = tools_module.ToolHandler(tools_module.ToolConfig())
    container = PosixContainer()

    state = handler._get_state(container)

    if container.requested_path == r"\root\state.json" and state == {}:
        print(f"OBSERVED BUG: state read used {container.requested_path!r} and returned {state}")
        raise AssertionError("Windows path was sent to the POSIX container")

    assert container.requested_path == "/root/state.json", container.requested_path
    assert state == {"cwd": "/root"}, state
    print("BUG NOT OBSERVED: state was read using the POSIX path")


if __name__ == "__main__":
    main()
