#!/usr/bin/env python3
"""Minimal reproduction for tensorflow/models issue 11058.

The notebook helper `show_batch(raw_records, num_of_examples)` accepts
`num_of_examples`, but the function body never reads it. This script loads the
exact notebook cell from the checked-in codebase, executes it in a stubbed
environment, and proves that changing `num_of_examples` does not change the
number of records rendered.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
NOTEBOOK = ROOT / "codebase" / "docs" / "vision" / "instance_segmentation.ipynb"
RESULT_PATH = ROOT / "reproduction.json"


class TensorLike:
    def __init__(self, value: Any):
        self.value = value

    def numpy(self) -> "TensorLike":
        return self

    def astype(self, _dtype: str) -> "TensorLike":
        return self

    def __len__(self) -> int:
        return len(self.value)


class FakePlot:
    def __init__(self) -> None:
        self.subplot_calls: list[tuple[int, int, int]] = []
        self.imshow_calls: list[Any] = []
        self.axis_calls: list[Any] = []
        self.title_calls: list[str] = []
        self.figure_calls: list[dict[str, Any]] = []
        self.show_calls = 0

    def figure(self, **kwargs: Any) -> None:
        self.figure_calls.append(kwargs)

    def subplot(self, *args: int) -> None:
        self.subplot_calls.append(args)

    def imshow(self, image: Any) -> None:
        self.imshow_calls.append(image)

    def axis(self, value: Any) -> None:
        self.axis_calls.append(value)

    def title(self, value: str) -> None:
        self.title_calls.append(value)

    def show(self) -> None:
        self.show_calls += 1


class FakeNP:
    @staticmethod
    def ones(shape: Any) -> list[int]:
        if isinstance(shape, int):
            size = shape
        else:
            size = shape[0]
        return [1] * size


class FakeDecoder:
    @staticmethod
    def decode(_serialized_example: Any) -> dict[str, TensorLike]:
        return {
            "image": TensorLike([[0, 0], [0, 0]]),
            "groundtruth_boxes": TensorLike([[0, 0, 1, 1], [0, 0, 1, 1]]),
            "groundtruth_classes": TensorLike([1, 2]),
            "groundtruth_instance_masks": TensorLike([[[1, 1], [1, 1]], [[1, 1], [1, 1]]]),
        }


class FakeViz:
    calls: list[dict[str, Any]] = []

    @classmethod
    def visualize_boxes_and_labels_on_image_array(cls, *args: Any, **kwargs: Any) -> None:
        cls.calls.append({"args": args, "kwargs": kwargs})


def load_show_batch_source() -> str:
    import json as _json

    data = _json.loads(NOTEBOOK.read_text())
    for cell in data.get("cells", []):
        source = "".join(cell.get("source", []))
        if source.lstrip().startswith("def show_batch"):
            return source
    raise RuntimeError("show_batch cell not found in notebook")


def parameter_unused(source: str, parameter_name: str) -> bool:
    tree = ast.parse(source)
    fn = next(node for node in tree.body if isinstance(node, ast.FunctionDef))
    used = any(
        isinstance(node, ast.Name) and node.id == parameter_name and isinstance(node.ctx, ast.Load)
        for node in ast.walk(fn)
    )
    return not used


def run_show_batch(source: str) -> dict[str, Any]:
    fake_plt = FakePlot()
    namespace = {
        "plt": fake_plt,
        "np": FakeNP(),
        "tf_ex_decoder": FakeDecoder(),
        "visualization_utils": FakeViz,
        "category_index": {1: {"name": "thing"}},
    }
    exec(compile(source, str(NOTEBOOK), "exec"), namespace)
    show_batch = namespace["show_batch"]

    records = ["record-1", "record-2", "record-3"]
    show_batch(records, 1)

    return {
        "subplot_calls": len(fake_plt.subplot_calls),
        "show_calls": fake_plt.show_calls,
        "rendered_records": len(fake_plt.title_calls),
        "visualization_calls": len(FakeViz.calls),
        "records_length": len(records),
    }


def write_result(payload: dict[str, Any]) -> None:
    RESULT_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def main() -> int:
    source = load_show_batch_source()
    unused = parameter_unused(source, "num_of_examples")
    runtime = run_show_batch(source)

    reproducible = unused and runtime["subplot_calls"] == runtime["records_length"]
    payload = {
        "reproducible": reproducible,
        "evidence": (
            "The notebook helper defines `show_batch(raw_records, num_of_examples)` "
            "but never references `num_of_examples`; when called with three records "
            "and `num_of_examples=1`, it still renders three subplots."
        ),
        "steps": [
            "Load the `show_batch` cell from `codebase/docs/vision/instance_segmentation.ipynb`.",
            "Inspect the function body and confirm `num_of_examples` is never read.",
            "Execute `show_batch` with three records and `num_of_examples=1` in a stubbed environment.",
            "Observe that the function still processes all three records.",
        ],
        "blocking_reason": "" if reproducible else "The helper did not demonstrate the expected unused-parameter behavior.",
        "reproduction_command": "bash run_repro.sh",
    }
    write_result(payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if reproducible else 1


if __name__ == "__main__":
    raise SystemExit(main())
