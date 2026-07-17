#!/usr/bin/env python3
"""Bug reproduction helper for tensorflow/models#11133.

This script is intentionally conservative:
* It first records source-level evidence from the checked-in codebase.
* If TensorFlow is available, it can exercise the local exporter module.
* In this workspace TensorFlow is not installed, so the script exits with a
  blocker code after printing the evidence needed to explain why the runtime
  repro cannot be completed here.
"""

from __future__ import annotations

import ast
import pathlib
import sys
from typing import Optional


ROOT = pathlib.Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
EXPORTER_LIB = CODEBASE / "research" / "object_detection" / "exporter_lib_v2.py"
EXPORTER_MAIN = CODEBASE / "research" / "object_detection" / "exporter_main_v2.py"


def _find_class(path: pathlib.Path, class_name: str) -> Optional[ast.ClassDef]:
  tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
  for node in tree.body:
    if isinstance(node, ast.ClassDef) and node.name == class_name:
      return node
  return None


def _has_attr_assignment(class_node: ast.ClassDef, attr_name: str) -> bool:
  for node in ast.walk(class_node):
    if isinstance(node, ast.Assign):
      for target in node.targets:
        if isinstance(target, ast.Attribute) and target.attr == attr_name:
          return True
    if isinstance(node, ast.AnnAssign):
      target = node.target
      if isinstance(target, ast.Attribute) and target.attr == attr_name:
        return True
  return False


def _count_attribute_reads(path: pathlib.Path, attr_name: str) -> int:
  tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
  count = 0
  for node in ast.walk(tree):
    if isinstance(node, ast.Attribute) and node.attr == attr_name:
      count += 1
  return count


def main() -> int:
  print("Bug: AttributeError: 'DetectionFromImageModule' object has no attribute 'outputs'")
  print(f"Exporter source: {EXPORTER_LIB.relative_to(ROOT)}")
  print(f"Entry-point source: {EXPORTER_MAIN.relative_to(ROOT)}")

  class_node = _find_class(EXPORTER_LIB, "DetectionFromImageModule")
  if class_node is None:
    print("Could not locate DetectionFromImageModule in exporter_lib_v2.py.")
    return 2

  print(f"DetectionFromImageModule is defined at line {class_node.lineno}.")
  print(
      "Class defines an 'outputs' attribute assignment:",
      _has_attr_assignment(class_node, "outputs"),
  )
  print(
      "exporter_main_v2.py contains attribute reads named 'outputs':",
      _count_attribute_reads(EXPORTER_MAIN, "outputs"),
  )

  try:
    import tensorflow as tf  # type: ignore
  except ModuleNotFoundError as exc:
    print(
        "TensorFlow is not installed in this workspace, so the runtime "
        "export path cannot be executed here.",
        file=sys.stderr,
    )
    print(f"Import failure: {exc}", file=sys.stderr)
    return 2

  sys.path.insert(0, str(CODEBASE / "research"))
  from object_detection import exporter_lib_v2  # pylint: disable=import-error

  class DummyModel:
    pass

  module = exporter_lib_v2.DetectionFromImageModule(DummyModel())
  print("Created DetectionFromImageModule with TensorFlow available.")
  try:
    _ = module.outputs
  except AttributeError as exc:
    print(f"Observed AttributeError: {exc}")
    return 1

  print("Unexpectedly found an outputs attribute; bug not reproduced.")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
