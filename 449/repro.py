#!/usr/bin/env python3
"""Reproduce the broken DIA documentation example.

The example from issue 46909 references `model` before assignment and later
uses `torch_device` and an invalid `device_map` keyword with `.to(...)`.
This script demonstrates all three failures without downloading a checkpoint.
"""

import sys


class DummyTensorDict(dict):
    def to(self, device):
        self["device"] = device
        return self


class DummyProcessor:
    @classmethod
    def from_pretrained(cls, checkpoint):
        return cls()

    def __call__(self, *, text, padding, return_tensors):
        return DummyTensorDict(
            text=text,
            padding=padding,
            return_tensors=return_tensors,
        )


class DummyModel:
    @classmethod
    def from_pretrained(cls, checkpoint):
        return cls()

    def to(self, *args, **kwargs):
        if kwargs:
            unexpected = next(iter(kwargs))
            raise TypeError(f"to() got an unexpected keyword argument {unexpected!r}")
        return self


def run_case(name, code, base_ns):
    ns = dict(base_ns)
    try:
        exec(code, ns, ns)
    except Exception as exc:  # noqa: BLE001 - repro should capture the exact error
        print(f"{name}: {type(exc).__name__}: {exc}")
        return type(exc).__name__, str(exc)

    print(f"{name}: unexpectedly succeeded")
    return None, None


def main():
    model_checkpoint = "nari-labs/Dia-1.6B-0626"
    text = ["[S1] Dia is an open weights text to dialogue model."]

    base_ns = {
        "AutoProcessor": DummyProcessor,
        "DiaForConditionalGeneration": DummyModel,
        "model_checkpoint": model_checkpoint,
        "text": text,
    }

    phase_1 = """
processor = AutoProcessor.from_pretrained(model_checkpoint)
inputs = processor(text=text, padding=True, return_tensors="pt").to(model.device)
"""

    phase_2 = """
processor = AutoProcessor.from_pretrained(model_checkpoint)
inputs = processor(text=text, padding=True, return_tensors="pt").to("cpu")
model = DiaForConditionalGeneration.from_pretrained(model_checkpoint).to(torch_device, device_map="auto")
"""

    phase_3 = """
torch_device = "cpu"
processor = AutoProcessor.from_pretrained(model_checkpoint)
inputs = processor(text=text, padding=True, return_tensors="pt").to("cpu")
model = DiaForConditionalGeneration.from_pretrained(model_checkpoint).to(torch_device, device_map="auto")
"""

    results = [
        run_case("phase_1_missing_model", phase_1, base_ns),
        run_case("phase_2_missing_torch_device", phase_2, base_ns),
        run_case("phase_3_invalid_device_map_kwarg", phase_3, base_ns),
    ]

    expected = [
        ("NameError", "name 'model' is not defined"),
        ("NameError", "name 'torch_device' is not defined"),
        ("TypeError", "to() got an unexpected keyword argument 'device_map'"),
    ]

    if results != expected:
        print(f"unexpected results: {results}", file=sys.stderr)
        return 1

    print("reproduction confirmed: the documentation example is broken in three distinct ways")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
