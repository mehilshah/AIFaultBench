import torch
import kornia.augmentation as K


def main() -> None:
    # Use a 4D tensor to exercise the augmentation path directly.
    x = torch.arange(100, dtype=torch.float32).reshape(1, 1, 10, 10)
    aug = K.PadTo((5, 5), pad_value=0)
    out = aug(x)

    print(f"input_shape={tuple(x.shape)}")
    print(f"output_shape={tuple(out.shape)}")
    print(f"matches_top_left_crop={torch.equal(out, x[..., :5, :5])}")
    print("output_tensor=")
    print(out[0, 0])

    # The reported bug is that smaller PadTo sizes crop the image instead of
    # either erroring out or returning the original image unchanged.
    if not torch.equal(out, x):
        raise AssertionError(
            "PadTo((5, 5)) on a 10x10 input should not crop the image or change "
            f"its contents, but returned shape {tuple(out.shape)}."
        )


if __name__ == "__main__":
    main()
