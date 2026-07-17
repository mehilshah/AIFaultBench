from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")

import gymnasium as gym

import stable_baselines3 as sb3
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv


def make_env() -> gym.Env:
    return gym.make("CartPole-v1")


def main() -> int:
    num_envs = 1
    n_steps = 2
    total_timesteps = 1

    env = DummyVecEnv([make_env for _ in range(num_envs)])
    model = PPO("MlpPolicy", env, n_steps=n_steps, batch_size=2, n_epochs=1, seed=0, verbose=0, device="cpu")
    model.learn(total_timesteps=total_timesteps)

    print(f"stable_baselines3_version={sb3.__version__}")
    print(f"num_envs={num_envs}")
    print(f"n_steps={n_steps}")
    print(f"total_timesteps={total_timesteps}")
    print(f"final_num_timesteps={model.num_timesteps}")

    if model.num_timesteps > total_timesteps:
        print("BUG_REPRODUCED: learn() overshot total_timesteps")
        return 0

    print("BUG_NOT_REPRODUCED: num_timesteps did not exceed total_timesteps")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
