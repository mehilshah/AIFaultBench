#!/usr/bin/env python3
"""Reproduce the HMASynthesizer PerformanceAlert column-count display bug."""

from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
import types
from pathlib import Path
from unittest.mock import patch
import sys


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / 'codebase'

def register_package(name, **attributes):
    package = types.ModuleType(name)
    package.__path__ = [str(CODEBASE.joinpath(*name.split('.')))]
    package.__package__ = name
    for key, value in attributes.items():
        setattr(package, key, value)
    sys.modules.setdefault(name, package)


register_package('sdv')
register_package(
    'sdv.metadata',
    Metadata=type('Metadata', (), {}),
    MultiTableMetadata=type('MultiTableMetadata', (), {}),
    SingleTableMetadata=type('SingleTableMetadata', (), {}),
)
register_package('sdv.multi_table')
register_package('sdv.single_table')

version_module = types.ModuleType('sdv.version')
version_module.community = '1.27.1.dev0'
version_module.enterprise = None
version_module.__all__ = ('community', 'enterprise')
sys.modules.setdefault('sdv.version', version_module)

from sdv.metadata.metadata import Metadata
from sdv.multi_table.hma import HMASynthesizer


def build_metadata():
    """Return the smallest valid metadata needed to construct an HMA synthesizer."""
    return Metadata.load_from_dict(
        {
            'tables': {
                'table': {
                    'columns': {
                        'id': {'sdtype': 'id'},
                        'value': {'sdtype': 'numerical'},
                    },
                    'primary_key': 'id',
                }
            },
            'relationships': [],
        }
    )


def main():
    metadata = build_metadata()
    huge_count = 10**30

    stdout_buffer = StringIO()
    stderr_buffer = StringIO()
    with patch.object(
        HMASynthesizer, '_estimate_num_columns', return_value={'table': huge_count}
    ), patch.object(HMASynthesizer, '_get_distributions', return_value={'table': None}), redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
        HMASynthesizer(metadata)

    stdout_text = stdout_buffer.getvalue()
    stderr_text = stderr_buffer.getvalue()
    combined = stdout_text + stderr_text

    reproducible = f'({huge_count} columns)' in combined and '(1000000+ columns)' not in combined
    print('reproducible:', reproducible)
    print('expected_cap_present:', '(1000000+ columns)' in combined)
    print('exact_count_present:', f'({huge_count} columns)' in combined)
    print('--- captured stdout ---')
    print(stdout_text, end='')
    print('--- captured stderr ---')
    print(stderr_text, end='')


if __name__ == '__main__':
    main()
