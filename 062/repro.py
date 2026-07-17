#!/usr/bin/env python3
"""Minimal reproduction for keras-io issue 1518.

The bug is triggered by the deprecated pandas DataFrame.append API used in:
codebase/examples/nlp/masked_language_modeling.py:114
"""

from __future__ import annotations

import sys

import pandas as pd


def main() -> int:
    print(f"pandas={pd.__version__}")

    train_df = pd.DataFrame({"review": ["train"], "sentiment": [0]})
    test_df = pd.DataFrame({"review": ["test"], "sentiment": [1]})

    print("About to call train_df.append(test_df)")
    # This matches the failing notebook/script line in the codebase.
    all_data = train_df.append(test_df)
    print(all_data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
