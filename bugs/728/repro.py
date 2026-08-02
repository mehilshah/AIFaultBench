#!/usr/bin/env python3
"""Offline assertion for Semantic Kernel issue #13316."""

import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
VENV = ROOT / ".venv"
PROJECT = VENV / "repro-project" / "Repro.csproj"
DOTNET = VENV / "dotnet" / "dotnet"


def main() -> int:
    if not PROJECT.is_file() or not DOTNET.is_file():
        print("REPRODUCTION SETUP ERROR: run setup_env.sh first", file=sys.stderr)
        return 2

    environment = os.environ.copy()
    environment.update(
        {
            "DOTNET_CLI_HOME": str(VENV / "dotnet-home"),
            "DOTNET_CLI_TELEMETRY_OPTOUT": "1",
            "DOTNET_SKIP_FIRST_TIME_EXPERIENCE": "1",
            "NUGET_PACKAGES": str(VENV / "nuget"),
        }
    )
    completed = subprocess.run(
        [str(DOTNET), "build", str(PROJECT), "--no-restore", "--verbosity", "minimal"],
        cwd=ROOT,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    output = completed.stdout
    expected = (
        "warning MSB3277: Found conflicts between different versions of \"Microsoft.Bcl.AsyncInterfaces\"",
        "Microsoft.Bcl.AsyncInterfaces, Version=9.0.0.8",
        "Microsoft.Bcl.AsyncInterfaces, Version=9.0.0.9",
    )
    if completed.returncode != 0:
        print(f"REPRODUCTION SETUP ERROR: dotnet build exited {completed.returncode}", file=sys.stderr)
        print(output, file=sys.stderr, end="")
        return 2
    if all(marker in output for marker in expected):
        lines = output.splitlines()
        print(next(line for line in lines if expected[0] in line))
        print(next(line for line in lines if expected[1] in line and expected[2] in line))
        print("OBSERVED BUG: MSB3277 Microsoft.Bcl.AsyncInterfaces assembly conflict")
        print("Conflict versions: 9.0.0.8 vs 9.0.0.9")
        return 1

    print("BUG NOT OBSERVED: expected Microsoft.Bcl.AsyncInterfaces MSB3277 conflict was absent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
