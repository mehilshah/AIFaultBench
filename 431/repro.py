#!/usr/bin/env python3
"""Minimal reproduction for SDV issue 2813."""

from __future__ import annotations

import importlib.util
import pathlib
import sys
import types


ROOT = pathlib.Path(__file__).resolve().parent
CODEBASE = ROOT / 'codebase'
EXPECTED_REMAINING_RELATIONSHIP = {
    'parent_table_name': 'table1',
    'parent_primary_key': 'id',
    'child_table_name': 'table3',
    'child_foreign_key': 'fk_1',
}


def load_module(module_name: str, relative_path: str, *, package: bool = False):
    """Load a module directly from the checked-out source tree."""
    path = CODEBASE / relative_path
    search_locations = [str(path.parent)] if package else None
    spec = importlib.util.spec_from_file_location(
        module_name, path, submodule_search_locations=search_locations
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def bootstrap_sdv_modules() -> None:
    """Load the small portion of SDV needed for the metadata bug."""
    sdv_pkg = types.ModuleType('sdv')
    sdv_pkg.__path__ = [str(CODEBASE / 'sdv')]
    sys.modules['sdv'] = sdv_pkg

    version_mod = types.ModuleType('sdv.version')
    version_mod.community = '1.34.1.dev0'
    version_mod.enterprise = None
    sys.modules['sdv.version'] = version_mod

    # Package stubs that the imported modules expect to exist.
    sys.modules['sdv.logging'] = types.ModuleType('sdv.logging')
    sys.modules['sdv.constraints'] = types.ModuleType('sdv.constraints')
    sys.modules['sdv.metadata'] = types.ModuleType('sdv.metadata')

    load_module('sdv.errors', 'sdv/errors.py')
    load_module('sdv._utils', 'sdv/_utils.py')

    load_module('sdv.logging.utils', 'sdv/logging/utils.py')
    load_module('sdv.logging.logger', 'sdv/logging/logger.py')
    logging_pkg = sys.modules['sdv.logging']
    logging_pkg.get_sdv_logger = sys.modules['sdv.logging.logger'].get_sdv_logger
    logging_pkg.disable_single_table_logger = sys.modules['sdv.logging.utils'].disable_single_table_logger
    logging_pkg.get_sdv_logger_config = sys.modules['sdv.logging.utils'].get_sdv_logger_config
    logging_pkg.load_logfile_dataframe = sys.modules['sdv.logging.utils'].load_logfile_dataframe

    load_module('sdv.constraints.errors', 'sdv/constraints/errors.py')
    load_module('sdv.constraints.utils', 'sdv/constraints/utils.py')
    load_module('sdv.constraints.base', 'sdv/constraints/base.py')
    load_module('sdv.constraints.tabular', 'sdv/constraints/tabular.py')
    constraints_pkg = sys.modules['sdv.constraints']
    tabular_mod = sys.modules['sdv.constraints.tabular']
    base_mod = sys.modules['sdv.constraints.base']
    constraints_pkg.Constraint = base_mod.Constraint
    constraints_pkg.FixedCombinations = tabular_mod.FixedCombinations
    constraints_pkg.FixedIncrements = tabular_mod.FixedIncrements
    constraints_pkg.Inequality = tabular_mod.Inequality
    constraints_pkg.Negative = tabular_mod.Negative
    constraints_pkg.OneHotEncoding = tabular_mod.OneHotEncoding
    constraints_pkg.Positive = tabular_mod.Positive
    constraints_pkg.Range = tabular_mod.Range
    constraints_pkg.ScalarInequality = tabular_mod.ScalarInequality
    constraints_pkg.ScalarRange = tabular_mod.ScalarRange
    constraints_pkg.Unique = tabular_mod.Unique
    constraints_pkg.create_custom_constraint_class = tabular_mod.create_custom_constraint_class

    load_module('sdv.metadata.errors', 'sdv/metadata/errors.py')
    load_module('sdv.metadata.utils', 'sdv/metadata/utils.py')
    load_module('sdv.metadata.visualization', 'sdv/metadata/visualization.py')
    load_module('sdv.metadata.metadata_upgrader', 'sdv/metadata/metadata_upgrader.py')
    load_module('sdv.metadata.single_table', 'sdv/metadata/single_table.py')
    load_module('sdv.metadata.multi_table', 'sdv/metadata/multi_table.py')
    load_module('sdv.metadata.metadata', 'sdv/metadata/metadata.py')


def build_metadata():
    from sdv.metadata.metadata import Metadata

    return Metadata.load_from_dict(
        {
            'tables': {
                'table1': {
                    'primary_key': 'id',
                    'columns': {
                        'id': {'sdtype': 'id'},
                        'A': {'sdtype': 'numerical'},
                        'B': {'sdtype': 'categorical'},
                    },
                },
                'table2': {
                    'primary_key': 'id',
                    'columns': {
                        'id': {'sdtype': 'id'},
                        'fk_1': {'sdtype': 'id'},
                        'A': {'sdtype': 'numerical'},
                        'B': {'sdtype': 'categorical'},
                    },
                },
                'table3': {
                    'primary_key': 'id',
                    'columns': {
                        'id': {'sdtype': 'id'},
                        'fk_1': {'sdtype': 'id'},
                        'A': {'sdtype': 'numerical'},
                        'B': {'sdtype': 'categorical'},
                    },
                },
            },
            'relationships': [
                {
                    'parent_table_name': 'table1',
                    'parent_primary_key': 'id',
                    'child_table_name': 'table2',
                    'child_foreign_key': 'fk_1',
                },
                {
                    'parent_table_name': 'table1',
                    'parent_primary_key': 'id',
                    'child_table_name': 'table3',
                    'child_foreign_key': 'fk_1',
                },
            ],
        }
    )


def main() -> None:
    bootstrap_sdv_modules()
    metadata = build_metadata()

    print('before:', metadata.relationships, flush=True)
    metadata.remove_column(table_name='table2', column_name='fk_1')
    print('after:', metadata.relationships, flush=True)

    graph = metadata.visualize()
    print('visualization:', graph.source, flush=True)

    if metadata.relationships != [EXPECTED_REMAINING_RELATIONSHIP]:
        raise AssertionError(
            'Expected only the table1 -> table3 relationship to remain after removing '
            'table2.fk_1, but got: '
            f'{metadata.relationships!r}'
        )


if __name__ == '__main__':
    main()
