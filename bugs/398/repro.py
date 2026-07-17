#!/usr/bin/env python3
"""Minimal reproduction for Detectron2 issue 1132.

This avoids dataset downloads and model weights.  It loads the bundled cascade
configuration, constructs a dummy cascade ROI-head object, and executes the
inference branch that references the missing `test_score_thresh` attribute.
"""

from __future__ import annotations

import importlib.util
import pathlib
import sys
import types

import torch
from PIL import Image


ROOT = pathlib.Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
CONFIG_FILE = CODEBASE / "configs" / "Misc" / "cascade_mask_rcnn_X_152_32x8d_FPN_IN5k_gn_dconv.yaml"


def _install_fake_c_extension() -> None:
    """Provide the small subset of detectron2._C symbols that import-time code expects.

    The repro never reaches the custom ops, but several Detectron2 modules import
    `detectron2._C` eagerly.  A tiny stub keeps the script self-contained.
    """

    if "detectron2._C" in sys.modules:
        return

    fake_c = types.ModuleType("detectron2._C")

    def _unreachable(*args, **kwargs):  # pragma: no cover - only guards import-time access
        raise RuntimeError("detectron2._C stub should not be executed in this repro")

    fake_c.roi_align_forward = _unreachable
    fake_c.roi_align_backward = _unreachable
    fake_c.nms_rotated = _unreachable
    sys.modules["detectron2._C"] = fake_c


def _install_pillow_compat_aliases() -> None:
    """Backfill Pillow constants that this older Detectron2 snapshot expects."""

    if not hasattr(Image, "LINEAR"):
        Image.LINEAR = Image.BILINEAR


def main() -> None:
    _install_fake_c_extension()
    _install_pillow_compat_aliases()
    sys.path.insert(0, str(CODEBASE))

    from detectron2.config import get_cfg
    from detectron2.modeling.roi_heads.cascade_rcnn import CascadeROIHeads
    from detectron2.structures import Boxes, Instances

    cfg = get_cfg()
    cfg.merge_from_file(str(CONFIG_FILE))
    cfg.MODEL.DEVICE = "cpu"

    print(f"Loaded config: {CONFIG_FILE}")
    print(f"ROI head name: {cfg.MODEL.ROI_HEADS.NAME}")
    print(f"Cascade stages: {len(cfg.MODEL.ROI_BOX_CASCADE_HEAD.IOUS)}")

    class DummyPredictor:
        def predict_boxes(self, predictions, proposals):
            return [torch.tensor([[1.0, 1.0, 9.0, 9.0]], dtype=torch.float32)]

        def predict_probs(self, predictions, proposals):
            return [torch.tensor([[0.05, 0.95]], dtype=torch.float32)]

    dummy = object.__new__(CascadeROIHeads)
    dummy.__dict__.update(
        {
            "training": False,
            "in_features": list(cfg.MODEL.ROI_HEADS.IN_FEATURES),
            "num_cascade_stages": len(cfg.MODEL.ROI_BOX_CASCADE_HEAD.IOUS),
        }
    )
    dummy.__dict__["box_predictor"] = [DummyPredictor() for _ in range(dummy.num_cascade_stages)]
    dummy.__dict__["_run_stage"] = lambda features, proposals, stage: torch.zeros(
        (1, 1), dtype=torch.float32
    )
    dummy.__dict__["_create_proposals_from_boxes"] = (
        CascadeROIHeads._create_proposals_from_boxes.__get__(dummy, CascadeROIHeads)
    )

    proposals = []
    for _ in range(1):
        inst = Instances((32, 32))
        inst.proposal_boxes = Boxes(torch.tensor([[0.0, 0.0, 10.0, 10.0]], dtype=torch.float32))
        proposals.append(inst)

    features = {name: torch.zeros((1, 1, 1, 1), dtype=torch.float32) for name in dummy.in_features}

    try:
        CascadeROIHeads._forward_box(dummy, features, proposals)
    except Exception as exc:  # noqa: BLE001 - the point of the repro is the thrown exception
        print(f"{type(exc).__name__}: {exc}")
        raise


if __name__ == "__main__":
    main()
