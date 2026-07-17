"""Minimal reproduction for SDV issue 2736."""

import pandas as pd

from sdv.cag import Inequality
from sdv.metadata import Metadata
from sdv.multi_table import HMASynthesizer


def make_data():
    parent = pd.DataFrame(
        {
            'id': range(10),
            'l1': range(10),
            'h1': [x + 1 for x in range(10)],
            'l2': [x + 2 for x in range(10)],
            'h2': [x + 3 for x in range(10)],
        }
    )
    child = pd.DataFrame(
        {
            'child_id': range(20),
            'parent_id': [i % 10 for i in range(20)],
            'val': [i * 2 for i in range(20)],
        }
    )
    return {'parent': parent, 'child': child}


def make_metadata():
    metadata_dict = {
        'tables': {
            'parent': {
                'primary_key': 'id',
                'columns': {
                    'id': {'sdtype': 'id'},
                    'l1': {'sdtype': 'numerical'},
                    'h1': {'sdtype': 'numerical'},
                    'l2': {'sdtype': 'numerical'},
                    'h2': {'sdtype': 'numerical'},
                },
            },
            'child': {
                'primary_key': 'child_id',
                'columns': {
                    'child_id': {'sdtype': 'id'},
                    'parent_id': {'sdtype': 'id'},
                    'val': {'sdtype': 'numerical'},
                },
            },
        },
        'relationships': [
            {
                'parent_table_name': 'parent',
                'parent_primary_key': 'id',
                'child_table_name': 'child',
                'child_foreign_key': 'parent_id',
            }
        ],
        'METADATA_SPEC_VERSION': 'MULTI_TABLE_V1',
    }
    return Metadata.load_from_dict(metadata_dict)


def main():
    data = make_data()
    metadata = make_metadata()

    print('control: add both constraints in one call')
    control = HMASynthesizer(metadata)
    control.add_constraints(
        [
            Inequality('l1', 'h1', table_name='parent'),
            Inequality('l2', 'h2', table_name='parent'),
        ]
    )
    control.fit(data)
    print('control: fit succeeded')

    print('bug: add the same constraints in two calls')
    stepwise = HMASynthesizer(metadata)
    stepwise.add_constraints([Inequality('l1', 'h1', table_name='parent')])
    stepwise.add_constraints([Inequality('l2', 'h2', table_name='parent')])
    stepwise.fit(data)


if __name__ == '__main__':
    main()

