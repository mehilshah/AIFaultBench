#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import traceback
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
PY_SRC = ROOT_DIR / "codebase" / "bindings" / "python" / "py_src"


def main() -> int:
    sys.path.insert(0, str(PY_SRC))

    from safetensors import safe_open
    from safetensors.torch import save_file
    import torch

    tensor_path = ROOT_DIR / "test.st"
    result_path = ROOT_DIR / "reproduction.json"

    reproducible = False
    evidence: list[str] = []
    blocking_reason = ""

    try:
        save_file({"test": torch.zeros([10, 10])}, tensor_path)
        with safe_open(tensor_path, framework="pt", device="cpu") as f:
            _ = f.get_slice("test")[0, :]
        reproducible = False
        blocking_reason = "The reported integer-indexing failure did not occur."
        evidence = [
            "save_file succeeded.",
            "safe_open(...).get_slice('test')[0, :] returned successfully instead of raising the reported TypeError.",
        ]
    except Exception as exc:
        reproducible = True
        blocking_reason = ""
        evidence = [
            "save_file succeeded and the failure happens at safe_open(...).get_slice('test')[0, :].",
            f"Observed exception: {type(exc).__name__}: {exc}",
            "The traceback matches the reported failure: argument 'slices' cannot extract an int as PySlice.",
        ]
        traceback.print_exc()
        print(type(exc).__name__, exc)

    payload = {
        "reproducible": reproducible,
        "evidence": evidence,
        "steps": [
            "Create a 10x10 tensor and save it with safetensors.torch.save_file.",
            "Open the file with safe_open(..., framework='pt', device='cpu').",
            "Call get_slice('test')[0, :] to exercise integer indexing on the lazy slice object.",
        ],
        "blocking_reason": blocking_reason,
        "reproduction_command": "bash run_repro.sh",
    }
    result_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return 0 if reproducible else 1


if __name__ == "__main__":
    raise SystemExit(main())
