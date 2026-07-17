#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
TARGET = "lightning==2.6.3"


def sha256_b64(path: Path) -> str:
    digest = hashlib.sha256(path.read_bytes()).digest()
    return base64.urlsafe_b64encode(digest).decode().rstrip("=")


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
        check=False,
    )


def print_section(title: str) -> None:
    print(f"\n== {title} ==")


def inspect_source_tree() -> list[str]:
    findings: list[str] = []
    runtime_dirs = list(CODEBASE.glob("src/lightning/**/_runtime"))
    if runtime_dirs:
        findings.append("unexpected _runtime directory in source checkout")
    else:
        findings.append("source checkout has no src/lightning/**/_runtime directory")

    init_py = CODEBASE / "src/lightning/__init__.py"
    if init_py.exists():
        text = init_py.read_text(encoding="utf-8")
        if "_run_runtime" in text or "router_runtime" in text:
            findings.append("source checkout contains import-time runtime launcher")
        else:
            findings.append("src/lightning/__init__.py is clean")
    return findings


def download_wheel(tmpdir: Path) -> tuple[bool, str, Path | None]:
    wheel_dir = tmpdir / "wheel"
    wheel_dir.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, "-m", "pip", "download", TARGET, "--no-deps", "-d", str(wheel_dir)]
    proc = run(cmd, cwd=ROOT)
    output = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0:
        return False, output.strip(), None
    wheels = sorted(wheel_dir.glob("*.whl"))
    if not wheels:
        return False, "pip reported success but no wheel was downloaded", None
    return True, output.strip(), wheels[0]


def inspect_wheel(wheel_path: Path) -> list[str]:
    results: list[str] = []
    with zipfile.ZipFile(wheel_path) as zf:
        names = set(zf.namelist())
        runtime_files = [
            "lightning/_runtime/start.py",
            "lightning/_runtime/router_runtime.js",
        ]
        for rel in runtime_files:
            results.append(f"{rel}: {'present' if rel in names else 'missing'}")

        if "lightning/_runtime/start.py" in names:
            data = zf.read("lightning/_runtime/start.py")
            results.append(f"start.py sha256_b64={base64.urlsafe_b64encode(hashlib.sha256(data).digest()).decode().rstrip('=')}")
        if "lightning/_runtime/router_runtime.js" in names:
            data = zf.read("lightning/_runtime/router_runtime.js")
            results.append(f"router_runtime.js sha256_hex={hashlib.sha256(data).hexdigest()}")
    return results


def main() -> int:
    print_section("workspace")
    print(f"root={ROOT}")
    print(f"codebase_present={CODEBASE.exists()}")
    print(f"target={TARGET}")

    print_section("source tree")
    for item in inspect_source_tree():
        print(item)

    print_section("wheel download")
    with tempfile.TemporaryDirectory(prefix="bug392-", dir=str(ROOT)) as tmp:
        ok, output, wheel = download_wheel(Path(tmp))
        if not ok:
            print(output)
            print("BLOCKER: exact wheel is unavailable from the live index in this workspace")
            return 2

        print(output)
        print(f"downloaded={wheel}")
        print_section("wheel inspection")
        for item in inspect_wheel(wheel):
            print(item)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
