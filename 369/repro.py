from detectron2.structures import BoxMode, RotatedBoxes, pairwise_iou_rotated
import torch


def main():
    dt = RotatedBoxes(
        torch.tensor(
            [
                [
                    296.6620178222656,
                    458.73883056640625,
                    23.515729904174805,
                    47.677001953125,
                    0.08795166015625,
                ]
            ]
        )
    )

    gt1 = RotatedBoxes(
        torch.tensor([[296.66201, 458.73882000000003, 23.51573, 47.67702, 0.087951]])
    )
    iou1 = pairwise_iou_rotated(dt, gt1)
    print(f"iou1: {iou1.item():.6f}")

    gt2 = RotatedBoxes(
        torch.tensor([[296.66201, 458.73882000000003, 23.51573, 47.6770, 0.087951]])
    )
    iou2 = pairwise_iou_rotated(dt, gt2)
    print(f"iou2: {iou2.item():.6f}")

    if not torch.isclose(iou1, torch.ones_like(iou1)).item() or not torch.isclose(
        iou2, torch.ones_like(iou2)
    ).item():
        raise AssertionError("Expected both IoUs to be 1.0")


if __name__ == "__main__":
    main()
