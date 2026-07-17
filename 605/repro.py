#!/usr/bin/env python3
"""Minimal reproduction for SDV DayZ validation edge cases."""

from __future__ import annotations

import json
from copy import deepcopy

from sdv.errors import SynthesizerProcessingError
from sdv.metadata import Metadata
from sdv.multi_table.dayz import DayZSynthesizer as MultiTableDayZ
from sdv.single_table.dayz import DayZSynthesizer as SingleTableDayZ


def build_metadata() -> Metadata:
    """Build a compact multi-table metadata object."""
    return Metadata.load_from_dict(
        {
            'tables': {
                'district': {
                    'columns': {'district_id': {'sdtype': 'id'}},
                    'primary_key': 'district_id',
                },
                'account': {
                    'columns': {
                        'account_id': {'sdtype': 'id'},
                        'district_id': {'sdtype': 'id'},
                    },
                    'primary_key': 'account_id',
                },
            },
            'relationships': [
                {
                    'parent_table_name': 'district',
                    'parent_primary_key': 'district_id',
                    'child_table_name': 'account',
                    'child_foreign_key': 'district_id',
                }
            ],
        }
    )


def build_parameters() -> dict:
    """Build a valid DayZ parameter dictionary."""
    return {
        'DAYZ_SPEC_VERSION': 'V1',
        'tables': {
            'district': {
                'num_rows': 1,
                'columns': {'district_id': {'missing_values_proportion': 0.0}},
            },
            'account': {
                'num_rows': 1,
                'columns': {
                    'account_id': {'missing_values_proportion': 0.0},
                    'district_id': {'missing_values_proportion': 0.0},
                },
            },
        },
        'relationships': [
            {
                'parent_table_name': 'district',
                'parent_primary_key': 'district_id',
                'child_table_name': 'account',
                'child_foreign_key': 'district_id',
            }
        ],
    }


def run_case(label, func):
    """Execute a case and report its outcome."""
    print(label)
    try:
        func()
    except Exception as exc:  # noqa: BLE001 - deliberate repro harness
        print(f'  exception={type(exc).__name__}')
        print(f'  message={exc}')
        return type(exc).__name__, str(exc)

    print('  result=NO_EXCEPTION')
    return None, None


def main() -> None:
    metadata = build_metadata()
    base_parameters = build_parameters()

    results = {}

    case1_parameters = deepcopy(base_parameters)
    case1_parameters.pop('relationships')
    results['single_table_accepts_multi_table_metadata_without_relationships'] = run_case(
        'case1: single-table validation with multi-table metadata and no relationships',
        lambda: SingleTableDayZ.validate_parameters(metadata, case1_parameters),
    )

    case2_parameters = deepcopy(base_parameters)
    case2_parameters['relationships'] = ['a', 'b', 'c']
    results['invalid_relationship_entries_raise_structured_error'] = run_case(
        "case2: invalid 'relationships' entries",
        lambda: MultiTableDayZ.validate_parameters(metadata, case2_parameters),
    )

    case3_parameters = deepcopy(base_parameters)
    case3_parameters['relationships'][0]['min_cardinality'] = 0
    results['min_cardinality_zero_is_allowed'] = run_case(
        "case3: 'min_cardinality' set to zero",
        lambda: MultiTableDayZ.validate_parameters(metadata, case3_parameters),
    )

    reproducible = (
        results['single_table_accepts_multi_table_metadata_without_relationships'][0] is None
        and results['invalid_relationship_entries_raise_structured_error'][0] == 'AttributeError'
    )
    summary = {
        'reproducible': reproducible,
        'results': results,
    }
    print('summary=' + json.dumps(summary, sort_keys=True))


if __name__ == '__main__':
    main()
