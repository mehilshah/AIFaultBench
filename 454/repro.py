#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def run(cmd: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def gpu_summary() -> dict[str, str]:
    code, stdout, stderr = run(
        [
            "nvidia-smi",
            "--query-gpu=name,compute_cap,driver_version",
            "--format=csv,noheader",
        ]
    )
    if code != 0:
        return {"error": stderr or "nvidia-smi failed"}
    line = stdout.splitlines()[0] if stdout else ""
    parts = [part.strip() for part in line.split(",")]
    if len(parts) < 3:
        return {"error": f"unexpected nvidia-smi output: {stdout!r}"}
    return {"name": parts[0], "compute_cap": parts[1], "driver_version": parts[2]}


def main() -> int:
    print("Bug 454 repro probe")
    print(f"repo_root={ROOT}")
    print(f"python={sys.version.split()[0]}")
    print(f"fill_value={os.environ.get('FILL_VALUE', '0xff')}")

    gpu = gpu_summary()
    print(f"gpu={json.dumps(gpu, sort_keys=True)}")

    if "error" in gpu:
        print("BLOCKER: cannot query GPU details.")
        print(gpu["error"])
        return 2

    if gpu["compute_cap"] != "9.0":
        print(
            "BLOCKER: the reported Triton MXFP4 corruption is Hopper-specific "
            "(sm90)."
        )
        print(f"Detected GPU {gpu['name']} with compute capability {gpu['compute_cap']}.")
        return 3

    try:
        import torch  # type: ignore
    except Exception as exc:  # pragma: no cover - environment probe
        print("BLOCKER: failed to import torch.")
        print(repr(exc))
        return 4

    try:
        import triton_kernels  # type: ignore
    except Exception as exc:  # pragma: no cover - environment probe
        print("BLOCKER: triton_kernels is unavailable.")
        print(repr(exc))
        return 5

    print(f"torch={torch.__version__}")
    print(f"triton_kernels={getattr(triton_kernels, '__file__', 'n/a')}")

    if not torch.cuda.is_available():
        print("BLOCKER: CUDA is not available to torch.")
        return 6

    if torch.cuda.get_device_capability(0) != (9, 0):
        print(
            "BLOCKER: this kernel repro is only expected to show corruption on "
            "Hopper (sm90)."
        )
        return 7

    print(
        "The local environment now satisfies the basic prerequisites, but the "
        "repository state in this folder does not ship the full upstream Triton "
        "kernel package needed to exercise the OOB scale-load path."
    )
    return 8


if __name__ == "__main__":
    raise SystemExit(main())
