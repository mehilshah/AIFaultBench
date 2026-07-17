#!/usr/bin/env python3
"""Minimal reproduction for the MPS float64 crash described in bug 429."""

from __future__ import annotations

import os
import platform
import sys
import traceback
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"

if str(CODEBASE) not in sys.path:
    sys.path.insert(0, str(CODEBASE))


def main() -> int:
    import torch

    print(f"platform={platform.system()} machine={platform.machine()}")
    print(f"torch={torch.__version__}")
    print(f"mps_available={getattr(torch.backends, 'mps', None) and torch.backends.mps.is_available()}")

    if platform.system() != "Darwin":
        print(
            "BLOCKED: this bug is MPS-specific and needs macOS with Apple Silicon "
            "or another machine where torch.backends.mps.is_available() is true."
        )
        return 2

    if not torch.backends.mps.is_available():
        print("BLOCKED: MPS backend is unavailable on this host.")
        return 2

    from torchrl.collectors import SyncDataCollector
    from torchrl.envs import GymEnv

    env = GymEnv("HalfCheetah-v4")
    print(f"env_output_spec_device={env.output_spec.device}")

    try:
        _collector = SyncDataCollector(
            env,
            policy=env.rand_action,
            frames_per_batch=10,
            total_frames=10,
            device="mps",
            env_device="mps",
        )
    except Exception as exc:  # noqa: BLE001
        print(f"EXCEPTION: {type(exc).__name__}: {exc}")
        traceback.print_exc()
        return 1

    print("Collector constructed successfully; the reported crash did not occur.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
