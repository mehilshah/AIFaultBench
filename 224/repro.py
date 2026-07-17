#!/usr/bin/env python3
"""
Minimal reproduction for ART issue 2473.

This exercises the exact parsing logic used in:
`codebase/art/estimators/object_detection/pytorch_object_detector.py`
for a torchvision version string that contains a pre-release segment.
"""

from types import SimpleNamespace


def main() -> None:
    # Reported failing version from the bug report.
    torchvision = SimpleNamespace(__version__="0.18.1a0+405940f")

    print(f"torchvision.__version__={torchvision.__version__}")
    print("Executing the exact parsing expression from pytorch_object_detector.py:L98")

    # Exact logic from the codebase:
    # list(map(int, torchvision.__version__.lower().split("+", maxsplit=1)[0].split(".")))
    torchvision_version = list(
        map(int, torchvision.__version__.lower().split("+", maxsplit=1)[0].split("."))
    )

    # Unreachable for the reported failing version.
    print(torchvision_version)


if __name__ == "__main__":
    main()
