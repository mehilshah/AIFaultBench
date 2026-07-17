#!/usr/bin/env python3
"""Minimal reproducer for detectron2 issue 3227.

This script triggers the bug in detectron2.data.build._test_loader_from_config
where a dataset name is wrapped into a list and then used as a list index.
"""

from __future__ import annotations

import os
import sys
import traceback
import types


ROOT = os.path.dirname(os.path.abspath(__file__))
CODEBASE = os.path.join(ROOT, "codebase")
sys.path.insert(0, CODEBASE)


def main() -> None:
    # detectron2.layers imports detectron2._C during module import, but the
    # failing code path here never touches compiled ops. A stub keeps imports
    # lightweight and avoids needing to build the extension for this repro.
    sys.modules.setdefault("detectron2._C", types.ModuleType("detectron2._C"))

    import detectron2  # noqa: F401
    from detectron2.config import get_cfg
    from detectron2.data.build import build_detection_test_loader
    from detectron2.data.catalog import DatasetCatalog

    cfg = get_cfg()
    cfg.DATASETS.TEST = ("dummy_dataset",)
    cfg.DATASETS.PROPOSAL_FILES_TEST = ("dummy.pkl",)
    cfg.MODEL.LOAD_PROPOSALS = True

    if "dummy_dataset" not in DatasetCatalog.list():
        DatasetCatalog.register(
            "dummy_dataset",
            lambda: [
                {
                    "file_name": "x.jpg",
                    "image_id": 1,
                    "height": 1,
                    "width": 1,
                }
            ],
        )

    print("Invoking build_detection_test_loader(cfg, cfg.DATASETS.TEST[0])")
    build_detection_test_loader(cfg, cfg.DATASETS.TEST[0])


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        raise
