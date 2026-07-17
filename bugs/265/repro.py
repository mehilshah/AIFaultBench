#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
import traceback
from pathlib import Path

import pandas as pd


def main() -> int:
    os.environ.setdefault("DARTS_CONFIGURE_MATPLOTLIB", "0")

    root = Path(__file__).resolve().parent
    sys.path.insert(0, str(root / "codebase"))

    from darts import TimeSeries
    from darts.models import LinearRegressionModel
    from darts.utils.timeseries_generation import datetime_attribute_timeseries

    csv_path = root / "codebase" / "datasets" / "AirPassengers.csv"
    df = pd.read_csv(csv_path)
    df["Month"] = pd.to_datetime(df["Month"])

    series = TimeSeries.from_dataframe(df, time_col="Month", value_cols="#Passengers")
    air_year = datetime_attribute_timeseries(series, attribute="year")
    air_month = datetime_attribute_timeseries(series, attribute="month")
    series = series.drop_before(12).drop_after(120)

    print("Loaded AirPassengers series from local CSV.")
    print("Target length after slicing:", len(series))
    print("Attempting to instantiate LinearRegressionModel with mixed lag types.")

    try:
        LinearRegressionModel(
            lags_past_covariates={"month": [-6]},
            lags_future_covariates=[0],
            output_chunk_shift=1,
        )
        print("Model constructor unexpectedly succeeded.")
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"Reproduced failure: {type(exc).__name__}: {exc}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
