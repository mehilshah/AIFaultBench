#!/usr/bin/env python3
"""Minimal check for the reported token/ParquetConfig failure."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import pandas as pd
from datasets import load_dataset


def banner() -> None:
    import datasets
    import huggingface_hub
    import numpy
    import pyarrow

    print("python:", sys.version.split()[0])
    print("datasets:", datasets.__version__)
    print("huggingface_hub:", huggingface_hub.__version__)
    print("numpy:", numpy.__version__)
    print("pyarrow:", pyarrow.__version__)


def check_wikitext() -> None:
    print("checking wikitext load with token=...")
    ds = load_dataset(
        "wikitext",
        "wikitext-2-raw-v1",
        token="dummy-token",
        split="train[:1%]",
    )
    print(f"wikitext rows: {len(ds)}")


def check_parquet() -> None:
    print("checking local parquet load with token=...")
    with tempfile.TemporaryDirectory() as tmpdir:
        parquet_path = Path(tmpdir) / "sample.parquet"
        pd.DataFrame({"x": [1, 2]}).to_parquet(parquet_path)
        ds = load_dataset(
            "parquet",
            data_files=str(parquet_path),
            token="dummy-token",
            split="train",
        )
        print(f"parquet rows: {len(ds)}")


def main() -> int:
    banner()
    try:
        check_wikitext()
        check_parquet()
    except Exception as exc:  # pragma: no cover - explicit repro output
        print(f"unexpected exception: {type(exc).__name__}: {exc}")
        if type(exc).__name__ == "TypeError" and "ParquetConfig" in str(exc):
            print("BUG_REPRODUCED")
            return 1
        return 2

    print("BUG_NOT_REPRODUCED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

