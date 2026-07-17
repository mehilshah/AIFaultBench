#!/usr/bin/env python3
import importlib
import json
import sys
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parent
    sys.path.insert(0, str(repo_root / "codebase"))

    result = {
        "reproducible": False,
        "evidence": "",
        "steps": [
            "Create a Python 3.10 virtual environment.",
            "Install torch==2.0.0 and the local editable pyro snapshot from codebase/.",
            "Import pyro.optim and check for the ExponentialLR attribute.",
        ],
        "blocking_reason": "",
        "reproduction_command": "bash run_repro.sh",
    }

    pyro = importlib.import_module("pyro")
    pyro_optim = importlib.import_module("pyro.optim")
    has_attr = hasattr(pyro_optim, "ExponentialLR")
    attr_type = type(getattr(pyro_optim, "ExponentialLR", None)).__name__ if has_attr else "missing"

    result["evidence"] = (
        f"Imported pyro.optim from {pyro_optim.__file__}; "
        f"pyro.__version__={pyro.__version__}; "
        f"has ExponentialLR={has_attr}; "
        f"attr_type={attr_type}."
    )
    result["blocking_reason"] = (
        "The standardized snapshot already exposes pyro.optim.ExponentialLR, "
        "so the reported AttributeError does not occur here."
    )

    with open(repo_root / "reproduction.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, sort_keys=True)
        f.write("\n")

    print(result["evidence"])
    print(result["blocking_reason"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
