#!/usr/bin/env python3
"""Minimal reproduction for the TorchRL Minari cache-path bug.

The issue in `codebase/torchrl/data/datasets/minari_data.py` is that the code
downloads a dataset with `MINARI_DATASETS_PATH` pointing at a temporary cache,
then restores the environment before calling `minari.load_dataset(...)`.
That makes the metadata lookup consult the wrong cache location.

This script mirrors that control flow with a tiny fake Minari implementation so
the failure is reproducible without heavyweight ML dependencies.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile


DATASET_ID = "D4RL/door/human-v2"


class FakeMinari:
    def download_dataset(self, dataset_id: str) -> None:
        cache_root = Path(os.environ["MINARI_DATASETS_PATH"])
        dataset_dir = cache_root / dataset_id / "data"
        dataset_dir.mkdir(parents=True, exist_ok=True)
        (dataset_dir / "main_data.hdf5").write_text("placeholder")
        (cache_root / dataset_id / "spec.json").write_text(
            json.dumps({"dataset_id": dataset_id})
        )
        print(f"downloaded dataset into {dataset_dir}")

    def load_dataset(self, dataset_id: str) -> dict[str, str]:
        cache_root = Path(
            os.environ.get("MINARI_DATASETS_PATH", os.path.expanduser("~/.minari/datasets"))
        )
        file_path = cache_root / dataset_id
        data_path = file_path / "data"
        print(f"minari.load_dataset sees cache root: {cache_root}")
        if not data_path.exists():
            raise FileNotFoundError(
                f"Dataset {dataset_id} not found locally at {file_path}. "
                "Use download=True to download the dataset."
            )
        return {"dataset_id": dataset_id}


def reproduce_bug() -> None:
    """Mirror the buggy env handling in `MinariExperienceReplay._download_and_preproc`."""

    minari = FakeMinari()
    prev_minari_datasets_path_save = prev_minari_datasets_path = os.environ.get(
        "MINARI_DATASETS_PATH"
    )
    try:
        if prev_minari_datasets_path is None:
            prev_minari_datasets_path = os.path.expanduser("~/.minari/datasets")
        with tempfile.TemporaryDirectory() as tmpdir:
            print(f"initial MINARI_DATASETS_PATH: {prev_minari_datasets_path_save!r}")
            print(f"temporary download cache: {tmpdir}")

            prev_minari_datasets_path_save2 = os.environ.get("MINARI_DATASETS_PATH")
            os.environ["MINARI_DATASETS_PATH"] = tmpdir
            try:
                minari.download_dataset(dataset_id=DATASET_ID)
            finally:
                if prev_minari_datasets_path_save2 is not None:
                    os.environ["MINARI_DATASETS_PATH"] = prev_minari_datasets_path_save2
                else:
                    os.environ.pop("MINARI_DATASETS_PATH", None)

            # This is the buggy line pattern from the codebase:
            # after restoring the env, the metadata read no longer points at tmpdir.
            print(
                "about to load dataset metadata after restoring MINARI_DATASETS_PATH"
            )
            minari.load_dataset(DATASET_ID)
    finally:
        if prev_minari_datasets_path_save is not None:
            os.environ["MINARI_DATASETS_PATH"] = prev_minari_datasets_path_save
        else:
            os.environ.pop("MINARI_DATASETS_PATH", None)


if __name__ == "__main__":
    reproduce_bug()
