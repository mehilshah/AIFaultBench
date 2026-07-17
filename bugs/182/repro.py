from __future__ import annotations

import dataclasses
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase" / "src"))

import lightning.pytorch as L  # noqa: E402


@dataclasses.dataclass
class Module(L.LightningModule):
    param: float
    not_a_param: float = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        self.save_hyperparameters()


def main() -> int:
    print(f"Using lightning source from: {ROOT / 'codebase' / 'src'}")
    print(f"Python executable: {sys.executable}")
    try:
        Module(param=1e-3)
    except Exception as ex:
        print(f"Observed exception: {type(ex).__name__}: {ex}", file=sys.stderr)
        raise
    print("No error was raised.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
