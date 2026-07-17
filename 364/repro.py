from __future__ import annotations

import tempfile
from pathlib import Path

import torch
import torch.nn as nn

from accelerate.big_modeling import load_checkpoint_and_dispatch


class ModelWithNoneSubmodule(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.linear1 = nn.Linear(2, 2)
        self.linear2 = nn.Linear(2, 2)
        self._modules["broken"] = None

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.linear2(self.linear1(x))


def main() -> None:
    print(f"torch={torch.__version__}")
    import accelerate

    print(f"accelerate={accelerate.__version__}")

    model = ModelWithNoneSubmodule()
    print(f"modules={model._modules}")
    with tempfile.TemporaryDirectory() as tmp_dir:
        checkpoint = Path(tmp_dir) / "model.bin"
        torch.save(model.state_dict(), checkpoint)
        print(f"checkpoint={checkpoint}")
        print("calling load_checkpoint_and_dispatch()")
        load_checkpoint_and_dispatch(ModelWithNoneSubmodule(), str(checkpoint), device_map={"": "cpu"})
        print("repro did not trigger")


if __name__ == "__main__":
    main()
