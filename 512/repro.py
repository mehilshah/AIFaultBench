from __future__ import annotations

import importlib
import types
from pathlib import Path
import sys

import torch


ROOT = Path(__file__).resolve().parent


def _install_package_stub(name: str, path: Path) -> types.ModuleType:
    module = types.ModuleType(name)
    module.__path__ = [str(path)]
    sys.modules[name] = module
    return module


sys.path.insert(0, str(ROOT / "codebase" / "src"))

_install_package_stub("lightning", ROOT / "codebase" / "src" / "lightning")
_install_package_stub("lightning.fabric", ROOT / "codebase" / "src" / "lightning" / "fabric")
_install_package_stub("lightning.fabric.plugins", ROOT / "codebase" / "src" / "lightning" / "fabric" / "plugins")
_install_package_stub(
    "lightning.fabric.plugins.precision", ROOT / "codebase" / "src" / "lightning" / "fabric" / "plugins" / "precision"
)
utilities_pkg = _install_package_stub("lightning.fabric.utilities", ROOT / "codebase" / "src" / "lightning" / "fabric" / "utilities")

rank_zero = importlib.import_module("lightning.fabric.utilities.rank_zero")
utilities_pkg.rank_zero_warn = rank_zero.rank_zero_warn

FSDPPrecision = importlib.import_module("lightning.fabric.plugins.precision.fsdp").FSDPPrecision


def main() -> None:
    precision = FSDPPrecision("bf16-mixed")

    with precision.module_init_context():
        model = torch.nn.Sequential(torch.nn.Linear(4, 8), torch.nn.GELU(), torch.nn.Linear(8, 2))

    actual = next(model.parameters()).dtype
    expected = torch.float32

    print(f"expected_dtype={expected}")
    print(f"actual_dtype={actual}")

    assert actual == expected, f"Expected module init to keep parameters in {expected}, got {actual}"


if __name__ == "__main__":
    main()
