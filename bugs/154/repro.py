#!/usr/bin/env python3
"""Minimal TVP repro for missing `type_vocab_size` on TvpConfig."""

from __future__ import annotations

import os
import sys
import traceback


ROOT = os.path.dirname(os.path.abspath(__file__))
CODEBASE_SRC = os.path.join(ROOT, "codebase", "src")
if CODEBASE_SRC not in sys.path:
    sys.path.insert(0, CODEBASE_SRC)


def main() -> int:
    from transformers import ResNetConfig, TvpConfig, TvpModel

    backbone = ResNetConfig(out_features=["stage4"], image_size=512)
    config = TvpConfig(
        backbone_config=backbone,
        backbone=None,
        use_timm_backbone=False,
        use_pretrained_backbone=False,
        max_img_size=512,
    )

    print(f"has_type_vocab_size={hasattr(config, 'type_vocab_size')}")
    print("constructing TvpModel without type_vocab_size ...")
    try:
        TvpModel(config)
    except Exception:
        traceback.print_exc()
        return 1

    print("unexpectedly succeeded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
