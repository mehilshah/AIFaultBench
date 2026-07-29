#!/usr/bin/env python3
"""Reproduce issue #2962 without starting a provider sandbox or an LLM."""

import asyncio
from pathlib import PureWindowsPath
from types import SimpleNamespace

import agents.sandbox.session.base_sandbox_session as base_module
from agents.sandbox.session.base_sandbox_session import BaseSandboxSession
from agents.sandbox.session.runtime_helpers import RuntimeHelperScript
from agents.sandbox.errors import ExecNonZeroError
from agents.sandbox.types import ExecResult


class WindowsWorkspacePolicy:
    """The Windows view of the already-normalized remote /workspace path."""

    def normalize_path(self, _path, *, for_write=False):
        assert for_write
        return PureWindowsPath("/workspace")

    def extra_path_grant_rules(self):
        return ()


class RecordingSandbox(BaseSandboxSession):
    """A no-network sandbox backend that records the SDK command it receives."""

    def __init__(self):
        self.state = SimpleNamespace(
            manifest=SimpleNamespace(root="/workspace", extra_path_grants=()),
            exposed_ports=(),
        )
        self.commands = []

    def _workspace_path_policy(self):
        return WindowsWorkspacePolicy()

    async def _exec_internal(self, *command, timeout=None):
        assert timeout is None
        self.commands.append(command)
        if command[0].startswith("\\tmp\\openai-agents\\bin\\"):
            return ExecResult(
                stdout=b"",
                stderr=b"error finding executable in Linux PATH",
                exit_code=127,
            )
        return ExecResult(stdout=b"/workspace\n", stderr=b"", exit_code=0)

    async def read(self, path, *, user=None):
        raise NotImplementedError

    async def write(self, path, data, *, user=None):
        raise NotImplementedError

    async def running(self):
        return True

    async def persist_workspace(self):
        raise NotImplementedError

    async def hydrate_workspace(self, data):
        raise NotImplementedError


async def main():
    # On Windows, the two module-level Path constructions in the buggy code become
    # PureWindowsPath values.  Rebuild the helper exactly as that import produces it.
    original_helper = base_module.RESOLVE_WORKSPACE_PATH_HELPER
    windows_helper = RuntimeHelperScript(
        name=original_helper.name,
        content=original_helper.content,
        install_path=(
            PureWindowsPath("/tmp/openai-agents/bin") / original_helper.install_path.name
        ),
        install_marker=original_helper.install_marker,
    )
    base_module.Path = PureWindowsPath
    base_module.RESOLVE_WORKSPACE_PATH_HELPER = windows_helper

    sandbox = RecordingSandbox()
    try:
        await sandbox._validate_remote_path_access("workspace", for_write=True)
    except ExecNonZeroError as error:
        assert error.exit_code == 127
    else:
        raise AssertionError("expected Linux to reject the backslash helper executable")
    helper_command = sandbox.commands[-1]
    executable = helper_command[0]

    assert executable.startswith("\\tmp\\openai-agents\\bin\\resolve-workspace-path-")
    assert "/tmp/openai-agents/bin" not in executable
    assert helper_command[1:] == ("\\workspace", "\\workspace", "1")
    print(f"OBSERVED malformed Linux helper command: {' '.join(helper_command)}")
    raise AssertionError("BUG REPRODUCED: Windows backslashes make the Linux helper unfindable")


asyncio.run(main())
