from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))

import gymnasium as gym
from gymnasium import spaces

from torchrl.envs import GymWrapper, TransformedEnv
from torchrl.envs.transforms import ActionMask
from torchrl.envs.utils import check_env_specs


class TestEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.action_space = spaces.MultiDiscrete([5, 5])
        self.observation_space = spaces.Dict(
            {
                "observation": spaces.Box(low=0, high=1, shape=(5, 5)),
                "action_mask": spaces.Box(low=0, high=1, shape=(5, 5), dtype=bool),
            }
        )

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        return self.observation_space.sample(), {}

    def step(self, action):
        return self.observation_space.sample(), 0.0, False, False, {}


def main() -> None:
    env = GymWrapper(TestEnv(), categorical_action_encoding=True)
    print("base action spec:", env.action_spec)
    check_env_specs(env)

    env_transformed = TransformedEnv(env, ActionMask())
    print("transformed action spec:", env_transformed.action_spec)
    check_env_specs(env_transformed)


if __name__ == "__main__":
    main()
