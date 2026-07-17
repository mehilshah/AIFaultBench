#!/usr/bin/env python3
"""Minimal reproducer for the TP + CPU KV Offloading + CUDA graph hang."""

from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path


def _cuda_summary() -> tuple[int, list[str]]:
    try:
        listing = subprocess.run(
            ["nvidia-smi", "-L"],
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception as exc:  # pragma: no cover - environment-specific
        return -1, [f"nvidia-smi check failed: {exc!r}"]

    gpu_lines = [
        line.strip()
        for line in listing.stdout.splitlines()
        if line.strip().startswith("GPU ")
    ]
    lines = [f"nvidia_smi_gpu_count={len(gpu_lines)}"]
    lines.extend(gpu_lines)
    return len(gpu_lines), lines


def _build_serve_cmd(model: str, tp_size: int, cpu_bytes: int) -> list[str]:
    kv_transfer_config = {
        "kv_connector": "OffloadingConnector",
        "kv_role": "kv_both",
        "kv_connector_extra_config": {
            "spec_name": "CPUOffloadingSpec",
            "cpu_bytes_to_use": cpu_bytes,
            "eviction_policy": "lru",
        },
    }
    return [
        sys.executable,
        "-m",
        "vllm.entrypoints.cli.main",
        "serve",
        model,
        "--tensor-parallel-size",
        str(tp_size),
        "--kv-transfer-config",
        json.dumps(kv_transfer_config),
        "--enable-prefix-caching",
        "--no-disable-hybrid-kv-cache-manager",
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="openai/gpt-oss-120b")
    parser.add_argument("--tp-size", type=int, default=2)
    parser.add_argument("--cpu-bytes", type=int, default=26_843_545_600)
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    args = parser.parse_args()

    print("Bug signature: TP + CPU KV Offloading + CUDA Graph capture hang")
    print(f"repo_root={Path(__file__).resolve().parent}")
    print(f"model={args.model}")
    print(f"tp_size={args.tp_size}")
    print(f"cpu_bytes={args.cpu_bytes}")

    cuda_count, summary_lines = _cuda_summary()
    for line in summary_lines:
        print(line)

    if cuda_count < 0:
        print("BLOCKER: torch is not available, so the repro cannot start.", file=sys.stderr)
        return 2

    if cuda_count < args.tp_size:
        print(
            "BLOCKER: the bug needs at least "
            f"{args.tp_size} CUDA devices, but this machine exposes {cuda_count}.",
            file=sys.stderr,
        )
        return 2

    cmd = _build_serve_cmd(args.model, args.tp_size, args.cpu_bytes)
    print("launch_command=" + " ".join(shlex.quote(part) for part in cmd))
    print(f"timeout_seconds={args.timeout_seconds}")
    completed = subprocess.run(cmd, check=False, timeout=args.timeout_seconds)
    print(f"serve_exit_code={completed.returncode}")
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
