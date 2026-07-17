from __future__ import annotations

import json
import os
import sys
import traceback
from pathlib import Path

import torch
from torch import nn


ROOT = Path(__file__).resolve().parent
CODEBASE_SRC = ROOT / "codebase" / "src"
if str(CODEBASE_SRC) not in sys.path:
    sys.path.insert(0, str(CODEBASE_SRC))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from peft.tuners.lora.bnb import Linear4bit as PeftLinear4bit


class TinyQuantModel(nn.Module):
    def __init__(self, in_features: int = 2048, hidden_features: int = 2048):
        super().__init__()
        import bitsandbytes as bnb

        self.is_loaded_in_4bit = True
        self.config = type("Config", (), {"model_type": "custom"})()
        self.linear = bnb.nn.Linear4bit(in_features, hidden_features, bias=False)

    def forward(self, x):
        return self.linear(x)


def run_case(init_lora_weights):
    torch.manual_seed(0)
    base_layer = TinyQuantModel().linear
    peft_layer = PeftLinear4bit(base_layer, "default", r=8, init_lora_weights=init_lora_weights)
    x = torch.randn(3, 2048)
    y = peft_layer(x)
    return y


def main():
    results = {}
    for init_mode in [True, "olora", "pissa"]:
        try:
            out = run_case(init_mode)
            results[str(init_mode)] = {
                "ok": True,
                "shape": list(out.shape),
            }
        except Exception as exc:
            results[str(init_mode)] = {
                "ok": False,
                "error": f"{type(exc).__name__}: {exc}",
                "traceback": traceback.format_exc(),
            }
    print(json.dumps(results, indent=2, sort_keys=True))
    return results


if __name__ == "__main__":
    main()
