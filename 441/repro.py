from __future__ import annotations

from stubs import load_transforms_module


def main() -> None:
    transforms = load_transforms_module()
    resize_keep_ratio = transforms.ResizeKeepRatio(
        size=224,
        random_scale_range=(0.50, 1.20),
        random_aspect_range=(0.90, 1.10),
    )
    observed = repr(resize_keep_ratio)
    expected_fragment = "random_scale_range=(0.500, 1.200)"

    print("Observed repr:")
    print(observed)
    print()
    print("Expected fragment:")
    print(expected_fragment)
    print()
    print("Bug reproduced:", expected_fragment not in observed)

    assert expected_fragment in observed, observed


if __name__ == "__main__":
    main()
