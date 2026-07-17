#!/usr/bin/env python3
"""Minimal repro for tensorflow_models.vision.augment not being exported."""

from __future__ import annotations

import importlib
import sys
import traceback
from pathlib import Path
from types import ModuleType


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"


def _register_module(name: str, *, is_package: bool = True) -> ModuleType:
  module = ModuleType(name)
  if is_package:
    module.__path__ = []  # type: ignore[attr-defined]
  sys.modules[name] = module
  if "." in name:
    parent_name, child_name = name.rsplit(".", 1)
    parent = sys.modules.get(parent_name)
    if parent is not None:
      setattr(parent, child_name, module)
  return module


def _ensure_stub(name: str) -> ModuleType:
  if name in sys.modules:
    return sys.modules[name]
  return _register_module(name, is_package=True)


def install_dependency_stubs() -> None:
  """Provide tiny module stubs for unrelated dependencies."""
  _ensure_stub("tensorflow_models.nlp")
  _ensure_stub("official")
  _ensure_stub("official.core")
  _ensure_stub("official.modeling")
  _ensure_stub("official.modeling.hyperparams")
  _ensure_stub("official.modeling.optimization")
  _ensure_stub("official.modeling.tf_utils")
  _ensure_stub("official.vision")
  _ensure_stub("official.vision.configs")
  _ensure_stub("official.vision.serving")
  _ensure_stub("official.vision.modeling")
  _ensure_stub("official.vision.ops")
  _ensure_stub("official.vision.tasks")


def main() -> int:
  sys.path.insert(0, str(CODEBASE))
  install_dependency_stubs()

  tfm = importlib.import_module("tensorflow_models")

  has_augment = hasattr(tfm.vision, "augment")
  print(f"TFM_IMPORT_OK=True")
  print(f"VISION_MODULE={tfm.vision.__name__}")
  print(f"VISION_FILE={Path(tfm.vision.__file__).as_posix()}")
  print(f"HAS_AUGMENT={has_augment}")

  try:
    _ = tfm.vision.augment
    print("ERROR=unexpectedly_found_augment")
    return 1
  except AttributeError as exc:
    print(f"ERROR={type(exc).__name__}: {exc}")
    print("RESULT=bug_reproduced")
    return 0
  except Exception:
    print("ERROR=unexpected_exception")
    traceback.print_exc()
    return 2


if __name__ == "__main__":
  raise SystemExit(main())
