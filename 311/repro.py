import json

import pandas as pd

from sdv.cag import OneHotEncoding
from sdv.evaluation.multi_table import run_diagnostic
from sdv.metadata import Metadata
from sdv.multi_table import HMASynthesizer


def build_input_data():
    players = pd.DataFrame(
        {
            'PlayerID': list(range(1, 6)),
            'Age': [21, 22, 23, 24, 25],
        }
    )
    actions = pd.DataFrame(
        {
            'ActionID': list(range(1, 11)),
            'PlayerID': [1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
            'Starts': pd.Series([1, 0] * 5, dtype='int64'),
            'SubstituteOn': pd.Series([0, 1] * 5, dtype='int64'),
            'Minute': [10, 80, 15, 75, 20, 70, 25, 65, 30, 60],
        }
    )

    metadata = Metadata.load_from_dict(
        {
            'tables': {
                'Players': {
                    'primary_key': 'PlayerID',
                    'columns': {
                        'PlayerID': {'sdtype': 'id'},
                        'Age': {'sdtype': 'numerical'},
                    },
                },
                'Actions': {
                    'primary_key': 'ActionID',
                    'columns': {
                        'ActionID': {'sdtype': 'id'},
                        'PlayerID': {'sdtype': 'id'},
                        'Starts': {'sdtype': 'numerical', 'computer_representation': 'Int64'},
                        'SubstituteOn': {
                            'sdtype': 'numerical',
                            'computer_representation': 'Int64',
                        },
                        'Minute': {'sdtype': 'numerical'},
                    },
                },
            },
            'relationships': [
                {
                    'parent_table_name': 'Players',
                    'child_table_name': 'Actions',
                    'parent_primary_key': 'PlayerID',
                    'child_foreign_key': 'PlayerID',
                }
            ],
        }
    )

    return {'Players': players, 'Actions': actions}, metadata


def main():
    real_data, metadata = build_input_data()
    synthesizer = HMASynthesizer(metadata, verbose=False)
    synthesizer.add_constraints(
        [OneHotEncoding(column_names=['Starts', 'SubstituteOn'], table_name='Actions')]
    )

    synthesizer.fit(real_data)
    synthetic_data = synthesizer.sample(scale=1.0)

    metadata.validate_data(synthetic_data)
    synthesizer.validate(synthetic_data)

    diagnostic_report = run_diagnostic(real_data, synthetic_data, metadata, verbose=False)
    data_structure = diagnostic_report.get_details('Data Structure')

    if hasattr(data_structure, 'to_dict'):
        data_structure = data_structure.to_dict()

    payload = {
        'reproducible': bool(diagnostic_report.get_score() < 1.0),
        'diagnostic_score': diagnostic_report.get_score(),
        'data_structure': data_structure,
    }
    print(json.dumps(payload, indent=2, default=str))


if __name__ == '__main__':
    main()
