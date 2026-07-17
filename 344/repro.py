#!/usr/bin/env python3
"""Reproduce the PyG legacy ``Data`` deserialization failure.

This script creates a pickle payload that mimics an older PyG ``Data`` object
by omitting the internal ``_store`` attribute, then loads and prints it.
Printing triggers ``Data.__repr__`` which raises the reported RuntimeError.
"""

from __future__ import annotations

import pickle
import sys
from pathlib import Path

import torch


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
LEGACY_PICKLE = ROOT / "legacy_data.pkl"

sys.path.insert(0, str(CODEBASE))

from torch_geometric.data import Data  # noqa: E402


def build_legacy_pickle(path: Path) -> None:
    data = Data(x=torch.tensor([1, 2, 3]))
    # Simulate the state of a Data object pickled by an older PyG release.
    data.__dict__.pop("_store")
    with path.open("wb") as fh:
        pickle.dump(data, fh)


def main() -> None:
    build_legacy_pickle(LEGACY_PICKLE)
    with LEGACY_PICKLE.open("rb") as fh:
        obj = pickle.load(fh)

    print(type(obj), flush=True)
    print(obj, flush=True)


if __name__ == "__main__":
    main()
