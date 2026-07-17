#!/usr/bin/env python3
"""Negative reproduction for Lightning issue #21692.

This script checks whether the local checkout contains the malicious import-time
runtime chain described in the upstream report:

- `lightning/_runtime/start.py`
- `lightning/_runtime/router_runtime.js`
- a daemon thread spawned from `lightning/__init__.py`

The checked-in source tree in this folder does not contain that payload, so the
script reports a non-reproducible result for this workspace.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    lightning_pkg = CODEBASE / "src" / "lightning"
    local_version = (CODEBASE / "src" / "version.info").read_text(encoding="utf-8").splitlines()[0].strip()

    findings: list[str] = []

    runtime_dir = lightning_pkg / "_runtime"
    if runtime_dir.exists():
        findings.append(f"unexpected runtime directory present: {runtime_dir}")

    start_py = runtime_dir / "start.py"
    if start_py.exists():
        findings.append(f"unexpected runtime downloader present: {start_py}")

    router_js = runtime_dir / "router_runtime.js"
    if router_js.exists():
        findings.append(f"unexpected obfuscated payload present: {router_js}")

    init_py = lightning_pkg / "__init__.py"
    init_src = _read_text(init_py)
    suspicious_markers = ["threading.Thread", "subprocess.Popen", "DEVNULL", "_runtime", "router_runtime"]
    for marker in suspicious_markers:
        if marker in init_src:
            findings.append(f"found suspicious import-time marker {marker!r} in {init_py}")

    report = {
        "local_version": local_version,
        "runtime_dir_exists": runtime_dir.exists(),
        "start_py_exists": start_py.exists(),
        "router_js_exists": router_js.exists(),
        "findings": findings,
    }
    print(json.dumps(report, indent=2, sort_keys=True))

    if findings:
        print("Result: reproducible")
        return 1

    print("Result: not reproducible in this checkout")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
