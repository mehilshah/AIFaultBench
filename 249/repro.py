from __future__ import annotations

from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR / "codebase"))

import torch  # noqa: E402
from torchrl.modules import MLP  # noqa: E402


def main() -> None:
    mlp = MLP(in_features=1024, out_features=512)
    actual = repr(mlp)
    expected = (
        "MLP(\n"
        "  (0): Linear(in_features=1024, out_features=512, bias=True)\n"
        ")"
    )

    print("torch:", torch.__version__)
    print("observed modules:", [type(module).__name__ for module in mlp])
    print("observed repr:")
    print(actual)
    print("expected repr:")
    print(expected)

    if actual != expected:
        raise AssertionError(
            "Default MLP construction inserts hidden layers when depth and num_cells are omitted."
        )


if __name__ == "__main__":
    main()
