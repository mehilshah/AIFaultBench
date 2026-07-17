#!/usr/bin/env python3
"""Minimal reproducer for overlapping single-table constraints in HMASynthesizer."""

import numpy as np
import pandas as pd

from sdv.cag import Inequality
from sdv.metadata import Metadata
from sdv.multi_table import HMASynthesizer


def main():
    parent = pd.DataFrame(
        {
            'id': np.arange(20),
            'colA': np.arange(20),
        }
    )
    parent['colB'] = parent['colA'] + 1
    parent['colC'] = parent['colB'] + 1

    child = pd.DataFrame(
        {
            'parent_id': np.arange(100) % 20,
            'colD': np.arange(100, 200),
        }
    )

    data = {'parent': parent, 'child': child}
    metadata = Metadata.detect_from_dataframes(data)

    synthesizer = HMASynthesizer(metadata)
    constraint1 = Inequality(low_column_name='colA', high_column_name='colB', table_name='parent')
    constraint2 = Inequality(low_column_name='colB', high_column_name='colC', table_name='parent')

    print('before add_constraints')
    synthesizer.add_constraints([constraint1, constraint2])
    print('after add_constraints')


if __name__ == '__main__':
    main()
