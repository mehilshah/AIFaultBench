import sys

import torch

from accelerate import Accelerator


class ToyModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = torch.nn.Linear(4, 4)

    def forward(self, x):
        return self.linear(x)


def main():
    accelerator = Accelerator(dynamo_backend="eager")
    model = ToyModel()
    prepared = accelerator.prepare(model)
    unwrapped = accelerator.unwrap_model(prepared)

    print(f"prepared_type={type(prepared).__module__}.{type(prepared).__qualname__}")
    print(f"unwrapped_type={type(unwrapped).__module__}.{type(unwrapped).__qualname__}")
    print(f"is_same_object={prepared is unwrapped}")

    if type(unwrapped) is not ToyModel:
        print("BUG: unwrap_model returned the compiled wrapper instead of the original module.", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
