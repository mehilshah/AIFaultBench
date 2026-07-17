#!/usr/bin/env python3
"""Repro harness for vLLM issue #47037.

The reported failure needs a Hopper-class CUDA machine with FlashInfer or
Triton attention and an FP8 KV cache. In this workspace we only have a partial
Python stack, so the script performs a preflight check first and exits with a
clear blocker when the runtime is not capable of running the real repro.

When the environment is capable, it runs the issue reporter's exact server and
LM-Eval commands against `poolside/Laguna-XS.2-FP8`.
"""

from __future__ import annotations

import argparse
import os
import shlex
import subprocess
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass


SERVER_CMD = [
    "uv",
    "run",
    "--no-project",
    "--python",
    "3.12",
    "--with",
    "vllm==0.23.0",
    "vllm",
    "serve",
    "poolside/Laguna-XS.2-FP8",
    "--served-model-name",
    "poolside/Laguna-XS.2-FP8",
    "--tensor-parallel-size",
    "1",
    "--trust-remote-code",
    "--kv-cache-dtype",
    "fp8",
    "--max-model-len",
    "4096",
    "--gpu-memory-utilization",
    "0.85",
    "--attention-backend",
    "FLASHINFER",
]

EVAL_CMD = [
    "uv",
    "run",
    "--no-project",
    "--python",
    "3.12",
    "--with",
    "lm-eval[api]",
    "lm_eval",
    "--model",
    "local-completions",
    "--model_args",
    "model=poolside/Laguna-XS.2-FP8,base_url=http://127.0.0.1:8000/v1/completions,num_concurrent=128",
    "--tasks",
    "gsm8k",
    "--batch_size",
    "auto",
]


@dataclass
class PreflightResult:
    ok: bool
    blocker: str | None = None


def run_cmd(cmd: list[str], *, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def print_section(title: str) -> None:
    print(f"\n== {title} ==")


def preflight() -> PreflightResult:
    print_section("Environment")
    print(f"python: {sys.executable}")
    print(f"cwd: {os.getcwd()}")

    try:
        import torch  # type: ignore
    except Exception as exc:  # pragma: no cover - local environment blocker
        return PreflightResult(
            ok=False,
            blocker=f"torch import failed: {type(exc).__name__}: {exc}",
        )

    print(f"torch: {torch.__version__}")

    if not torch.cuda.is_available():
        return PreflightResult(
            ok=False,
            blocker="CUDA is not available in this workspace.",
        )

    device_count = torch.cuda.device_count()
    print(f"cuda_device_count: {device_count}")
    if device_count < 1:
        return PreflightResult(ok=False, blocker="No CUDA devices were detected.")

    major, minor = torch.cuda.get_device_capability(0)
    print(f"cuda_capability: sm_{major}{minor}")
    if major < 9:
        return PreflightResult(
            ok=False,
            blocker="The report requires Hopper-class hardware (SM90 / H200).",
        )

    return PreflightResult(ok=True)


def wait_for_server(timeout_s: int = 900) -> str:
    deadline = time.time() + timeout_s
    url = "http://127.0.0.1:8000/v1/models"
    last_error = ""
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2) as response:
                body = response.read().decode("utf-8", errors="replace")
                return body
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            last_error = f"{type(exc).__name__}: {exc}"
            time.sleep(2)
    raise RuntimeError(f"server did not become ready: {last_error}")


def stream_process_output(proc: subprocess.Popen[str]) -> tuple[str, str]:
    stdout, stderr = proc.communicate()
    return stdout or "", stderr or ""


def run_repro() -> int:
    preflight_result = preflight()
    if not preflight_result.ok:
        print_section("Blocked")
        print(f"BLOCKED: {preflight_result.blocker}")
        print("\nExpected reproduction command:")
        print(" ".join(shlex.quote(part) for part in SERVER_CMD))
        print(" ".join(shlex.quote(part) for part in EVAL_CMD))
        return 2

    print_section("Server")
    print("Starting vLLM server...")
    server = subprocess.Popen(
        SERVER_CMD,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        ready_body = wait_for_server()
        print("Server is ready.")
        print(ready_body[:2000])

        print_section("Eval")
        eval_proc = subprocess.run(
            EVAL_CMD,
            text=True,
            capture_output=True,
            check=False,
        )
        if eval_proc.stdout:
            print(eval_proc.stdout)
        if eval_proc.stderr:
            print(eval_proc.stderr, file=sys.stderr)

        if eval_proc.returncode != 0:
            print_section("Result")
            print(f"lm_eval exited with code {eval_proc.returncode}")
            return eval_proc.returncode

        print_section("Result")
        print("lm_eval completed. Inspect the GSM8K scores above.")
        return 0
    finally:
        if server.poll() is None:
            server.terminate()
            try:
                server.wait(timeout=30)
            except subprocess.TimeoutExpired:
                server.kill()

        server_stdout, server_stderr = stream_process_output(server)
        if server_stdout:
            print_section("Server stdout")
            print(server_stdout)
        if server_stderr:
            print_section("Server stderr")
            print(server_stderr, file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--attempt",
        action="store_true",
        help="Run the full server + eval repro when the environment is capable.",
    )
    args = parser.parse_args()

    if not args.attempt:
        result = preflight()
        if result.ok:
            print("Environment looks usable. Re-run with --attempt to execute the repro.")
            return 0
        print(f"BLOCKED: {result.blocker}")
        return 2

    return run_repro()


if __name__ == "__main__":
    raise SystemExit(main())
