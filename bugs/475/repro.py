"""Minimal reproduction for SDV issue 2768."""

from __future__ import annotations

import sys
import traceback

from sdv_bootstrap import load_sdv_classes


def main() -> int:
    Metadata, HMASynthesizer, FixedCombinations = load_sdv_classes()

    metadata_example = Metadata.load_from_dict(
        {
            'tables': {
                'table': {
                    'columns': {
                        'id': {'sdtype': 'id'},
                        'street': {'sdtype': 'street_address'},
                        'city': {'sdtype': 'city'},
                        'state': {'sdtype': 'administrative_unit'},
                        'zip': {'sdtype': 'postcode'},
                        'code': {'sdtype': 'categorical'},
                        'description': {'sdtype': 'categorical'},
                    }
                },
                'table_two': {
                    'columns': {
                        'id': {'sdtype': 'id'},
                    }
                },
            }
        }
    )

    metadata_example.add_column_relationship(
        table_name='table',
        relationship_type='address',
        column_names=['street', 'city', 'state', 'zip'],
    )

    print(
        'original_valid_relationships_attr=',
        hasattr(metadata_example.tables['table'], '_valid_column_relationships'),
    )
    print('original_relationships=', metadata_example.tables['table'].column_relationships)

    try:
        synthesizer = HMASynthesizer(metadata_example, locales=['en_US'])
        constraint = FixedCombinations(table_name='table', column_names=['code', 'description'])
        synthesizer.add_constraints(constraints=[constraint])
    except Exception:
        traceback.print_exc()
        return 1

    print('unexpected_success')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
