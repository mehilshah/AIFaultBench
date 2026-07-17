#!/usr/bin/env python3
"""Reproduce the conditional-sampling-on-unfitted-synthesizer bug."""

from __future__ import annotations

import importlib
import sys
import types
from pathlib import Path
import traceback


def _install_sdv_package_shim() -> None:
    """Expose the local `codebase/sdv` tree without executing `sdv.__init__`."""
    repo_root = Path(__file__).resolve().parent
    sdv_root = repo_root / 'codebase' / 'sdv'
    package = types.ModuleType('sdv')
    package.__path__ = [str(sdv_root)]
    package.__file__ = str(sdv_root / '__init__.py')
    sys.modules['sdv'] = package

    single_table = types.ModuleType('sdv.single_table')
    single_table.__path__ = [str(sdv_root / 'single_table')]
    single_table.__file__ = str(sdv_root / 'single_table' / '__init__.py')
    sys.modules['sdv.single_table'] = single_table


_install_sdv_package_shim()

download_demo = importlib.import_module('sdv.datasets.demo').download_demo
Condition = importlib.import_module('sdv.sampling.tabular').Condition
GaussianCopulaSynthesizer = importlib.import_module(
    'sdv.single_table.copulas'
).GaussianCopulaSynthesizer


def main() -> int:
    data, metadata = download_demo(
        modality='single_table',
        dataset_name='fake_hotel_guests',
    )
    print(f'demo_shape={data.shape}')

    synthesizer = GaussianCopulaSynthesizer(metadata)
    conditions = [
        Condition(num_rows=454, column_values={'room_type': 'BASIC'}),
        Condition(num_rows=455, column_values={'room_type': 'DELUXE'}),
    ]

    try:
        synthesizer.sample_from_conditions(
            max_tries_per_batch=100000,
            batch_size=1000,
            conditions=conditions,
        )
    except Exception as error:
        print(f'exception_type={type(error).__name__}')
        print(f'exception_message={error}')
        print(f'cause_type={type(error.__cause__).__name__ if error.__cause__ else None}')
        print(f'cause_message={error.__cause__}')
        traceback.print_exc()
        return 0

    print('unexpected_success')
    return 2


if __name__ == '__main__':
    raise SystemExit(main())
