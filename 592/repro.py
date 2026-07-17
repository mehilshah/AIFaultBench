from __future__ import annotations

import importlib.util
import json
import sys
import types
from copy import deepcopy
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent / 'codebase' / 'sdv'


def ensure_package(name: str) -> types.ModuleType:
    """Create a lightweight package module so local files can import each other."""
    module = sys.modules.get(name)
    if module is None:
        module = types.ModuleType(name)
        if name == 'sdv':
            module.__path__ = [str(BASE_DIR)]
        else:
            module.__path__ = [str(BASE_DIR / name.split('.')[-1])]
        sys.modules[name] = module
    return module


def load_module(module_name: str, relative_path: str) -> types.ModuleType:
    """Load a module directly from the local source tree."""
    path = BASE_DIR / relative_path
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f'Unable to load {module_name} from {path}')

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    parent_name, _, child_name = module_name.rpartition('.')
    if parent_name:
        parent = sys.modules[parent_name]
        setattr(parent, child_name, module)

    return module


def bootstrap_sdv_modules():
    """Load only the local SDV modules needed for this repro."""
    sdv_pkg = ensure_package('sdv')
    single_table_pkg = ensure_package('sdv.single_table')

    version_module = types.ModuleType('sdv.version')
    version_module.community = 'local'
    version_module.enterprise = None
    sys.modules['sdv.version'] = version_module
    sdv_pkg.version = version_module

    load_module('sdv.errors', 'errors.py')
    load_module('sdv._utils', '_utils.py')
    load_module('sdv.single_table._dayz_utils', 'single_table/_dayz_utils.py')
    load_module('sdv.single_table.dayz', 'single_table/dayz.py')

    return single_table_pkg


class FakeTable:
    def __init__(self, columns):
        self.columns = columns


class FakeMetadata:
    def __init__(self):
        self.tables = {
            'table': FakeTable(
                {
                    'id': {'sdtype': 'id'},
                    'value': {'sdtype': 'categorical'},
                }
            )
        }
        self.validate_calls = 0
        self.validate_data_calls = []

    def validate(self):
        self.validate_calls += 1

    def validate_data(self, datas):
        self.validate_data_calls.append(datas)

    def _get_single_table_name(self):
        return 'table'


def main():
    bootstrap_sdv_modules()
    from sdv.errors import SynthesizerProcessingError
    from sdv.single_table.dayz import DayZSynthesizer

    data = pd.DataFrame(
        {
            'id': [1, 2, 3, 4],
            'value': ['alpha', 'beta', 'gamma', 'delta'],
        }
    )
    metadata = FakeMetadata()

    parameters = DayZSynthesizer.create_parameters(data, metadata)
    print('CREATED_PARAMETERS=' + json.dumps(parameters, sort_keys=True))

    parameters = deepcopy(parameters)
    parameters['tables']['table']['columns']['id']['missing_values_proportion'] = 0.5
    print(
        'MUTATED_PRIMARY_KEY_PARAMETER='
        + json.dumps(parameters['tables']['table']['columns']['id'], sort_keys=True)
    )

    try:
        DayZSynthesizer.validate_parameters(metadata, parameters)
    except SynthesizerProcessingError as error:
        print(f'VALIDATION_REJECTED={error}')
        return 0

    print('VALIDATION_ACCEPTED_NONZERO_PRIMARY_KEY_MISSING_VALUES_PROPORTION')
    raise AssertionError(
        "validate_parameters accepted a nonzero 'missing_values_proportion' "
        'for the primary key'
    )


if __name__ == '__main__':
    raise SystemExit(main())
