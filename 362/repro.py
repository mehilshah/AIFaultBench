#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase" / "src"))

from diffusers import FlowMatchEulerDiscreteScheduler  # noqa: E402


def main() -> None:
    scheduler = FlowMatchEulerDiscreteScheduler(shift=3.0)

    scheduler.set_timesteps(num_inference_steps=2, timesteps=[1000.0, 2.99401209])
    manual_timesteps = scheduler.timesteps.tolist()
    manual_sigmas = scheduler.sigmas.tolist()

    scheduler.set_timesteps(num_inference_steps=2)
    auto_timesteps = scheduler.timesteps.tolist()
    auto_sigmas = scheduler.sigmas.tolist()

    print("manual timesteps:", json.dumps(manual_timesteps))
    print("manual sigmas   :", json.dumps(manual_sigmas))
    print("auto timesteps  :", json.dumps(auto_timesteps))
    print("auto sigmas     :", json.dumps(auto_sigmas))

    assert manual_sigmas == auto_sigmas, "Expected the sigma schedule to stay unchanged"
    assert manual_timesteps != auto_timesteps, "Expected the timestep schedule to differ"


if __name__ == "__main__":
    main()
