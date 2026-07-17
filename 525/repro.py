#!/usr/bin/env python3
from __future__ import annotations

import sys
import tempfile
from pathlib import Path
import traceback

import torch
from PIL import Image

from timm.data.dataset_factory import create_dataset


def build_minimal_imagenet_root(root: Path) -> None:
    val_class_dir = root / "val" / "n00000000"
    val_class_dir.mkdir(parents=True, exist_ok=True)

    image_path = val_class_dir / "0.jpg"
    image = Image.new("RGB", (1, 1), color=(255, 0, 0))
    image.save(image_path)

    # torchvision.datasets.ImageNet expects this metadata file to exist before it
    # instantiates ImageFolder. The actual contents are only needed to get past the
    # metadata load step in this minimal reproduction.
    torch.save(({"n00000000": ("dummy class",)}, ["n00000000"]), root / "meta.bin")


def main() -> int:
    print(f"python={sys.version.split()[0]}")
    print(f"torch={torch.__version__}")
    try:
        import torchvision

        print(f"torchvision={torchvision.__version__}")
    except Exception as exc:  # pragma: no cover - defensive logging
        print(f"torchvision import failed: {exc}", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory(prefix="imagenet-repro-") as tmpdir:
        root = Path(tmpdir)
        build_minimal_imagenet_root(root)
        print(f"imagenet_root={root}")

        try:
            ds = create_dataset("torch/imagenet", root=str(root))
        except TypeError as exc:
            print(f"caught TypeError: {exc}")
            traceback.print_exc()
            if "unexpected keyword argument 'download'" in str(exc):
                print("reproduced: torchvision ImageFolder rejects the forwarded download kwarg")
                return 0
            raise
        except Exception as exc:
            print(f"unexpected exception: {type(exc).__name__}: {exc}", file=sys.stderr)
            raise

        print(f"dataset_created: {type(ds).__name__}, len={len(ds)}")
        print("bug not reproduced")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
