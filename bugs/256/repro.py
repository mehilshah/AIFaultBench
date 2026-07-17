#!/usr/bin/env python3
"""Minimal reproduction for SDV issue 1741.

The bug appears when all columns are dropped during preprocessing, leaving the
synthesizer with no trained model but still allowing ``sample`` to proceed.
"""

from __future__ import annotations

import traceback

import pandas as pd

from sdv.metadata import SingleTableMetadata
from sdv.single_table import CTGANSynthesizer, CopulaGANSynthesizer, TVAESynthesizer


def _run_case(cls):
    data = pd.DataFrame(
        {
            'user_id': ['100', '101', '102', '103', '104'],
            'user_ssn': [
                '111-11-1111',
                '222-22-2222',
                '333-33-3333',
                '444-44-4444',
                '555-55-5555',
            ],
        }
    )
    metadata = SingleTableMetadata.load_from_dict(
        {
            'primary_key': 'user_id',
            'columns': {
                'user_id': {'sdtype': 'id'},
                'user_ssn': {'sdtype': 'ssn'},
            },
        }
    )

    synth = cls(metadata, epochs=1, cuda=False)
    synth.fit(data)
    print(f'{cls.__name__}: fit complete, has _model={hasattr(synth, "_model")}')
    print(f'{cls.__name__}: _model value={getattr(synth, "_model", None)!r}')

    try:
        synth.sample(10)
    except Exception as exc:  # noqa: BLE001
        print(f'{cls.__name__}: sample raised {type(exc).__name__}: {exc}')
        traceback.print_exc()
        return True

    print(f'{cls.__name__}: sample unexpectedly succeeded')
    return False


def main():
    print('Starting SDV reproduction')
    print('Testing CTGANSynthesizer, TVAESynthesizer, and CopulaGANSynthesizer')

    reproduced = False
    for cls in (CTGANSynthesizer, TVAESynthesizer, CopulaGANSynthesizer):
        reproduced |= _run_case(cls)

    if reproduced:
        print('Reproduction succeeded: sample() fails after fitting with all columns dropped.')
        return 0

    print('Reproduction failed: no exception was raised.')
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
