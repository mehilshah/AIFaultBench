from __future__ import annotations

import pathlib
import importlib.util
import types
import sys
import traceback
from itertools import product
from typing import Optional

import gymnasium as gym
import numpy as np
from gymnasium import spaces


ROOT_DIR = pathlib.Path(__file__).resolve().parent
CODEBASE_DIR = ROOT_DIR / "codebase"


def _ensure_package(module_name: str, package_dir: pathlib.Path) -> types.ModuleType:
    module = sys.modules.get(module_name)
    if module is None:
        module = types.ModuleType(module_name)
        module.__path__ = [str(package_dir)]  # type: ignore[attr-defined]
        sys.modules[module_name] = module
    return module


def _load_module(module_name: str, file_path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {module_name} from {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _load_env_checker():
    sb3_pkg = _ensure_package("stable_baselines3", CODEBASE_DIR / "stable_baselines3")
    common_pkg = _ensure_package("stable_baselines3.common", CODEBASE_DIR / "stable_baselines3" / "common")
    vec_env_pkg = _ensure_package(
        "stable_baselines3.common.vec_env", CODEBASE_DIR / "stable_baselines3" / "common" / "vec_env"
    )

    _load_module(
        "stable_baselines3.common.vec_env.base_vec_env",
        CODEBASE_DIR / "stable_baselines3" / "common" / "vec_env" / "base_vec_env.py",
    )
    _load_module(
        "stable_baselines3.common.vec_env.patch_gym",
        CODEBASE_DIR / "stable_baselines3" / "common" / "vec_env" / "patch_gym.py",
    )
    _load_module(
        "stable_baselines3.common.vec_env.util",
        CODEBASE_DIR / "stable_baselines3" / "common" / "vec_env" / "util.py",
    )
    dummy_vec_env = _load_module(
        "stable_baselines3.common.vec_env.dummy_vec_env",
        CODEBASE_DIR / "stable_baselines3" / "common" / "vec_env" / "dummy_vec_env.py",
    )
    vec_check_nan = _load_module(
        "stable_baselines3.common.vec_env.vec_check_nan",
        CODEBASE_DIR / "stable_baselines3" / "common" / "vec_env" / "vec_check_nan.py",
    )
    vec_env_pkg.DummyVecEnv = dummy_vec_env.DummyVecEnv
    vec_env_pkg.VecCheckNan = vec_check_nan.VecCheckNan

    sb3_pkg.common = common_pkg
    common_pkg.vec_env = vec_env_pkg
    _load_module(
        "stable_baselines3.common.preprocessing",
        CODEBASE_DIR / "stable_baselines3" / "common" / "preprocessing.py",
    )
    return _load_module(
        "stable_baselines3.common.env_checker",
        CODEBASE_DIR / "stable_baselines3" / "common" / "env_checker.py",
    )


check_env = _load_env_checker().check_env


class DummySeqEnv(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self, stack: bool, inside: str):
        super().__init__()
        seq_space = spaces.Sequence(
            spaces.Box(low=-100, high=100, shape=(1,), dtype=np.float32),
            stack=stack,
        )
        if inside == "dict":
            self.observation_space = spaces.Dict({"seq": seq_space})
        elif inside == "tuple":
            self.observation_space = spaces.Tuple((seq_space,))
        elif inside == "oneof":
            self.observation_space = spaces.OneOf((seq_space, spaces.Discrete(3)))
        elif inside == "none":
            self.observation_space = seq_space
        else:
            raise ValueError(f"unsupported inside={inside}")
        self.action_space = spaces.Discrete(2)

    def reset(self, *, seed: Optional[int] = None, options: Optional[dict] = None):
        super().reset(seed=seed)
        return self.observation_space.sample(), {}

    def step(self, action):
        return self.observation_space.sample(), 0.0, False, False, {}

    def render(self):
        return None


def main() -> int:
    print(f"gymnasium={gym.__version__}")
    print("checking nested Sequence spaces inside Dict, Tuple, and OneOf")
    failures: list[tuple[str, bool, str]] = []

    for inside, stack in product(("none", "dict", "tuple", "oneof"), (False, True)):
        print(f"case inside={inside!r} stack={stack!r}")
        env = DummySeqEnv(stack=stack, inside=inside)
        try:
            check_env(env)
        except Exception as exc:  # noqa: BLE001
            failures.append((inside, stack, f"{type(exc).__name__}: {exc}"))
            traceback.print_exc()
        else:
            print("PASSED")
        print("=" * 80)

    if failures:
        print("FAILURES:")
        for inside, stack, message in failures:
            print(f"inside={inside!r} stack={stack!r} -> {message}")
        return 1

    print("No failures observed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
