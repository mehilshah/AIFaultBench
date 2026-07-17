#!/usr/bin/env python3
"""Minimal reproduction for keras-io issue 1489.

The original example calls `show_heatmap(df)` where `df` still contains the
`Date Time` string column. `DataFrame.corr()` then tries to coerce that column
to float and raises `ValueError`.
"""

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


def show_heatmap(data):
    print("Data columns:", list(data.columns), flush=True)
    print("Calling data.corr() from show_heatmap(...)", flush=True)
    plt.matshow(data.corr())


def main():
    df = pd.DataFrame(
        {
            "Date Time": [
                "01.01.2009 00:10:00",
                "01.01.2009 00:20:00",
                "01.01.2009 00:30:00",
            ],
            "p (mbar)": [996.52, 996.84, 997.13],
            "T (degC)": [-8.02, -8.41, -8.29],
        }
    )
    print(f"pandas version: {pd.__version__}", flush=True)
    show_heatmap(df)


if __name__ == "__main__":
    main()
