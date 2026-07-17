#!/usr/bin/env python3
import json
from pathlib import Path

import torch
import timm


def run_case():
    torch.manual_seed(0)
    x = torch.randn(1, 3, 224, 224)

    m1 = timm.create_model("resnet50_clip.openai", pretrained=True, num_classes=0, global_pool="")
    m1.eval()
    m2 = timm.create_model("resnet50_clip.openai", pretrained=True, num_classes=0, global_pool="")
    m2.eval()

    with torch.no_grad():
        buggy_diff = (m1(x) - m2(x)).abs().max().item()

    m3 = timm.create_model("resnet50_clip.openai", pretrained=True)
    m3.reset_classifier(0, "")
    m3.eval()
    m4 = timm.create_model("resnet50_clip.openai", pretrained=True)
    m4.reset_classifier(0, "")
    m4.eval()

    with torch.no_grad():
        workaround_diff = (m3(x) - m4(x)).abs().max().item()

    return {
        "torch_version": torch.__version__,
        "timm_version": timm.__version__,
        "buggy_diff": buggy_diff,
        "workaround_diff": workaround_diff,
        "buggy_proj_type": type(m1.head.proj).__name__,
        "workaround_proj_type": type(m3.head.proj).__name__,
    }


def main():
    result_path = Path("reproduction.json")
    out = run_case()
    reproducible = out["buggy_diff"] > 0 and out["workaround_diff"] == 0
    result = {
        "reproducible": reproducible,
        "evidence": (
            f"buggy_diff={out['buggy_diff']}; workaround_diff={out['workaround_diff']}; "
            f"buggy_proj_type={out['buggy_proj_type']}; workaround_proj_type={out['workaround_proj_type']}"
        ),
        "steps": [
            "Create an isolated virtualenv and install the bundle requirements.",
            "Run repro.py, which compares two pretrained resnet50_clip.openai feature-extraction instantiations.",
            "Compare the same model after reset_classifier(0, '') as the documented workaround.",
        ],
        "blocking_reason": "" if reproducible else "The bug did not reproduce in this environment.",
        "reproduction_command": "./run_repro.sh",
    }
    result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print(f"torch={out['torch_version']}")
    print(f"timm={out['timm_version']}")
    print(f"buggy_proj_type={out['buggy_proj_type']}")
    print(f"buggy_diff={out['buggy_diff']}")
    print(f"workaround_proj_type={out['workaround_proj_type']}")
    print(f"workaround_diff={out['workaround_diff']}")
    print(f"reproducible={reproducible}")


if __name__ == "__main__":
    main()
