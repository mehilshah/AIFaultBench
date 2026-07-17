#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import traceback
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
if str(CODEBASE) not in sys.path:
    sys.path.insert(0, str(CODEBASE))

import pyro  # noqa: E402
from pyro.nn import PyroModule, PyroParam  # noqa: E402
from torch.distributions import constraints  # noqa: E402


class Model(PyroModule):
    @PyroParam(constraint=constraints.positive)
    def x(self):
        return torch.tensor(1.234)

    @PyroParam(constraint=constraints.real)
    def y(self):
        return torch.tensor(0.456)

    def forward(self):
        return self.x + self.y


def main() -> int:
    torch.set_default_dtype(torch.float64)
    cases = []

    for use_module_local_params in (True, False):
        pyro.clear_param_store()
        with pyro.settings.context(module_local_params=use_module_local_params):
            model = Model()
            try:
                pyro.render_model(model)
            except Exception as exc:  # noqa: BLE001
                traceback.print_exc()
                cases.append(
                    {
                        "use_module_local_params": use_module_local_params,
                        "outcome": "exception",
                        "exception_type": type(exc).__name__,
                        "exception_message": str(exc),
                    }
                )
                print(
                    f"use_module_local_params={use_module_local_params}: "
                    f"raised {type(exc).__name__}: {exc}"
                )
            else:
                cases.append(
                    {
                        "use_module_local_params": use_module_local_params,
                        "outcome": "success",
                    }
                )
                print(
                    f"use_module_local_params={use_module_local_params}: render_model succeeded"
                )

    reproducible = any(
        case["use_module_local_params"]
        and case["outcome"] == "exception"
        and case["exception_type"] == "KeyError"
        and case["exception_message"] == "'constraint'"
        for case in cases
    )
    if not any(
        case["use_module_local_params"] and case["outcome"] == "exception" for case in cases
    ):
        print("Expected failure did not occur for module_local_params=True")

    result = {
        "reproducible": reproducible,
        "evidence": (
            "With module_local_params=True, pyro.render_model(Model()) raised "
            "KeyError: 'constraint'. With module_local_params=False, the same "
            "model rendered successfully."
            if reproducible
            else "The expected KeyError did not occur in this environment."
        ),
        "steps": [
            "Imported the local pyro code from codebase/.",
            "Rendered the PyroModule model with module_local_params=True and False.",
            "Observed KeyError: 'constraint' only when module_local_params=True.",
        ],
        "blocking_reason": "" if reproducible else "The failure did not reproduce in this environment.",
        "reproduction_command": "bash run_repro.sh",
    }

    (ROOT / "reproduction.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
