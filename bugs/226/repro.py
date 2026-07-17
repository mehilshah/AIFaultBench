#!/usr/bin/env python3
import pathlib
import shutil
import subprocess
import sys


def main() -> int:
    root = pathlib.Path(__file__).resolve().parent
    requirements = root / "requirements.txt"
    venv_python = root / ".venv" / "bin" / "python"
    if not venv_python.exists():
        print("missing virtual environment: .venv/bin/python", file=sys.stderr)
        return 2

    uv = shutil.which("uv")
    if uv is None:
        print("missing uv on PATH", file=sys.stderr)
        return 2

    cmd = [uv, "pip", "install", "--python", str(venv_python), "-r", str(requirements)]

    proc = subprocess.run(cmd, text=True, capture_output=True)
    if proc.stdout:
        print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, end="", file=sys.stderr)
    print(f"repro_exit_code={proc.returncode}")
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
