#!/usr/bin/env python3
"""Minimal reproduction for repeated SingleTableMetadata warnings in HMASynthesizer.sample()."""

from __future__ import annotations

import json
import warnings

import pandas as pd
from sdv.metadata import MultiTableMetadata
from sdv.multi_table import HMASynthesizer


def build_demo_data():
    """Create a tiny parent/child hierarchy that still exercises the sampling path."""
    parent = pd.DataFrame(
        {
            'parent_id': [1, 2, 3, 4, 5, 6],
            'value': [10.0, 20.0, 30.0, 40.0, 50.0, 60.0],
        }
    )
    child = pd.DataFrame(
        {
            'child_id': list(range(100, 112)),
            'parent_id': [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6],
            'amount': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2],
        }
    )

    metadata = MultiTableMetadata()
    metadata.add_table('parent')
    metadata.add_column('parent', 'parent_id', sdtype='id')
    metadata.set_primary_key('parent', 'parent_id')
    metadata.add_column('parent', 'value', sdtype='numerical')

    metadata.add_table('child')
    metadata.add_column('child', 'child_id', sdtype='id')
    metadata.set_primary_key('child', 'child_id')
    metadata.add_column('child', 'parent_id', sdtype='id')
    metadata.add_column('child', 'amount', sdtype='numerical')
    metadata.add_relationship('parent', 'child', 'parent_id', 'parent_id')

    return {'parent': parent, 'child': child}, metadata


def collect_warnings(func):
    """Run `func` with warnings captured and returned as plain strings."""
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        result = func()
        warning_texts = [f'{type(item.message).__name__}: {item.message}' for item in caught]

    return result, warning_texts


def main():
    data, metadata = build_demo_data()

    synthesizer, init_warnings = collect_warnings(
        lambda: HMASynthesizer(metadata, verbose=False)
    )
    _, fit_warnings = collect_warnings(lambda: synthesizer.fit(data))
    sample, sample_warnings = collect_warnings(lambda: synthesizer.sample())

    report = {
        'init_warning_count': len(init_warnings),
        'fit_warning_count': len(fit_warnings),
        'sample_warning_count': len(sample_warnings),
        'init_warnings': init_warnings,
        'fit_warnings': fit_warnings,
        'sample_warnings': sample_warnings,
        'sample_shapes': {table_name: list(frame.shape) for table_name, frame in sample.items()},
    }
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
