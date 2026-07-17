import os
import sys

import torch


ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "codebase"))

from torch_geometric.nn import HGTConv  # noqa: E402


def main() -> None:
    print(f"torch {torch.__version__}")
    model = HGTConv(16, 16, ([], []))
    print(f"constructed {type(model).__name__}")
    torch.jit.script(model)
    print("scripted")


if __name__ == "__main__":
    main()
