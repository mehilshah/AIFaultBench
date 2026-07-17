#!/usr/bin/env python3
"""Minimal reproduction for the OneHotEncoding / integer computer_representation bug."""

from pathlib import Path
import sys
import traceback

import pandas as pd

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'codebase'))

from sdv.cag import OneHotEncoding
from sdv.metadata import Metadata
from sdv.single_table import GaussianCopulaSynthesizer


def main():
    data = pd.DataFrame(
        {
            'a': [1, 0, 0],
            'b': [0, 1, 0],
            'c': [0, 0, 1],
        }
    )

    metadata = Metadata.detect_from_dataframe(data, table_name='table')
    metadata.update_columns(
        ['a', 'b', 'c'], sdtype='numerical', computer_representation='Int64'
    )

    print('metadata:', metadata.to_dict())

    synthesizer = GaussianCopulaSynthesizer(metadata)
    synthesizer.add_constraints([OneHotEncoding(column_names=['a', 'b', 'c'])])
    print('starting fit')
    try:
        synthesizer.fit(data)
    except Exception as exc:  # noqa: BLE001
        print(f'caught: {type(exc).__name__}: {exc}')
        traceback.print_exc()
        raise

    print('fit completed successfully')


if __name__ == '__main__':
    main()
