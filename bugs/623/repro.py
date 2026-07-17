#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import sys
import tempfile
import types
from pathlib import Path

import numpy as np
import pandas as pd
import torch


def _load_asteroid_module(module_name: str, path: Path) -> types.ModuleType:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {module_name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def load_librimix_class() -> type:
    asteroid_spec = importlib.util.find_spec("asteroid")
    if asteroid_spec is None or asteroid_spec.origin is None:
        raise RuntimeError("asteroid must be installed before running this repro")

    asteroid_root = Path(asteroid_spec.origin).resolve().parent

    # Avoid importing asteroid.__init__ and its optional audio stack.
    asteroid_pkg = types.ModuleType("asteroid")
    asteroid_pkg.__path__ = [str(asteroid_root)]
    sys.modules.setdefault("asteroid", asteroid_pkg)

    asteroid_data_pkg = types.ModuleType("asteroid.data")
    asteroid_data_pkg.__path__ = [str(asteroid_root / "data")]
    sys.modules.setdefault("asteroid.data", asteroid_data_pkg)

    _load_asteroid_module("asteroid.data.wham_dataset", asteroid_root / "data" / "wham_dataset.py")
    librimix_module = _load_asteroid_module(
        "asteroid.data.librimix_dataset", asteroid_root / "data" / "librimix_dataset.py"
    )
    return librimix_module.LibriMix


def build_synthetic_minilibri_metadata(root: Path) -> tuple[Path, Path]:
    train_dir = root / "metadata" / "train"
    val_dir = root / "metadata" / "val"
    train_dir.mkdir(parents=True)
    val_dir.mkdir(parents=True)

    # The critical detail is that `length` is serialized as a float, which pandas
    # reads back as numpy.float64.
    row = {
        "mixture_path": "dummy_mix.wav",
        "source_1_path": "dummy_s1.wav",
        "source_2_path": "dummy_s2.wav",
        "length": np.float64(48000.0),
    }
    frame = pd.DataFrame([row])
    frame.to_csv(train_dir / "mini_clean_train.csv", index=False)
    frame.to_csv(val_dir / "mini_clean_val.csv", index=False)
    return train_dir, val_dir


def main() -> None:
    print(f"python={sys.version.split()[0]}")
    print(f"torch={torch.__version__}")
    print(f"numpy={np.__version__}")

    LibriMix = load_librimix_class()
    fixture_root = Path(tempfile.mkdtemp(prefix="bug623_minilibri_"))
    train_dir, val_dir = build_synthetic_minilibri_metadata(fixture_root)

    original_mini_from_download = LibriMix.mini_from_download

    @classmethod
    def fake_mini_from_download(cls, **kwargs):
        return (
            cls(str(train_dir), **kwargs),
            cls(str(val_dir), **kwargs),
        )

    LibriMix.mini_from_download = fake_mini_from_download
    try:
        train_loader, _ = LibriMix.loaders_from_mini(task="sep_clean", batch_size=1, segment=3)
        dataset = train_loader.dataset
        print(f"fixture_root={fixture_root}")
        print(f"length_value={dataset.df.iloc[0]['length']!r}")
        print(f"length_type={type(dataset.df.iloc[0]['length']).__name__}")
        print(f"seg_len={dataset.seg_len!r}")
        print("fetching first batch now")
        next(iter(train_loader))
        print("unexpected: no failure")
    finally:
        LibriMix.mini_from_download = original_mini_from_download


if __name__ == "__main__":
    main()
