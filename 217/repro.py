#!/usr/bin/env python3
"""Reproduce the Stanza POS loading KeyError from issue 1357."""

from __future__ import annotations

import os
from pathlib import Path

import stanza


ROOT = Path(__file__).resolve().parent


def main() -> None:
    resources_dir = ROOT / "stanza_resources"
    resources_dir.mkdir(exist_ok=True)
    os.environ.setdefault("STANZA_RESOURCES_DIR", str(resources_dir))

    print(f"stanza version: {stanza.__version__}")
    print("building Pipeline('en', package='mimic', processors={'ner': 'i2b2'})")
    stanza.Pipeline(
        "en",
        package="mimic",
        processors={"ner": "i2b2"},
        use_gpu=False,
        verbose=True,
    )
    print("pipeline initialized successfully")


if __name__ == "__main__":
    main()
