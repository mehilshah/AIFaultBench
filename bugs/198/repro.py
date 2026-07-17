#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
RESULT_PATH = ROOT / "reproduction.json"


def create_minimal_h5(path: Path) -> None:
    import h5py

    with h5py.File(path, "w") as model_file:
        model_file.create_dataset("payload", data=[1, 2, 3])


def run_modelscan(path: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(
        [str(CODEBASE), env.get("PYTHONPATH", "")] if env.get("PYTHONPATH") else [str(CODEBASE)]
    )
    cmd = [sys.executable, "-m", "modelscan.cli", "-p", str(path)]
    return subprocess.run(cmd, capture_output=True, text=True, env=env)


def main() -> int:
    print(f"Using codebase at: {CODEBASE}")
    with tempfile.TemporaryDirectory(prefix="modelscan-h5-repro-") as tmpdir:
        h5_path = Path(tmpdir) / "repro.h5"
        create_minimal_h5(h5_path)
        print(f"Created minimal HDF5 file at: {h5_path}")
        print(f"File size: {h5_path.stat().st_size} bytes")

        proc = run_modelscan(h5_path)

        if proc.stdout:
            print(proc.stdout, end="")
        if proc.stderr:
            print(proc.stderr, end="", file=sys.stderr)

        failed_with_expected_exception = (
            proc.returncode == 2
            and "the JSON object must be str, bytes or bytearray, not dict"
            in proc.stdout
        )

        result = {
            "reproducible": failed_with_expected_exception,
            "evidence": (
                "modelscan.cli exited with code 2 and printed "
                "'Exception: the JSON object must be str, bytes or bytearray, not dict' "
                "while scanning a valid HDF5 file with no model_config attribute."
            ),
            "steps": [
                "Create a minimal HDF5 file without a model_config attribute.",
                "Run modelscan CLI against the file with PYTHONPATH pointing at codebase/.",
                "Observe the TypeError surfaced as 'Exception: the JSON object must be str, bytes or bytearray, not dict'.",
            ],
            "blocking_reason": "" if failed_with_expected_exception else "The expected TypeError did not occur.",
            "reproduction_command": "bash run_repro.sh",
        }
        RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote result JSON to: {RESULT_PATH}")
        return 0 if failed_with_expected_exception else proc.returncode or 1


if __name__ == "__main__":
    raise SystemExit(main())
