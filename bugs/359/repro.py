import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))

import torch

from torch_geometric.nn import HypergraphConv  # noqa: E402


def script_module(use_attention: bool) -> str:
    conv = HypergraphConv(16, 32, use_attention=use_attention)

    try:
        torch.jit.script(conv)
    except Exception as exc:  # noqa: BLE001
        message = str(exc)
        print(f"use_attention={use_attention}: {type(exc).__name__}")
        print(message)
        return message

    raise AssertionError(
        f"Expected torch.jit.script to fail for use_attention={use_attention}")


def main() -> int:
    print(f"torch={torch.__version__}")

    false_msg = script_module(False)
    true_msg = script_module(True)

    assert "Module 'HypergraphConv' has no attribute 'att'" in false_msg
    assert "Variable 'alpha' previously had type NoneType" in true_msg

    print("reproduced: HypergraphConv is not TorchScript-compatible")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
