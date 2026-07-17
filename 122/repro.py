#!/usr/bin/env python3
"""Minimal reproduction for SB3 issue 1928.

This script intentionally exercises PPO.save()/load() with policy_kwargs
containing net_arch=None. The vulnerable load path calls len(None) and raises
TypeError in the bundled codebase.
"""

from __future__ import annotations

import pathlib
import sys
import traceback

import gymnasium as gym

from stable_baselines3 import PPO


def main() -> int:
    model_path = pathlib.Path("ppo_cartpole_net_arch_none")
    print("creating CartPole-v1 environment")
    env = gym.make("CartPole-v1")

    print("building PPO with policy_kwargs={'net_arch': None}")
    model = PPO("MlpPolicy", env, policy_kwargs=dict(net_arch=None), verbose=0)

    print(f"saving model to {model_path}")
    model.save(model_path)

    print("loading model")
    try:
        PPO.load(model_path)
    except TypeError as exc:
        print(f"reproduced TypeError: {exc}")
        traceback.print_exc()
        return 0

    print("load succeeded unexpectedly; bug not reproduced")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
