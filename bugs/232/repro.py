#!/usr/bin/env python3
"""Reproduce the NeuralProphet future-regressor null forecast bug."""

from __future__ import annotations

import json

import numpy as np
import pandas as pd
from neuralprophet import NeuralProphet


def summarize_forecast(forecast: pd.DataFrame) -> dict[str, object]:
    yhat_cols = [col for col in forecast.columns if col.startswith("yhat")]
    tail = forecast[["ds"] + yhat_cols].tail(5).copy()
    tail["ds"] = tail["ds"].astype(str)
    return {
        "rows": int(len(forecast)),
        "yhat_columns": yhat_cols,
        "non_null_counts": {col: int(forecast[col].notna().sum()) for col in yhat_cols},
        "tail": tail.to_dict(orient="records"),
    }


def main() -> None:
    np.random.seed(42)
    demo_df = pd.DataFrame(
        {
            "ds": pd.date_range("2022-04-01", "2022-04-30"),
            "y": np.random.random(30),
            "reg": np.random.random(30),
        }
    )

    model = NeuralProphet(n_forecasts=15, n_lags=15, epochs=1)
    model.add_future_regressor("reg")
    model.fit(demo_df, freq="D", progress=None, learning_rate=1e-3)
    forecast = model.predict(demo_df)
    future_summary = summarize_forecast(forecast)

    control = NeuralProphet(n_forecasts=15, n_lags=15, epochs=1)
    control.fit(demo_df[["ds", "y"]], freq="D", progress=None, learning_rate=1e-3)
    control_forecast = control.predict(demo_df[["ds", "y"]])
    control_summary = summarize_forecast(control_forecast)

    result = {
        "future_regressor": future_summary,
        "control": control_summary,
        "reproduced": all(count == 0 for count in future_summary["non_null_counts"].values())
        and any(count > 0 for count in control_summary["non_null_counts"].values()),
    }

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
