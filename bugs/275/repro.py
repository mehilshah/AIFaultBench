#!/usr/bin/env python3
from __future__ import annotations

import tempfile
from pathlib import Path
import sys

import PIL.Image as Image

if not hasattr(Image, "LINEAR"):
    Image.LINEAR = Image.BILINEAR

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))

import torch
from detectron2.config import get_cfg
from detectron2.export import scripting_with_instances
from detectron2.modeling import build_model
from detectron2.structures import Boxes


def build_mask_rcnn():
    cfg = get_cfg()
    cfg.merge_from_file(
        str(ROOT / "codebase" / "configs" / "COCO-InstanceSegmentation" / "mask_rcnn_R_50_FPN_3x.yaml")
    )
    cfg.MODEL.WEIGHTS = ""
    cfg.MODEL.DEVICE = "cpu"
    model = build_model(cfg)
    model.eval()
    return model


def main() -> None:
    model = build_mask_rcnn()
    fields = {
        "proposal_boxes": Boxes,
        "objectness_logits": torch.Tensor,
        "pred_boxes": Boxes,
        "scores": torch.Tensor,
        "pred_classes": torch.Tensor,
        "pred_masks": torch.Tensor,
    }

    scripted = scripting_with_instances(model, fields)
    print(f"Scripted module type: {type(scripted).__name__}")

    with tempfile.TemporaryDirectory(prefix="detectron2_torchscript_") as tmpdir:
        out = Path(tmpdir) / "model.ts"
        print(f"Attempting torch.jit.save -> {out}")
        torch.jit.save(scripted, str(out))
        raise RuntimeError("Expected torch.jit.save() to fail, but it succeeded.")


if __name__ == "__main__":
    main()
