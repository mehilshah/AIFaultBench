from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import torch
from torch import nn


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
if str(CODEBASE) not in sys.path:
    sys.path.insert(0, str(CODEBASE))


class FakeConfig:
    architectures = None
    num_labels = 1
    classifier_dropout = None


class FakeModel(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.linear = nn.Linear(1, 1)
        self.to_calls: list[str] = []

    def to(self, device, *args, **kwargs):  # noqa: ANN001
        self.to_calls.append(str(device))
        return self

    def forward(self, **kwargs):  # noqa: ANN003
        input_ids = kwargs["input_ids"]
        batch_size = input_ids.shape[0]
        logits = torch.zeros((batch_size, 1), dtype=torch.float32)
        return SimpleNamespace(logits=logits)


class FakeTokenizer:
    def __call__(self, *texts, **kwargs):  # noqa: ANN002, ANN003
        batch_size = len(texts[0])
        input_ids = torch.ones((batch_size, 4), dtype=torch.long)
        attention_mask = torch.ones((batch_size, 4), dtype=torch.long)
        return {"input_ids": input_ids, "attention_mask": attention_mask}


def main() -> int:
    ce_mod = importlib.import_module("sentence_transformers.cross_encoder.CrossEncoder")

    fake_model = FakeModel()

    ce_mod.AutoConfig.from_pretrained = lambda *args, **kwargs: FakeConfig()
    ce_mod.AutoModelForSequenceClassification.from_pretrained = lambda *args, **kwargs: fake_model
    ce_mod.AutoTokenizer.from_pretrained = lambda *args, **kwargs: FakeTokenizer()

    model = ce_mod.CrossEncoder("local-fake-model", device="cuda:0")

    init_device = str(model._target_device)
    param_device = next(model.model.parameters()).device.type
    to_calls_after_init = list(model.model.to_calls)

    pred = model.predict([["how are you?", "fine"]], batch_size=1)
    to_calls_after_predict = list(model.model.to_calls)

    reproducible = init_device == "cuda:0" and param_device == "cpu" and to_calls_after_init == [] and to_calls_after_predict == [
        "cuda:0"
    ]

    result = {
        "reproducible": reproducible,
        "evidence": [
            f"Constructor target device: {init_device}",
            f"Model parameter device immediately after init: {param_device}",
            f"Model.to calls after init: {to_calls_after_init}",
            f"Model.to calls after predict: {to_calls_after_predict}",
            f"Predict output: {pred.tolist()}",
            "CrossEncoder.__init__ stores the requested device but does not move the model until predict() is called.",
        ],
        "steps": [
            "Install the requirements with ./setup_env.sh",
            "Run ./run_repro.sh",
            "Inspect repro_stdout.log and reproduction.json",
        ],
        "blocking_reason": "" if reproducible else "The constructor behavior did not match the reported bug in this environment.",
        "reproduction_command": "./run_repro.sh",
    }

    output_path = ROOT / "reproduction.json"
    output_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(result, indent=2))
    return 0 if reproducible else 1


if __name__ == "__main__":
    raise SystemExit(main())
