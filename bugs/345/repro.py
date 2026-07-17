#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
VENV_DIR = ROOT_DIR / ".venv"
PYTHON_BIN = VENV_DIR / "bin" / "python"
BUILD_SCRIPT = ROOT_DIR / "codebase" / "build" / "build.py"


def run(cmd: list[str], *, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=ROOT_DIR,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> int:
    if not PYTHON_BIN.exists():
        print("missing virtualenv; run setup_env.sh first", file=sys.stderr)
        return 2

    site_packages = subprocess.check_output(
        [
            str(PYTHON_BIN),
            "-c",
            "import sysconfig; print(sysconfig.get_paths()['purelib'])",
        ],
        text=True,
    ).strip()

    env = os.environ.copy()
    env["PYTHONPATH"] = site_packages + (
        os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else ""
    )

    probe = run(
        [
            str(PYTHON_BIN),
            "-c",
            "import argparse; print(argparse.__file__)",
        ],
        env=env,
    )
    sys.stdout.write(probe.stdout)
    sys.stderr.write(probe.stderr)

    result = run([str(PYTHON_BIN), str(BUILD_SCRIPT), "--help"], env=env)
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())

