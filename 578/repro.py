#!/usr/bin/env python3
"""Minimal reproduction harness for the reported pyro.param device issue.

The original report requires a CUDA tensor input. This script records the
observed environment and only executes the CUDA code path when CUDA is
available, so it can still produce a deterministic result on CPU-only hosts.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
RESULT_PATH = ROOT_DIR / "reproduction.json"


def main() -> int:
    import pyro
    import torch

    pyro.clear_param_store()

    evidence = []
    steps = []

    evidence.append(f"pyro={pyro.__version__}")
    evidence.append(f"torch={torch.__version__}")
    evidence.append(f"cuda_available={torch.cuda.is_available()}")
    steps.append("Imported the standardized Pyro 1.7.0 codebase under Torch 1.13.1+cpu.")
    steps.append("Checked whether CUDA is available before running the reported snippet.")

    if not torch.cuda.is_available():
        result = {
            "reproducible": False,
            "evidence": "; ".join(evidence),
            "steps": steps,
            "blocking_reason": (
                "This machine has no CUDA device, so the reported "
                "torch.rand(3).cuda() input cannot be created here."
            ),
            "reproduction_command": "bash run_repro.sh",
        }
        RESULT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0

    value = pyro.param("alpha_loc", torch.rand(3, device="cuda"))
    steps.append("Created a CUDA tensor and passed it through pyro.param().")
    evidence.append(f"param_device={value.device}")
    evidence.append(f"unconstrained_device={value.unconstrained().device}")

    reproducible = value.device.type == "cpu"
    result = {
        "reproducible": reproducible,
        "evidence": "; ".join(evidence),
        "steps": steps,
        "blocking_reason": None if reproducible else "The CUDA path returned the expected device on this machine.",
        "reproduction_command": "bash run_repro.sh",
    }
    RESULT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not reproducible else 1


if __name__ == "__main__":
    raise SystemExit(main())
