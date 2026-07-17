import sys

import pandas as pd

from sdv.metadata import Metadata
from sdv.single_table import DayZSynthesizer
from sdv.errors import SynthesizerProcessingError


def main() -> int:
    data = pd.DataFrame(
        {
            'id': [1, 2, 3],
            'value': [10.1, 20.2, 30.3],
            'category': ['a', 'b', 'a'],
            'event_date': ['01 Jan 2020', '02 Jan 2020', '03 Jan 2020'],
        }
    )

    metadata = Metadata.load_from_dict(
        {
            'tables': {
                'table': {
                    'columns': {
                        'id': {'sdtype': 'id'},
                        'value': {'sdtype': 'numerical'},
                        'category': {'sdtype': 'categorical'},
                        'event_date': {'sdtype': 'datetime', 'datetime_format': '%d %b %Y'},
                    }
                }
            }
        }
    )

    dayz_parameters = DayZSynthesizer.create_parameters(data, metadata)
    dayz_parameters['DAYZ_SPEC_VERSION'] = 'V1000'

    try:
        DayZSynthesizer.validate_parameters(metadata, dayz_parameters)
    except SynthesizerProcessingError as error:
        print(f'RAISED: {type(error).__name__}: {error}')
        return 1

    print('NO_ERROR')
    print(dayz_parameters['DAYZ_SPEC_VERSION'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
