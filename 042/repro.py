#!/usr/bin/env python3
"""Minimal reproduction for imagen-pytorch issue 378."""

from importlib.metadata import version
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))


def main() -> None:
    print(f"python={sys.version.split()[0]}")
    print(f"beartype={version('beartype')}")
    print("importing imagen_pytorch ...")
    from imagen_pytorch import Unet, Imagen  # noqa: F401
    print("import succeeded")


if __name__ == "__main__":
    main()
