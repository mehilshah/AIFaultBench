"""Minimal reproduction for SDV issue 2711.

This mirrors the `HMASynthesizer._clear_nans` branch in
`codebase/sdv/multi_table/hma.py:378-383`.
"""

from __future__ import annotations

import json
import warnings

import pandas as pd


def clear_nans_like_hma(table_data: pd.DataFrame, ignore_cols=None) -> None:
    """Apply the same fillna logic used by HMA's `_clear_nans` helper."""
    columns = set(table_data.columns)
    if ignore_cols is not None:
        columns = columns - set(ignore_cols)

    for column in columns:
        column_data = table_data[column]
        if column_data.dtype in (int, float):
            fill_value = 0 if column_data.isna().all() else column_data.mean()
        else:
            fill_value = column_data.mode()[0]

        table_data[column] = table_data[column].fillna(fill_value)


def main() -> int:
    # Object-dtype numerics are enough to trigger the pandas 2.2.x warning.
    frame = pd.DataFrame({'value': pd.Series([1, None], dtype='object')})

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always', FutureWarning)
        clear_nans_like_hma(frame)

    messages = [str(item.message) for item in caught]
    payload = {
        'caught_warning_count': len(caught),
        'warnings': messages,
        'result_dtype': str(frame['value'].dtype),
        'result_values': frame['value'].tolist(),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))

    if not any('Downcasting object dtype arrays on .fillna' in message for message in messages):
        raise SystemExit('Expected pandas FutureWarning was not emitted.')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
