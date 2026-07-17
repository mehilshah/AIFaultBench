#!/usr/bin/env python3
from __future__ import annotations

import sys
import traceback
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))

import timm  # noqa: E402


def main() -> int:
    print(f"timm_version={timm.__version__}")
    print("case=bad_overlay")
    try:
        timm.create_model(
            "mobilenetv4_conv_medium",
            pretrained=True,
            pretrained_cfg_overlay="file=./pytorch_model.bin",
        )
    except Exception as exc:
        print(f"exception={type(exc).__name__}: {exc}")
        traceback.print_exc()
        reproduced = isinstance(exc, TypeError) and "dataclasses.replace()" in str(exc)
    else:
        print("unexpected_success=true")
        reproduced = False

    print("case=control_backbone")
    model = timm.create_model(
        "mobilenetv4_conv_medium",
        pretrained=False,
        pretrained_cfg_overlay={"file": "./pytorch_model.bin"},
    )
    backbone = torch.nn.Sequential(model.conv_stem, model.bn1, model.blocks[:3])
    output = backbone(torch.randn(1, 3, 224, 224))
    print(f"control_output_shape={tuple(output.shape)}")

    if reproduced:
        print("result=reproduced")
        return 0
    print("result=not_reproduced")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
