from __future__ import annotations

import copy
import json
import os
import tempfile
from dataclasses import asdict, dataclass

import torch
from peft import LoraConfig, PeftModel, get_peft_model
from torch import nn


@dataclass
class ReproResult:
    reproducible: bool
    output_max_abs_diff: float
    base_weight_max_abs_diff: float
    before_output: list[list[float]]
    after_output: list[list[float]]
    notes: str


class TinyModule(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(8, 8, bias=False)

    def forward(self, x):
        return self.linear(x)


def main() -> None:
    torch.manual_seed(0)
    torch.set_printoptions(precision=8, sci_mode=False)

    base = TinyModule().eval()
    inputs = torch.randn(2, 8)

    with tempfile.TemporaryDirectory(prefix="pissa-repro-") as workdir:
        non_pissa_dir = os.path.join(workdir, "non-pissa")
        pissa_dir = os.path.join(workdir, "pissa")

        non_pissa = get_peft_model(
            copy.deepcopy(base),
            LoraConfig(target_modules=["linear"], r=2, init_lora_weights=True),
        )
        non_pissa.save_pretrained(non_pissa_dir)

        pissa = get_peft_model(
            copy.deepcopy(base),
            LoraConfig(target_modules=["linear"], r=2, init_lora_weights="pissa"),
        )
        pissa.save_pretrained(pissa_dir)

        model = PeftModel.from_pretrained(copy.deepcopy(base), non_pissa_dir, adapter_name="non-pissa")
        model.set_adapter("non-pissa")
        before_base_weight = model.base_model.model.linear.base_layer.weight.detach().clone()
        before_output = model(inputs).detach().clone()

        model.load_adapter(pissa_dir, "pissa")
        after_base_weight = model.base_model.model.linear.base_layer.weight.detach().clone()
        model.set_adapter("non-pissa")
        after_output = model(inputs).detach().clone()

        output_max_abs_diff = (before_output - after_output).abs().max().item()
        base_weight_max_abs_diff = (before_base_weight - after_base_weight).abs().max().item()
        reproducible = output_max_abs_diff > 0.0 and base_weight_max_abs_diff > 0.0

        result = ReproResult(
            reproducible=reproducible,
            output_max_abs_diff=output_max_abs_diff,
            base_weight_max_abs_diff=base_weight_max_abs_diff,
            before_output=before_output.tolist(),
            after_output=after_output.tolist(),
            notes=(
                "Loading the PiSSA adapter mutates the shared base linear weight. "
                "When the earlier non-PiSSA adapter is re-activated, its output changes."
            ),
        )

        print(json.dumps(asdict(result), indent=2))

        if not reproducible:
            raise SystemExit("Reproduction did not trigger the expected output drift.")


if __name__ == "__main__":
    main()
