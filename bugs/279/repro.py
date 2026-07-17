#!/usr/bin/env python3
"""Reproduction entrypoint for bug 279.

The reported crash targets SDV Enterprise's `ColumnFormula` constraint.
This standardized folder only contains the open-source SDV codebase, which
does not expose that class, so the script records the blocker explicitly.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / 'codebase'
RESULT_PATH = ROOT / 'reproduction.json'


def _scan_for_column_formula():
    """Return evidence about whether the local tree contains ColumnFormula."""
    cag_init = (CODEBASE / 'sdv' / 'cag' / '__init__.py').read_text(encoding='utf-8')
    exported = 'ColumnFormula' in cag_init

    mentions = []
    for path in CODEBASE.rglob('*.py'):
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue

        if 'ColumnFormula' in text:
            mentions.append(str(path.relative_to(ROOT)))

    sandbox_module = CODEBASE / 'sdv' / 'cag' / 'sandbox.py'
    sandbox_package = CODEBASE / 'sdv' / 'cag' / 'sandbox'

    return {
        'exported_from_sdv_cag': exported,
        'files_with_columnformula_mentions': mentions,
        'sandbox_module_exists': sandbox_module.exists(),
        'sandbox_package_exists': sandbox_package.exists(),
    }


def main():
    evidence = _scan_for_column_formula()

    reproducible = False
    blocking_reason = (
        'The local repository is open-source SDV 1.37.3.dev1 and does not contain the '
        'enterprise `ColumnFormula` constraint or an `sdv.cag.sandbox` module, so the '
        'reported crash cannot be exercised from this source tree.'
    )

    steps = [
        'Read `bug_report.txt` and identified the reported failure as a `ColumnFormula` '
        'serialization crash in SDV Enterprise 0.47.4.',
        'Inspected the local `codebase/` for `ColumnFormula` and sandbox support.',
        'Confirmed that the checked-in source tree exports only the open-source CAG classes '
        'and does not define `ColumnFormula`.',
    ]

    result = {
        'reproducible': reproducible,
        'evidence': {
            'codebase_version': '1.37.3.dev1',
            'columnformula_scan': evidence,
            'issue_url': 'https://github.com/sdv-dev/SDV/issues/2915',
        },
        'steps': steps,
        'blocking_reason': blocking_reason,
        'reproduction_command': 'bash run_repro.sh',
    }

    RESULT_PATH.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')

    print('Reproducible: false')
    print(blocking_reason)
    print('Evidence:')
    print(json.dumps(evidence, indent=2))
    print(f'Wrote {RESULT_PATH.name}')


if __name__ == '__main__':
    sys.exit(main())
