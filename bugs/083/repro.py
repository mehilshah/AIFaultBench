#!/usr/bin/env python3
"""Reproduce the CrossViT constructor failure from vit-pytorch issue 279."""

from pathlib import Path
import importlib.util
import sys
import traceback


def main() -> int:
    repo_root = Path(__file__).resolve().parent
    codebase = repo_root / "codebase"
    sys.path.insert(0, str(codebase))

    module_path = codebase / "vit_pytorch" / "cross_vit.py"

    try:
        spec = importlib.util.spec_from_file_location("cross_vit_repro", module_path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.CrossViT(
            image_size=48,
            num_classes=10,
            sm_dim=32,
            lg_dim=64,
        )
    except Exception:
        traceback.print_exc()
        return 1

    print("CrossViT instantiated successfully; bug not reproduced.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
