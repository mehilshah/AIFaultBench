from __future__ import annotations

import importlib.util
import logging
import sys
import types
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SDV_ROOT = ROOT / 'codebase' / 'sdv'


def _stub_module(name: str, **attrs):
    module = types.ModuleType(name)
    for attr_name, attr_value in attrs.items():
        setattr(module, attr_name, attr_value)
    sys.modules[name] = module
    return module


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def _bootstrap_sdv():
    """Load the local SDV source tree without importing sdv/__init__.py."""
    sdv_pkg = _stub_module('sdv')
    sdv_pkg.__path__ = [str(SDV_ROOT)]

    version_mod = _stub_module('sdv.version', community='test', enterprise=None)
    sdv_pkg.version = version_mod

    logging_mod = _stub_module('sdv.logging', get_sdv_logger=logging.getLogger)
    sdv_pkg.logging = logging_mod

    metadata_pkg = _stub_module('sdv.metadata')
    metadata_pkg.__path__ = [str(SDV_ROOT / 'metadata')]

    _load_module('sdv.errors', SDV_ROOT / 'errors.py')
    _load_module('sdv.metadata.errors', SDV_ROOT / 'metadata' / 'errors.py')
    _load_module('sdv.metadata.utils', SDV_ROOT / 'metadata' / 'utils.py')
    _load_module('sdv._utils', SDV_ROOT / '_utils.py')

    # The current repro does not need the upgrader or visualization helpers.
    _stub_module('sdv.metadata.metadata_upgrader', convert_metadata=lambda metadata: metadata)
    _stub_module(
        'sdv.metadata.visualization',
        create_columns_node=lambda columns: str(columns),
        create_summarized_columns_node=lambda columns: str(columns),
        visualize_graph=lambda *args, **kwargs: None,
    )

    module = _load_module('sdv.metadata.single_table', SDV_ROOT / 'metadata' / 'single_table.py')
    return module.SingleTableMetadata, sys.modules['sdv.metadata.errors'].InvalidMetadataError


def main():
    SingleTableMetadata, InvalidMetadataError = _bootstrap_sdv()

    metadata = SingleTableMetadata()
    metadata.add_column('guest_email', sdtype='email', pii=True)
    metadata.add_column('billing_address', sdtype='street_address', pii=True)
    metadata.add_column_relationship('address', ['billing_address'])

    try:
        metadata.set_primary_key(['guest_email', 'billing_address'])
    except InvalidMetadataError as exc:
        print('BLOCKED: current snapshot rejects composite primary keys before relationship')
        print(f'{type(exc).__name__}: {exc}')
        return 0

    try:
        metadata.validate()
    except InvalidMetadataError as exc:
        print('NOT REPRODUCIBLE HERE: composite key is accepted but validation still rejects it')
        print(f'{type(exc).__name__}: {exc}')
        return 0

    print('BUG REPRODUCED: composite primary key with a relationship column passed validation.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
