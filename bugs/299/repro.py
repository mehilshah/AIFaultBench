#!/usr/bin/env python3
from __future__ import annotations

import json
import platform
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
RESULT_PATH = ROOT / "reproduction.json"


def run(cmd: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    print(f"$ {' '.join(cmd)}")
    return subprocess.run(
        cmd,
        cwd=str(cwd or ROOT),
        text=True,
        capture_output=True,
        check=False,
    )


def emit_result(*, reproducible: bool, evidence: str, steps: list[str], blocking_reason: str, reproduction_command: str) -> None:
    payload = {
        "reproducible": reproducible,
        "evidence": evidence,
        "steps": steps,
        "blocking_reason": blocking_reason,
        "reproduction_command": reproduction_command,
    }
    RESULT_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def main() -> int:
    print("Environment")
    print(f"  python: {sys.version.split()[0]}")
    print(f"  platform: {platform.platform()}")
    print(f"  machine: {platform.machine()}")
    print(f"  processor: {platform.processor() or 'unknown'}")
    print(f"  executable: {sys.executable}")

    if not CODEBASE.exists():
        emit_result(
            reproducible=False,
            evidence="The local `codebase/` directory is missing, so the repro cannot be executed.",
            steps=["Inspect environment", "Attempt local package install"],
            blocking_reason="Missing local Transformers checkout.",
            reproduction_command="bash run_repro.sh",
        )
        return 2

    pip = [sys.executable, "-m", "pip"]
    steps: list[str] = []

    step1 = run(
        [
            *pip,
            "install",
            "--no-cache-dir",
            "--no-build-isolation",
            "--no-deps",
            "--ignore-installed",
            str(CODEBASE),
        ]
    )
    steps.append("Installed local Transformers tree without dependencies.")
    print(step1.stdout, end="")
    print(step1.stderr, end="", file=sys.stderr)
    if step1.returncode != 0:
        emit_result(
            reproducible=False,
            evidence="Installing the local Transformers tree failed before reaching the tokenizers/esaxx-rs build path.",
            steps=steps,
            blocking_reason="Local package install failed in this environment.",
            reproduction_command="bash run_repro.sh",
        )
        return step1.returncode

    step2 = run([*pip, "install", "--no-cache-dir", "--ignore-installed", "tokenizers==0.23.0"])
    print(step2.stdout, end="")
    print(step2.stderr, end="", file=sys.stderr)
    if step2.returncode != 0:
        if "No matching distribution found" in step2.stderr:
            steps.append("tokenizers==0.23.0 was unavailable on this package index, so the Linux wheel fallback was tried instead.")
            fallback = run([*pip, "install", "--no-cache-dir", "--ignore-installed", "tokenizers==0.23.1"])
            print(fallback.stdout, end="")
            print(fallback.stderr, end="", file=sys.stderr)
            if fallback.returncode != 0:
                emit_result(
                    reproducible=False,
                    evidence="Tokenizers could not be installed from the package index here, but the local Transformers install still succeeded.",
                    steps=steps,
                    blocking_reason="No tokenizers distribution was installable in this environment.",
                    reproduction_command="bash run_repro.sh",
                )
                return fallback.returncode
            steps.append("Installed tokenizers==0.23.1 from the Linux wheel path.")
        else:
            emit_result(
                reproducible=False,
                evidence="Tokenizers installation failed for a host-specific reason unrelated to the reported Android build failure.",
                steps=steps,
                blocking_reason="Tokenizers installation failed in this environment.",
                reproduction_command="bash run_repro.sh",
            )
            return step2.returncode
    else:
        steps.append("Installed tokenizers==0.23.0 from the Linux wheel path.")

    step3 = run(
        [
            sys.executable,
            "-c",
            (
                "from importlib import metadata; "
                "print(metadata.version('transformers')); "
                "print(metadata.version('tokenizers'))"
            ),
        ]
    )
    steps.append("Verified installed package metadata without importing the library.")
    print(step3.stdout, end="")
    print(step3.stderr, end="", file=sys.stderr)
    if step3.returncode != 0:
        emit_result(
            reproducible=False,
            evidence="The package install completed, but metadata verification failed before any Android-specific compile error could occur.",
            steps=steps,
            blocking_reason="Metadata verification failed after a successful install.",
            reproduction_command="bash run_repro.sh",
        )
        return step3.returncode

    print("Result: not reproducible in this environment.")
    print("Reason: this host is Linux x86_64 and does not have the Android/Termux clang++ toolchain used in the report.")

    emit_result(
        reproducible=False,
        evidence=(
            "Local installation succeeded and tokenizers was resolved through the normal Linux wheel path; "
            "the reported `pthread_cond_clockwait` / `esaxx-rs` Android build failure did not occur."
        ),
        steps=steps,
        blocking_reason=(
            "The reported failure depends on the Android/Termux aarch64 build stack with clang++ and libc++ headers; "
            "this folder is running on Linux x86_64 without that toolchain."
        ),
        reproduction_command="bash run_repro.sh",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
