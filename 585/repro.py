#!/usr/bin/env python3

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
VENV_ACCELERATE = ROOT / ".venv" / "bin" / "accelerate"


def main() -> int:
    if not VENV_ACCELERATE.is_file():
        print("Missing .venv/bin/accelerate. Run ./setup_env.sh first.", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory(prefix="accelerate-repro-") as tmpdir:
        dummy_script = Path(tmpdir) / "dummy_train.py"
        dummy_script.write_text('print("dummy training script should not execute")\n', encoding="utf-8")

        env = os.environ.copy()
        pythonpath = env.get("PYTHONPATH")
        env["PYTHONPATH"] = str(ROOT) if not pythonpath else os.pathsep.join([str(ROOT), pythonpath])
        env.setdefault("ACCELERATE_DISABLE_RICH", "1")

        cmd = [
            str(VENV_ACCELERATE),
            "launch",
            "--multi_gpu",
            "--num_processes",
            "2",
            str(dummy_script),
        ]

        proc = subprocess.run(cmd, env=env)
        print(f"accelerate return code: {proc.returncode}")

        if proc.returncode == 0:
            print("BUG reproduced: the launcher swallowed the injected failure and returned 0.")
            return 0

        print("Unexpected: the launcher propagated the failure.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
