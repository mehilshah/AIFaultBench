#!/usr/bin/env python3
"""Reproduce the reported SDV metadata primary-key error."""

from __future__ import annotations

import importlib
import json
import sys
import types
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODEBASE_SDV = ROOT / 'codebase' / 'sdv'
EXPECTED_MESSAGE = "InvalidMetadataError: The primary_keys [['col1', 'col2']] must have a column of type 'id' or another PII type."


def _load_metadata_class():
    """Import ``Metadata`` without executing the top-level ``sdv.__init__``."""
    if 'sdv' not in sys.modules:
        package = types.ModuleType('sdv')
        package.__path__ = [str(CODEBASE_SDV)]
        sys.modules['sdv'] = package

    if 'sdv.version' not in sys.modules:
        version_module = types.ModuleType('sdv.version')
        version_module.community = '0.0.0'
        version_module.enterprise = None
        sys.modules['sdv.version'] = version_module

    metadata_module = importlib.import_module('sdv.metadata')
    return metadata_module.Metadata


def main() -> int:
    Metadata = _load_metadata_class()

    account_metadata = Metadata.load_from_dict(
        {
            'tables': {
                'accounts': {
                    'columns': {
                        'user_id': {'sdtype': 'id', 'regex_format': 'ID_[0-9]{1,2}'},
                        'account_type': {'sdtype': 'categorical'},
                        'col1': {'sdtype': 'numerical'},
                        'col2': {'sdtype': 'numerical'},
                    }
                }
            }
        }
    )

    observed_exception = None
    observed_message = None
    try:
        account_metadata.set_primary_key(['col1', 'col2'])
    except Exception as exc:  # noqa: BLE001 - capture the exact runtime behavior
        observed_exception = type(exc).__name__
        observed_message = str(exc)

    reproduced = f"{observed_exception}: {observed_message}" == EXPECTED_MESSAGE
    evidence = {
        'expected': EXPECTED_MESSAGE,
        'observed': f'{observed_exception}: {observed_message}',
    }
    result = {
        'reproducible': reproduced,
        'evidence': evidence,
        'steps': [
            'Loaded SDV metadata from a dict with one table and two numerical columns.',
            "Called Metadata.set_primary_key(['col1', 'col2']).",
            f'Observed {observed_exception}: {observed_message}',
        ],
        'blocking_reason': (
            "The checkout raises 'primary_key' must be a string instead of the nested-list "
            'message described in the report.'
            if not reproduced
            else ''
        ),
        'reproduction_command': 'bash setup_env.sh && bash run_repro.sh',
    }

    result_path = ROOT / 'reproduction.json'
    result_path.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')

    print(json.dumps(evidence, indent=2))
    return 0 if reproduced else 1


if __name__ == '__main__':
    raise SystemExit(main())
