#!/usr/bin/env python3
"""Static repro for keras-io issue 1711.

The bug report claims that examples/vision/pointnet.py uses the test split as
validation data during training. This script inspects the local source file and
verifies that the example still does exactly that.
"""

from __future__ import annotations

import ast
from pathlib import Path
import json
import sys


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "codebase" / "examples" / "vision" / "pointnet.py"
RESULT = ROOT / "reproduction.json"
STDOUT_LOG = ROOT / "repro_stdout.log"
STDERR_LOG = ROOT / "repro_stderr.log"


def line_number(lines: list[str], needle: str) -> int | None:
    for i, line in enumerate(lines, start=1):
        if needle in line:
            return i
    return None


def main() -> int:
    text = SOURCE.read_text(encoding="utf-8")
    lines = text.splitlines()
    tree = ast.parse(text, filename=str(SOURCE))

    fit_lineno = None
    validation_arg = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr != "fit":
                continue
            fit_lineno = getattr(node, "lineno", None)
            for kw in node.keywords:
                if kw.arg == "validation_data" and isinstance(kw.value, ast.Name):
                    validation_arg = kw.value.id
            break

    test_dataset_line = line_number(
        lines, "test_dataset = tf_data.Dataset.from_tensor_slices((test_points, test_labels))"
    )
    fit_line = line_number(lines, "model.fit(train_dataset, epochs=20, validation_data=test_dataset)")

    reproduced = (
        "validation_data=test_dataset" in text
        and validation_arg == "test_dataset"
        and test_dataset_line is not None
        and fit_line is not None
    )

    evidence_lines = [
        f"source_file={SOURCE}",
        f"fit_line={fit_line}",
        f"test_dataset_line={test_dataset_line}",
        f"ast_validation_arg={validation_arg!r}",
        "finding=validation_data is bound to test_dataset, which is constructed from the test split",
    ]
    if fit_lineno is not None:
        evidence_lines.append(f"ast_fit_lineno={fit_lineno}")

    payload = {
        "reproducible": reproduced,
        "evidence": " | ".join(evidence_lines),
        "steps": [
            "Read examples/vision/pointnet.py from the local codebase.",
            "Verify that test_dataset is created from test_points and test_labels.",
            "Verify that model.fit passes validation_data=test_dataset.",
        ],
        "blocking_reason": "" if reproduced else "The expected validation_data=test_dataset call was not present in the local source.",
        "reproduction_command": "bash run_repro.sh",
    }

    print("BUG_REPRODUCED=" + ("1" if reproduced else "0"))
    for item in evidence_lines:
        print(item)
    RESULT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    if reproduced:
        return 0
    return 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover
        print(f"ERROR: {exc}", file=sys.stderr)
        RESULT.write_text(
            json.dumps(
                {
                    "reproducible": False,
                    "evidence": "",
                    "steps": [],
                    "blocking_reason": str(exc),
                    "reproduction_command": "bash run_repro.sh",
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        raise
