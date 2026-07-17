#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "codebase" / "examples" / "mms" / "tts" / "infer.py"
RESULT_PATH = ROOT / "reproduction.json"


def _write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_stub_env(stub_root: Path) -> None:
    _write_file(
        stub_root / "numpy.py",
        "class ndarray: pass\n",
    )
    _write_file(
        stub_root / "torch" / "__init__.py",
        "from . import nn, utils\n",
    )
    _write_file(
        stub_root / "torch" / "nn" / "__init__.py",
        "from . import functional\n",
    )
    _write_file(
        stub_root / "torch" / "nn" / "functional.py",
        "",
    )
    _write_file(
        stub_root / "torch" / "utils" / "__init__.py",
        "",
    )
    _write_file(
        stub_root / "torch" / "utils" / "data.py",
        "class DataLoader:\n    pass\n",
    )


def main() -> int:
    if not TARGET.is_file():
        raise FileNotFoundError(f"Missing target script: {TARGET}")

    with tempfile.TemporaryDirectory(prefix="bug043-stubs-") as tmp:
        stub_root = Path(tmp)
        build_stub_env(stub_root)

        env = os.environ.copy()
        env["PYTHONPATH"] = os.pathsep.join(
            [str(stub_root), str(TARGET.parent), env.get("PYTHONPATH", "")]
        ).rstrip(os.pathsep)

        cmd = [
            sys.executable,
            str(TARGET.name),
            "--model-dir",
            "dummy-model-dir",
            "--wav",
            "dummy.wav",
            "--txt",
            "Heute ist ein schoener Tag.",
        ]

        proc = subprocess.run(
            cmd,
            cwd=str(TARGET.parent),
            env=env,
            capture_output=True,
            text=True,
        )

        sys.stdout.write(proc.stdout)
        sys.stderr.write(proc.stderr)
        sys.stdout.flush()
        sys.stderr.flush()

        reproducible = "ModuleNotFoundError: No module named 'commons'" in proc.stderr
        result = {
            "reproducible": reproducible,
            "evidence": (
                "Running examples/mms/tts/infer.py with stubbed torch/numpy modules "
                "fails immediately on 'import commons'."
            ),
            "steps": [
                "Create temporary stub modules for unrelated imports so infer.py can start loading.",
                "Run codebase/examples/mms/tts/infer.py from codebase/examples/mms/tts.",
                "Observe ModuleNotFoundError: No module named 'commons'.",
            ],
            "blocking_reason": "" if reproducible else "The exact commons import failure was not observed.",
            "reproduction_command": (
                "bash run_repro.sh"
            ),
        }
        RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

        print(f"returncode: {proc.returncode}")
        print(f"reproducible: {reproducible}")
        print(f"result written to: {RESULT_PATH.name}")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
