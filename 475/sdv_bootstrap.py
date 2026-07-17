"""Helpers to import the local SDV snapshot without loading optional heavy extras."""

from __future__ import annotations

import importlib
import pathlib
import sys
import types


def _ensure_package(name: str, path: pathlib.Path) -> None:
    module = sys.modules.get(name)
    if module is None:
        module = types.ModuleType(name)
        module.__path__ = [str(path)]
        sys.modules[name] = module


def load_sdv_classes():
    """Load the SDV classes needed for the repro from the local codebase."""
    root = pathlib.Path(__file__).resolve().parent / 'codebase' / 'sdv'

    # Avoid executing sdv/__init__.py, which imports optional single-table models.
    _ensure_package('sdv', root)
    _ensure_package('sdv.single_table', root / 'single_table')

    version_mod = types.ModuleType('sdv.version')
    version_mod.community = 'dev'
    version_mod.enterprise = None
    sys.modules['sdv.version'] = version_mod
    sys.modules['sdv'].version = version_mod

    metadata_module = importlib.import_module('sdv.metadata.metadata')
    hma_module = importlib.import_module('sdv.multi_table.hma')
    fixed_combinations_module = importlib.import_module('sdv.cag.fixed_combinations')

    return (
        metadata_module.Metadata,
        hma_module.HMASynthesizer,
        fixed_combinations_module.FixedCombinations,
    )
