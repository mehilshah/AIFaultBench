#!/usr/bin/env python3
"""Reproduce the ResNet50 pretrained-from-file state_dict key mismatch."""

from __future__ import annotations

import tempfile
import traceback
from pathlib import Path
import sys

import torch


ROOT = Path(__file__).resolve().parent
CONVNETS_ROOT = ROOT / "codebase" / "PyTorch" / "Classification" / "ConvNets"
if str(CONVNETS_ROOT) not in sys.path:
    sys.path.insert(0, str(CONVNETS_ROOT))

from image_classification.models import resnet50  # noqa: E402


def remap_to_legacy_keys(state_dict: dict[str, torch.Tensor]) -> dict[str, torch.Tensor]:
    """Convert current `layers.*` keys into the legacy `layerN.*` layout."""

    renamed = {}
    for key, value in state_dict.items():
        if key.startswith("layers."):
            parts = key.split(".")
            layer_index = int(parts[1]) + 1
            renamed_key = ".".join([f"layer{layer_index}"] + parts[2:])
        else:
            renamed_key = key
        renamed[renamed_key] = value
    return renamed


def make_checkpoint(path: Path) -> None:
    """Create a synthetic checkpoint with the legacy checkpoint naming scheme."""

    model = resnet50(pretrained=False)
    current_state = model.state_dict()
    legacy_state = remap_to_legacy_keys(current_state)
    torch.save(legacy_state, path)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="resnet50_repro_") as tmpdir:
        checkpoint_path = Path(tmpdir) / "nvidia_resnet50_200821.pth.tar"
        make_checkpoint(checkpoint_path)

        print(f"checkpoint={checkpoint_path}")
        print("loading via resnet50(pretrained_from_file=...)")
        try:
            resnet50(pretrained=False, pretrained_from_file=str(checkpoint_path))
        except RuntimeError as exc:
            print("EXPECTED_RUNTIME_ERROR")
            print(str(exc))
            return 1
        except Exception:
            print("UNEXPECTED_EXCEPTION")
            traceback.print_exc()
            return 2

        print("UNEXPECTED_SUCCESS")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
