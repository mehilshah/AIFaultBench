from __future__ import annotations

import importlib
import inspect
import sys
import types
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"


def bootstrap_torchrl_package() -> None:
    """Load the config module without importing torchrl.__init__.

    The local environment has a broken global torch install, so importing the
    package root would fail before we reach the config bug. The config module
    itself only depends on the package layout and omegaconf.
    """

    package_paths = {
        "torchrl": CODEBASE / "torchrl",
        "torchrl.trainers": CODEBASE / "torchrl" / "trainers",
        "torchrl.trainers.algorithms": CODEBASE / "torchrl" / "trainers" / "algorithms",
        "torchrl.trainers.algorithms.configs": CODEBASE
        / "torchrl"
        / "trainers"
        / "algorithms"
        / "configs",
    }
    for name, path in package_paths.items():
        module = sys.modules.get(name)
        if module is None:
            module = types.ModuleType(name)
            module.__path__ = [str(path)]  # type: ignore[attr-defined]
            sys.modules[name] = module
        else:
            module.__path__ = [str(path)]  # type: ignore[attr-defined]

    if str(CODEBASE) not in sys.path:
        sys.path.insert(0, str(CODEBASE))


def main() -> int:
    bootstrap_torchrl_package()
    module = importlib.import_module(
        "torchrl.trainers.algorithms.configs.transforms"
    )
    cls = module.InitTrackerConfig

    print(f"InitTrackerConfig signature: {inspect.signature(cls)}")
    print("Attempting InitTrackerConfig(init_key='is_test_init') ...")
    try:
        cls(init_key="is_test_init")
    except TypeError as exc:
        print(f"TypeError: {exc}")
        return 1

    print("Unexpected success: the bug is not reproducible in this checkout.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
