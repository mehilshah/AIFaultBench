#!/usr/bin/env python3
"""Minimal repro harness for issue #2481.

This does not attempt to retrain CIFAR-100 end-to-end. The report is about a
training-accuracy gap, so the useful local check is whether `timm.create_model`
returns the expected ResNet-34 architecture and can execute a forward pass.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
RESULT_PATH = ROOT / "reproduction.json"


def main() -> int:
    sys.path.insert(0, str(CODEBASE))

    import timm  # type: ignore
    import torch  # type: ignore

    model = timm.create_model("resnet34", pretrained=False, num_classes=100)
    model.eval()

    x = torch.randn(2, 3, 32, 32)
    with torch.inference_mode():
        y = model(x)

    evidence_lines = [
        f"timm version: {timm.__version__}",
        f"model type: {type(model).__name__}",
        f"conv1 kernel/stride/padding: {model.conv1.kernel_size}/{model.conv1.stride}/{model.conv1.padding}",
        f"maxpool present: {type(model.maxpool).__name__}",
        f"classifier out_features: {getattr(model.get_classifier(), 'out_features', 'n/a')}",
        f"forward output shape: {tuple(y.shape)}",
    ]

    result = {
        "reproducible": False,
        "evidence": " | ".join(evidence_lines),
        "steps": [
            "Install the local CPU-only PyTorch/torchvision environment.",
            "Import the local `codebase/` copy of timm and instantiate `resnet34` with `num_classes=100`.",
            "Run a random 32x32 forward pass to confirm the model path works.",
        ],
        "blocking_reason": (
            "The reported symptom is an end-to-end CIFAR-100 accuracy gap after 200 epochs, "
            "which is not deterministically reproducible from the repository alone here. "
            "The local smoke test shows `timm.create_model('resnet34')` builds and runs, and "
            "the source documents `resnet34` as the standard torchvision-style 7x7-stem ResNet, "
            "not a CIFAR-specific variant."
        ),
        "reproduction_command": "bash run_repro.sh",
    }

    RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
