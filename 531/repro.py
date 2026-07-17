#!/usr/bin/env python3
"""Minimal RT-DETR reproduction for transformers issue 46832."""

from __future__ import annotations

import sys
import traceback
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase" / "src"))


def run_forward(num_feature_levels: int, image_size: int = 640) -> tuple[bool, BaseException | None]:
    import torch
    from transformers import RTDetrConfig, RTDetrForObjectDetection

    config = RTDetrConfig(num_feature_levels=num_feature_levels, num_labels=80, image_size=image_size)
    model = RTDetrForObjectDetection(config)
    model.eval()
    pixel_values = torch.rand(1, 3, image_size, image_size)

    try:
        with torch.no_grad():
            model(pixel_values=pixel_values)
    except BaseException as exc:  # noqa: BLE001
        return False, exc
    return True, None


def main() -> int:
    import torch
    import transformers

    print(f"torch={torch.__version__}")
    print(f"transformers={transformers.__version__}")
    print("case=bug num_feature_levels=4")

    bug_ok, bug_exc = run_forward(4)
    if bug_ok:
        print("BUG_REPRODUCED=False")
        print("unexpected: forward completed without error")
        return 1

    print("BUG_REPRODUCED=True")
    print(f"exception_type={type(bug_exc).__name__}")
    print(f"exception_message={bug_exc}")
    print("traceback_start", file=sys.stderr)
    traceback.print_exception(type(bug_exc), bug_exc, bug_exc.__traceback__, file=sys.stderr)
    print("traceback_end", file=sys.stderr)

    print("case=control num_feature_levels=3")
    control_ok, control_exc = run_forward(3)
    if control_ok:
        print("CONTROL_PASS=True")
        return 0

    print("CONTROL_PASS=False")
    print(f"control_exception_type={type(control_exc).__name__}")
    print(f"control_exception_message={control_exc}")
    traceback.print_exception(type(control_exc), control_exc, control_exc.__traceback__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
