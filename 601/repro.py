#!/usr/bin/env python3
"""Minimal reproducer for timm issue 2447."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))

from timm import create_model


def main() -> None:
    print("import ok")
    create_model("hf-hub:google/mobilenet_v2_1.0_224", pretrained=True)
    print("model created")


if __name__ == "__main__":
    main()
