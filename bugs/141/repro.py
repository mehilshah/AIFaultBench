#!/usr/bin/env python3
from __future__ import annotations

import sys
import traceback
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PY_SRC = ROOT / "codebase" / "bindings" / "python" / "py_src"
if str(PY_SRC) not in sys.path:
    sys.path.insert(0, str(PY_SRC))

import torch  # type: ignore
from safetensors.torch import load, load_file, save_file  # type: ignore


def main() -> int:
    path = ROOT / "repro_empty_tensor.safetensors"
    tensors = {
        "empty": torch.zeros((0,), dtype=torch.float32),
    }

    save_file(tensors, path)
    print(f"saved={path.name} size={path.stat().st_size}")

    loaded_from_file = load_file(path)
    print(f"load_file_keys={list(loaded_from_file.keys())}")
    print(f"load_file_shape={tuple(loaded_from_file['empty'].shape)}")

    raw = path.read_bytes()
    print(f"bytes_length={len(raw)}")

    try:
        loaded_from_bytes = load(raw)
    except Exception as exc:  # expected failure for this bug
        print(f"load_bytes_error={type(exc).__name__}: {exc}", file=sys.stderr)
        traceback.print_exc()
        return 0

    print(f"load_bytes_keys={list(loaded_from_bytes.keys())}")
    print("load(bytes) unexpectedly succeeded", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
