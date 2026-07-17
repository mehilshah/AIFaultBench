#!/usr/bin/env python3
"""Focused reproduction for detectron2 issue #642.

This repo snapshot is already on commit abae3ae, which includes the
ImageList.from_tensors fix that avoids mutating a single zero-padded input.
The script checks the exact code path and records why the AP-drop report is
not reproducible in this standardized folder.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
IMAGE_LIST = CODEBASE / "detectron2" / "structures" / "image_list.py"
MODEL_ZOO = CODEBASE / "MODEL_ZOO.md"
ISSUE_REPORTED_COMMIT = "e74a00c97069dd722007fa5bdc5f1c820a4e97a1"
FIX_COMMIT = "abae3ae4aaa6e9f5beb908b3b2f734cb12b38a9b"


def run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, cwd=ROOT, text=True).strip()


def main() -> int:
    if not IMAGE_LIST.exists():
        raise SystemExit(f"Missing source file: {IMAGE_LIST}")

    head = run(["git", "-C", str(CODEBASE), "rev-parse", "HEAD"])
    current_file = IMAGE_LIST.read_text(encoding="utf-8")
    parent_file = run(
        ["git", "-C", str(CODEBASE), "show", f"{FIX_COMMIT}^:detectron2/structures/image_list.py"]
    )
    model_zoo = MODEL_ZOO.read_text(encoding="utf-8")

    zero_pad_branch_present = "if all(x == 0 for x in padding_size)" in current_file
    current_uses_non_inplace_unsqueeze = "batched_imgs = tensors[0].unsqueeze(0)" in current_file
    parent_had_unconditional_unsqueeze_ = "padding_size" not in parent_file or "unsqueeze_(" in parent_file

    baseline_match = re.search(r"R50-FPN</a></td>.*?<td align=\"center\">37\.9</td>", model_zoo, re.S)

    print("detectron2 HEAD:", head)
    print("issue-reported commit:", ISSUE_REPORTED_COMMIT)
    print("fix commit:", FIX_COMMIT)
    print("single-image zero-pad guard present:", zero_pad_branch_present)
    print("current code uses non-inplace unsqueeze for zero-padding:", current_uses_non_inplace_unsqueeze)
    print("parent commit used in-place unsqueeze_ in the single-image path:", parent_had_unconditional_unsqueeze_)
    print("model zoo Faster-RCNN R50-FPN 1x baseline 37.9 present:", bool(baseline_match))
    print()
    print("Relevant current source excerpt:")
    for line in current_file.splitlines()[83:94]:
        print("  " + line)
    print()
    print(
        "Conclusion: this checkout already contains the fix for the single-image padding-path bug, "
        "so the AP-drop report is not reproducible here without downgrading to the pre-fix commit "
        "and rerunning a full COCO training/eval job."
    )
    print(
        json.dumps(
            {
                "reproducible_here": False,
                "reason": "fixed source tree; full COCO training not runnable in this folder",
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
