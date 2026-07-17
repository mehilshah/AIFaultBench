from __future__ import annotations

import importlib
import traceback

import tensorflow as tf


def try_import(module_name: str):
  print(f"\n== import {module_name} ==")
  try:
    module = importlib.import_module(module_name)
    print(f"{module_name} imported from {module.__file__}")
    return module
  except Exception:
    traceback.print_exc()
    return None


def main():
  print(f"tensorflow={tf.__version__}")
  try_import("tensorflow_models")

  # This is the direct native import that reproduces the undefined-symbol
  # failure described in the bug report.
  import tensorflow_text  # noqa: F401


if __name__ == "__main__":
  main()

