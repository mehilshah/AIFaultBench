#!/usr/bin/env python3
"""Offline reproduction of SWE-agent issue #1179 at the pinned checkout.

The target image used Python 3.5.  ``tree-sitter==0.21.3`` requires Python
3.8+, so its pip invocation fails.  This script supplies a local fake pip
that deterministically represents that compatibility failure, then executes
the exact bundle-install shell sequence used by ToolHandler._install_commands.
"""

from __future__ import annotations

import os
import shlex
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PINNED_COMMIT = "b21a0614da892c758ca15ab91f759caa147f09e4"
TOOL_DIR = ROOT / "codebase" / "tools" / "edit_anthropic"


def main() -> None:
    installer = TOOL_DIR / "install.sh"
    if not installer.is_file():
        raise AssertionError(f"missing pinned installer: {installer}")
    checkout = subprocess.run(
        ["git", "-C", str(ROOT / "codebase"), "rev-parse", "HEAD"],
        text=True,
        capture_output=True,
        check=True,
    ).stdout.strip()
    if checkout != PINNED_COMMIT:
        raise AssertionError(f"expected pinned checkout {PINNED_COMMIT}, got {checkout}")

    with tempfile.TemporaryDirectory(prefix="swe-agent-1179-") as tmp:
        tmp_path = Path(tmp)
        fake_bin = tmp_path / "bin"
        fake_bin.mkdir()
        fake_pip = fake_bin / "pip"
        fake_pip.write_text(
            "#!/bin/sh\n"
            "echo \"ERROR: Could not find a version that satisfies requirement $2 "
            "(requires Python >=3.8; simulated Python 3.5.6)\" >&2\n"
            "exit 1\n",
            encoding="utf-8",
        )
        fake_pip.chmod(fake_pip.stat().st_mode | stat.S_IXUSR)

        # ToolHandler uploads bundles into the target before this command.  Use
        # a temporary uploaded copy so the reproduction never changes codebase.
        target_tool_dir = tmp_path / "root" / "tools" / "edit_anthropic"
        target_tool_dir.parent.mkdir(parents=True)
        shutil.copytree(TOOL_DIR, target_tool_dir)

        # This is the relevant command built in ToolHandler._install_commands.
        command = " && ".join(
            [
                "export PATH=/root/tools/edit_anthropic/bin:$PATH",
                f"chmod +x {shlex.quote(str(target_tool_dir / 'bin'))}/*",
                f"cd {shlex.quote(str(target_tool_dir))} && source install.sh",
                f"chmod +x {shlex.quote(str(target_tool_dir / 'bin'))}/*",
            ]
        )
        env = os.environ.copy()
        env["PATH"] = f"{fake_bin}{os.pathsep}{env['PATH']}"
        result = subprocess.run(
            ["bash", "-c", command],
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )

    expected = "tree-sitter==0.21.3 (requires Python >=3.8; simulated Python 3.5.6)"
    if result.returncode == 0:
        raise AssertionError("expected the unguarded pinned installer to fail")
    if expected not in result.stderr:
        raise AssertionError(f"missing simulated Python-3.5 pip error: {result.stderr!r}")

    print(
        "OBSERVED BUG: pinned edit_anthropic install.sh propagates the "
        f"tree-sitter Python-3.5 pip failure (exit {result.returncode})."
    )
    print(f"PINNED COMMIT: {PINNED_COMMIT}")
    sys.stderr.write(result.stderr)
    raise SystemExit(1)


if __name__ == "__main__":
    main()
