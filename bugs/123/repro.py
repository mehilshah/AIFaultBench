from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path

import gymnasium as gym
import numpy as np
from gymnasium import spaces


ROOT_DIR = Path(__file__).resolve().parent
SB3_COMMON_DIR = ROOT_DIR / "codebase" / "stable_baselines3" / "common"


def load_source_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def install_sb3_stubs() -> None:
    # Prevent importing stable_baselines3/__init__.py, which pulls in torch.
    sb3_pkg = types.ModuleType("stable_baselines3")
    sb3_pkg.__path__ = [str(ROOT_DIR / "codebase" / "stable_baselines3")]
    sys.modules["stable_baselines3"] = sb3_pkg

    common_pkg = types.ModuleType("stable_baselines3.common")
    common_pkg.__path__ = [str(SB3_COMMON_DIR)]
    sys.modules["stable_baselines3.common"] = common_pkg

    vec_env_pkg = types.ModuleType("stable_baselines3.common.vec_env")
    vec_env_pkg.__path__ = [str(SB3_COMMON_DIR / "vec_env")]
    sys.modules["stable_baselines3.common.vec_env"] = vec_env_pkg

    preprocessing = types.ModuleType("stable_baselines3.common.preprocessing")

    def check_for_nested_spaces(_obs_space):
        return None

    preprocessing.check_for_nested_spaces = check_for_nested_spaces
    sys.modules["stable_baselines3.common.preprocessing"] = preprocessing

    # `make_vec_env` only needs the Atari wrapper symbol at import time.
    atari_wrappers = types.ModuleType("stable_baselines3.common.atari_wrappers")

    class AtariWrapper:
        def __init__(self, env, **kwargs):
            self.env = env
            self.action_space = env.action_space
            self.observation_space = env.observation_space

        def __getattr__(self, item):
            return getattr(self.env, item)

    atari_wrappers.AtariWrapper = AtariWrapper
    sys.modules["stable_baselines3.common.atari_wrappers"] = atari_wrappers


def load_sb3_modules() -> types.SimpleNamespace:
    install_sb3_stubs()

    base_vec_env = load_source_module(
        "stable_baselines3.common.vec_env.base_vec_env",
        SB3_COMMON_DIR / "vec_env" / "base_vec_env.py",
    )
    load_source_module("stable_baselines3.common.vec_env.util", SB3_COMMON_DIR / "vec_env" / "util.py")
    load_source_module("stable_baselines3.common.vec_env.patch_gym", SB3_COMMON_DIR / "vec_env" / "patch_gym.py")
    dummy_vec_env = load_source_module(
        "stable_baselines3.common.vec_env.dummy_vec_env",
        SB3_COMMON_DIR / "vec_env" / "dummy_vec_env.py",
    )
    subproc_vec_env = load_source_module(
        "stable_baselines3.common.vec_env.subproc_vec_env",
        SB3_COMMON_DIR / "vec_env" / "subproc_vec_env.py",
    )
    monitor = load_source_module("stable_baselines3.common.monitor", SB3_COMMON_DIR / "monitor.py")

    vec_env_pkg = sys.modules["stable_baselines3.common.vec_env"]
    vec_env_pkg.VecEnv = base_vec_env.VecEnv
    vec_env_pkg.DummyVecEnv = dummy_vec_env.DummyVecEnv
    vec_env_pkg.SubprocVecEnv = subproc_vec_env.SubprocVecEnv

    env_util = load_source_module("stable_baselines3.common.env_util", SB3_COMMON_DIR / "env_util.py")
    return types.SimpleNamespace(env_util=env_util, monitor=monitor)


class TinyContinuousEnv(gym.Env):
    def __init__(self):
        self.action_space = spaces.Box(low=-2.0, high=2.0, shape=(2,), dtype=np.float32)
        self.observation_space = spaces.Box(low=-1.0, high=1.0, shape=(3,), dtype=np.float32)

    def reset(self, *, seed=None, options=None):
        return self.observation_space.sample(), {}

    def step(self, action):
        return self.observation_space.sample(), 0.0, False, False, {}


def main() -> int:
    modules = load_sb3_modules()
    vec_env = modules.env_util.make_vec_env(
        TinyContinuousEnv,
        n_envs=1,
        wrapper_class=gym.wrappers.ClipAction,
    )
    print(vec_env.action_space)

    expected_low = np.isneginf(vec_env.action_space.low).all()
    expected_high = np.isposinf(vec_env.action_space.high).all()
    if not (expected_low and expected_high):
        raise AssertionError(f"Unexpected action space: {vec_env.action_space}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
