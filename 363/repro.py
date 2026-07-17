#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent
    python = root / ".venv" / "bin" / "python"
    if not python.exists():
        print(f"missing virtualenv interpreter: {python}", file=sys.stderr)
        return 2

    env = os.environ.copy()
    env.setdefault("PIP_DISABLE_PIP_VERSION_CHECK", "1")
    env.setdefault("PIP_NO_INPUT", "1")

    cmd = [
        str(python),
        "-m",
        "pip",
        "install",
        "--dry-run",
        "--isolated",
        "whisperx==3.4.3",
    ]

    print("running:", " ".join(cmd))
    proc = subprocess.run(cmd, cwd=root, env=env)
    print(f"exit_code={proc.returncode}")
    if proc.returncode == 0:
        print("resolver_status=success")
    else:
        print("resolver_status=failure")
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())

