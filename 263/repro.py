#!/usr/bin/env python3
from __future__ import annotations

import json

import numpy as np
import gymnasium as gym
from gymnasium import spaces
from gymnasium.wrappers import FrameStack

from tianshou.env import DummyVectorEnv, ShmemVectorEnv


class DummyEnv(gym.Env):
    def __init__(self) -> None:
        self.observation_space = spaces.Box(0, 9, shape=(1,), dtype=np.int32)
        self.action_space = spaces.Discrete(2)
        self.t = 0

    def reset(self, *, seed=None, options=None):
        self.t = 0
        return np.array([0], dtype=np.int32), {}

    def step(self, action):
        self.t += 1
        return (
            np.array([self.t], dtype=np.int32),
            float(action),
            self.t >= 5,
            False,
            {"timestep": self.t},
        )


def format_obs(obs: np.ndarray) -> str:
    return np.array2string(obs, separator=", ")


def run(env_cls, name: str) -> list[np.ndarray]:
    print(f"=== {name} ===")
    envs = env_cls([lambda: FrameStack(DummyEnv(), 3) for _ in range(2)])
    obs, _ = envs.reset()
    print(f"reset_type={type(obs).__name__}")
    print(f"reset_obs={format_obs(obs)}")

    step_obs: list[np.ndarray] = []
    for i in range(3):
        obs, rew, done, _, info = envs.step([0, 1])
        step_obs.append(obs.copy())
        print(f"step_{i}_type={type(obs).__name__}")
        print(f"step_{i}_obs={format_obs(obs)}")
        print(f"step_{i}_rew={rew.tolist()} done={done.tolist()} info={info.tolist()}")
    envs.close()
    return step_obs


def main() -> int:
    print(json.dumps({"numpy": np.__version__, "gymnasium": gym.__version__}))

    dummy_steps = run(DummyVectorEnv, "DummyVectorEnv")
    shmem_steps = run(ShmemVectorEnv, "ShmemVectorEnv")

    if np.array_equal(dummy_steps[0], shmem_steps[0]):
        raise AssertionError("Expected ShmemVectorEnv to diverge from DummyVectorEnv")

    if not np.array_equal(shmem_steps[0], np.zeros_like(shmem_steps[0])):
        raise AssertionError("Expected stale shared-memory frames to remain at the reset value")

    print("BUG_REPRODUCED: ShmemVectorEnv keeps returning the reset frame stack after step()")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
