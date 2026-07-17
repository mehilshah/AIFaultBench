#!/usr/bin/env python3
"""Minimal reproduction for the Python 3.8 dict-union failure.

The bug report points at official/core/base_trainer.py:442, where the trainer
returns `passthrough_logs | logs`. That syntax is only supported by Python 3.9+
and raises TypeError on Python 3.8.
"""

from pathlib import Path
import sys
import traceback


SOURCE_FILE = Path(__file__).resolve().parent / "codebase/official/core/base_trainer.py"


def main() -> int:
  print(f"python_version={sys.version}")
  print(f"source_file={SOURCE_FILE}")
  source_lines = SOURCE_FILE.read_text().splitlines()
  print(f"source_line_442={source_lines[441]}")

  # Recreate the exact failure mode from the trainer using a snippet that has
  # the same problematic `dict | dict` expression.
  snippet = (
      "def eval_step():\n"
      "    passthrough_logs = {}\n"
      "    logs = {}\n"
      "    return passthrough_logs | logs\n"
  )

  try:
    namespace = {}
    exec(compile(snippet, str(SOURCE_FILE), "exec"), namespace)
    namespace["eval_step"]()
  except TypeError:
    traceback.print_exc()
    return 1

  print("unexpected_success")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
