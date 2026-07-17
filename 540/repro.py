import traceback

import numpy as np
import pandas as pd

from sdv.metadata import Metadata
from sdv.sequential import PARSynthesizer


def main():
    data = pd.DataFrame(
        data={
            'sequence': ['id-0'] * 3 + ['id-1'] * 4 + ['id-2'] * 3,
            'context1': ['M'] * 3 + ['F'] * 4 + ['M'] * 3,
            'context2': [12.0] * 3 + [np.nan] * 4 + [34.0] * 3,
            'seq1': [12, 34, 12, 78, 12, 56, 34, 78, 12, 67],
            'seq2': ['Yes', 'Yes', 'No', 'No', 'No', 'No', 'Yes', 'Yes', 'No', 'No'],
        }
    )

    metadata = Metadata.load_from_dict(
        {
            'tables': {
                'table': {
                    'columns': {
                        'sequence': {'sdtype': 'id'},
                        'context1': {'sdtype': 'categorical'},
                        'context2': {'sdtype': 'numerical'},
                        'seq1': {'sdtype': 'numerical'},
                        'seq2': {'sdtype': 'categorical'},
                    },
                    'sequence_key': 'sequence',
                }
            }
        }
    )

    synthesizer = PARSynthesizer(
        metadata,
        context_columns=['context2', 'context1'],
        epochs=1,
        sample_size=1,
        cuda=False,
        verbose=False,
    )

    print('sdv import ok')
    print('init ok')

    try:
        synthesizer.fit(data)
    except Exception as exc:
        print(type(exc).__name__, exc)
        traceback.print_exc()
        return 1

    print('fit ok')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
