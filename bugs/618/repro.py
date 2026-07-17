#!/usr/bin/env python3
"""Reproduce SDV issue 2702."""

from __future__ import annotations

import json
from typing import Any

import pandas as pd

from sdv.metadata import Metadata
from sdv.multi_table import DayZSynthesizer


def run_case(name: str, data: pd.DataFrame, metadata: Metadata) -> dict[str, Any]:
    """Run one parameter-detection case and capture the outcome."""
    print(f"CASE: {name}")
    print("METADATA:", json.dumps(metadata.to_dict(), indent=2, default=str))

    try:
        parameters = DayZSynthesizer.create_parameters(data, metadata)
    except Exception as exc:  # noqa: BLE001 - reproduce the public API failure directly
        print(f"RESULT: {type(exc).__name__}: {exc}")
        return {
            'case': name,
            'status': 'exception',
            'exception_type': type(exc).__name__,
            'exception_message': str(exc),
        }

    print("RESULT: success")
    print(json.dumps(parameters, indent=2, default=str))
    return {
        'case': name,
        'status': 'success',
        'parameters': parameters,
    }


def main() -> int:
    """Exercise the reported edge cases."""
    cases = []

    empty_data = pd.DataFrame({'col': []})
    empty_metadata = Metadata().detect_from_dataframe(empty_data)
    cases.append(run_case('empty_rows_detected_metadata', empty_data, empty_metadata))

    null_numeric_data = pd.DataFrame({'col': [None, None]})
    null_numeric_metadata = Metadata.load_from_dict(
        {
            'METADATA_SPEC_VERSION': 'V1',
            'tables': {
                'table': {
                    'columns': {
                        'col': {'sdtype': 'numerical'},
                    }
                }
            },
        }
    )
    cases.append(run_case('all_null_numerical', null_numeric_data, null_numeric_metadata))

    null_datetime_data = pd.DataFrame({'col': [None, None]})
    null_datetime_metadata = Metadata.load_from_dict(
        {
            'METADATA_SPEC_VERSION': 'V1',
            'tables': {
                'table': {
                    'columns': {
                        'col': {'sdtype': 'datetime', 'datetime_format': '%Y-%m-%d'},
                    }
                }
            },
        }
    )
    cases.append(run_case('all_null_datetime', null_datetime_data, null_datetime_metadata))

    summary = {'cases': cases}
    print("SUMMARY:", json.dumps(summary, indent=2, default=str))

    if all(case['status'] == 'exception' for case in cases):
        print('BUG REPRODUCED: all targeted cases raised exceptions instead of falling back.')
        return 0

    print('BUG NOT REPRODUCED: at least one targeted case returned parameters.')
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
