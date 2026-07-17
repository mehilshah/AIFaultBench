import warnings

import torch


def main() -> None:
    print(f"torch={torch.__version__}")
    warnings.simplefilter("error", DeprecationWarning)

    try:
        from deepspeed import DeepSpeedEngine  # noqa: F401
    except DeprecationWarning as exc:
        print("reproduced: DeprecationWarning raised during DeepSpeed import")
        print(exc)
        raise

    print("imported DeepSpeedEngine without warnings")


if __name__ == "__main__":
    main()
