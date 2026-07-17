#!/usr/bin/env python3
"""Minimal reproduction for SB3 issue 1900."""

from __future__ import annotations

import json
import tempfile
import traceback
import sys
from pathlib import Path

import numpy as np

ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR / "codebase"))

from stable_baselines3 import PPO
from stable_baselines3.common.envs import IdentityEnvBox


RESULT_PATH = Path("reproduction.json")


def main() -> int:
    steps = [
        "Create a PPO model on IdentityEnvBox with learning_rate=lambda _: np.sin(1.0).",
        "Save the model to a zip archive.",
        "Call PPO.load() on the saved archive.",
    ]
    reproduction_command = "bash run_repro.sh"

    result = {
        "reproducible": False,
        "evidence": "",
        "steps": steps,
        "blocking_reason": "",
        "reproduction_command": reproduction_command,
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "ppo_identity.zip"
        try:
            env = IdentityEnvBox(-10, 10)
            model = PPO("MlpPolicy", env, learning_rate=lambda _: np.sin(1.0), verbose=0, device="cpu")
            model.save(path)
            PPO.load(path, device="cpu")
        except Exception as exc:  # noqa: BLE001
            traceback.print_exc()
            message = f"{type(exc).__name__}: {exc}"
            result["evidence"] = message
            if "Weights only load failed" in message and "numpy.core.multiarray.scalar" in message:
                result["reproducible"] = True
                result["blocking_reason"] = ""
                RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
                print(json.dumps(result, indent=2))
                return 0

            result["blocking_reason"] = "The observed failure did not match the expected weights_only pickle error."
            RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
            print(json.dumps(result, indent=2))
            return 1

        result["evidence"] = "PPO.load() completed successfully; the bug did not reproduce."
        result["blocking_reason"] = "The current environment did not trigger the expected unpickling failure."
        RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
