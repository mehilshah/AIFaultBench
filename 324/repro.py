from __future__ import annotations

import os
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
if str(CODEBASE) not in sys.path:
    sys.path.insert(0, str(CODEBASE))

import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
from gymnasium import spaces
from tensordict.nn import TensorDictModule

from torchrl.collectors import MultiSyncCollector
from torchrl.envs.libs.gym import GymWrapper


class SleepEnv(gym.Env):
    def __init__(self, sleep_time: float = 1.1):
        super().__init__()
        self.sleep_time = sleep_time
        self.observation_space = spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(1,),
            dtype=np.float32,
        )
        self.action_space = spaces.Box(
            low=-1.0,
            high=1.0,
            shape=(1,),
            dtype=np.float32,
        )

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        return np.zeros((1,), dtype=np.float32), {}

    def step(self, action):
        time.sleep(self.sleep_time)
        return np.zeros((1,), dtype=np.float32), 0.0, False, False, {}


class ZeroPolicy(nn.Module):
    def forward(self, observation):
        return torch.zeros(
            (*observation.shape[:-1], 1),
            dtype=observation.dtype,
            device=observation.device,
        )


def make_env() -> GymWrapper:
    return GymWrapper(SleepEnv(sleep_time=1.1))


def run_once(preemptive_threshold: float, num_workers: int = 16) -> float:
    policy = TensorDictModule(
        ZeroPolicy(),
        in_keys=["observation"],
        out_keys=["action"],
    )

    collector = MultiSyncCollector(
        create_env_fn=[make_env] * num_workers,
        policy=policy,
        frames_per_batch=num_workers,
        total_frames=num_workers,
        preemptive_threshold=preemptive_threshold,
        device="cpu",
        storing_device="cpu",
    )

    t0 = time.perf_counter()
    try:
        next(iter(collector))
    finally:
        collector.shutdown()
    return time.perf_counter() - t0


def main() -> int:
    # Multiprocessing uses spawn under this code path; be explicit so the
    # collector behaves consistently across machines.
    try:
        torch.multiprocessing.set_start_method("spawn", force=True)
    except RuntimeError:
        pass

    results: dict[str, float] = {}
    for threshold in (1.0, 0.99):
        elapsed = run_once(threshold)
        results[f"{threshold}"] = elapsed
        print(f"preemptive_threshold={threshold}, elapsed={elapsed:.3f}s")

    ratio = results["1.0"] / max(results["0.99"], 1e-9)
    print(f"elapsed_ratio={ratio:.2f}x")
    if results["1.0"] > 10.0 and results["0.99"] < 5.0:
        print("bug_reproduced=yes")
    else:
        print("bug_reproduced=no")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
