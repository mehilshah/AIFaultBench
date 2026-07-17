import warnings

import pandas as pd
from sdv.metadata import Metadata
from sdv.multi_table import HMASynthesizer


def main():
    composite_data = {
        'main': pd.DataFrame(
            {
                'pk': [1, 2, 3, 4, 5],
                'denormalized_primary_key_1': [1, 1, 2, 2, 5],
                'denormalized_primary_key_2': ['a', 'a', 'b', 'c', 'c'],
                'denormalized_column': [
                    '2020-01-01',
                    '2020-01-01',
                    '2020-01-02',
                    '2020-01-02',
                    '2020-01-03',
                ],
                'other_col': [
                    '2020-01-01',
                    '2020-01-02',
                    '2020-01-03',
                    '2020-01-04',
                    '2020-01-05',
                ],
            }
        )
    }

    composite_metadata = Metadata.load_from_dict(
        {
            'tables': {
                'main': {
                    'columns': {
                        'pk': {'sdtype': 'id'},
                        'denormalized_primary_key_1': {'sdtype': 'id'},
                        'denormalized_primary_key_2': {'sdtype': 'categorical'},
                        'denormalized_column': {'sdtype': 'datetime'},
                        'other_col': {
                            'sdtype': 'datetime',
                            'datetime_format': '%Y-%m-%d',
                        },
                    },
                    'primary_key': 'pk',
                },
            },
        }
    )

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        synthesizer = HMASynthesizer(composite_metadata, verbose=False)
        synthesizer.fit(composite_data)
        synthesizer.sample(1)

    datetime_warnings = [
        warning for warning in caught if "No 'datetime_format' is present" in str(warning.message)
    ]

    print(f'total_captured_warnings={len(caught)}')
    print(f'datetime_warning_count={len(datetime_warnings)}')
    for index, warning in enumerate(datetime_warnings, start=1):
        print(f'datetime_warning_{index}={warning.message}')

    if len(datetime_warnings) <= 1:
        raise SystemExit('Expected the missing datetime_format warning to be emitted multiple times.')


if __name__ == '__main__':
    main()
