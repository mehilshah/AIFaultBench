#!/usr/bin/env python3
from __future__ import annotations

import json

import cv2
import numpy as np
import torch

from detectron2.structures import Instances, RotatedBoxes, pairwise_iou_rotated
from detectron2.utils.visualizer import Visualizer


def main() -> None:
    boxes1 = torch.tensor([[160.0, 153.0, 230.0, 23.0, -37.0]], dtype=torch.float32)
    boxes2 = torch.tensor([[190.0, 127.0, 80.0, 21.0, -46.0]], dtype=torch.float32)

    iou = pairwise_iou_rotated(RotatedBoxes(boxes1), RotatedBoxes(boxes2))
    expected = torch.zeros_like(iou)

    instances = Instances((300, 300))
    instances.pred_boxes = RotatedBoxes(torch.cat((boxes1, boxes2)))
    instances.scores = torch.tensor([1.0, 1.0], dtype=torch.float32)
    instances.pred_classes = torch.tensor([0, 0], dtype=torch.int64)
    viz = Visualizer(np.full((300, 300, 3), 127, dtype=np.uint8), {"thing_classes": ["thing"]})
    image = viz.draw_instance_predictions(instances).get_image()[:, :, ::-1]
    wrote_image = cv2.imwrite("out.png", image)

    payload = {
        "boxes1": boxes1.tolist(),
        "boxes2": boxes2.tolist(),
        "actual_iou": iou.tolist(),
        "expected_iou": expected.tolist(),
        "matches_expected": bool(torch.allclose(iou, expected)),
        "wrote_image": wrote_image,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
