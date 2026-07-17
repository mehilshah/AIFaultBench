#!/usr/bin/env python3
"""Minimal reproduction for the SDV regex test regression."""

from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / 'codebase'


def _load_module(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f'Could not load {module_name} from {file_path}')
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _load_local_sdv_utils():
    # Build a minimal sdv package so sdv._utils can be imported without installing
    # the full package dependencies. The bug is isolated to this utility function.
    sdv_pkg = types.ModuleType('sdv')
    sdv_pkg.__path__ = [str(CODEBASE / 'sdv')]
    sys.modules['sdv'] = sdv_pkg

    version_mod = types.ModuleType('sdv.version')
    version_mod.community = '0.0.0'
    version_mod.enterprise = None
    sys.modules['sdv.version'] = version_mod
    sdv_pkg.version = version_mod

    errors_mod = _load_module('sdv.errors', CODEBASE / 'sdv' / 'errors.py')
    sdv_pkg.errors = errors_mod

    return _load_module('sdv._utils', CODEBASE / 'sdv' / '_utils.py')


def main() -> int:
    utils = _load_local_sdv_utils()

    regex = '(ab)*'
    expected_message = 'REGEX operation: SUBPATTERN is not supported by SDV.'

    print(f'regex: {regex}')
    try:
        result = utils.get_possible_chars(regex)
    except ValueError as exc:
        print('unexpected ValueError:')
        print(exc)
        return 1

    print(f'expected ValueError: {expected_message}')
    print(f'observed result: {result}')
    print('result: bug reproduced, because no ValueError was raised')
    raise AssertionError('Expected get_possible_chars to raise ValueError, but it returned normally.')


if __name__ == '__main__':
    raise SystemExit(main())
